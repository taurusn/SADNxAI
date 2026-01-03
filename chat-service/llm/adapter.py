"""
LLM Adapter
Handles communication with LLM providers (Claude API, Ollama, or Mock)
"""

import os
import json
from typing import List, Dict, Any, Optional, AsyncGenerator

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.openai_schema import get_tools


class LLMAdapter:
    """
    Unified adapter for LLM communication.

    Supports:
    - Claude API (Anthropic)
    - Ollama (local SLM)
    - Mock mode (testing)
    """

    def __init__(
        self,
        provider: Optional[str] = None,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-20250514",
        mock_mode: bool = False
    ):
        """
        Initialize LLM adapter.

        Args:
            provider: 'claude', 'ollama', or None (auto-detect)
            api_key: Anthropic API key (for Claude)
            model: Model to use
            mock_mode: If True, return mock responses
        """
        self.mock_mode = mock_mode or os.getenv("LLM_MOCK_MODE", "false").lower() == "true"
        self.provider = provider or os.getenv("LLM_PROVIDER", "ollama")
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model

        # Initialize the appropriate client
        self.client = None
        self.ollama_adapter = None

        if not self.mock_mode:
            if self.provider == "claude" and self.api_key:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=self.api_key)
                print(f"LLM Provider: Claude API ({self.model})")
            elif self.provider == "ollama":
                from llm.ollama_adapter import get_ollama_adapter
                self.ollama_adapter = get_ollama_adapter()
                print(f"LLM Provider: Ollama ({self.ollama_adapter.model})")
            else:
                print("LLM Provider: Mock Mode (no provider configured)")
                self.mock_mode = True
        else:
            print("LLM Provider: Mock Mode (explicitly enabled)")

    def _convert_tools_to_anthropic_format(self) -> List[Dict]:
        """Convert OpenAI-style tools to Anthropic format."""
        openai_tools = get_tools()
        anthropic_tools = []

        for tool in openai_tools:
            if tool["type"] == "function":
                func = tool["function"]
                anthropic_tools.append({
                    "name": func["name"],
                    "description": func["description"],
                    "input_schema": func["parameters"]
                })

        return anthropic_tools

    def _convert_messages_to_anthropic_format(self, messages: List[Dict]) -> tuple[str, List[Dict]]:
        """Convert OpenAI-style messages to Anthropic format."""
        system_prompt = ""
        anthropic_messages = []

        for msg in messages:
            role = msg["role"]

            if role == "system":
                if system_prompt:
                    system_prompt += "\n\n"
                system_prompt += msg["content"]

            elif role == "user":
                anthropic_messages.append({
                    "role": "user",
                    "content": msg["content"]
                })

            elif role == "assistant":
                content = []

                if msg.get("content"):
                    content.append({
                        "type": "text",
                        "text": msg["content"]
                    })

                if msg.get("tool_calls"):
                    for tool_call in msg["tool_calls"]:
                        content.append({
                            "type": "tool_use",
                            "id": tool_call["id"],
                            "name": tool_call["function"]["name"],
                            "input": json.loads(tool_call["function"]["arguments"])
                        })

                if content:
                    anthropic_messages.append({
                        "role": "assistant",
                        "content": content
                    })

            elif role == "tool":
                anthropic_messages.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": msg["tool_call_id"],
                        "content": msg["content"]
                    }]
                })

        return system_prompt, anthropic_messages

    async def chat_async(
        self,
        messages: List[Dict],
        session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Async chat method - routes to appropriate provider.

        Args:
            messages: List of messages
            session_context: Optional session context for Ollama

        Returns:
            Response dict with content and tool_calls
        """
        if self.mock_mode:
            return self._mock_response(messages)

        if self.ollama_adapter:
            return await self.ollama_adapter.chat(messages, session_context)

        # Claude is synchronous, wrap it
        return self.chat(messages)

    def chat(self, messages: List[Dict]) -> Dict[str, Any]:
        """
        Send chat request to the configured LLM provider.

        Args:
            messages: List of messages in OpenAI format

        Returns:
            Response dict with content and tool_calls
        """
        if self.mock_mode:
            return self._mock_response(messages)

        if self.ollama_adapter:
            # For sync context, we need to run async
            import asyncio
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(self.ollama_adapter.chat(messages))
            finally:
                loop.close()

        if not self.client:
            raise ValueError("No LLM provider configured")

        # Claude API call
        system_prompt, anthropic_messages = self._convert_messages_to_anthropic_format(messages)
        tools = self._convert_tools_to_anthropic_format()

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_prompt,
            messages=anthropic_messages,
            tools=tools
        )

        result = {
            "content": None,
            "tool_calls": [],
            "stop_reason": response.stop_reason
        }

        for block in response.content:
            if block.type == "text":
                result["content"] = block.text
            elif block.type == "tool_use":
                result["tool_calls"].append({
                    "id": block.id,
                    "type": "function",
                    "function": {
                        "name": block.name,
                        "arguments": json.dumps(block.input)
                    }
                })

        return result

    async def chat_stream(
        self,
        messages: List[Dict],
        session_context: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream chat response token-by-token.
        Filters out tool_call blocks to show only natural language.
        """
        if self.mock_mode:
            # Mock: just yield the response as done
            result = self._mock_response(messages)
            yield {"type": "done", "content": result.get("content", ""), "tool_calls": result.get("tool_calls")}
            return

        if self.ollama_adapter:
            import re
            # Track state for filtering
            buffer = ""
            emitted_length = 0
            in_code_block = False
            in_json_block = False
            json_brace_count = 0
            code_block_start = -1

            async for chunk in self.ollama_adapter.chat_stream(messages, session_context):
                if chunk["type"] == "token":
                    token = chunk["content"]
                    buffer += token

                    # --- Filter 1: Code blocks (```) ---
                    # Look for code block markers in the unemitted portion
                    search_start = max(emitted_length, 0)

                    if not in_code_block:
                        # Look for opening ```
                        code_start = buffer.find("```", search_start)
                        if code_start != -1:
                            # Emit text before the code block
                            text_before = buffer[emitted_length:code_start]
                            if text_before.strip():
                                # Clean any stray JSON from text
                                text_before = re.sub(r'\{"tool"[^}]*\}', '', text_before)
                                if text_before.strip():
                                    yield {"type": "token", "content": text_before}
                            in_code_block = True
                            code_block_start = code_start
                            emitted_length = code_start

                    if in_code_block:
                        # Look for closing ``` (must be after the opening)
                        close_pos = buffer.find("```", code_block_start + 3)
                        if close_pos != -1:
                            # Found closing, skip entire code block
                            in_code_block = False
                            emitted_length = close_pos + 3
                            code_block_start = -1
                        continue  # Don't emit while in code block

                    # --- Filter 2: Raw JSON objects {"tool": ...} ---
                    if not in_json_block:
                        # Look for JSON tool call pattern
                        json_start = buffer.find('{"tool"', emitted_length)
                        if json_start != -1:
                            # Emit text before JSON
                            text_before = buffer[emitted_length:json_start]
                            if text_before.strip():
                                yield {"type": "token", "content": text_before}
                            in_json_block = True
                            emitted_length = json_start
                            json_brace_count = 0

                    if in_json_block:
                        # Track braces to find end of JSON, respecting quoted strings
                        i = 0
                        scan_start = emitted_length
                        in_string = False
                        escape_next = False
                        for i, c in enumerate(buffer[scan_start:]):
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
                                json_brace_count += 1
                            elif c == '}':
                                json_brace_count -= 1
                                if json_brace_count == 0:
                                    # Found end of JSON, skip it
                                    in_json_block = False
                                    emitted_length = scan_start + i + 1
                                    break
                        continue  # Don't emit while in JSON block

                    # --- Emit clean content ---
                    if not in_code_block and not in_json_block:
                        new_text = buffer[emitted_length:]
                        # Only hold back if we might be starting a JSON tool call
                        # Check if buffer ends with partial '{"tool' pattern
                        partial_json = False
                        for partial in ['{"', '{"t', '{"to', '{"too', '{"tool']:
                            if new_text.endswith(partial):
                                # Hold back this partial, don't emit yet
                                new_text = new_text[:-len(partial)]
                                partial_json = True
                                break

                        if new_text:
                            yield {"type": "token", "content": new_text}
                            emitted_length = len(buffer) - (len(partial) if partial_json else 0)
                else:
                    # Pass through done events
                    # But first emit any remaining buffered content
                    if buffer and emitted_length < len(buffer) and not in_code_block and not in_json_block:
                        remaining = buffer[emitted_length:]
                        # Final cleanup of any JSON patterns
                        remaining = re.sub(r'\{"tool"[^}]*\}', '', remaining)
                        if remaining.strip():
                            yield {"type": "token", "content": remaining}
                    yield chunk
            return

        # Claude fallback: non-streaming
        result = self.chat(messages)
        yield {"type": "done", "content": result.get("content", ""), "tool_calls": result.get("tool_calls")}

    async def check_health(self) -> Dict[str, Any]:
        """Check health of the LLM provider."""
        if self.mock_mode:
            return {"status": "healthy", "provider": "mock"}

        if self.ollama_adapter:
            is_healthy = await self.ollama_adapter.check_health()
            return {
                "status": "healthy" if is_healthy else "unhealthy",
                "provider": "ollama",
                "model": self.ollama_adapter.model
            }

        if self.client:
            return {"status": "healthy", "provider": "claude", "model": self.model}

        return {"status": "unhealthy", "provider": "none"}

    async def ensure_model(self) -> bool:
        """Ensure the model is available (pulls if needed for Ollama)."""
        if self.ollama_adapter:
            is_available = await self.ollama_adapter.check_health()
            if not is_available:
                print(f"Model not found, pulling {self.ollama_adapter.model}...")
                return await self.ollama_adapter.pull_model()
            return True
        return True

    def _mock_response(self, messages: List[Dict]) -> Dict[str, Any]:
        """Generate mock response for testing."""
        last_user_msg = None
        for msg in reversed(messages):
            if msg["role"] == "user":
                last_user_msg = msg["content"]
                break

        has_file_context = any(
            "CURRENT FILE:" in msg.get("content", "")
            for msg in messages if msg["role"] == "system"
        )

        if has_file_context and last_user_msg is None:
            return {
                "content": "I've analyzed your dataset. Let me classify the columns based on privacy risk.",
                "tool_calls": [{
                    "id": "mock_tool_1",
                    "type": "function",
                    "function": {
                        "name": "classify_columns",
                        "arguments": json.dumps({
                            "direct_identifiers": ["national_id", "phone", "email"],
                            "quasi_identifiers": ["age", "city", "gender"],
                            "linkage_identifiers": ["patient_id"],
                            "date_columns": ["admission_date"],
                            "sensitive_attributes": ["diagnosis"],
                            "recommended_techniques": {
                                "national_id": "SUPPRESS",
                                "phone": "SUPPRESS",
                                "email": "SUPPRESS",
                                "age": "GENERALIZE",
                                "city": "GENERALIZE",
                                "gender": "GENERALIZE",
                                "patient_id": "PSEUDONYMIZE",
                                "admission_date": "DATE_SHIFT",
                                "diagnosis": "KEEP"
                            },
                            "reasoning": {
                                "national_id": "Saudi National ID directly identifies individuals",
                                "age": "Age is a quasi-identifier that can help identify when combined",
                                "diagnosis": "Medical diagnosis is the sensitive attribute to preserve"
                            },
                            "generalization_config": {
                                "age_level": 1,
                                "location_level": 1,
                                "date_level": 1
                            }
                        })
                    }
                }],
                "stop_reason": "tool_use"
            }

        if last_user_msg and any(word in last_user_msg.lower() for word in ["approve", "proceed", "yes", "go ahead"]):
            return {
                "content": "Starting the anonymization pipeline now.",
                "tool_calls": [{
                    "id": "mock_tool_2",
                    "type": "function",
                    "function": {
                        "name": "execute_pipeline",
                        "arguments": json.dumps({"confirmed": True})
                    }
                }],
                "stop_reason": "tool_use"
            }

        return {
            "content": "I understand. How can I help you with the anonymization process? You can upload a CSV file, ask questions about the classification, or adjust the privacy thresholds.",
            "tool_calls": [],
            "stop_reason": "end_turn"
        }


# Global adapter instance
_llm_adapter: Optional[LLMAdapter] = None


def get_llm_adapter() -> LLMAdapter:
    """Get or create the LLM adapter singleton."""
    global _llm_adapter
    if _llm_adapter is None:
        _llm_adapter = LLMAdapter()
    return _llm_adapter
