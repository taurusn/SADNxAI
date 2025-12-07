"""
SADNxAI - Shared Data Models
Pydantic models for all services
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field


# ============================================================
# Enums
# ============================================================

class SessionStatus(str, Enum):
    IDLE = "idle"
    ANALYZING = "analyzing"
    PROPOSED = "proposed"
    DISCUSSING = "discussing"
    APPROVED = "approved"
    MASKING = "masking"
    VALIDATING = "validating"
    COMPLETED = "completed"
    FAILED = "failed"


class MaskingTechnique(str, Enum):
    SUPPRESS = "SUPPRESS"
    GENERALIZE = "GENERALIZE"
    PSEUDONYMIZE = "PSEUDONYMIZE"
    DATE_SHIFT = "DATE_SHIFT"
    KEEP = "KEEP"


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


# ============================================================
# Generalization Config
# ============================================================

class GeneralizationConfig(BaseModel):
    """Configuration for generalization levels (0-3)"""
    age_level: int = Field(default=1, ge=0, le=3, description="0=exact, 1=5yr, 2=10yr, 3=category")
    location_level: int = Field(default=1, ge=0, le=3, description="0=city, 1=province, 2=region, 3=country")
    date_level: int = Field(default=1, ge=0, le=3, description="0=day, 1=week, 2=month, 3=quarter")


# ============================================================
# Classification
# ============================================================

class Classification(BaseModel):
    """Column classification result from AI analysis"""
    direct_identifiers: list[str] = Field(default_factory=list, description="Columns to suppress")
    quasi_identifiers: list[str] = Field(default_factory=list, description="Columns to generalize")
    linkage_identifiers: list[str] = Field(default_factory=list, description="Columns to pseudonymize")
    date_columns: list[str] = Field(default_factory=list, description="Date columns to shift")
    sensitive_attributes: list[str] = Field(default_factory=list, description="Sensitive columns to keep")
    recommended_techniques: dict[str, MaskingTechnique] = Field(default_factory=dict)
    reasoning: dict[str, str] = Field(default_factory=dict, description="AI reasoning per column")
    generalization_config: GeneralizationConfig = Field(default_factory=GeneralizationConfig)


# ============================================================
# Privacy Thresholds
# ============================================================

class ThresholdRange(BaseModel):
    """Min and target values for a threshold"""
    minimum: float
    target: float


class PrivacyThresholds(BaseModel):
    """Configurable privacy thresholds"""
    k_anonymity: ThresholdRange = Field(default_factory=lambda: ThresholdRange(minimum=5, target=10))
    l_diversity: ThresholdRange = Field(default_factory=lambda: ThresholdRange(minimum=2, target=3))
    t_closeness: ThresholdRange = Field(default_factory=lambda: ThresholdRange(minimum=0.2, target=0.15))
    risk_score: ThresholdRange = Field(default_factory=lambda: ThresholdRange(minimum=20, target=10))


# ============================================================
# Validation Result
# ============================================================

class MetricResult(BaseModel):
    """Result for a single privacy metric"""
    value: float
    threshold: float
    passed: bool


class RemediationSuggestion(BaseModel):
    """Suggestion for fixing a failed metric"""
    metric: str
    suggestion: str
    action: Optional[dict[str, Any]] = None


class ValidationResult(BaseModel):
    """Complete validation result"""
    passed: bool
    metrics: dict[str, MetricResult]
    failed_metrics: list[str] = Field(default_factory=list)
    remediation_suggestions: list[RemediationSuggestion] = Field(default_factory=list)


# ============================================================
# Message (OpenAI-Compatible)
# ============================================================

class ToolCall(BaseModel):
    """Tool call in assistant message"""
    id: str
    type: str = "function"
    function: dict[str, str]  # {"name": "...", "arguments": "..."}


class Message(BaseModel):
    """OpenAI-compatible message format"""
    role: MessageRole
    content: Optional[str] = None
    tool_calls: Optional[list[ToolCall]] = None
    tool_call_id: Optional[str] = None


# ============================================================
# Session
# ============================================================

class Session(BaseModel):
    """Complete session state"""
    id: str
    title: str = "New Chat"
    status: SessionStatus = SessionStatus.IDLE
    file_path: Optional[str] = None
    columns: list[str] = Field(default_factory=list)
    sample_data: list[dict[str, Any]] = Field(default_factory=list)
    row_count: int = 0
    classification: Optional[Classification] = None
    thresholds: PrivacyThresholds = Field(default_factory=PrivacyThresholds)
    validation_result: Optional[ValidationResult] = None
    messages: list[Message] = Field(default_factory=list)
    output_path: Optional[str] = None
    report_path: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


# ============================================================
# API Request/Response Models
# ============================================================

# Masking Service
class MaskingRequest(BaseModel):
    """Request to masking service"""
    job_id: str
    input_path: str
    classification: Classification
    salt: str = Field(description="Salt for pseudonymization HMAC")


class MaskingResponse(BaseModel):
    """Response from masking service"""
    output_path: str
    techniques_applied: dict[str, str]
    rows_processed: int
    columns_masked: int


# Validation Service
class ValidationRequest(BaseModel):
    """Request to validation service"""
    job_id: str
    input_path: str
    quasi_identifiers: list[str]
    sensitive_attributes: list[str]
    thresholds: PrivacyThresholds


class ValidationResponse(BaseModel):
    """Response from validation service"""
    passed: bool
    metrics: dict[str, MetricResult]
    failed_metrics: list[str]
    remediation_suggestions: list[RemediationSuggestion]


class ReportRequest(BaseModel):
    """Request to generate PDF report"""
    job_id: str
    session: Session
    validation_result: ValidationResult


class ReportResponse(BaseModel):
    """Response from report generation"""
    report_path: str


# Chat Service
class ChatRequest(BaseModel):
    """Chat message request"""
    message: str


class ChatResponse(BaseModel):
    """Chat message response"""
    response: str
    status: SessionStatus
    classification: Optional[Classification] = None


class UploadResponse(BaseModel):
    """File upload response"""
    columns: list[str]
    sample_data: list[dict[str, Any]]
    row_count: int
    ai_response: str
