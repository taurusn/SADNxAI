"""
SADNxAI - vLLM Adapter
Uses OpenAI-compatible API with native streaming tool call support.
Much simpler than Ollama adapter - no regex parsing needed!
"""

import os
import json
import httpx
from typing import List, Dict, Any, Optional, AsyncGenerator

from openai import AsyncOpenAI

from shared.openai_schema import get_system_prompt, get_tools
from shared.prompts import get_prompt_for_state


class VLLMAdapter:
    """Adapter for vLLM using OpenAI-compatible API with native tool calling."""

    def __init__(self):
        self.base_url = os.getenv("VLLM_URL", "http://localhost:8000")
        self.api_key = os.getenv("VLLM_API_KEY", "token-sadnxai")
        self.model = os.getenv("VLLM_MODEL", "meta-llama/Llama-3.1-8B-Instruct")
        self.system_prompt = get_system_prompt()
        self.tools = get_tools()
        self.timeout = 240.0  # 4 minutes for inference

        # Lazy-initialized AsyncOpenAI client
        self._client: Optional[AsyncOpenAI] = None

    def _get_client(self) -> AsyncOpenAI:
        """Get or create AsyncOpenAI client."""
        if self._client is None:
            self._client = AsyncOpenAI(
                base_url=f"{self.base_url}/v1",
                api_key=self.api_key,
                timeout=self.timeout
            )
        return self._client

    async def check_health(self) -> bool:
        """Check if vLLM is healthy and ready."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/health",
                    timeout=10.0
                )
                return response.status_code == 200
        except Exception as e:
            print(f"vLLM health check failed: {e}")
            return False

    async def chat(
        self,
        messages: List[Dict[str, Any]],
        session_context: Optional[Dict[str, Any]] = None,
        max_retries: int = 2
    ) -> Dict[str, Any]:
        """
        Send non-streaming chat request to vLLM.

        Args:
            messages: Conversation history
            session_context: Current session context (file info, classification, etc.)
            max_retries: Number of retries for failed requests

        Returns:
            Response dict with content and tool_calls
        """
        client = self._get_client()

        # Build messages with system prompt
        full_messages = [
            {"role": "system", "content": self._build_system_prompt(session_context)}
        ]

        # Add conversation history, skip system messages
        for msg in messages:
            role = msg.get("role", "user")
            if role == "system":
                continue
            full_messages.append({
                "role": role,
                "content": msg.get("content", "")
            })

        for attempt in range(max_retries + 1):
            try:
                response = await client.chat.completions.create(
                    model=self.model,
                    messages=full_messages,
                    tools=self.tools,
                    tool_choice="auto",
                    temperature=0.1,
                    max_tokens=4096
                )

                message = response.choices[0].message
                content = message.content or ""
                tool_calls = None

                # Extract tool calls (already in OpenAI format!)
                if message.tool_calls:
                    tool_calls = []
                    for tc in message.tool_calls:
                        tool_calls.append({
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        })

                return {
                    "content": content,
                    "tool_calls": tool_calls
                }

            except Exception as e:
                if attempt < max_retries:
                    print(f"vLLM chat error (attempt {attempt + 1}): {e}")
                    continue
                print(f"vLLM chat error (final): {e}")
                return {
                    "content": f"Error communicating with vLLM: {str(e)}",
                    "tool_calls": None
                }

        return {"content": "Max retries exceeded", "tool_calls": None}

    async def chat_stream(
        self,
        messages: List[Dict[str, Any]],
        session_context: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream chat response with native tool calling support.

        vLLM streams tool calls natively - no regex parsing needed!

        Yields:
            {"type": "token", "content": "..."} for text tokens
            {"type": "done", "content": "...", "tool_calls": [...]} when complete
        """
        client = self._get_client()

        # Build messages with system prompt
        full_messages = [
            {"role": "system", "content": self._build_system_prompt(session_context)}
        ]

        # Add conversation history, skip system messages
        for msg in messages:
            role = msg.get("role", "user")
            if role == "system":
                continue

            msg_dict = {
                "role": role,
                "content": msg.get("content", "")
            }

            # Include tool_calls if present (for assistant messages)
            if msg.get("tool_calls"):
                msg_dict["tool_calls"] = msg["tool_calls"]

            # Include tool_call_id if present (for tool result messages)
            if msg.get("tool_call_id"):
                msg_dict["tool_call_id"] = msg["tool_call_id"]

            full_messages.append(msg_dict)

        try:
            # Create streaming chat completion with tools
            response = await client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                tools=self.tools,
                tool_choice="auto",
                stream=True,
                temperature=0.1,
                max_tokens=4096
            )

            full_content = ""
            tool_calls = []

            # Process streaming response
            async for chunk in response:
                if not chunk.choices:
                    continue

                delta = chunk.choices[0].delta
                finish_reason = chunk.choices[0].finish_reason

                # Handle text content
                if delta.content:
                    full_content += delta.content
                    yield {"type": "token", "content": delta.content}

                # Handle streaming tool calls (vLLM native support!)
                if delta.tool_calls:
                    for tc_delta in delta.tool_calls:
                        idx = tc_delta.index if tc_delta.index is not None else 0

                        # Expand tool_calls list if needed
                        while len(tool_calls) <= idx:
                            tool_calls.append({
                                "id": "",
                                "type": "function",
                                "function": {"name": "", "arguments": ""}
                            })

                        # Accumulate tool call data
                        if tc_delta.id:
                            tool_calls[idx]["id"] = tc_delta.id
                        if tc_delta.function:
                            if tc_delta.function.name:
                                tool_calls[idx]["function"]["name"] = tc_delta.function.name
                            if tc_delta.function.arguments:
                                tool_calls[idx]["function"]["arguments"] += tc_delta.function.arguments

                # Check for completion
                if finish_reason in ("stop", "tool_calls"):
                    # Filter out incomplete tool calls
                    valid_tool_calls = [
                        tc for tc in tool_calls
                        if tc["id"] and tc["function"]["name"]
                    ]

                    yield {
                        "type": "done",
                        "content": full_content,
                        "tool_calls": valid_tool_calls if valid_tool_calls else None
                    }
                    return

            # Fallback if no finish_reason received
            valid_tool_calls = [
                tc for tc in tool_calls
                if tc["id"] and tc["function"]["name"]
            ]

            yield {
                "type": "done",
                "content": full_content,
                "tool_calls": valid_tool_calls if valid_tool_calls else None
            }

        except Exception as e:
            print(f"vLLM stream error: {e}")
            yield {
                "type": "done",
                "content": f"Error: {str(e)}",
                "tool_calls": None
            }

    def _build_system_prompt(self, session_context: Optional[Dict[str, Any]] = None) -> str:
        """Build system prompt with session context using state-based templates."""
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

        # Add TOON format info if enabled
        format_info = get_format_info()
        if format_info:
            prompt += f"\n\n## DATA FORMAT\n{format_info}\n"

        # Add dynamic context based on state
        if session_context:
            # ALWAYS include file info if available
            if session_context.get("file_info"):
                fi = session_context["file_info"]
                prompt += f"\n\n## CURRENT FILE: {fi.get('filename', '?')} ({fi.get('row_count', '?')} rows)\n"
                columns = fi.get('columns', [])
                prompt += f"Columns: {', '.join(columns)}\n"

                # Format sample data
                sample_data = fi.get("sample_data")
                if sample_data and isinstance(sample_data, list) and len(sample_data) > 0:
                    prompt += "\n### Sample Data:\n"
                    if is_toon_enabled():
                        prompt += format_sample_data_for_prompt(sample_data)
                        prompt += "\n"
                    else:
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
                    prompt += format_classification_for_prompt(cls)
                    prompt += "\n"
                else:
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


# Singleton instance
_vllm_adapter: Optional[VLLMAdapter] = None


def get_vllm_adapter() -> VLLMAdapter:
    """Get or create the vLLM adapter singleton."""
    global _vllm_adapter
    if _vllm_adapter is None:
        _vllm_adapter = VLLMAdapter()
    return _vllm_adapter
