"""
Session Manager
Handles session persistence with Redis
"""

import json
import os
import uuid
from datetime import datetime
from typing import List, Optional

import redis

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.models import Session, SessionStatus, Message, Classification, PrivacyThresholds, ValidationResult


class SessionManager:
    """
    Manages session state persistence with Redis.

    Sessions store:
    - Chat history
    - File metadata
    - Classification results
    - Validation results
    - Privacy thresholds
    """

    def __init__(self, redis_url: Optional[str] = None):
        """
        Initialize session manager.

        Args:
            redis_url: Redis connection URL (default from env)
        """
        redis_url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.session_prefix = "session:"
        self.session_list_key = "sessions"

    def _serialize_session(self, session: Session) -> str:
        """Serialize session to JSON string"""
        return session.model_dump_json()

    def _deserialize_session(self, data: str) -> Session:
        """Deserialize session from JSON string"""
        return Session.model_validate_json(data)

    def create_session(self, title: str = "New Chat") -> Session:
        """
        Create a new session.

        Args:
            title: Session title (default: "New Chat")

        Returns:
            New Session object
        """
        session = Session(
            id=str(uuid.uuid4()),
            title=title,
            status=SessionStatus.IDLE,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Save to Redis
        key = f"{self.session_prefix}{session.id}"
        self.redis.set(key, self._serialize_session(session))

        # Add to session list
        self.redis.zadd(self.session_list_key, {session.id: datetime.utcnow().timestamp()})

        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """
        Get session by ID.

        Args:
            session_id: Session UUID

        Returns:
            Session or None if not found
        """
        key = f"{self.session_prefix}{session_id}"
        data = self.redis.get(key)

        if data is None:
            return None

        return self._deserialize_session(data)

    def update_session(self, session: Session) -> Session:
        """
        Update existing session.

        Args:
            session: Session object with updates

        Returns:
            Updated session
        """
        session.updated_at = datetime.utcnow()

        key = f"{self.session_prefix}{session.id}"
        self.redis.set(key, self._serialize_session(session))

        # Update timestamp in list
        self.redis.zadd(self.session_list_key, {session.id: datetime.utcnow().timestamp()})

        return session

    def delete_session(self, session_id: str) -> bool:
        """
        Delete session.

        Args:
            session_id: Session UUID

        Returns:
            True if deleted, False if not found
        """
        key = f"{self.session_prefix}{session_id}"
        result = self.redis.delete(key)
        self.redis.zrem(self.session_list_key, session_id)

        return result > 0

    def list_sessions(self, limit: int = 50, offset: int = 0) -> List[Session]:
        """
        List sessions ordered by most recent.

        Args:
            limit: Max sessions to return
            offset: Pagination offset

        Returns:
            List of sessions
        """
        # Get session IDs sorted by timestamp (most recent first)
        session_ids = self.redis.zrevrange(
            self.session_list_key,
            offset,
            offset + limit - 1
        )

        sessions = []
        for session_id in session_ids:
            session = self.get_session(session_id)
            if session:
                sessions.append(session)

        return sessions

    def add_message(self, session_id: str, message: Message) -> Optional[Session]:
        """
        Add message to session.

        Args:
            session_id: Session UUID
            message: Message to add

        Returns:
            Updated session or None if not found
        """
        session = self.get_session(session_id)
        if session is None:
            return None

        session.messages.append(message)
        return self.update_session(session)

    def set_status(self, session_id: str, status: SessionStatus) -> Optional[Session]:
        """
        Update session status.

        Args:
            session_id: Session UUID
            status: New status

        Returns:
            Updated session or None if not found
        """
        session = self.get_session(session_id)
        if session is None:
            return None

        session.status = status
        return self.update_session(session)

    def set_classification(self, session_id: str, classification: Classification) -> Optional[Session]:
        """
        Set classification for session.

        Args:
            session_id: Session UUID
            classification: Classification result

        Returns:
            Updated session or None if not found
        """
        session = self.get_session(session_id)
        if session is None:
            return None

        session.classification = classification
        return self.update_session(session)

    def set_validation_result(self, session_id: str, result: ValidationResult) -> Optional[Session]:
        """
        Set validation result for session.

        Args:
            session_id: Session UUID
            result: Validation result

        Returns:
            Updated session or None if not found
        """
        session = self.get_session(session_id)
        if session is None:
            return None

        session.validation_result = result
        return self.update_session(session)

    def set_thresholds(self, session_id: str, thresholds: PrivacyThresholds) -> Optional[Session]:
        """
        Update privacy thresholds.

        Args:
            session_id: Session UUID
            thresholds: New thresholds

        Returns:
            Updated session or None if not found
        """
        session = self.get_session(session_id)
        if session is None:
            return None

        session.thresholds = thresholds
        return self.update_session(session)
