"""
SADNxAI State-Based Prompt Templates

Provides optimized prompts for each session state to reduce token usage
while maintaining context relevance.
"""

from .base import BASE_CONTEXT, TOOL_FORMAT
from .idle import IDLE_PROMPT
from .analyzing import ANALYZING_PROMPT
from .proposed import PROPOSED_PROMPT
from .discussing import DISCUSSING_PROMPT
from .approved import APPROVED_PROMPT
from .completed import COMPLETED_PROMPT
from .failed import FAILED_PROMPT


def get_prompt_for_state(status: str) -> str:
    """
    Get optimized prompt template for the given session state.

    Args:
        status: Session status string (idle, analyzing, proposed, etc.)

    Returns:
        Optimized system prompt for the state
    """
    status_lower = status.lower() if status else "idle"

    prompts = {
        "idle": IDLE_PROMPT,
        "analyzing": ANALYZING_PROMPT,
        "proposed": PROPOSED_PROMPT,
        "discussing": DISCUSSING_PROMPT,
        "approved": APPROVED_PROMPT,
        "masking": APPROVED_PROMPT,
        "validating": APPROVED_PROMPT,
        "completed": COMPLETED_PROMPT,
        "failed": FAILED_PROMPT,
    }

    return prompts.get(status_lower, ANALYZING_PROMPT)


__all__ = [
    "get_prompt_for_state",
    "BASE_CONTEXT",
    "TOOL_FORMAT",
    "IDLE_PROMPT",
    "ANALYZING_PROMPT",
    "PROPOSED_PROMPT",
    "DISCUSSING_PROMPT",
    "APPROVED_PROMPT",
    "COMPLETED_PROMPT",
    "FAILED_PROMPT",
]
