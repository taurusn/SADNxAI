"""
WebSocket API Routes
Real-time communication for chat and session updates
"""

import os
import json
import time
import asyncio
from typing import Dict, Any, Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.models import (
    Session, SessionStatus, Message, MessageRole, ToolCall
)

from core.session import SessionManager
from core.conversation import ConversationManager
from core.ws_manager import manager
from llm.adapter import LLMAdapter
from llm.tools import ToolExecutor
from pipeline.executor import PipelineExecutor


router = APIRouter()

# Initialize components (reuse from routes.py pattern)
session_manager = SessionManager()
llm_adapter = LLMAdapter(mock_mode=os.getenv("LLM_MOCK_MODE", "false").lower() == "true")
pipeline_executor = PipelineExecutor()

# Maximum iterations for agentic loop (safety limit)
MAX_AGENTIC_ITERATIONS = 10


def _build_session_context(session: Session) -> Dict[str, Any]:
    """Build session context for LLM with file info and classification."""
    context = {}

    if session.file_path:
        context["file_info"] = {
            "filename": session.title,
            "columns": session.columns,
            "row_count": session.row_count,
            "sample_data": session.sample_data
        }

    if session.classification:
        context["classification"] = {
            "direct_identifiers": session.classification.direct_identifiers,
            "quasi_identifiers": session.classification.quasi_identifiers,
            "linkage_identifiers": session.classification.linkage_identifiers,
            "date_columns": session.classification.date_columns,
            "sensitive_attributes": session.classification.sensitive_attributes,
            "recommended_techniques": session.classification.recommended_techniques
        }

    context["status"] = session.status.value
    return context


def _session_to_dict(session: Session) -> Dict[str, Any]:
    """Convert session to a dict suitable for WebSocket transmission."""
    return {
        "id": session.id,
        "title": session.title,
        "status": session.status.value,
        "file_path": session.file_path,
        "columns": session.columns,
        "sample_data": session.sample_data,
        "row_count": session.row_count,
        "classification": session.classification.model_dump() if session.classification else None,
        "thresholds": session.thresholds.model_dump(),
        "validation_result": session.validation_result.model_dump() if session.validation_result else None,
        "messages": [
            {
                "role": msg.role.value,
                "content": msg.content,
                "tool_calls": [tc.model_dump() for tc in msg.tool_calls] if msg.tool_calls else None,
                "tool_call_id": msg.tool_call_id
            }
            for msg in session.messages
        ],
        "output_path": session.output_path,
        "report_path": session.report_path,
        "created_at": session.created_at.isoformat(),
        "updated_at": session.updated_at.isoformat()
    }


async def _send_event(session_id: str, websocket: WebSocket, event_type: str, payload: Dict[str, Any], msg_id: Optional[str] = None) -> None:
    """Send a WebSocket event to the client."""
    message = {
        "type": event_type,
        "payload": payload,
        "timestamp": time.time()
    }
    if msg_id:
        message["id"] = msg_id

    await manager.send_to_websocket(websocket, message)


async def _broadcast_event(session_id: str, event_type: str, payload: Dict[str, Any]) -> None:
    """Broadcast a WebSocket event to all connections in a session."""
    message = {
        "type": event_type,
        "payload": payload,
        "timestamp": time.time()
    }
    await manager.send_to_session(session_id, message)


async def _handle_chat_message(
    session_id: str,
    websocket: WebSocket,
    message_text: str,
    msg_id: str
) -> None:
    """
    Handle a chat message from the client.

    This runs the agentic loop and streams responses via WebSocket.
    """
    session = session_manager.get_session(session_id)
    if not session:
        await _send_event(session_id, websocket, "error", {"message": "Session not found"}, msg_id)
        return

    # Add user message
    user_msg = Message(role=MessageRole.USER, content=message_text)
    session.messages.append(user_msg)

    # Check for approval
    print(f"[WS Chat] Session status: {session.status.value}, has_classification: {session.classification is not None}")
    conversation = ConversationManager(session)
    approval_detected = conversation.detect_approval(message_text)
    print(f"[WS Chat] Approval detected: {approval_detected}, message: '{message_text[:50]}...'")
    if approval_detected:
        if session.classification is not None:
            session.status = SessionStatus.APPROVED
            print(f"[WS Chat] Status changed to APPROVED")
        else:
            print(f"[WS Chat] Cannot approve - no classification yet")

    # Get messages for LLM
    messages = conversation.get_messages_for_llm()
    session_context = _build_session_context(session)
    tool_executor = ToolExecutor(session)

    # Track terminal tool info
    terminal_tool_info = None

    # Send thinking event
    await _send_event(session_id, websocket, "thinking", {"iteration": 1}, msg_id)

    iteration = 0
    while iteration < MAX_AGENTIC_ITERATIONS:
        iteration += 1
        print(f"[WS Agentic Loop] Iteration {iteration}")

        # Stream LLM response
        content = ""
        tool_calls_raw = None

        async for chunk in llm_adapter.chat_stream(messages, session_context):
            if chunk["type"] == "token":
                # Stream each token
                await _send_event(session_id, websocket, "token", {"content": chunk["content"]}, msg_id)
            elif chunk["type"] == "done":
                content = chunk.get("content", "")
                tool_calls_raw = chunk.get("tool_calls")

        # If no tool calls, we're done
        if not tool_calls_raw:
            print(f"[WS Agentic Loop] No tool calls, final response")
            print(f"[WS Agentic Loop] Content length: {len(content)} chars")
            print(f"[WS Agentic Loop] Content preview: {content[:200]}..." if len(content) > 200 else f"[WS Agentic Loop] Content: {content}")
            if content.strip():
                final_msg = Message(role=MessageRole.ASSISTANT, content=content)
                session.messages.append(final_msg)

            await _send_event(session_id, websocket, "message", {"content": content}, msg_id)
            break

        print(f"[WS Agentic Loop] Processing {len(tool_calls_raw)} tool call(s)")

        # Build ToolCall objects
        tool_calls = []
        for tc in tool_calls_raw:
            tool_calls.append(ToolCall(
                id=tc["id"],
                type=tc["type"],
                function=tc["function"]
            ))

        # Add assistant message with tool calls
        if content.strip():
            assistant_msg = Message(
                role=MessageRole.ASSISTANT,
                content=content,
                tool_calls=tool_calls
            )
            session.messages.append(assistant_msg)

        # Add to messages for next LLM call
        messages.append({
            "role": "assistant",
            "content": content,
            "tool_calls": tool_calls_raw
        })

        should_break = False

        # Execute each tool
        for tc in tool_calls_raw:
            tool_name = tc["function"]["name"]

            # Parse arguments
            try:
                args_raw = tc["function"]["arguments"]
                if isinstance(args_raw, str):
                    args = json.loads(args_raw)
                elif isinstance(args_raw, dict):
                    args = args_raw
                else:
                    args = {}
            except (json.JSONDecodeError, TypeError, KeyError) as e:
                print(f"[WS Agentic Loop] Failed to parse tool arguments: {e}")
                await _send_event(session_id, websocket, "error", {"message": f"Invalid tool arguments: {e}"}, msg_id)
                continue

            # Send tool_start event
            await _send_event(session_id, websocket, "tool_start", {"tool": tool_name, "args": args}, msg_id)

            # Check if terminal tool
            if tool_name == "execute_pipeline":
                print(f"[WS Agentic Loop] Terminal tool: execute_pipeline")
                terminal_tool_info = {"tool_name": tool_name, "args": args, "tool_call": tc}
                should_break = True
                continue

            # Execute tool
            print(f"[WS Agentic Loop] Executing: {tool_name}")
            result = await tool_executor.execute(tool_name, args)

            # Send tool_end event
            await _send_event(session_id, websocket, "tool_end", {
                "tool": tool_name,
                "success": result.get("success", False),
                "result": result
            }, msg_id)

            # Add tool result to session
            tool_result_msg = Message(
                role=MessageRole.TOOL,
                content=json.dumps(result),
                tool_call_id=tc["id"]
            )
            session.messages.append(tool_result_msg)

            # Add to messages for next LLM call
            messages.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tc["id"]
            })

            # Track classification updates
            if tool_name == "classify_columns" and result.get("success"):
                session.status = SessionStatus.PROPOSED
                session_context = _build_session_context(session)
                print(f"[WS Agentic Loop] Classification updated, status -> PROPOSED")

        if should_break:
            break

    # Handle execute_pipeline if called
    print(f"[WS Pipeline] terminal_tool_info={terminal_tool_info}")
    if terminal_tool_info and terminal_tool_info["tool_name"] == "execute_pipeline":
        print(f"[WS Pipeline] Executing pipeline...")
        tc = terminal_tool_info["tool_call"]
        args = terminal_tool_info["args"]
        print(f"[WS Pipeline] tc={tc}, args={args}")

        await _send_event(session_id, websocket, "pipeline_start", {"message": "Starting anonymization pipeline..."}, msg_id)
        print(f"[WS Pipeline] Sent pipeline_start event")

        # Execute the tool
        print(f"[WS Pipeline] Calling tool_executor.execute...")
        tool_result = await tool_executor.execute("execute_pipeline", args)
        print(f"[WS Pipeline] tool_result={tool_result}")

        # Add tool result
        tool_result_msg = Message(
            role=MessageRole.TOOL,
            content=json.dumps(tool_result),
            tool_call_id=tc["id"]
        )
        session.messages.append(tool_result_msg)

        if tool_result.get("success"):
            session.status = SessionStatus.MASKING

            # Clean up old output/report files
            if session.output_path and os.path.exists(session.output_path):
                os.remove(session.output_path)
                session.output_path = None
            if session.report_path and os.path.exists(session.report_path):
                os.remove(session.report_path)
                session.report_path = None
            session.validation_result = None

            session_manager.update_session(session)

            await _send_event(session_id, websocket, "pipeline_progress", {"stage": "masking", "message": "Applying anonymization techniques..."}, msg_id)

            # Execute pipeline
            pipeline_result = await pipeline_executor.execute(session)

            if pipeline_result.get("error"):
                session.status = SessionStatus.FAILED
                await _send_event(session_id, websocket, "message", {"content": f"Pipeline execution failed: {pipeline_result['error']}"}, msg_id)
            else:
                if pipeline_result.get("validation_result"):
                    session.validation_result = pipeline_result["validation_result"]
                    session.output_path = pipeline_result.get("output_path")
                    session.report_path = pipeline_result.get("report_path")

                    if pipeline_result["validation_result"].passed:
                        session.status = SessionStatus.COMPLETED
                        await _send_event(session_id, websocket, "message", {
                            "content": "Anonymization complete! Validation passed. You can now download the anonymized CSV and privacy report."
                        }, msg_id)
                    else:
                        session.status = SessionStatus.FAILED
                        failed = pipeline_result["validation_result"].failed_metrics
                        await _send_event(session_id, websocket, "message", {
                            "content": f"Validation failed for metrics: {', '.join(failed)}. You can still download the anonymized CSV and report. Would you like to adjust the generalization levels or thresholds and try again?"
                        }, msg_id)

    # Save session
    session_manager.update_session(session)

    # Send final session state and done event
    await _send_event(session_id, websocket, "session", _session_to_dict(session), msg_id)
    await _send_event(session_id, websocket, "done", {
        "status": session.status.value,
        "has_classification": session.classification is not None,
        "has_validation": session.validation_result is not None
    }, msg_id)


async def _handle_ping(session_id: str, websocket: WebSocket, msg_id: str) -> None:
    """Handle ping message."""
    manager.update_heartbeat(websocket)
    await _send_event(session_id, websocket, "pong", {}, msg_id)


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time chat and session updates.

    Message Protocol:

    Client -> Server:
    {
        "type": "chat" | "ping",
        "payload": { "message": "..." },
        "id": "correlation-id"
    }

    Server -> Client:
    {
        "type": "connected" | "session" | "token" | "thinking" |
                "tool_start" | "tool_end" | "pipeline_start" |
                "pipeline_progress" | "message" | "done" | "error" | "pong",
        "payload": { ... },
        "id": "correlation-id",
        "timestamp": 1234567890.123
    }
    """
    # Validate session exists
    session = session_manager.get_session(session_id)
    if not session:
        await websocket.close(code=4004, reason="Session not found")
        return

    # Accept connection
    connected = await manager.connect(session_id, websocket)
    if not connected:
        return

    try:
        # Send connected event
        await _send_event(session_id, websocket, "connected", {"session_id": session_id})

        # Send initial session state
        await _send_event(session_id, websocket, "session", _session_to_dict(session))

        # Message loop
        while True:
            try:
                # Receive message with timeout for heartbeat
                data = await asyncio.wait_for(websocket.receive_json(), timeout=60.0)

                msg_type = data.get("type", "")
                payload = data.get("payload", {})
                msg_id = data.get("id", "")

                print(f"[WS] Received: type={msg_type}, id={msg_id}")

                if msg_type == "ping":
                    await _handle_ping(session_id, websocket, msg_id)

                elif msg_type == "chat":
                    message_text = payload.get("message", "")
                    if message_text.strip():
                        await _handle_chat_message(session_id, websocket, message_text, msg_id)
                    else:
                        await _send_event(session_id, websocket, "error", {"message": "Empty message"}, msg_id)

                elif msg_type == "get_session":
                    # Refresh session state
                    session = session_manager.get_session(session_id)
                    if session:
                        await _send_event(session_id, websocket, "session", _session_to_dict(session), msg_id)

                else:
                    await _send_event(session_id, websocket, "error", {"message": f"Unknown message type: {msg_type}"}, msg_id)

            except asyncio.TimeoutError:
                # Send ping to keep connection alive
                try:
                    await _send_event(session_id, websocket, "ping", {})
                except:
                    break

    except WebSocketDisconnect:
        print(f"[WS] Client disconnected: session={session_id}")

    except Exception as e:
        print(f"[WS] Error: {e}")
        try:
            await _send_event(session_id, websocket, "error", {"message": str(e)})
        except:
            pass

    finally:
        await manager.disconnect(session_id, websocket)
