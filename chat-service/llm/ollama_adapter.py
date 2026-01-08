"""
SADNxAI - Ollama LLM Adapter
Connects to local Ollama instance for SLM inference
"""

import os
import json
import httpx
from typing import List, Dict, Any, Optional, AsyncGenerator

from shared.openai_schema import get_system_prompt, get_tools
from shared.prompts import get_prompt_for_state


class OllamaAdapter:
    """Adapter for Ollama local LLM with support for both custom and native tool calling."""

    def __init__(self):
        self.base_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
        self.system_prompt = get_system_prompt()
        self.tools = get_tools()
        self.timeout = 240.0  # 4 minutes for CPU inference

        # Enable native Ollama function calling (experimental)
        # Set OLLAMA_NATIVE_TOOLS=true to use Ollama's built-in tool support
        self.use_native_tools = os.getenv("OLLAMA_NATIVE_TOOLS", "false").lower() == "true"

        # Persistent client for connection reuse
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create persistent HTTP client"""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def check_health(self) -> bool:
        """Check if Ollama is running and model is available"""
        try:
            client = await self._get_client()
            response = await client.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                models = [m.get("name", "").split(":")[0] for m in data.get("models", [])]
                model_name = self.model.split(":")[0]
                return model_name in models or any(model_name in m for m in models)
            return False
        except Exception as e:
            print(f"Ollama health check failed: {e}")
            return False

    async def pull_model(self) -> bool:
        """Pull the model if not available"""
        try:
            print(f"Pulling model {self.model}...")
            client = await self._get_client()
            response = await client.post(
                f"{self.base_url}/api/pull",
                json={"name": self.model},
                timeout=600.0
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Failed to pull model: {e}")
            return False

    async def chat(
        self,
        messages: List[Dict[str, Any]],
        session_context: Optional[Dict[str, Any]] = None,
        max_retries: int = 2
    ) -> Dict[str, Any]:
        """
        Send chat request to Ollama with retry logic for failed tool calls.

        Args:
            messages: Conversation history
            session_context: Current session context (file info, classification, etc.)
            max_retries: Number of retries for invalid tool calls (default: 2)
        """
        # Build the full message list with our system prompt (includes context + tool instructions)
        full_messages = [
            {"role": "system", "content": self._build_system_prompt(session_context)}
        ]

        # Add conversation history, SKIP any system messages to avoid duplication
        for msg in messages:
            role = msg.get("role", "user")
            # Skip system messages - we already added our comprehensive system prompt
            if role == "system":
                continue
            full_messages.append({
                "role": role,
                "content": msg.get("content", "")
            })

        for attempt in range(max_retries + 1):
            try:
                client = await self._get_client()

                # Build request payload
                payload = {
                    "model": self.model,
                    "messages": full_messages,
                    "stream": False,
                    "keep_alive": "10m",  # Keep model loaded for 10 minutes
                    "options": {
                        "temperature": 0.1,  # Low temp for structured JSON output
                        "num_ctx": int(os.getenv("OLLAMA_NUM_CTX", "32000")),  # Configurable context window
                    }
                }

                # Add native tools if enabled (experimental - requires Ollama 0.3.0+)
                if self.use_native_tools:
                    payload["tools"] = self.tools

                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=self.timeout
                )

                if response.status_code != 200:
                    error_text = response.text
                    print(f"Ollama error: {error_text}")
                    return {
                        "content": f"Error communicating with local LLM: {error_text}",
                        "tool_calls": None
                    }

                data = response.json()
                message = data.get("message", {})
                assistant_message = message.get("content", "")

                # Check for native tool calls first (Ollama 0.3.0+)
                native_tool_calls = message.get("tool_calls")
                if native_tool_calls and self.use_native_tools:
                    # Convert native format to our format
                    tool_calls = []
                    for i, tc in enumerate(native_tool_calls):
                        func = tc.get("function", {})
                        tool_calls.append({
                            "id": f"call_{i}",
                            "type": "function",
                            "function": {
                                "name": func.get("name"),
                                "arguments": json.dumps(func.get("arguments", {}))
                            }
                        })
                    return {
                        "content": assistant_message,
                        "tool_calls": tool_calls if tool_calls else None
                    }

                # Fallback to custom tool call parsing
                tool_calls, validation_errors = self._extract_tool_calls_with_errors(assistant_message)

                # Determine if we expected a tool call based on session state
                expects_tool = False
                if session_context:
                    status = session_context.get("status", "").upper()
                    # These states expect tool calls
                    expects_tool = status in ["ANALYZING", "PROPOSED", "DISCUSSING", "FAILED"]

                # Retry if: validation errors OR (expected tools but got none)
                missing_expected_tool = expects_tool and not tool_calls
                should_retry = (validation_errors or missing_expected_tool) and attempt < max_retries

                if should_retry:
                    if validation_errors:
                        error_feedback = f"Your tool call had errors: {validation_errors}. Please fix and try again."
                        print(f"Retry {attempt + 1}: Tool call validation errors - {validation_errors}")
                    else:
                        error_feedback = (
                            "You must call a tool. Do not describe what you would do - actually call the tool. "
                            "Use classify_columns to classify the data, execute_pipeline after approval, "
                            "or update_thresholds to adjust privacy settings."
                        )
                        print(f"Retry {attempt + 1}: Expected tool call but got text response")

                    # Add the assistant's failed response and error feedback
                    full_messages.append({"role": "assistant", "content": assistant_message})
                    full_messages.append({
                        "role": "user",
                        "content": error_feedback
                    })
                    continue  # Retry

                # Clean the response if tool calls were extracted
                if tool_calls:
                    assistant_message = self._clean_response(assistant_message)

                return {
                    "content": assistant_message,
                    "tool_calls": tool_calls
                }

            except httpx.TimeoutException:
                return {
                    "content": "The local LLM took too long to respond. Please try again.",
                    "tool_calls": None
                }
            except Exception as e:
                print(f"Ollama chat error: {e}")
                return {
                    "content": f"Error with local LLM: {str(e)}",
                    "tool_calls": None
                }

        # Exhausted all retries
        return {
            "content": assistant_message,
            "tool_calls": None
        }

    async def chat_stream(
        self,
        messages: List[Dict[str, Any]],
        session_context: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream chat response token-by-token from Ollama.

        Yields:
            {"type": "token", "content": "..."} for each token
            {"type": "done", "content": "full response", "tool_calls": [...]} when complete
        """
        # Build the full message list with our system prompt
        full_messages = [
            {"role": "system", "content": self._build_system_prompt(session_context)}
        ]

        # Add conversation history, SKIP any system messages
        for msg in messages:
            role = msg.get("role", "user")
            if role == "system":
                continue
            full_messages.append({
                "role": role,
                "content": msg.get("content", "")
            })

        try:
            client = await self._get_client()

            payload = {
                "model": self.model,
                "messages": full_messages,
                "stream": True,  # Enable streaming
                "keep_alive": "10m",
                "options": {
                    "temperature": 0.1,
                    "num_ctx": int(os.getenv("OLLAMA_NUM_CTX", "32000")),  # Configurable context window
                }
            }

            # Add native tools if enabled (experimental - requires Ollama 0.3.0+)
            if self.use_native_tools:
                payload["tools"] = self.tools

            async with client.stream(
                "POST",
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=self.timeout
            ) as response:
                if response.status_code != 200:
                    error_text = await response.aread()
                    yield {
                        "type": "done",
                        "content": f"Error: {error_text.decode()}",
                        "tool_calls": None
                    }
                    return

                full_content = ""
                accumulated_tool_calls = []  # Accumulate tool_calls from ANY chunk

                async for line in response.aiter_lines():
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        message = data.get("message", {})
                        token = message.get("content", "")

                        if token:
                            full_content += token
                            yield {"type": "token", "content": token}

                        # Check for tool_calls in EVERY chunk (not just when done)
                        # Ollama sends tool_calls with done: false
                        if self.use_native_tools:
                            chunk_tool_calls = message.get("tool_calls")
                            if chunk_tool_calls:
                                print(f"[Native Tools] Found {len(chunk_tool_calls)} tool call(s) in chunk")
                                for tc in chunk_tool_calls:
                                    func = tc.get("function", {})
                                    accumulated_tool_calls.append({
                                        "id": f"call_{len(accumulated_tool_calls)}",
                                        "type": "function",
                                        "function": {
                                            "name": func.get("name"),
                                            "arguments": json.dumps(func.get("arguments", {}))
                                        }
                                    })

                        # Check if done
                        if data.get("done", False):
                            tool_calls = None

                            # Debug: Log response structure
                            if self.use_native_tools:
                                print(f"[Native Tools] use_native_tools={self.use_native_tools}")
                                print(f"[Native Tools] Accumulated tool_calls: {len(accumulated_tool_calls)}")

                            # Use accumulated tool calls if we have any
                            if accumulated_tool_calls and self.use_native_tools:
                                tool_calls = accumulated_tool_calls
                                print(f"[LLM Response] Native tool calls: {len(tool_calls)}")
                            else:
                                # Fallback to regex extraction
                                tool_calls = self._extract_tool_calls(full_content)
                                print(f"[LLM Response] Regex tool calls: {len(tool_calls) if tool_calls else 0}")

                            # Debug: Log full LLM response
                            print(f"[LLM Response] Raw content ({len(full_content)} chars):")
                            print(f"[LLM Response] {full_content[:500]}{'...' if len(full_content) > 500 else ''}")
                            if tool_calls:
                                for tc in tool_calls:
                                    func = tc.get("function", {})
                                    print(f"[LLM Response] Tool: {func.get('name', 'unknown')}")
                                full_content = self._clean_response(full_content)

                            yield {
                                "type": "done",
                                "content": full_content,
                                "tool_calls": tool_calls
                            }
                            return
                    except json.JSONDecodeError:
                        continue

        except httpx.TimeoutException:
            yield {
                "type": "done",
                "content": "The local LLM took too long to respond.",
                "tool_calls": None
            }
        except Exception as e:
            print(f"Ollama stream error: {e}")
            yield {
                "type": "done",
                "content": f"Error: {str(e)}",
                "tool_calls": None
            }

    def _build_system_prompt(self, session_context: Optional[Dict[str, Any]] = None) -> str:
        """Build system prompt with session context using state-based templates"""
        # Import TOON utilities for efficient data encoding
        from shared.toon_utils import (
            format_sample_data_for_prompt,
            format_classification_for_prompt,
            format_validation_for_prompt,
            get_format_info,
            is_toon_enabled
        )

        # Get status from context or default to idle
        status = "idle"
        if session_context and session_context.get("status"):
            status = session_context["status"]

        # Get state-based prompt (optimized for each state)
        prompt = get_prompt_for_state(status)

        # Add TOON format info if enabled (helps LLM understand the data format)
        format_info = get_format_info()
        if format_info:
            prompt += f"\n\n## DATA FORMAT\n{format_info}\n"

        # Add dynamic context based on state
        if session_context:
            # ALWAYS include file info if available - LLM needs to see columns
            if session_context.get("file_info"):
                fi = session_context["file_info"]
                prompt += f"\n\n## CURRENT FILE: {fi.get('filename', '?')} ({fi.get('row_count', '?')} rows)\n"
                columns = fi.get('columns', [])
                prompt += f"Columns: {', '.join(columns)}\n"

                # Format sample data (TOON or markdown table based on config)
                sample_data = fi.get("sample_data")
                if sample_data and isinstance(sample_data, list) and len(sample_data) > 0:
                    prompt += "\n### Sample Data:\n"
                    if is_toon_enabled():
                        # Use TOON encoding for 55-60% token savings
                        prompt += format_sample_data_for_prompt(sample_data)
                        prompt += "\n"
                    else:
                        # Fallback to markdown table (original format)
                        if isinstance(sample_data[0], dict):
                            headers = list(sample_data[0].keys())
                            prompt += "| " + " | ".join(headers) + " |\n"
                            prompt += "| " + " | ".join(["---"] * len(headers)) + " |\n"
                            for row in sample_data[:5]:
                                values = [str(row.get(h, ""))[:30] for h in headers]
                                prompt += "| " + " | ".join(values) + " |\n"

            # Add classification for PROPOSED/DISCUSSING states
            if status.lower() in ["proposed", "discussing"] and session_context.get("classification"):
                cls = session_context['classification']
                prompt += "\n## CURRENT CLASSIFICATION:\n"
                if is_toon_enabled():
                    # Use TOON encoding for classification
                    prompt += format_classification_for_prompt(cls)
                    prompt += "\n"
                else:
                    # Fallback to text format (original)
                    prompt += f"- Direct IDs (SUPPRESS): {cls.get('direct_identifiers', [])}\n"
                    prompt += f"- Quasi-IDs (GENERALIZE): {cls.get('quasi_identifiers', [])}\n"
                    prompt += f"- Linkage IDs (PSEUDONYMIZE): {cls.get('linkage_identifiers', [])}\n"
                    prompt += f"- Dates (DATE_SHIFT): {cls.get('date_columns', [])}\n"
                    prompt += f"- Sensitive (KEEP): {cls.get('sensitive_attributes', [])}\n"

            # Add validation results for FAILED state
            if status.lower() == "failed" and session_context.get("validation_result"):
                vr = session_context["validation_result"]
                prompt += "\n## VALIDATION RESULTS (FAILED):\n"
                if is_toon_enabled():
                    prompt += format_validation_for_prompt(vr)
                    prompt += "\n"
                elif isinstance(vr, dict):
                    for metric, data in vr.items():
                        if isinstance(data, dict):
                            prompt += f"- {metric}: {data.get('value', '?')} (threshold: {data.get('threshold', '?')}, passed: {data.get('passed', '?')})\n"

            # Add validation results for COMPLETED state
            if status.lower() == "completed" and session_context.get("validation_result"):
                vr = session_context["validation_result"]
                prompt += "\n## VALIDATION RESULTS (PASSED):\n"
                if is_toon_enabled():
                    prompt += format_validation_for_prompt(vr)
                    prompt += "\n"
                elif isinstance(vr, dict):
                    for metric, data in vr.items():
                        if isinstance(data, dict):
                            prompt += f"- {metric}: {data.get('value', '?')} (threshold: {data.get('threshold', '?')})\n"

        return prompt

    # Valid tools and their required fields
    VALID_TOOLS = {
        "query_regulations": {
            "required": ["query_type", "value"],
            "types": {
                "query_type": str,
                "value": str
            }
        },
        "classify_columns": {
            "required": ["direct_identifiers", "quasi_identifiers", "linkage_identifiers",
                        "date_columns", "sensitive_attributes", "recommended_techniques"],
            "types": {
                "direct_identifiers": list,
                "quasi_identifiers": list,
                "linkage_identifiers": list,
                "date_columns": list,
                "sensitive_attributes": list,
                "recommended_techniques": dict,
                "reasoning": dict
            }
        },
        "execute_pipeline": {
            "required": [],  # confirmed defaults to True in handler
            "types": {
                "confirmed": bool,
                # Allow threshold params to be passed alongside execute_pipeline
                "k_anonymity_minimum": int,
                "k_anonymity_target": int,
                "l_diversity_minimum": int,
                "l_diversity_target": int,
                "t_closeness_minimum": float,
                "t_closeness_target": float,
                "risk_score_minimum": float,
                "risk_score_target": float
            }
        },
        "update_thresholds": {
            "required": [],
            "types": {
                "k_anonymity_minimum": int,
                "k_anonymity_target": int,
                "l_diversity_minimum": int,
                "l_diversity_target": int,
                "t_closeness_minimum": float,
                "t_closeness_target": float,
                "risk_score_minimum": float,
                "risk_score_target": float
            }
        }
    }

    def _validate_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> tuple[bool, str]:
        """Validate a tool call against its schema. Returns (is_valid, error_message)."""
        if tool_name not in self.VALID_TOOLS:
            return False, f"Unknown tool: {tool_name}. Valid tools: {list(self.VALID_TOOLS.keys())}"

        schema = self.VALID_TOOLS[tool_name]

        # Check required fields
        for field in schema["required"]:
            if field not in arguments:
                return False, f"Missing required field '{field}' for tool '{tool_name}'"

        # Check types
        for field, expected_type in schema["types"].items():
            if field in arguments:
                value = arguments[field]
                # Allow int when expecting float (common in JSON)
                if expected_type is float and isinstance(value, int):
                    arguments[field] = float(value)  # Convert int to float
                # Allow list when expecting str - convert to comma-separated string
                elif expected_type is str and isinstance(value, list):
                    arguments[field] = ",".join(str(v) for v in value)
                elif not isinstance(value, expected_type):
                    return False, f"Field '{field}' should be {expected_type.__name__}, got {type(value).__name__}"

        return True, ""

    def _extract_tool_calls_with_errors(self, content: str) -> tuple[Optional[List[Dict[str, Any]]], List[str]]:
        """
        Extract and validate tool calls from the response.
        Returns (tool_calls, validation_errors) tuple.
        """
        import re

        matches = []

        # Pattern 1: ```tool_call blocks (preferred)
        pattern1 = r'```tool_call\s*\n?(.*?)\n?```'
        matches.extend(re.findall(pattern1, content, re.DOTALL))

        # Pattern 2: ```json blocks with "tool" key
        # Use a more robust approach: match code fences, then validate JSON separately
        if not matches:
            pattern2 = r'```(?:json)?\s*\n?([\s\S]*?)\n?```'
            for block in re.findall(pattern2, content, re.DOTALL):
                block = block.strip()
                # Check if this looks like a tool call JSON
                if '"tool"' in block and block.startswith('{'):
                    try:
                        # Validate it's proper JSON with required fields
                        parsed = json.loads(block)
                        if "tool" in parsed:
                            matches.append(block)
                    except json.JSONDecodeError:
                        continue  # Not valid JSON, skip

        # Pattern 3: Raw JSON with "tool" key (LLM sometimes outputs without code fences)
        if not matches:
            # Find potential JSON objects starting with {"tool"
            # Use JSON decoder for proper parsing (handles braces inside strings)
            decoder = json.JSONDecoder()
            idx = 0
            while idx < len(content):
                start = content.find('{"tool"', idx)
                if start == -1:
                    break
                try:
                    # Use raw_decode to properly parse JSON including nested braces in strings
                    # raw_decode returns (obj, end) where end is the ABSOLUTE position in content
                    parsed, end_pos = decoder.raw_decode(content, start)
                    if "tool" in parsed and "arguments" in parsed:
                        matches.append(json.dumps(parsed))
                    # end_pos is already absolute, not relative to start
                    idx = end_pos
                except json.JSONDecodeError:
                    # If parsing fails, skip this potential match
                    idx = start + 1

        if not matches:
            return None, []

        tool_calls = []
        validation_errors = []

        for match in matches:
            try:
                data = json.loads(match.strip())
                if "tool" in data:
                    tool_name = data["tool"]
                    arguments = data.get("arguments", {})

                    # Validate the tool call
                    is_valid, error = self._validate_tool_call(tool_name, arguments)
                    if not is_valid:
                        validation_errors.append(error)
                        print(f"Tool call validation failed: {error}")
                        continue  # Skip invalid tool calls

                    tool_calls.append({
                        "id": f"call_{len(tool_calls)}",
                        "type": "function",
                        "function": {
                            "name": tool_name,
                            "arguments": json.dumps(arguments)
                        }
                    })
            except json.JSONDecodeError as e:
                error_msg = f"Invalid JSON: {str(e)}"
                validation_errors.append(error_msg)
                print(f"Failed to parse tool call JSON: {e}")
                continue

        return (tool_calls if tool_calls else None), validation_errors

    def _extract_tool_calls(self, content: str) -> Optional[List[Dict[str, Any]]]:
        """Extract and validate tool calls (backwards compatible wrapper)"""
        tool_calls, _ = self._extract_tool_calls_with_errors(content)
        return tool_calls

    def _find_json_end(self, content: str, start: int) -> int:
        """
        Find the end of a JSON object respecting quoted strings.
        Returns the index after the closing brace, or -1 if not found.
        """
        brace_count = 0
        in_string = False
        escape_next = False

        for i in range(start, len(content)):
            c = content[i]

            if escape_next:
                escape_next = False
                continue

            if c == '\\' and in_string:
                escape_next = True
                continue

            if c == '"' and not escape_next:
                in_string = not in_string
                continue

            if in_string:
                continue

            if c == '{':
                brace_count += 1
            elif c == '}':
                brace_count -= 1
                if brace_count == 0:
                    return i + 1

        return -1  # Unclosed JSON

    def _clean_response(self, content: str) -> str:
        """Remove tool call blocks from the response"""
        import re
        # Remove code-fenced tool calls
        content = re.sub(r'```tool_call\s*\n?.*?\n?```', '', content, flags=re.DOTALL)
        content = re.sub(r'```(?:json)?\s*\n?\{[^`]*"tool"[^`]*\}\n?```', '', content, flags=re.DOTALL)

        # Remove raw JSON tool calls (find and remove balanced JSON objects with "tool" key)
        result = []
        idx = 0
        while idx < len(content):
            start = content.find('{"tool"', idx)
            if start == -1:
                result.append(content[idx:])
                break
            # Add content before the JSON
            result.append(content[idx:start])
            # Find end of JSON respecting quoted strings
            end = self._find_json_end(content, start)
            idx = end if end > start else start + 1

        return ''.join(result).strip()


# Singleton instance
_ollama_adapter: Optional[OllamaAdapter] = None


def get_ollama_adapter() -> OllamaAdapter:
    """Get or create the Ollama adapter singleton"""
    global _ollama_adapter
    if _ollama_adapter is None:
        _ollama_adapter = OllamaAdapter()
    return _ollama_adapter
