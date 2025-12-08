"""
SADNxAI - Ollama LLM Adapter
Connects to local Ollama instance for SLM inference
"""

import os
import json
import httpx
from typing import List, Dict, Any, Optional

from shared.openai_schema import get_system_prompt, get_tools


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
                        "num_ctx": 8192,  # Increased context window for full prompts
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

                # If there are validation errors and we haven't exhausted retries, retry with feedback
                if validation_errors and attempt < max_retries:
                    print(f"Retry {attempt + 1}: Tool call validation errors - {validation_errors}")
                    # Add the assistant's failed response and error feedback
                    full_messages.append({"role": "assistant", "content": assistant_message})
                    full_messages.append({
                        "role": "user",
                        "content": f"Your tool call had errors: {validation_errors}. Please fix and try again with a valid tool call."
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

    def _build_system_prompt(self, session_context: Optional[Dict[str, Any]] = None) -> str:
        """Build system prompt with session context and tool instructions"""
        prompt = self.system_prompt

        # Add compact tool calling instructions
        prompt += """

## TOOL FORMAT
When you need to call a tool, output:
```tool_call
{"tool": "tool_name", "arguments": {...}}
```

Tools: classify_columns, execute_pipeline, update_thresholds
Only call execute_pipeline after user says "approve/yes/proceed".
"""

        # Add session context if available
        if session_context:
            if session_context.get("file_info"):
                fi = session_context["file_info"]
                prompt += f"\n\n## CURRENT FILE: {fi.get('filename', '?')} ({fi.get('row_count', '?')} rows)\n"
                columns = fi.get('columns', [])
                prompt += f"Columns: {', '.join(columns)}\n"

                # Format sample data as markdown table (more compact than JSON)
                sample_data = fi.get("sample_data")
                if sample_data and isinstance(sample_data, list) and len(sample_data) > 0:
                    prompt += "\n### Sample Data:\n"
                    # Build header
                    if isinstance(sample_data[0], dict):
                        headers = list(sample_data[0].keys())
                        prompt += "| " + " | ".join(headers) + " |\n"
                        prompt += "| " + " | ".join(["---"] * len(headers)) + " |\n"
                        # Build rows (limit to 5)
                        for row in sample_data[:5]:
                            values = [str(row.get(h, ""))[:30] for h in headers]  # Truncate long values
                            prompt += "| " + " | ".join(values) + " |\n"
                    else:
                        # Fallback for other formats
                        prompt += f"```\n{sample_data}\n```\n"

            if session_context.get("classification"):
                cls = session_context['classification']
                prompt += "\n## CURRENT CLASSIFICATION:\n"
                prompt += f"- Direct IDs (SUPPRESS): {cls.get('direct_identifiers', [])}\n"
                prompt += f"- Quasi-IDs (GENERALIZE): {cls.get('quasi_identifiers', [])}\n"
                prompt += f"- Linkage IDs (PSEUDONYMIZE): {cls.get('linkage_identifiers', [])}\n"
                prompt += f"- Dates (DATE_SHIFT): {cls.get('date_columns', [])}\n"
                prompt += f"- Sensitive (KEEP): {cls.get('sensitive_attributes', [])}\n"

            prompt += f"\nStatus: {session_context.get('status', 'unknown')}\n"

        return prompt

    # Valid tools and their required fields
    VALID_TOOLS = {
        "classify_columns": {
            "required": ["direct_identifiers", "quasi_identifiers", "linkage_identifiers",
                        "date_columns", "sensitive_attributes", "recommended_techniques", "reasoning"],
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
            "required": ["confirmed"],
            "types": {"confirmed": bool}
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
                if not isinstance(arguments[field], expected_type):
                    return False, f"Field '{field}' should be {expected_type.__name__}, got {type(arguments[field]).__name__}"

        return True, ""

    def _extract_tool_calls_with_errors(self, content: str) -> tuple[Optional[List[Dict[str, Any]]], List[str]]:
        """
        Extract and validate tool calls from the response.
        Returns (tool_calls, validation_errors) tuple.
        """
        import re

        # Look for ```tool_call blocks
        pattern = r'```tool_call\s*\n?(.*?)\n?```'
        matches = re.findall(pattern, content, re.DOTALL)

        if not matches:
            # Also try JSON blocks with "tool" key
            pattern = r'```(?:json)?\s*\n?(\{[^`]*"tool"[^`]*\})\n?```'
            matches = re.findall(pattern, content, re.DOTALL)

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

    def _clean_response(self, content: str) -> str:
        """Remove tool call blocks from the response"""
        import re
        content = re.sub(r'```tool_call\s*\n?.*?\n?```', '', content, flags=re.DOTALL)
        content = re.sub(r'```(?:json)?\s*\n?\{[^`]*"tool"[^`]*\}\n?```', '', content, flags=re.DOTALL)
        return content.strip()


# Singleton instance
_ollama_adapter: Optional[OllamaAdapter] = None


def get_ollama_adapter() -> OllamaAdapter:
    """Get or create the Ollama adapter singleton"""
    global _ollama_adapter
    if _ollama_adapter is None:
        _ollama_adapter = OllamaAdapter()
    return _ollama_adapter
