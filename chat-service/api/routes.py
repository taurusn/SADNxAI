"""
Chat Service API Routes
Main API for frontend communication
"""

import os
import json
import shutil
import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, List, Any, Optional

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.models import (
    Session, SessionStatus, Message, MessageRole,
    Classification, PrivacyThresholds, ToolCall,
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

    # Get AI analysis
    conversation = ConversationManager(session)
    messages = conversation.get_messages_for_llm()

    # Add user message about upload
    user_msg = Message(role=MessageRole.USER, content=f"I've uploaded a file: {file.filename}")
    session.messages.append(user_msg)
    messages.append({"role": "user", "content": user_msg.content})

    # Build session context for LLM
    session_context = _build_session_context(session)

    # Get LLM response with context
    llm_response = await llm_adapter.chat_async(messages, session_context)

    # Process response
    ai_response_text = llm_response.get("content", "")

    # Handle tool calls if any
    if llm_response.get("tool_calls"):
        tool_executor = ToolExecutor(session)

        tool_calls = []
        for tc in llm_response["tool_calls"]:
            tool_calls.append(ToolCall(
                id=tc["id"],
                type=tc["type"],
                function=tc["function"]
            ))

            # Execute tool
            args = json.loads(tc["function"]["arguments"])
            result = tool_executor.execute(tc["function"]["name"], args)

            # Add tool result to messages
            tool_result_msg = Message(
                role=MessageRole.TOOL,
                content=json.dumps(result),
                tool_call_id=tc["id"]
            )
            session.messages.append(tool_result_msg)

        # Add assistant message with tool calls
        assistant_msg = Message(
            role=MessageRole.ASSISTANT,
            content=ai_response_text,
            tool_calls=tool_calls if tool_calls else None
        )
        session.messages.append(assistant_msg)

        # Update status based on classification
        if session.classification:
            session.status = SessionStatus.PROPOSED

    else:
        # Add plain assistant message
        assistant_msg = Message(role=MessageRole.ASSISTANT, content=ai_response_text)
        session.messages.append(assistant_msg)

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

    # Get LLM response with context
    llm_response = await llm_adapter.chat_async(messages, session_context)

    ai_response_text = llm_response.get("content", "")
    classification_updated = None

    # Handle tool calls
    if llm_response.get("tool_calls"):
        tool_executor = ToolExecutor(session, pipeline_callback=_execute_pipeline)

        tool_calls = []
        for tc in llm_response["tool_calls"]:
            tool_calls.append(ToolCall(
                id=tc["id"],
                type=tc["type"],
                function=tc["function"]
            ))

            # Execute tool
            tool_name = tc["function"]["name"]
            args = json.loads(tc["function"]["arguments"])
            result = tool_executor.execute(tool_name, args)

            # Add tool result message
            tool_result_msg = Message(
                role=MessageRole.TOOL,
                content=json.dumps(result),
                tool_call_id=tc["id"]
            )
            session.messages.append(tool_result_msg)

            # Handle pipeline execution
            if tool_name == "execute_pipeline" and result.get("success"):
                session.status = SessionStatus.MASKING
                session_manager.update_session(session)

                # Execute pipeline asynchronously
                pipeline_result = await pipeline_executor.execute(session)

                if pipeline_result.get("error"):
                    session.status = SessionStatus.FAILED
                    ai_response_text = f"Pipeline execution failed: {pipeline_result['error']}"
                else:
                    if pipeline_result.get("validation_result"):
                        session.validation_result = pipeline_result["validation_result"]
                        if pipeline_result["validation_result"].passed:
                            session.status = SessionStatus.COMPLETED
                            session.output_path = pipeline_result.get("output_path")
                            session.report_path = pipeline_result.get("report_path")
                            ai_response_text = "Anonymization complete! Validation passed. You can now download the anonymized CSV and privacy report."
                        else:
                            session.status = SessionStatus.FAILED
                            failed = pipeline_result["validation_result"].failed_metrics
                            ai_response_text = f"Validation failed for metrics: {', '.join(failed)}. Would you like to adjust the generalization levels or thresholds and try again?"

            # Track classification updates
            if tool_name == "classify_columns" and result.get("success"):
                classification_updated = session.classification
                session.status = SessionStatus.PROPOSED

        # Add assistant message with tool calls
        assistant_msg = Message(
            role=MessageRole.ASSISTANT,
            content=ai_response_text,
            tool_calls=tool_calls
        )
        session.messages.append(assistant_msg)

    else:
        # Plain assistant message
        assistant_msg = Message(role=MessageRole.ASSISTANT, content=ai_response_text)
        session.messages.append(assistant_msg)

        # Update status based on conversation
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
        future = asyncio.ensure_future(pipeline_executor.execute(session))
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
