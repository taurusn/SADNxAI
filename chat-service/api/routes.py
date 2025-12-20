"""
Chat Service API Routes
Main API for frontend communication
"""

import os
import json
import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, List, Any, Optional

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.models import (
    Session, SessionStatus, Message, MessageRole,
    ToolCall,
    ChatRequest, ChatResponse, UploadResponse
)

from core.session import SessionManager
from core.conversation import ConversationManager
from llm.adapter import LLMAdapter
from llm.tools import ToolExecutor
from pipeline.executor import PipelineExecutor


router = APIRouter(prefix="/api")

# Initialize components
session_manager = SessionManager()
llm_adapter = LLMAdapter(mock_mode=os.getenv("LLM_MOCK_MODE", "false").lower() == "true")
pipeline_executor = PipelineExecutor()

# Maximum iterations for agentic loop (safety limit)
MAX_AGENTIC_ITERATIONS = 10


async def _run_agentic_loop(
    session: Session,
    messages: List[Dict[str, Any]],
    session_context: Dict[str, Any],
    tool_executor: "ToolExecutor",
    terminal_tools: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Run the agentic loop: call LLM, execute tools, repeat until no more tool calls.

    This implements the standard agentic pattern:
    1. Call LLM with current messages
    2. If LLM returns tool_calls, execute them and add results to messages
    3. Call LLM again with updated messages (including tool results)
    4. Repeat until LLM returns no tool_calls OR a terminal tool is called
    5. Return final response

    Args:
        session: Current session object
        messages: List of messages for LLM (will be modified in place)
        session_context: Context dict for LLM
        tool_executor: ToolExecutor instance
        terminal_tools: Optional list of tool names that should stop the loop
                       (e.g., ["execute_pipeline"] - handled separately)

    Returns:
        Dict with:
        - content: Final response text from LLM
        - classification_updated: Classification if classify_columns was called
        - iterations: Number of loop iterations
        - terminal_tool: Name of terminal tool that was called (if any)
        - terminal_tool_result: Result from terminal tool (if any)
    """
    terminal_tools = terminal_tools or []
    classification_updated = None
    terminal_tool_called = None
    terminal_tool_result = None
    iteration = 0
    final_content = ""

    while iteration < MAX_AGENTIC_ITERATIONS:
        iteration += 1
        print(f"[Agentic Loop] Iteration {iteration}")

        # Call LLM
        llm_response = await llm_adapter.chat_async(messages, session_context)
        content = llm_response.get("content", "")
        tool_calls_raw = llm_response.get("tool_calls")

        # If no tool calls, we're done - this is the final response
        if not tool_calls_raw:
            print(f"[Agentic Loop] No tool calls, returning final response")
            # Add final assistant message to session
            final_msg = Message(role=MessageRole.ASSISTANT, content=content)
            session.messages.append(final_msg)
            final_content = content
            break

        print(f"[Agentic Loop] Processing {len(tool_calls_raw)} tool call(s)")

        # Build ToolCall objects
        tool_calls = []
        for tc in tool_calls_raw:
            tool_calls.append(ToolCall(
                id=tc["id"],
                type=tc["type"],
                function=tc["function"]
            ))

        # Add assistant message WITH tool calls to session FIRST (correct order)
        assistant_msg = Message(
            role=MessageRole.ASSISTANT,
            content=content,
            tool_calls=tool_calls
        )
        session.messages.append(assistant_msg)

        # Also add to messages list for next LLM call
        messages.append({
            "role": "assistant",
            "content": content,
            "tool_calls": tool_calls_raw
        })

        # Check if any terminal tool is being called
        should_break = False

        # Execute each tool and add results
        for tc in tool_calls_raw:
            tool_name = tc["function"]["name"]
            args = json.loads(tc["function"]["arguments"])

            # Check if this is a terminal tool
            if tool_name in terminal_tools:
                print(f"[Agentic Loop] Terminal tool called: {tool_name}")
                terminal_tool_called = tool_name
                terminal_tool_result = {"tool_name": tool_name, "args": args, "tool_call": tc}
                should_break = True
                # Don't execute terminal tools here - caller will handle them
                continue

            print(f"[Agentic Loop] Executing tool: {tool_name}")
            result = tool_executor.execute(tool_name, args)

            # Add tool result to session AFTER assistant message (correct order)
            tool_result_msg = Message(
                role=MessageRole.TOOL,
                content=json.dumps(result),
                tool_call_id=tc["id"]
            )
            session.messages.append(tool_result_msg)

            # Also add to messages list for next LLM call
            messages.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tc["id"]
            })

            # Track classification updates
            if tool_name == "classify_columns" and result.get("success"):
                classification_updated = session.classification
                session.status = SessionStatus.PROPOSED
                # Update context for next iteration
                session_context = _build_session_context(session)
                print(f"[Agentic Loop] Classification updated, status -> PROPOSED")

        # Update final_content in case we hit max iterations or break
        final_content = content

        if should_break:
            print(f"[Agentic Loop] Breaking due to terminal tool")
            break

    if iteration >= MAX_AGENTIC_ITERATIONS:
        print(f"[Agentic Loop] Warning: Hit max iterations ({MAX_AGENTIC_ITERATIONS})")

    return {
        "content": final_content,
        "classification_updated": classification_updated,
        "iterations": iteration,
        "terminal_tool": terminal_tool_called,
        "terminal_tool_result": terminal_tool_result
    }


def _build_session_context(session: Session) -> Dict[str, Any]:
    """Build session context for LLM with file info and classification."""
    context = {}

    # Add file information if available
    if session.file_path:
        context["file_info"] = {
            "filename": session.title,
            "columns": session.columns,
            "row_count": session.row_count,
            "sample_data": session.sample_data
        }

    # Add classification if available
    if session.classification:
        context["classification"] = {
            "direct_identifiers": session.classification.direct_identifiers,
            "quasi_identifiers": session.classification.quasi_identifiers,
            "linkage_identifiers": session.classification.linkage_identifiers,
            "date_columns": session.classification.date_columns,
            "sensitive_attributes": session.classification.sensitive_attributes,
            "recommended_techniques": session.classification.recommended_techniques
        }

    # Add current status
    context["status"] = session.status.value

    return context

# Storage paths
STORAGE_PATH = os.getenv("STORAGE_PATH", "/storage")
INPUT_PATH = os.path.join(STORAGE_PATH, "input")


class SessionResponse(BaseModel):
    """Session response model"""
    id: str
    title: str
    status: str
    created_at: str
    updated_at: str
    row_count: int = 0
    has_classification: bool = False
    has_validation: bool = False


class SessionListResponse(BaseModel):
    """Session list response"""
    sessions: List[SessionResponse]


class ThresholdsRequest(BaseModel):
    """Thresholds update request"""
    k_anonymity_minimum: Optional[int] = None
    k_anonymity_target: Optional[int] = None
    l_diversity_minimum: Optional[int] = None
    l_diversity_target: Optional[int] = None
    t_closeness_minimum: Optional[float] = None
    t_closeness_target: Optional[float] = None
    risk_score_minimum: Optional[float] = None
    risk_score_target: Optional[float] = None


def session_to_response(session: Session) -> SessionResponse:
    """Convert Session to SessionResponse"""
    return SessionResponse(
        id=session.id,
        title=session.title,
        status=session.status.value,
        created_at=session.created_at.isoformat(),
        updated_at=session.updated_at.isoformat(),
        row_count=session.row_count,
        has_classification=session.classification is not None,
        has_validation=session.validation_result is not None
    )


# ============================================================
# Session Endpoints
# ============================================================

@router.post("/sessions")
async def create_session():
    """Create a new chat session"""
    session = session_manager.create_session()
    return {"session_id": session.id}


@router.get("/sessions", response_model=SessionListResponse)
async def list_sessions(limit: int = 50, offset: int = 0):
    """List all sessions"""
    sessions = session_manager.list_sessions(limit=limit, offset=offset)
    return SessionListResponse(
        sessions=[session_to_response(s) for s in sessions]
    )


@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session details"""
    session = session_manager.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return session.model_dump()


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    # Get session first to clean up files
    session = session_manager.get_session(session_id)
    if session:
        # Clean up associated files
        if session.file_path and os.path.exists(session.file_path):
            os.remove(session.file_path)
        if session.output_path and os.path.exists(session.output_path):
            os.remove(session.output_path)
        if session.report_path and os.path.exists(session.report_path):
            os.remove(session.report_path)

    deleted = session_manager.delete_session(session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found")

    return {"deleted": True}


# ============================================================
# File Upload
# ============================================================

@router.post("/sessions/{session_id}/upload", response_model=UploadResponse)
async def upload_file(session_id: str, file: UploadFile = File(...)):
    """Upload a CSV file for analysis"""
    session = session_manager.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    # Check file size (100MB limit)
    contents = await file.read()
    if len(contents) > 100 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 100MB)")

    # Ensure input directory exists
    os.makedirs(INPUT_PATH, exist_ok=True)

    # Save file
    file_path = os.path.join(INPUT_PATH, f"{session_id}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(contents)

    # Read and analyze CSV
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail=f"Failed to read CSV: {str(e)}")

    # Extract columns and sample data
    columns = df.columns.tolist()
    sample_data = df.head(10).to_dict(orient='records')
    row_count = len(df)

    # Update session
    session.file_path = file_path
    session.title = file.filename
    session.columns = columns
    session.sample_data = sample_data
    session.row_count = row_count
    session.status = SessionStatus.ANALYZING
    session_manager.update_session(session)

    # Get AI analysis using agentic loop
    conversation = ConversationManager(session)
    messages = conversation.get_messages_for_llm()

    # Add user message about upload
    user_msg = Message(role=MessageRole.USER, content=f"I've uploaded a file: {file.filename}")
    session.messages.append(user_msg)
    messages.append({"role": "user", "content": user_msg.content})

    # Build session context for LLM
    session_context = _build_session_context(session)

    # Create tool executor
    tool_executor = ToolExecutor(session)

    # Run agentic loop - LLM will call tools and we'll loop until it's done
    result = await _run_agentic_loop(session, messages, session_context, tool_executor)

    ai_response_text = result["content"]

    session_manager.update_session(session)

    return UploadResponse(
        columns=columns,
        sample_data=sample_data,
        row_count=row_count,
        ai_response=ai_response_text or "I'm analyzing your dataset..."
    )


# ============================================================
# Chat
# ============================================================

@router.post("/sessions/{session_id}/chat", response_model=ChatResponse)
async def chat(session_id: str, request: ChatRequest):
    """Send a chat message"""
    session = session_manager.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    # Add user message
    user_msg = Message(role=MessageRole.USER, content=request.message)
    session.messages.append(user_msg)

    # Check for approval
    conversation = ConversationManager(session)
    if conversation.detect_approval(request.message):
        if session.classification is not None:
            session.status = SessionStatus.APPROVED

    # Get messages for LLM
    messages = conversation.get_messages_for_llm()

    # Build session context for LLM
    session_context = _build_session_context(session)

    # Create tool executor
    tool_executor = ToolExecutor(session)

    # Run agentic loop with execute_pipeline as terminal tool
    # (execute_pipeline needs special async handling)
    result = await _run_agentic_loop(
        session, messages, session_context, tool_executor,
        terminal_tools=["execute_pipeline"]
    )

    ai_response_text = result["content"]
    classification_updated = result.get("classification_updated")

    # Handle execute_pipeline if it was called
    if result.get("terminal_tool") == "execute_pipeline":
        terminal_info = result["terminal_tool_result"]
        tc = terminal_info["tool_call"]

        # First execute the tool to validate
        args = terminal_info["args"]
        tool_result = tool_executor.execute("execute_pipeline", args)

        # Add tool result message
        tool_result_msg = Message(
            role=MessageRole.TOOL,
            content=json.dumps(tool_result),
            tool_call_id=tc["id"]
        )
        session.messages.append(tool_result_msg)

        if tool_result.get("success"):
            session.status = SessionStatus.MASKING

            # Clean up old output/report files before retry
            if session.output_path and os.path.exists(session.output_path):
                os.remove(session.output_path)
                session.output_path = None
            if session.report_path and os.path.exists(session.report_path):
                os.remove(session.report_path)
                session.report_path = None
            session.validation_result = None

            session_manager.update_session(session)

            # Execute pipeline asynchronously
            pipeline_result = await pipeline_executor.execute(session)

            if pipeline_result.get("error"):
                session.status = SessionStatus.FAILED
                ai_response_text = f"Pipeline execution failed: {pipeline_result['error']}"
            else:
                if pipeline_result.get("validation_result"):
                    session.validation_result = pipeline_result["validation_result"]
                    session.output_path = pipeline_result.get("output_path")
                    session.report_path = pipeline_result.get("report_path")

                    if pipeline_result["validation_result"].passed:
                        session.status = SessionStatus.COMPLETED
                        ai_response_text = "Anonymization complete! Validation passed. You can now download the anonymized CSV and privacy report."
                    else:
                        session.status = SessionStatus.FAILED
                        failed = pipeline_result["validation_result"].failed_metrics
                        ai_response_text = f"Validation failed for metrics: {', '.join(failed)}. You can still download the anonymized CSV and report. Would you like to adjust the generalization levels or thresholds and try again?"

    # Update status for discussion if no tools were called
    if result["iterations"] == 1 and not result.get("terminal_tool"):
        # If LLM just responded without tools
        if session.status == SessionStatus.PROPOSED:
            session.status = SessionStatus.DISCUSSING

    session_manager.update_session(session)

    return ChatResponse(
        response=ai_response_text or "I'm processing your request...",
        status=session.status,
        classification=classification_updated
    )


def _execute_pipeline(session: Session) -> Dict[str, Any]:
    """Sync wrapper for pipeline execution (used in tool callback)"""
    import asyncio
    try:
        # Try to get existing event loop (when called from async context)
        loop = asyncio.get_running_loop()
        # Create a task and return a placeholder - actual execution happens async
        asyncio.ensure_future(pipeline_executor.execute(session))
        # For sync context, we need to wait - but in async context just schedule it
        return {"status": "pipeline_scheduled", "message": "Pipeline execution started in background"}
    except RuntimeError:
        # No running loop - create one (shouldn't happen in FastAPI but handle it)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(pipeline_executor.execute(session))
        finally:
            loop.close()


# ============================================================
# Thresholds
# ============================================================

@router.patch("/sessions/{session_id}/thresholds")
async def update_thresholds(session_id: str, request: ThresholdsRequest):
    """Update privacy thresholds"""
    session = session_manager.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    thresholds = session.thresholds

    if request.k_anonymity_minimum is not None:
        thresholds.k_anonymity.minimum = request.k_anonymity_minimum
    if request.k_anonymity_target is not None:
        thresholds.k_anonymity.target = request.k_anonymity_target
    if request.l_diversity_minimum is not None:
        thresholds.l_diversity.minimum = request.l_diversity_minimum
    if request.l_diversity_target is not None:
        thresholds.l_diversity.target = request.l_diversity_target
    if request.t_closeness_minimum is not None:
        thresholds.t_closeness.minimum = request.t_closeness_minimum
    if request.t_closeness_target is not None:
        thresholds.t_closeness.target = request.t_closeness_target
    if request.risk_score_minimum is not None:
        thresholds.risk_score.minimum = request.risk_score_minimum
    if request.risk_score_target is not None:
        thresholds.risk_score.target = request.risk_score_target

    session.thresholds = thresholds
    session_manager.update_session(session)

    return {"thresholds": thresholds.model_dump()}


# ============================================================
# Downloads
# ============================================================

@router.get("/sessions/{session_id}/download/data")
async def download_data(session_id: str):
    """Download anonymized CSV"""
    session = session_manager.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.output_path is None or not os.path.exists(session.output_path):
        raise HTTPException(status_code=404, detail="Anonymized data not available")

    filename = os.path.basename(session.output_path)
    return FileResponse(
        session.output_path,
        media_type="text/csv",
        filename=filename
    )


@router.get("/sessions/{session_id}/download/report")
async def download_report(session_id: str):
    """Download PDF report"""
    session = session_manager.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.report_path is None or not os.path.exists(session.report_path):
        raise HTTPException(status_code=404, detail="Report not available")

    filename = os.path.basename(session.report_path)
    return FileResponse(
        session.report_path,
        media_type="application/pdf",
        filename=filename
    )


# ============================================================
# Health Check
# ============================================================

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "chat-service"}
