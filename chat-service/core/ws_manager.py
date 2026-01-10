"""
WebSocket Connection Manager
Handles WebSocket connections per session with thread-safe operations
"""

import asyncio
import time
from typing import Dict, Set, Optional, Any
from fastapi import WebSocket
import json


class ConnectionManager:
    """
    Manages WebSocket connections organized by session.

    Features:
    - Multiple connections per session (tabs/devices)
    - Thread-safe connection management
    - Broadcast to all connections in a session
    - Individual connection messaging
    - Connection heartbeat tracking
    """

    def __init__(self):
        # session_id -> set of WebSocket connections
        self._connections: Dict[str, Set[WebSocket]] = {}
        # websocket -> last heartbeat timestamp
        self._heartbeats: Dict[WebSocket, float] = {}
        # Lock for thread-safe operations
        self._lock = asyncio.Lock()

    async def connect(self, session_id: str, websocket: WebSocket) -> bool:
        """
        Accept and register a WebSocket connection for a session.

        Args:
            session_id: The session ID to associate with this connection
            websocket: The WebSocket connection to register

        Returns:
            True if connection was successful
        """
        try:
            await websocket.accept()

            async with self._lock:
                if session_id not in self._connections:
                    self._connections[session_id] = set()
                self._connections[session_id].add(websocket)
                self._heartbeats[websocket] = time.time()

            print(f"[WS] Connected: session={session_id}, total_connections={len(self._connections.get(session_id, set()))}")
            return True

        except Exception as e:
            print(f"[WS] Connection failed: {e}")
            return False

    async def disconnect(self, session_id: str, websocket: WebSocket) -> None:
        """
        Remove a WebSocket connection from a session.

        Args:
            session_id: The session ID the connection belongs to
            websocket: The WebSocket connection to remove
        """
        async with self._lock:
            if session_id in self._connections:
                self._connections[session_id].discard(websocket)
                # Clean up empty sessions
                if not self._connections[session_id]:
                    del self._connections[session_id]

            # Clean up heartbeat tracking
            self._heartbeats.pop(websocket, None)

        print(f"[WS] Disconnected: session={session_id}")

    async def send_to_session(self, session_id: str, message: Dict[str, Any]) -> int:
        """
        Broadcast a message to all connections in a session.

        Args:
            session_id: The session to broadcast to
            message: The message dict to send (will be JSON encoded)

        Returns:
            Number of connections that received the message
        """
        if session_id not in self._connections:
            return 0

        # Add timestamp if not present
        if "timestamp" not in message:
            message["timestamp"] = time.time()

        dead_connections: Set[WebSocket] = set()
        sent_count = 0

        # Get a copy of connections to iterate
        connections = self._connections.get(session_id, set()).copy()

        for websocket in connections:
            try:
                await websocket.send_json(message)
                sent_count += 1
            except Exception as e:
                print(f"[WS] Send failed, marking dead: {e}")
                dead_connections.add(websocket)

        # Clean up dead connections
        for ws in dead_connections:
            await self.disconnect(session_id, ws)

        return sent_count

    async def send_to_websocket(self, websocket: WebSocket, message: Dict[str, Any]) -> bool:
        """
        Send a message to a specific WebSocket connection.

        Args:
            websocket: The WebSocket to send to
            message: The message dict to send

        Returns:
            True if send was successful
        """
        # Add timestamp if not present
        if "timestamp" not in message:
            message["timestamp"] = time.time()

        try:
            await websocket.send_json(message)
            return True
        except Exception as e:
            print(f"[WS] Send to websocket failed: {e}")
            return False

    def update_heartbeat(self, websocket: WebSocket) -> None:
        """Update the heartbeat timestamp for a connection."""
        self._heartbeats[websocket] = time.time()

    def get_connection_count(self, session_id: str) -> int:
        """Get the number of connections for a session."""
        return len(self._connections.get(session_id, set()))

    def get_total_connections(self) -> int:
        """Get the total number of active connections."""
        return sum(len(conns) for conns in self._connections.values())

    def get_session_ids(self) -> Set[str]:
        """Get all session IDs with active connections."""
        return set(self._connections.keys())


# Global connection manager instance
manager = ConnectionManager()
