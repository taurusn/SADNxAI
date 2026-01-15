"""
SADNxAI - State-Based System Prompts
Optimized prompts for each session state
"""

from shared.openai_schema import SYSTEM_PROMPT


# State-specific instructions to append to base prompt
ANALYZING_INSTRUCTION = """

## IMPORTANT: CALL classify_columns TOOL NOW

A file has been uploaded. You MUST call the `classify_columns` tool immediately.

- Analyze the columns shown in CURRENT FILE section below
- Call the `classify_columns` tool with ALL columns classified appropriately
- Do NOT just describe what you would do - actually call the tool

The tool will be called automatically when you decide to use it.
"""

APPROVED_INSTRUCTION = """

## USER APPROVED - CALL execute_pipeline TOOL NOW

The user has approved the classification. Call the `execute_pipeline` tool with `confirmed: true`.
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
