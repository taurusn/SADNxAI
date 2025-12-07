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
    """Adapter for Ollama local LLM"""

    def __init__(self):
        self.base_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
        self.system_prompt = get_system_prompt()
        self.tools = get_tools()
        self.timeout = 240.0  # 4 minutes for CPU inference
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
        session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send chat request to Ollama
        """
        # Build the full message list with system prompt
        full_messages = [
            {"role": "system", "content": self._build_system_prompt(session_context)}
        ]

        # Add conversation history
        for msg in messages:
            full_messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })

        try:
            client = await self._get_client()
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": full_messages,
                    "stream": False,
                    "keep_alive": "10m",  # Keep model loaded for 10 minutes
                    "options": {
                        "temperature": 0.7,
                        "num_ctx": 4096,  # Context window for full prompts
                    }
                },
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
            assistant_message = data.get("message", {}).get("content", "")

            # Parse for tool calls
            tool_calls = self._extract_tool_calls(assistant_message)

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
                prompt += f"\n\n## FILE: {fi.get('filename', '?')} ({fi.get('row_count', '?')} rows)\n"
                prompt += f"Columns: {', '.join(fi.get('columns', []))}\n"
                if fi.get("sample_data"):
                    prompt += f"Sample:\n```\n{fi['sample_data']}\n```\n"

            if session_context.get("classification"):
                prompt += f"\n## CLASSIFICATION:\n```json\n{json.dumps(session_context['classification'], indent=2)}\n```\n"

        return prompt

    def _extract_tool_calls(self, content: str) -> Optional[List[Dict[str, Any]]]:
        """Extract tool calls from the response"""
        import re

        # Look for ```tool_call blocks
        pattern = r'```tool_call\s*\n?(.*?)\n?```'
        matches = re.findall(pattern, content, re.DOTALL)

        if not matches:
            # Also try JSON blocks with "tool" key
            pattern = r'```(?:json)?\s*\n?(\{[^`]*"tool"[^`]*\})\n?```'
            matches = re.findall(pattern, content, re.DOTALL)

        if not matches:
            return None

        tool_calls = []
        for match in matches:
            try:
                data = json.loads(match.strip())
                if "tool" in data:
                    tool_calls.append({
                        "id": f"call_{len(tool_calls)}",
                        "type": "function",
                        "function": {
                            "name": data["tool"],
                            "arguments": json.dumps(data.get("arguments", {}))
                        }
                    })
            except json.JSONDecodeError:
                continue

        return tool_calls if tool_calls else None

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
