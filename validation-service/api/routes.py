"""
Validation Service API Routes
"""

import os
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.models import PrivacyThresholds, MetricResult, RemediationSuggestion

from metrics.k_anonymity import calculate_k_anonymity
from metrics.l_diversity import calculate_l_diversity
from metrics.t_closeness import calculate_t_closeness
from report.generator import generate_pdf_report


router = APIRouter()

# Storage paths
STORAGE_PATH = os.getenv("STORAGE_PATH", "/storage")
REPORTS_PATH = os.path.join(STORAGE_PATH, "reports")


class ValidationRequest(BaseModel):
    """Request model for validation endpoint"""
    job_id: str
    input_path: str
    quasi_identifiers: List[str]
    sensitive_attributes: List[str]
    thresholds: PrivacyThresholds


class ValidationResponse(BaseModel):
    """Response model for validation endpoint"""
    passed: bool
    metrics: Dict[str, MetricResult]
    failed_metrics: List[str]
    remediation_suggestions: List[RemediationSuggestion]


class ReportRequest(BaseModel):
    """Request model for report generation"""
    job_id: str
    session: Dict[str, Any]
    validation_result: Dict[str, Any]


class ReportResponse(BaseModel):
    """Response model for report generation"""
    report_path: str


def calculate_risk_score(
    k_value: float,
    l_value: float,
    t_value: float,
    thresholds: PrivacyThresholds
) -> float:
    """
    Calculate composite risk score (0-100).

    Formula: 0.5 * k_risk + 0.3 * l_risk + 0.2 * t_risk

    Where each component risk is based on distance from threshold.
    """
    # k-anonymity risk (lower k = higher risk)
    k_target = thresholds.k_anonymity.target
    if k_value >= k_target:
        k_risk = 0
    elif k_value <= 1:
        k_risk = 100
    else:
        k_risk = max(0, min(100, (1 - (k_value / k_target)) * 100))

    # l-diversity risk (lower l = higher risk)
    l_target = thresholds.l_diversity.target
    if l_value >= l_target:
        l_risk = 0
    elif l_value <= 1:
        l_risk = 100
    else:
        l_risk = max(0, min(100, (1 - (l_value / l_target)) * 100))

    # t-closeness risk (higher t = higher risk)
    t_target = thresholds.t_closeness.target
    if t_value <= t_target:
        t_risk = 0
    elif t_value >= 1:
        t_risk = 100
    else:
        t_risk = max(0, min(100, (t_value / t_target - 1) * 50))

    # Weighted composite
    risk_score = 0.5 * k_risk + 0.3 * l_risk + 0.2 * t_risk

    return round(risk_score, 2)


@router.post("/validate", response_model=ValidationResponse)
async def validate_data(request: ValidationRequest) -> ValidationResponse:
    """
    Validate anonymized data against privacy thresholds.

    Calculates k-anonymity, l-diversity, t-closeness, and composite risk score.

    Args:
        request: ValidationRequest with file path, QIs, SAs, and thresholds

    Returns:
        ValidationResponse with metrics and pass/fail status
    """
    # Validate input file exists
    if not os.path.exists(request.input_path):
        raise HTTPException(status_code=404, detail=f"Input file not found: {request.input_path}")

    # Read CSV
    try:
        df = pd.read_csv(request.input_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read CSV: {str(e)}")

    thresholds = request.thresholds

    # Calculate k-anonymity
    k_result = calculate_k_anonymity(df, request.quasi_identifiers)
    k_value = k_result['k_value']
    k_threshold = thresholds.k_anonymity.minimum
    k_passed = k_value >= k_threshold

    # Calculate l-diversity
    l_result = calculate_l_diversity(df, request.quasi_identifiers, request.sensitive_attributes)
    l_value = l_result['l_value']
    l_threshold = thresholds.l_diversity.minimum
    l_passed = l_value >= l_threshold if l_value != float('inf') else True

    # Calculate t-closeness
    t_result = calculate_t_closeness(df, request.quasi_identifiers, request.sensitive_attributes)
    t_value = t_result['t_value']
    t_threshold = thresholds.t_closeness.minimum
    t_passed = t_value <= t_threshold

    # Calculate risk score
    risk_value = calculate_risk_score(k_value, l_value if l_value != float('inf') else 100, t_value, thresholds)
    risk_threshold = thresholds.risk_score.minimum
    risk_passed = risk_value < risk_threshold

    # Build metrics
    metrics = {
        "k_anonymity": MetricResult(value=k_value, threshold=k_threshold, passed=k_passed),
        "l_diversity": MetricResult(value=l_value if l_value != float('inf') else 999, threshold=l_threshold, passed=l_passed),
        "t_closeness": MetricResult(value=t_value, threshold=t_threshold, passed=t_passed),
        "risk_score": MetricResult(value=risk_value, threshold=risk_threshold, passed=risk_passed),
    }

    # Determine failed metrics
    failed_metrics = []
    if not k_passed:
        failed_metrics.append("k_anonymity")
    if not l_passed:
        failed_metrics.append("l_diversity")
    if not t_passed:
        failed_metrics.append("t_closeness")
    if not risk_passed:
        failed_metrics.append("risk_score")

    # Generate remediation suggestions
    remediation_suggestions = []

    if not k_passed:
        suggestion = RemediationSuggestion(
            metric="k_anonymity",
            suggestion=f"Current k={k_value}, need k≥{k_threshold}. Try increasing generalization level for quasi-identifiers (e.g., use 10-year age ranges instead of 5-year).",
            action={"increase_generalization": True}
        )
        remediation_suggestions.append(suggestion)

    if not l_passed:
        suggestion = RemediationSuggestion(
            metric="l_diversity",
            suggestion=f"Current l={l_value}, need l≥{l_threshold}. Consider suppressing more records or reducing the number of quasi-identifiers.",
            action={"reduce_quasi_identifiers": True}
        )
        remediation_suggestions.append(suggestion)

    if not t_passed:
        suggestion = RemediationSuggestion(
            metric="t_closeness",
            suggestion=f"Current t={t_value}, need t≤{t_threshold}. Try increasing generalization or suppressing outlier equivalence classes.",
            action={"increase_generalization": True}
        )
        remediation_suggestions.append(suggestion)

    # Overall pass/fail
    passed = len(failed_metrics) == 0

    return ValidationResponse(
        passed=passed,
        metrics=metrics,
        failed_metrics=failed_metrics,
        remediation_suggestions=remediation_suggestions
    )


@router.post("/report", response_model=ReportResponse)
async def generate_report(request: ReportRequest) -> ReportResponse:
    """
    Generate a PDF privacy report.

    Args:
        request: ReportRequest with session and validation data

    Returns:
        ReportResponse with path to generated PDF
    """
    # Ensure reports directory exists
    os.makedirs(REPORTS_PATH, exist_ok=True)

    try:
        report_path = generate_pdf_report(
            output_path=REPORTS_PATH,
            session=request.session,
            validation_result=request.validation_result,
            job_id=request.job_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

    return ReportResponse(report_path=report_path)


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "validation-service"}
