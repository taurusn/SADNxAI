"""
SADNxAI - State-Based System Prompts
Optimized prompts for each session state
"""

from shared.openai_schema import SYSTEM_PROMPT


def get_prompt_for_state(status: str) -> str:
    """
    Get the appropriate system prompt for the given session state.

    Args:
        status: Session status string (idle, analyzing, proposed, etc.)

    Returns:
        System prompt string optimized for the state
    """
    status = status.lower() if status else "idle"

    # For most states, use the full system prompt
    # This ensures the LLM has all context needed
    return SYSTEM_PROMPT
