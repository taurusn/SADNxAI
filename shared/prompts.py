"""
SADNxAI - State-Based System Prompts
Optimized prompts for each session state
"""

from shared.openai_schema import SYSTEM_PROMPT


# State-specific instructions to append to base prompt
ANALYZING_INSTRUCTION = """

## ⚠️ CRITICAL: YOU MUST CALL classify_columns NOW ⚠️

A file has been uploaded. Your ONLY job right now is to call the `classify_columns` tool.

**DO NOT** just describe the classification in text.
**DO NOT** explain what you would do.
**YOU MUST** call the `classify_columns` tool with ALL columns from the file.

If you respond with text only and no tool call, the system will fail.

The tool call format is:
```tool_call
{"tool": "classify_columns", "arguments": {...}}
```

Or if using native tools, just call the function directly.

NOW CALL THE TOOL with ALL columns from CURRENT FILE section below.
"""

APPROVED_INSTRUCTION = """

## ⚠️ USER APPROVED - CALL execute_pipeline NOW ⚠️

The user has approved the classification. Your ONLY job is to call `execute_pipeline`.

```tool_call
{"tool": "execute_pipeline", "arguments": {"confirmed": true}}
```
"""


def get_prompt_for_state(status: str) -> str:
    """
    Get the appropriate system prompt for the given session state.

    Args:
        status: Session status string (idle, analyzing, proposed, etc.)

    Returns:
        System prompt string optimized for the state
    """
    status = status.lower() if status else "idle"

    base = SYSTEM_PROMPT

    # Add state-specific instructions
    if status == "analyzing":
        return base + ANALYZING_INSTRUCTION
    elif status == "approved":
        return base + APPROVED_INSTRUCTION

    return base
