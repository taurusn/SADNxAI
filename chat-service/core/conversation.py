"""
Conversation Manager
Manages conversation state and transitions
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.models import Session, SessionStatus, Message, MessageRole, Classification
from shared.openai_schema import get_system_prompt


class ConversationManager:
    """
    Manages conversation flow and state transitions.

    State machine:
    IDLE → [upload] → ANALYZING → [AI proposes] → PROPOSED
    → [user responds] → DISCUSSING → [approve] → APPROVED
    → MASKING → VALIDATING → COMPLETED | FAILED
    """

    def __init__(self, session: Session):
        """
        Initialize conversation manager.

        Args:
            session: Current session
        """
        self.session = session

    def get_messages_for_llm(self) -> list[dict]:
        """
        Get messages formatted for LLM API.

        Returns:
            List of message dicts with role and content
        """
        messages = []

        # Add system prompt
        messages.append({
            "role": "system",
            "content": get_system_prompt()
        })

        # Add context about current state
        context = self._build_context()
        if context:
            messages.append({
                "role": "system",
                "content": context
            })

        # Add conversation history
        for msg in self.session.messages:
            msg_dict = {"role": msg.role.value, "content": msg.content}

            # Include tool calls if present
            if msg.tool_calls:
                msg_dict["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": tc.function
                    }
                    for tc in msg.tool_calls
                ]

            # Include tool_call_id if present
            if msg.tool_call_id:
                msg_dict["tool_call_id"] = msg.tool_call_id

            messages.append(msg_dict)

        return messages

    def _build_context(self) -> str:
        """
        Build context message with current session state.

        Returns:
            Context string for LLM
        """
        parts = []

        # File information
        if self.session.file_path:
            parts.append(f"CURRENT FILE: {self.session.title}")
            parts.append(f"COLUMNS: {', '.join(self.session.columns)}")
            parts.append(f"ROW COUNT: {self.session.row_count}")

            if self.session.sample_data:
                parts.append("SAMPLE DATA (first 5 rows):")
                for i, row in enumerate(self.session.sample_data[:5]):
                    parts.append(f"  Row {i+1}: {row}")

        # Current classification
        if self.session.classification:
            c = self.session.classification
            parts.append("\nCURRENT CLASSIFICATION:")
            if c.direct_identifiers:
                parts.append(f"  Direct Identifiers (SUPPRESS): {c.direct_identifiers}")
            if c.quasi_identifiers:
                parts.append(f"  Quasi-Identifiers (GENERALIZE): {c.quasi_identifiers}")
            if c.linkage_identifiers:
                parts.append(f"  Linkage Identifiers (PSEUDONYMIZE): {c.linkage_identifiers}")
            if c.date_columns:
                parts.append(f"  Date Columns (DATE_SHIFT): {c.date_columns}")
            if c.sensitive_attributes:
                parts.append(f"  Sensitive Attributes (KEEP): {c.sensitive_attributes}")

        # Current thresholds
        th = self.session.thresholds
        parts.append(f"\nPRIVACY THRESHOLDS:")
        parts.append(f"  k-Anonymity: min={th.k_anonymity.minimum}, target={th.k_anonymity.target}")
        parts.append(f"  l-Diversity: min={th.l_diversity.minimum}, target={th.l_diversity.target}")
        parts.append(f"  t-Closeness: min={th.t_closeness.minimum}, target={th.t_closeness.target}")
        parts.append(f"  Risk Score: max={th.risk_score.minimum}%, target={th.risk_score.target}%")

        # Current status
        parts.append(f"\nCURRENT STATUS: {self.session.status.value}")

        # Validation result if available
        if self.session.validation_result:
            vr = self.session.validation_result
            parts.append(f"\nVALIDATION RESULT: {'PASSED' if vr.passed else 'FAILED'}")
            for name, metric in vr.metrics.items():
                status = "✓" if metric.passed else "✗"
                parts.append(f"  {name}: {metric.value} (threshold: {metric.threshold}) {status}")

        return "\n".join(parts) if parts else ""

    def should_analyze_file(self) -> bool:
        """Check if AI should analyze a newly uploaded file."""
        return (
            self.session.status == SessionStatus.ANALYZING and
            self.session.file_path is not None and
            self.session.classification is None
        )

    def can_execute_pipeline(self) -> bool:
        """Check if pipeline execution is allowed."""
        return (
            self.session.status == SessionStatus.APPROVED and
            self.session.classification is not None and
            self.session.file_path is not None
        )

    def detect_approval(self, user_message: str) -> bool:
        """
        Detect if user message contains explicit approval.

        Args:
            user_message: User's message text

        Returns:
            True if approval detected
        """
        approval_phrases = [
            "approve", "approved", "yes", "proceed", "go ahead",
            "execute", "run it", "do it", "let's go", "confirm",
            "agreed", "looks good", "lgtm", "ship it"
        ]

        message_lower = user_message.lower().strip()

        # Check for explicit approval
        for phrase in approval_phrases:
            if phrase in message_lower:
                return True

        return False

    def get_next_status(self, current_status: SessionStatus, event: str) -> SessionStatus:
        """
        Determine next status based on current status and event.

        Args:
            current_status: Current session status
            event: Event that occurred (upload, propose, approve, mask_done, validate_pass, validate_fail)

        Returns:
            Next status
        """
        transitions = {
            (SessionStatus.IDLE, "upload"): SessionStatus.ANALYZING,
            (SessionStatus.ANALYZING, "propose"): SessionStatus.PROPOSED,
            (SessionStatus.PROPOSED, "discuss"): SessionStatus.DISCUSSING,
            (SessionStatus.DISCUSSING, "discuss"): SessionStatus.DISCUSSING,
            (SessionStatus.PROPOSED, "approve"): SessionStatus.APPROVED,
            (SessionStatus.DISCUSSING, "approve"): SessionStatus.APPROVED,
            (SessionStatus.APPROVED, "mask_start"): SessionStatus.MASKING,
            (SessionStatus.MASKING, "mask_done"): SessionStatus.VALIDATING,
            (SessionStatus.VALIDATING, "validate_pass"): SessionStatus.COMPLETED,
            (SessionStatus.VALIDATING, "validate_fail"): SessionStatus.FAILED,
            (SessionStatus.FAILED, "retry"): SessionStatus.DISCUSSING,
        }

        return transitions.get((current_status, event), current_status)
