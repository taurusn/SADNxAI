#!/usr/bin/env python3
"""
SADNxAI LLM Evaluation Framework

A comprehensive evaluation suite for assessing LLM performance in the
SADNxAI data anonymization platform.

Evaluates:
    1. Column classification accuracy (40% weight)
    2. Tool calling correctness (25% weight)
    3. Saudi data pattern detection (15% weight)
    4. Reasoning quality (10% weight)
    5. Regulatory compliance (10% weight)

Usage:
    # Run all evaluations (requires services running)
    python evals/run_evals.py

    # Run with specific provider
    python evals/run_evals.py --provider vllm

    # Run specific category only
    python evals/run_evals.py --category classification

    # Run in direct LLM mode (TODO: not yet implemented)
    # python evals/run_evals.py --direct --provider vllm

    # Run with parallel execution
    python evals/run_evals.py --parallel

    # Verbose output with debug logging
    python evals/run_evals.py -v --log-level DEBUG

Example Output:
    ============================================================
    SADNxAI LLM EVALUATION REPORT
    ============================================================
    Timestamp: 2025-01-25T10:30:00
    Provider:  vllm
    Model:     meta-llama/Llama-3.1-8B-Instruct
    Grade:     B (85.5%)

    Category Scores:
    ----------------------------------------
      classification         87.5% (weight: 40%)
      tool_calling           90.0% (weight: 25%)
      saudi_patterns         80.0% (weight: 15%)
      reasoning              75.0% (weight: 10%)
      regulatory             85.0% (weight: 10%)

    RESULT: PASS - LLM meets production standards
    ============================================================

Author: SADNxAI Team
Version: 1.0.0
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, TypedDict

import httpx

# =============================================================================
# Constants
# =============================================================================

# Evaluation weights by category
CATEGORY_WEIGHTS: dict[str, float] = {
    "classification": 0.40,
    "tool_calling": 0.25,
    "saudi_patterns": 0.15,
    "reasoning": 0.10,
    "regulatory": 0.10,
}

# Grade thresholds (percentage, grade)
GRADE_THRESHOLDS: list[tuple[int, str]] = [
    (90, "A"),
    (80, "B"),
    (70, "C"),
    (60, "D"),
    (0, "F"),
]

# Retry configuration
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 2.0  # seconds
RETRY_BACKOFF_MAX = 16.0  # seconds

# Timeout configuration
DEFAULT_TIMEOUT = 120.0  # seconds for LLM calls
HEALTH_CHECK_TIMEOUT = 10.0  # seconds for health checks

# Validation thresholds
MIN_REASONING_LENGTH = 50  # minimum characters for valid reasoning
MIN_REASONING_KEYWORDS = 2  # minimum privacy keywords required

# Classification categories
CLASSIFICATION_CATEGORIES = [
    "direct_identifiers",
    "quasi_identifiers",
    "linkage_identifiers",
    "date_columns",
    "sensitive_attributes",
]

# =============================================================================
# Logging Setup
# =============================================================================

logger = logging.getLogger("sadnxai.evals")


def setup_logging(level: str = "INFO") -> None:
    """Configure logging with structured format."""
    log_level = getattr(logging, level.upper(), logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))

    root_logger = logging.getLogger("sadnxai")
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)


# =============================================================================
# Type Definitions
# =============================================================================

class ClassificationDict(TypedDict, total=False):
    """Type for classification data structure."""
    direct_identifiers: list[str]
    quasi_identifiers: list[str]
    linkage_identifiers: list[str]
    date_columns: list[str]
    sensitive_attributes: list[str]
    recommended_techniques: dict[str, str]
    reasoning: str


class CriticalChecks(TypedDict, total=False):
    """Type for critical check configuration."""
    must_be_direct: list[str]
    must_be_sensitive: list[str]
    must_not_be_suppressed: list[str]


class ExpectedClassification(TypedDict):
    """Type for expected classification configuration."""
    direct_identifiers: list[str]
    quasi_identifiers: list[str]
    linkage_identifiers: list[str]
    date_columns: list[str]
    sensitive_attributes: list[str]
    recommended_techniques: dict[str, str]
    critical_checks: CriticalChecks


class CategoryScore(TypedDict):
    """Type for category score data."""
    score: float
    max_score: float
    percentage: float
    weight: float


# =============================================================================
# Data Classes
# =============================================================================

class EvalStatus(Enum):
    """Evaluation result status."""
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    SKIPPED = "skipped"


@dataclass
class EvalResult:
    """
    Result of a single evaluation test case.

    Attributes:
        test_id: Unique identifier for the test (e.g., "CLASS-fraud-direct")
        category: Evaluation category (classification, tool_calling, etc.)
        description: Human-readable description of what was tested
        passed: Whether the test passed
        score: Points earned (0 to max_score)
        max_score: Maximum possible points
        details: Additional context about the result
        error: Error message if test failed due to exception
        duration_ms: Time taken to run the test in milliseconds
    """
    test_id: str
    category: str
    description: str
    passed: bool
    score: float
    max_score: float
    details: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    duration_ms: float = 0.0

    @property
    def status(self) -> EvalStatus:
        """Get the status of this result."""
        if self.error:
            # Distinguish between "skipped" (couldn't run) and "error" (ran but crashed)
            if "not found" in self.error.lower() or "skipped" in self.error.lower():
                return EvalStatus.SKIPPED
            return EvalStatus.ERROR
        return EvalStatus.PASSED if self.passed else EvalStatus.FAILED


@dataclass
class EvalReport:
    """
    Complete evaluation report aggregating all test results.

    Attributes:
        timestamp: ISO format timestamp of when evaluation was run
        provider: LLM provider used (vllm, claude, ollama)
        model: Specific model name/version
        total_score: Sum of all scores
        max_score: Sum of all max_scores
        percentage: Weighted percentage score
        grade: Letter grade (A-F)
        results: List of all individual test results
        category_scores: Breakdown by category
        critical_failures: List of failed critical test IDs
        duration_ms: Total evaluation time in milliseconds
        sessions_created: Number of sessions created during evaluation
        sessions_cleaned: Number of sessions successfully cleaned up
    """
    timestamp: str
    provider: str
    model: str
    total_score: float
    max_score: float
    percentage: float
    grade: str
    results: list[EvalResult]
    category_scores: dict[str, CategoryScore]
    critical_failures: list[str]
    duration_ms: float = 0.0
    sessions_created: int = 0
    sessions_cleaned: int = 0


# =============================================================================
# HTTP Client with Retry Logic
# =============================================================================

class APIClient:
    """
    HTTP client wrapper with retry logic and exponential backoff.

    Handles transient failures gracefully and provides consistent
    error handling across all API calls.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = MAX_RETRIES,
    ):
        """
        Initialize the API client.

        Args:
            base_url: Base URL for the API (e.g., http://localhost:8000)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self._client: httpx.AsyncClient | None = None
        self._sessions_created: list[str] = []
        self._sessions_created_total: int = 0  # Track total even after cleanup
        self._sessions_cleaned: int = 0

    async def __aenter__(self) -> "APIClient":
        """Async context manager entry."""
        self._client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit with session cleanup."""
        self._sessions_cleaned = await self.cleanup_sessions()
        if self._client:
            await self._client.aclose()

    async def _request_with_retry(
        self,
        method: str,
        path: str,
        **kwargs,
    ) -> httpx.Response:
        """
        Make HTTP request with exponential backoff retry.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API path (e.g., /api/sessions)
            **kwargs: Additional arguments passed to httpx

        Returns:
            httpx.Response on success

        Raises:
            httpx.HTTPError: After all retries exhausted
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use async with context.")

        url = f"{self.base_url}{path}"
        last_error: Exception | None = None

        for attempt in range(self.max_retries + 1):
            try:
                response = await self._client.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except (httpx.HTTPError, httpx.TimeoutException) as e:
                last_error = e
                if attempt < self.max_retries:
                    delay = min(
                        RETRY_BACKOFF_BASE ** attempt,
                        RETRY_BACKOFF_MAX,
                    )
                    logger.warning(
                        f"Request failed (attempt {attempt + 1}/{self.max_retries + 1}): {e}. "
                        f"Retrying in {delay:.1f}s..."
                    )
                    await asyncio.sleep(delay)

        raise last_error  # type: ignore

    async def health_check(self) -> bool:
        """
        Check if the API is healthy and ready.

        Returns:
            True if healthy, False otherwise
        """
        try:
            # Try to list sessions as a health check
            async with httpx.AsyncClient(timeout=HEALTH_CHECK_TIMEOUT) as client:
                response = await client.get(f"{self.base_url}/api/sessions")
                return response.status_code == 200
        except Exception as e:
            logger.debug(f"Health check failed: {e}")
            return False

    async def create_session(self) -> str:
        """
        Create a new test session.

        Returns:
            Session ID
        """
        response = await self._request_with_retry("POST", "/api/sessions")
        session_id = response.json()["id"]
        self._sessions_created.append(session_id)
        self._sessions_created_total += 1
        logger.debug(f"Created session: {session_id}")
        return session_id

    async def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.

        Args:
            session_id: ID of session to delete

        Returns:
            True if deleted successfully
        """
        try:
            await self._request_with_retry("DELETE", f"/api/sessions/{session_id}")
            logger.debug(f"Deleted session: {session_id}")
            return True
        except Exception as e:
            logger.warning(f"Failed to delete session {session_id}: {e}")
            return False

    async def cleanup_sessions(self) -> int:
        """
        Clean up all sessions created during this client's lifetime.

        This method is idempotent - calling it multiple times is safe.
        After cleanup, the sessions list is cleared to prevent double-deletion.

        Returns:
            Number of sessions successfully cleaned up (0 if already cleaned)
        """
        if not self._sessions_created:
            # Already cleaned up or no sessions created
            return self._sessions_cleaned

        cleaned = 0
        total = len(self._sessions_created)
        for session_id in self._sessions_created:
            if await self.delete_session(session_id):
                cleaned += 1

        logger.info(f"Cleaned up {cleaned}/{total} sessions")

        # Clear the list to make this idempotent
        self._sessions_created.clear()
        self._sessions_cleaned = cleaned

        return cleaned

    async def upload_file(self, session_id: str, file_path: Path) -> dict[str, Any]:
        """
        Upload a CSV file to a session.

        Args:
            session_id: Target session ID
            file_path: Path to CSV file

        Returns:
            Upload response data
        """
        with open(file_path, "rb") as f:
            files = {"file": (file_path.name, f, "text/csv")}
            response = await self._request_with_retry(
                "POST",
                f"/api/sessions/{session_id}/upload",
                files=files,
            )
        return response.json()

    async def send_chat(self, session_id: str, message: str) -> dict[str, Any]:
        """
        Send a chat message and get response.

        Args:
            session_id: Target session ID
            message: User message to send

        Returns:
            Chat response data
        """
        response = await self._request_with_retry(
            "POST",
            f"/api/sessions/{session_id}/chat",
            json={"message": message},
        )
        return response.json()

    async def get_session(self, session_id: str) -> dict[str, Any]:
        """
        Get session details including classification.

        Args:
            session_id: Session ID to fetch

        Returns:
            Session data
        """
        response = await self._request_with_retry(
            "GET",
            f"/api/sessions/{session_id}",
        )
        return response.json()

    @property
    def sessions_created_count(self) -> int:
        """Number of sessions created (total, even after cleanup)."""
        return self._sessions_created_total

    @property
    def sessions_cleaned_count(self) -> int:
        """Number of sessions successfully cleaned up."""
        return self._sessions_cleaned


# =============================================================================
# Evaluation Engine
# =============================================================================

class LLMEvaluator:
    """
    Comprehensive LLM evaluation engine for SADNxAI.

    Evaluates LLM performance across multiple dimensions:
    - Classification accuracy
    - Tool calling correctness
    - Saudi data pattern recognition
    - Reasoning quality
    - Regulatory compliance

    Example:
        async with LLMEvaluator(provider="vllm") as evaluator:
            report = await evaluator.run()
            print(f"Grade: {report.grade}")
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        provider: str = "vllm",
        model: str = "",
        parallel: bool = False,
        direct_mode: bool = False,
    ):
        """
        Initialize the evaluator.

        Args:
            base_url: Base URL for chat-service API
            provider: LLM provider (vllm, claude, ollama, mock)
            model: Specific model name (auto-detected if empty)
            parallel: Run test files in parallel
            direct_mode: Test LLM directly without chat-service
        """
        self.base_url = base_url
        self.provider = provider
        self.model = model
        self.parallel = parallel
        self.direct_mode = direct_mode
        self.results: list[EvalResult] = []
        self.evals_dir = Path(__file__).parent
        self.data_dir = self.evals_dir / "data"
        self._client: APIClient | None = None
        self._start_time: float = 0

        # Load expected classifications
        with open(self.evals_dir / "expected_classifications.json") as f:
            self.expected: dict[str, ExpectedClassification] = json.load(f)

    async def __aenter__(self) -> "LLMEvaluator":
        """Async context manager entry."""
        self._client = APIClient(self.base_url)
        await self._client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        if self._client:
            await self._client.__aexit__(exc_type, exc_val, exc_tb)

    async def check_services(self) -> bool:
        """
        Verify required services are running.

        Returns:
            True if all services are healthy
        """
        if not self._client:
            raise RuntimeError("Evaluator not initialized. Use async with context.")

        logger.info("Checking service health...")
        healthy = await self._client.health_check()

        if healthy:
            logger.info("Services are healthy")
        else:
            logger.error(
                f"Services not available at {self.base_url}. "
                "Please start services with: docker compose up -d"
            )

        return healthy

    def _compare_classification(
        self,
        actual: ClassificationDict,
        expected: ExpectedClassification,
        file_name: str,
    ) -> list[EvalResult]:
        """
        Compare actual classification with expected.

        Args:
            actual: Classification returned by LLM
            expected: Expected classification from ground truth
            file_name: Name of test file for result IDs

        Returns:
            List of EvalResults for each category
        """
        results = []

        for category in CLASSIFICATION_CATEGORIES:
            expected_cols = set(expected.get(category, []))
            actual_cols = set(actual.get(category, []))

            correct = expected_cols & actual_cols
            missing = expected_cols - actual_cols
            extra = actual_cols - expected_cols

            score = len(correct)
            max_score = len(expected_cols) if expected_cols else 1
            passed = missing == set() and extra == set()

            results.append(EvalResult(
                test_id=f"CLASS-{file_name}-{category}",
                category="classification",
                description=f"{category} classification for {file_name}",
                passed=passed,
                score=float(score),
                max_score=float(max_score),
                details={
                    "correct": sorted(correct),
                    "missing": sorted(missing),
                    "extra": sorted(extra),
                },
            ))

            if missing:
                logger.debug(f"{category} missing: {missing}")
            if extra:
                logger.debug(f"{category} extra: {extra}")

        return results

    def _check_critical(
        self,
        actual: ClassificationDict,
        expected: ExpectedClassification,
        file_name: str,
    ) -> list[EvalResult]:
        """
        Check critical test cases that must pass for production readiness.

        Args:
            actual: Classification returned by LLM
            expected: Expected classification with critical_checks
            file_name: Name of test file for result IDs

        Returns:
            List of critical EvalResults
        """
        results = []
        critical = expected.get("critical_checks", {})

        # Check must_be_direct
        for col in critical.get("must_be_direct", []):
            passed = col in actual.get("direct_identifiers", [])
            results.append(EvalResult(
                test_id=f"CRIT-{file_name}-direct-{col}",
                category="classification",
                description=f"CRITICAL: {col} must be direct_identifier",
                passed=passed,
                score=1.0 if passed else 0.0,
                max_score=1.0,
                details={"column": col, "expected": "direct_identifiers"},
            ))
            if not passed:
                logger.warning(f"CRITICAL FAILURE: {col} not classified as direct_identifier")

        # Check must_be_sensitive
        for col in critical.get("must_be_sensitive", []):
            passed = col in actual.get("sensitive_attributes", [])
            results.append(EvalResult(
                test_id=f"CRIT-{file_name}-sensitive-{col}",
                category="classification",
                description=f"CRITICAL: {col} must be sensitive_attribute",
                passed=passed,
                score=1.0 if passed else 0.0,
                max_score=1.0,
                details={"column": col, "expected": "sensitive_attributes"},
            ))
            if not passed:
                logger.warning(f"CRITICAL FAILURE: {col} not classified as sensitive_attribute")

        # Check must_not_be_suppressed
        for col in critical.get("must_not_be_suppressed", []):
            techniques = actual.get("recommended_techniques", {})
            technique = techniques.get(col)
            # Fail if column is missing (None) OR if technique is SUPPRESS
            # A missing column means LLM didn't classify it, which is a failure
            passed = technique is not None and technique != "SUPPRESS"
            results.append(EvalResult(
                test_id=f"CRIT-{file_name}-nosuppress-{col}",
                category="classification",
                description=f"CRITICAL: {col} must NOT be suppressed",
                passed=passed,
                score=1.0 if passed else 0.0,
                max_score=1.0,
                details={
                    "column": col,
                    "actual_technique": technique,
                    "error": "Column not classified" if technique is None else None,
                },
            ))
            if not passed:
                if technique is None:
                    logger.warning(f"CRITICAL FAILURE: {col} not found in recommended_techniques")
                else:
                    logger.warning(f"CRITICAL FAILURE: {col} incorrectly marked for SUPPRESS")

        return results

    def _check_techniques(
        self,
        actual: ClassificationDict,
        expected: ExpectedClassification,
        file_name: str,
    ) -> list[EvalResult]:
        """
        Check that recommended techniques match expected.

        Args:
            actual: Classification returned by LLM
            expected: Expected classification with techniques
            file_name: Name of test file for result IDs

        Returns:
            List of technique EvalResults
        """
        expected_tech = expected.get("recommended_techniques", {})
        actual_tech = actual.get("recommended_techniques", {})

        correct = 0
        total = len(expected_tech)
        mismatches = {}

        for col, exp_technique in expected_tech.items():
            act_technique = actual_tech.get(col)
            if act_technique == exp_technique:
                correct += 1
            else:
                mismatches[col] = {"expected": exp_technique, "actual": act_technique}
                logger.debug(f"Technique mismatch for {col}: expected {exp_technique}, got {act_technique}")

        return [EvalResult(
            test_id=f"TECH-{file_name}",
            category="classification",
            description=f"Technique recommendations for {file_name}",
            passed=correct == total,
            score=float(correct),
            max_score=float(total) if total else 1.0,
            details={
                "correct": correct,
                "total": total,
                "mismatches": mismatches,
            },
        )]

    async def _eval_single_file(
        self,
        file_name: str,
        expected: ExpectedClassification,
    ) -> list[EvalResult]:
        """
        Evaluate classification for a single test file.

        Args:
            file_name: Name of CSV file to test
            expected: Expected classification

        Returns:
            List of all EvalResults for this file
        """
        if not self._client:
            raise RuntimeError("Evaluator not initialized")

        file_path = self.data_dir / file_name
        if not file_path.exists():
            logger.warning(f"Skipping {file_name}: file not found at {file_path}")
            return [EvalResult(
                test_id=f"CLASS-{file_name}-missing",
                category="classification",
                description=f"Test file {file_name}",
                passed=False,
                score=0,
                max_score=1,
                error=f"File not found: {file_path}",
            )]

        logger.info(f"Testing: {file_name}")
        results = []

        try:
            # Create session and upload file
            session_id = await self._client.create_session()
            logger.debug(f"Created session: {session_id}")

            await self._client.upload_file(session_id, file_path)
            logger.debug("File uploaded")

            # Send initial message to trigger classification
            await self._client.send_chat(session_id, "Please analyze this file")
            logger.debug("Classification requested")

            # Get session with classification
            session = await self._client.get_session(session_id)
            classification: ClassificationDict = session.get("classification", {})

            if not classification:
                return [EvalResult(
                    test_id=f"CLASS-{file_name}-none",
                    category="classification",
                    description=f"Classification for {file_name}",
                    passed=False,
                    score=0,
                    max_score=1,
                    error="No classification returned by LLM",
                )]

            # Compare classifications
            results.extend(self._compare_classification(classification, expected, file_name))

            # Check critical cases
            results.extend(self._check_critical(classification, expected, file_name))

            # Check techniques
            results.extend(self._check_techniques(classification, expected, file_name))

        except Exception as e:
            logger.error(f"Error evaluating {file_name}: {e}")
            results.append(EvalResult(
                test_id=f"CLASS-{file_name}-error",
                category="classification",
                description=f"Classification for {file_name}",
                passed=False,
                score=0,
                max_score=1,
                error=str(e),
            ))

        return results

    async def eval_classification(self) -> list[EvalResult]:
        """
        Evaluate column classification accuracy across all test files.

        Returns:
            List of all classification EvalResults
        """
        logger.info("=" * 40)
        logger.info("Classification Evaluation")
        logger.info("=" * 40)

        if self.parallel:
            # Run all files in parallel
            tasks = [
                self._eval_single_file(file_name, expected)
                for file_name, expected in self.expected.items()
            ]
            results_lists = await asyncio.gather(*tasks, return_exceptions=True)

            all_results = []
            for result in results_lists:
                if isinstance(result, Exception):
                    logger.error(f"Parallel task failed: {result}")
                else:
                    all_results.extend(result)
            return all_results
        else:
            # Run sequentially
            all_results = []
            for file_name, expected in self.expected.items():
                results = await self._eval_single_file(file_name, expected)
                all_results.extend(results)
            return all_results

    async def eval_tool_calling(self) -> list[EvalResult]:
        """
        Evaluate tool calling accuracy.

        Tests:
            - classify_columns called after file upload
            - execute_pipeline called after approval
            - No premature pipeline execution
            - update_thresholds works correctly
            - update_classification works correctly

        Returns:
            List of tool calling EvalResults
        """
        logger.info("=" * 40)
        logger.info("Tool Calling Evaluation")
        logger.info("=" * 40)

        if not self._client:
            raise RuntimeError("Evaluator not initialized")

        results = []
        file_path = self.data_dir / "fraud_detection.csv"

        # Test 1: Classification tool is called after upload
        logger.info("Test: classify_columns called after upload")
        try:
            session_id = await self._client.create_session()
            await self._client.upload_file(session_id, file_path)
            await self._client.send_chat(session_id, "Analyze this data")
            session = await self._client.get_session(session_id)

            has_classification = bool(session.get("classification"))
            results.append(EvalResult(
                test_id="TOOL-001-classify-after-upload",
                category="tool_calling",
                description="classify_columns called after upload",
                passed=has_classification,
                score=1.0 if has_classification else 0.0,
                max_score=1.0,
                details={"has_classification": has_classification},
            ))
        except Exception as e:
            logger.error(f"Test TOOL-001 failed: {e}")
            results.append(EvalResult(
                test_id="TOOL-001-classify-after-upload",
                category="tool_calling",
                description="classify_columns called after upload",
                passed=False,
                score=0.0,
                max_score=1.0,
                error=str(e),
            ))

        # Test 2: Pipeline execution after approval
        logger.info("Test: execute_pipeline called after approval")
        try:
            session_id = await self._client.create_session()
            await self._client.upload_file(session_id, file_path)
            await self._client.send_chat(session_id, "Analyze this data")
            await self._client.send_chat(session_id, "Yes, approved. Proceed with anonymization.")
            session = await self._client.get_session(session_id)

            status = session.get("status", "")
            pipeline_executed = status in ["masking", "validating", "completed", "failed"]

            results.append(EvalResult(
                test_id="TOOL-002-pipeline-after-approval",
                category="tool_calling",
                description="execute_pipeline called after approval",
                passed=pipeline_executed,
                score=1.0 if pipeline_executed else 0.0,
                max_score=1.0,
                details={"status": status, "pipeline_executed": pipeline_executed},
            ))
        except Exception as e:
            logger.error(f"Test TOOL-002 failed: {e}")
            results.append(EvalResult(
                test_id="TOOL-002-pipeline-after-approval",
                category="tool_calling",
                description="execute_pipeline called after approval",
                passed=False,
                score=0.0,
                max_score=1.0,
                error=str(e),
            ))

        # Test 3: No premature pipeline execution
        logger.info("Test: No premature pipeline execution")
        try:
            session_id = await self._client.create_session()
            await self._client.upload_file(session_id, file_path)
            await self._client.send_chat(session_id, "Analyze this data")
            await self._client.send_chat(session_id, "Can you explain the classification?")
            session = await self._client.get_session(session_id)

            status = session.get("status", "")
            no_premature = status not in ["masking", "validating", "completed", "failed"]

            results.append(EvalResult(
                test_id="TOOL-003-no-premature-execution",
                category="tool_calling",
                description="No premature pipeline execution",
                passed=no_premature,
                score=1.0 if no_premature else 0.0,
                max_score=1.0,
                details={"status": status, "no_premature": no_premature},
            ))
        except Exception as e:
            logger.error(f"Test TOOL-003 failed: {e}")
            results.append(EvalResult(
                test_id="TOOL-003-no-premature-execution",
                category="tool_calling",
                description="No premature pipeline execution",
                passed=False,
                score=0.0,
                max_score=1.0,
                error=str(e),
            ))

        # Test 4: Threshold update works
        logger.info("Test: update_thresholds tool works")
        try:
            session_id = await self._client.create_session()
            await self._client.upload_file(session_id, file_path)
            await self._client.send_chat(session_id, "Analyze this data")
            await self._client.send_chat(session_id, "Please increase k-anonymity minimum to 10")
            session = await self._client.get_session(session_id)

            thresholds = session.get("thresholds", {})
            k_anon = thresholds.get("k_anonymity", {})
            k_min = k_anon.get("minimum", 5)
            threshold_updated = k_min >= 10

            results.append(EvalResult(
                test_id="TOOL-004-threshold-update",
                category="tool_calling",
                description="update_thresholds tool works correctly",
                passed=threshold_updated,
                score=1.0 if threshold_updated else 0.0,
                max_score=1.0,
                details={"k_anonymity_minimum": k_min, "expected": 10},
            ))
        except Exception as e:
            logger.error(f"Test TOOL-004 failed: {e}")
            results.append(EvalResult(
                test_id="TOOL-004-threshold-update",
                category="tool_calling",
                description="update_thresholds tool works correctly",
                passed=False,
                score=0.0,
                max_score=1.0,
                error=str(e),
            ))

        # Test 5: Classification update works
        logger.info("Test: update_classification tool works")
        try:
            session_id = await self._client.create_session()
            await self._client.upload_file(session_id, file_path)
            await self._client.send_chat(session_id, "Analyze this data")
            await self._client.send_chat(
                session_id,
                "Please change 'gender' from quasi-identifier to sensitive attribute"
            )
            session = await self._client.get_session(session_id)

            classification = session.get("classification", {})
            sensitive = classification.get("sensitive_attributes", [])
            classification_updated = "gender" in sensitive

            results.append(EvalResult(
                test_id="TOOL-005-classification-update",
                category="tool_calling",
                description="update_classification tool works correctly",
                passed=classification_updated,
                score=1.0 if classification_updated else 0.0,
                max_score=1.0,
                details={"gender_in_sensitive": classification_updated},
            ))
        except Exception as e:
            logger.error(f"Test TOOL-005 failed: {e}")
            results.append(EvalResult(
                test_id="TOOL-005-classification-update",
                category="tool_calling",
                description="update_classification tool works correctly",
                passed=False,
                score=0.0,
                max_score=1.0,
                error=str(e),
            ))

        return results

    async def eval_saudi_patterns(self) -> list[EvalResult]:
        """
        Evaluate Saudi-specific data pattern detection.

        Tests detection of:
            - National ID (10 digits starting with 1)
            - Iqama (10 digits starting with 2)
            - Saudi phone numbers (+966, 05)
            - Saudi IBAN
            - Saudi cities as quasi-identifiers

        Returns:
            List of Saudi pattern EvalResults
        """
        logger.info("=" * 40)
        logger.info("Saudi Pattern Detection Evaluation")
        logger.info("=" * 40)

        if not self._client:
            raise RuntimeError("Evaluator not initialized")

        results = []

        try:
            session_id = await self._client.create_session()
            file_path = self.data_dir / "fraud_detection.csv"
            await self._client.upload_file(session_id, file_path)
            await self._client.send_chat(session_id, "Analyze this file")

            session = await self._client.get_session(session_id)
            classification: ClassificationDict = session.get("classification", {})

            # Test patterns
            pattern_tests = [
                ("SAUDI-001", "national_id", "direct_identifiers", "National ID pattern"),
                ("SAUDI-002", "phone", "direct_identifiers", "Saudi phone pattern"),
                ("SAUDI-003", "email", "direct_identifiers", "Email pattern"),
                ("SAUDI-004", "city", "quasi_identifiers", "Saudi city as quasi-identifier"),
                ("SAUDI-005", "age", "quasi_identifiers", "Age as quasi-identifier"),
                ("SAUDI-006", "gender", "quasi_identifiers", "Gender as quasi-identifier"),
            ]

            for test_id, column, expected_category, description in pattern_tests:
                detected = column in classification.get(expected_category, [])
                results.append(EvalResult(
                    test_id=test_id,
                    category="saudi_patterns",
                    description=description,
                    passed=detected,
                    score=1.0 if detected else 0.0,
                    max_score=1.0,
                    details={"column": column, "expected_category": expected_category},
                ))
                logger.debug(f"{test_id}: {column} in {expected_category} = {detected}")

        except Exception as e:
            logger.error(f"Saudi pattern evaluation failed: {e}")
            results.append(EvalResult(
                test_id="SAUDI-ERROR",
                category="saudi_patterns",
                description="Saudi pattern detection",
                passed=False,
                score=0.0,
                max_score=1.0,
                error=str(e),
            ))

        # Test with open_banking.csv for IBAN detection
        try:
            session_id = await self._client.create_session()
            file_path = self.data_dir / "open_banking.csv"
            await self._client.upload_file(session_id, file_path)
            await self._client.send_chat(session_id, "Analyze this file")

            session = await self._client.get_session(session_id)
            classification = session.get("classification", {})

            iban_detected = "iban" in classification.get("direct_identifiers", [])
            results.append(EvalResult(
                test_id="SAUDI-007",
                category="saudi_patterns",
                description="Saudi IBAN pattern detected",
                passed=iban_detected,
                score=1.0 if iban_detected else 0.0,
                max_score=1.0,
                details={"iban_detected": iban_detected},
            ))
        except Exception as e:
            logger.error(f"IBAN detection test failed: {e}")
            results.append(EvalResult(
                test_id="SAUDI-007",
                category="saudi_patterns",
                description="Saudi IBAN pattern detected",
                passed=False,
                score=0.0,
                max_score=1.0,
                error=str(e),
            ))

        return results

    async def eval_reasoning(self) -> list[EvalResult]:
        """
        Evaluate quality of LLM reasoning and explanations.

        Tests:
            - Reasoning is provided
            - Reasoning mentions privacy concepts
            - Reasoning mentions techniques
            - Reasoning is specific to the data

        Returns:
            List of reasoning EvalResults
        """
        logger.info("=" * 40)
        logger.info("Reasoning Quality Evaluation")
        logger.info("=" * 40)

        if not self._client:
            raise RuntimeError("Evaluator not initialized")

        results = []

        try:
            session_id = await self._client.create_session()
            file_path = self.data_dir / "fraud_detection.csv"
            await self._client.upload_file(session_id, file_path)
            await self._client.send_chat(session_id, "Analyze this file and explain your reasoning")

            session = await self._client.get_session(session_id)
            classification: ClassificationDict = session.get("classification", {})
            reasoning = classification.get("reasoning", "") or ""

            # Test 1: Reasoning is provided and substantial
            has_reasoning = len(reasoning) >= MIN_REASONING_LENGTH
            results.append(EvalResult(
                test_id="REASON-001",
                category="reasoning",
                description="Reasoning provided for classification",
                passed=has_reasoning,
                score=1.0 if has_reasoning else 0.0,
                max_score=1.0,
                details={
                    "reasoning_length": len(reasoning),
                    "min_required": MIN_REASONING_LENGTH,
                },
            ))

            reasoning_lower = reasoning.lower()

            # Test 2: Mentions privacy concepts
            privacy_keywords = ["pii", "personal", "identifier", "sensitive", "privacy", "confidential"]
            privacy_matches = [kw for kw in privacy_keywords if kw in reasoning_lower]
            mentions_privacy = len(privacy_matches) >= MIN_REASONING_KEYWORDS

            results.append(EvalResult(
                test_id="REASON-002",
                category="reasoning",
                description="Reasoning mentions privacy concepts",
                passed=mentions_privacy,
                score=1.0 if mentions_privacy else 0.0,
                max_score=1.0,
                details={"keywords_found": privacy_matches},
            ))

            # Test 3: Mentions anonymization techniques
            technique_keywords = ["suppress", "generalize", "pseudonymize", "hash", "mask", "anonymize", "remove"]
            technique_matches = [kw for kw in technique_keywords if kw in reasoning_lower]
            mentions_techniques = len(technique_matches) >= 1

            results.append(EvalResult(
                test_id="REASON-003",
                category="reasoning",
                description="Reasoning mentions anonymization techniques",
                passed=mentions_techniques,
                score=1.0 if mentions_techniques else 0.0,
                max_score=1.0,
                details={"keywords_found": technique_matches},
            ))

            # Test 4: Mentions specific columns from the data
            columns_in_data = ["national_id", "phone", "email", "age", "city", "fraud", "transaction"]
            column_matches = [col for col in columns_in_data if col in reasoning_lower]
            mentions_columns = len(column_matches) >= 2

            results.append(EvalResult(
                test_id="REASON-004",
                category="reasoning",
                description="Reasoning is specific to the data",
                passed=mentions_columns,
                score=1.0 if mentions_columns else 0.0,
                max_score=1.0,
                details={"columns_mentioned": column_matches},
            ))

        except Exception as e:
            logger.error(f"Reasoning evaluation failed: {e}")
            results.append(EvalResult(
                test_id="REASON-ERROR",
                category="reasoning",
                description="Reasoning evaluation",
                passed=False,
                score=0.0,
                max_score=1.0,
                error=str(e),
            ))

        return results

    async def eval_regulatory(self) -> list[EvalResult]:
        """
        Evaluate regulatory compliance references.

        Tests:
            - PDPL referenced
            - SAMA referenced
            - Specific articles cited
            - Appropriate regulations for data type

        Returns:
            List of regulatory EvalResults
        """
        logger.info("=" * 40)
        logger.info("Regulatory Compliance Evaluation")
        logger.info("=" * 40)

        if not self._client:
            raise RuntimeError("Evaluator not initialized")

        results = []

        try:
            session_id = await self._client.create_session()
            file_path = self.data_dir / "fraud_detection.csv"
            await self._client.upload_file(session_id, file_path)

            # Ask specifically about regulations
            await self._client.send_chat(
                session_id,
                "Analyze this file and explain which PDPL and SAMA regulations apply"
            )

            session = await self._client.get_session(session_id)
            messages = session.get("messages", [])

            # Get all assistant messages
            assistant_msgs = [m for m in messages if m.get("role") == "assistant"]
            all_content = " ".join(m.get("content", "") for m in assistant_msgs)
            content_lower = all_content.lower()

            # Test 1: PDPL referenced
            pdpl_mentioned = any(term in content_lower for term in ["pdpl", "personal data protection law"])
            results.append(EvalResult(
                test_id="REG-001",
                category="regulatory",
                description="PDPL referenced in response",
                passed=pdpl_mentioned,
                score=1.0 if pdpl_mentioned else 0.0,
                max_score=1.0,
            ))

            # Test 2: SAMA referenced
            sama_mentioned = any(term in content_lower for term in ["sama", "saudi arabian monetary", "monetary authority"])
            results.append(EvalResult(
                test_id="REG-002",
                category="regulatory",
                description="SAMA referenced in response",
                passed=sama_mentioned,
                score=1.0 if sama_mentioned else 0.0,
                max_score=1.0,
            ))

            # Test 3: Specific articles cited
            has_article = any(term in content_lower for term in ["article", "art.", "section", "art "])
            results.append(EvalResult(
                test_id="REG-003",
                category="regulatory",
                description="Specific regulation articles cited",
                passed=has_article,
                score=1.0 if has_article else 0.0,
                max_score=1.0,
            ))

            # Test 4: Fraud-specific regulations mentioned (for fraud detection dataset)
            fraud_relevant = any(term in content_lower for term in ["fraud", "financial", "transaction", "banking"])
            results.append(EvalResult(
                test_id="REG-004",
                category="regulatory",
                description="Domain-relevant regulations mentioned",
                passed=fraud_relevant,
                score=1.0 if fraud_relevant else 0.0,
                max_score=1.0,
            ))

        except Exception as e:
            logger.error(f"Regulatory evaluation failed: {e}")
            results.append(EvalResult(
                test_id="REG-ERROR",
                category="regulatory",
                description="Regulatory compliance evaluation",
                passed=False,
                score=0.0,
                max_score=1.0,
                error=str(e),
            ))

        return results

    def _calculate_grade(self, percentage: float) -> str:
        """
        Calculate letter grade from percentage.

        Args:
            percentage: Score as percentage (0-100)

        Returns:
            Letter grade (A-F)
        """
        for threshold, grade in GRADE_THRESHOLDS:
            if percentage >= threshold:
                return grade
        return "F"

    def _generate_report(self) -> EvalReport:
        """
        Generate evaluation report from accumulated results.

        Returns:
            Complete EvalReport
        """
        # Calculate category scores
        category_scores: dict[str, CategoryScore] = {}
        for category, weight in CATEGORY_WEIGHTS.items():
            cat_results = [r for r in self.results if r.category == category]
            if cat_results:
                total = sum(r.score for r in cat_results)
                max_total = sum(r.max_score for r in cat_results)
                percentage = (total / max_total * 100) if max_total > 0 else 0
                category_scores[category] = {
                    "score": total,
                    "max_score": max_total,
                    "percentage": round(percentage, 2),
                    "weight": weight,
                }

        # Calculate weighted total
        weighted_sum = sum(
            scores["percentage"] * CATEGORY_WEIGHTS[category]
            for category, scores in category_scores.items()
        )

        # Find critical failures
        critical_failures = [
            r.test_id for r in self.results
            if r.test_id.startswith("CRIT-") and not r.passed
        ]

        total_score = sum(r.score for r in self.results)
        max_score = sum(r.max_score for r in self.results)

        duration_ms = (time.monotonic() - self._start_time) * 1000 if self._start_time else 0

        return EvalReport(
            timestamp=datetime.now().isoformat(),
            provider=self.provider,
            model=self.model or f"{self.provider}-default",
            total_score=total_score,
            max_score=max_score,
            percentage=round(weighted_sum, 2),
            grade=self._calculate_grade(weighted_sum),
            results=self.results,
            category_scores=category_scores,
            critical_failures=critical_failures,
            duration_ms=duration_ms,
            sessions_created=self._client.sessions_created_count if self._client else 0,
            sessions_cleaned=0,  # Updated after cleanup
        )

    def _print_report(self, report: EvalReport) -> None:
        """
        Print evaluation report to stdout.

        Args:
            report: Report to print
        """
        print("\n" + "=" * 60)
        print("SADNxAI LLM EVALUATION REPORT")
        print("=" * 60)
        print(f"Timestamp:  {report.timestamp}")
        print(f"Provider:   {report.provider}")
        print(f"Model:      {report.model}")
        print(f"Duration:   {report.duration_ms:.0f}ms")
        print(f"Grade:      {report.grade} ({report.percentage}%)")
        print()

        print("Category Scores:")
        print("-" * 40)
        for category, scores in report.category_scores.items():
            weight_pct = int(scores["weight"] * 100)
            bar_len = int(scores["percentage"] / 5)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            print(f"  {category:18} {bar} {scores['percentage']:5.1f}% (w:{weight_pct}%)")
        print()

        if report.critical_failures:
            print("CRITICAL FAILURES:")
            print("-" * 40)
            for failure in report.critical_failures:
                print(f"  ✗ {failure}")
            print()

        # Show failed and skipped tests
        failed = [r for r in report.results if not r.passed]
        if failed:
            print(f"Failed/Skipped Tests ({len(failed)}):")
            print("-" * 40)
            for r in failed[:10]:
                if r.status == EvalStatus.SKIPPED:
                    icon = "⊘"  # Skipped
                elif r.status == EvalStatus.ERROR:
                    icon = "⚠"  # Error
                else:
                    icon = "✗"  # Failed
                print(f"  {icon} {r.test_id}: {r.description}")
                if r.error:
                    print(f"      {r.status.value}: {r.error}")
            if len(failed) > 10:
                print(f"  ... and {len(failed) - 10} more")
            print()

        # Summary
        passed = [r for r in report.results if r.passed]
        skipped = [r for r in report.results if r.status == EvalStatus.SKIPPED]
        errors = [r for r in report.results if r.status == EvalStatus.ERROR]
        print(f"Summary: {len(passed)} passed, {len(failed) - len(skipped) - len(errors)} failed, {len(skipped)} skipped, {len(errors)} errors")
        print(f"Sessions: {report.sessions_created} created, {report.sessions_cleaned} cleaned")
        print()

        print("=" * 60)
        if report.critical_failures:
            print("RESULT: FAIL - Critical test failures detected")
            print("        NOT PRODUCTION READY")
        elif report.grade in ["A", "B"]:
            print("RESULT: PASS - LLM meets production standards")
        elif report.grade == "C":
            print("RESULT: ACCEPTABLE - Minor improvements recommended")
        else:
            print("RESULT: FAIL - LLM does not meet production standards")
        print("=" * 60)

    def _save_report(self, report: EvalReport) -> Path:
        """
        Save report to JSON file.

        Args:
            report: Report to save

        Returns:
            Path to saved report
        """
        report_dir = self.evals_dir / "reports"
        report_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"eval_{self.provider}_{timestamp}.json"

        with open(report_file, "w") as f:
            json.dump({
                "timestamp": report.timestamp,
                "provider": report.provider,
                "model": report.model,
                "percentage": report.percentage,
                "grade": report.grade,
                "duration_ms": report.duration_ms,
                "sessions_created": report.sessions_created,
                "sessions_cleaned": report.sessions_cleaned,
                "category_scores": report.category_scores,
                "critical_failures": report.critical_failures,
                "summary": {
                    "total_tests": len(report.results),
                    "passed": len([r for r in report.results if r.passed]),
                    "failed": len([r for r in report.results if not r.passed]),
                    "errors": len([r for r in report.results if r.error]),
                },
                "results": [
                    {
                        "test_id": r.test_id,
                        "category": r.category,
                        "description": r.description,
                        "passed": r.passed,
                        "score": r.score,
                        "max_score": r.max_score,
                        "details": r.details,
                        "error": r.error,
                        "duration_ms": r.duration_ms,
                    }
                    for r in report.results
                ],
            }, f, indent=2)

        return report_file

    async def run(self, categories: list[str] | None = None) -> EvalReport:
        """
        Run all evaluations.

        Args:
            categories: List of categories to run, or None for all

        Returns:
            Complete EvalReport

        Raises:
            NotImplementedError: If direct_mode is True (not yet implemented)
        """
        # Check for unimplemented direct mode
        if self.direct_mode:
            raise NotImplementedError(
                "Direct LLM testing mode is not yet implemented. "
                "Please run without --direct flag and ensure chat-service is running. "
                "To implement: add direct vLLM/Claude API calls bypassing chat-service."
            )

        self._start_time = time.monotonic()

        logger.info("Starting SADNxAI LLM Evaluation")
        logger.info(f"Provider: {self.provider}")
        logger.info(f"Base URL: {self.base_url}")
        logger.info(f"Parallel: {self.parallel}")

        # Health check
        if not await self.check_services():
            return EvalReport(
                timestamp=datetime.now().isoformat(),
                provider=self.provider,
                model=self.model,
                total_score=0,
                max_score=0,
                percentage=0,
                grade="F",
                results=[EvalResult(
                    test_id="HEALTH-CHECK",
                    category="system",
                    description="Service health check",
                    passed=False,
                    score=0,
                    max_score=1,
                    error=f"Services not available at {self.base_url}",
                )],
                category_scores={},
                critical_failures=["HEALTH-CHECK"],
            )

        # Run selected evaluations
        if categories is None:
            categories = list(CATEGORY_WEIGHTS.keys())

        for category in categories:
            if category == "classification":
                self.results.extend(await self.eval_classification())
            elif category == "tool_calling":
                self.results.extend(await self.eval_tool_calling())
            elif category == "saudi_patterns":
                self.results.extend(await self.eval_saudi_patterns())
            elif category == "reasoning":
                self.results.extend(await self.eval_reasoning())
            elif category == "regulatory":
                self.results.extend(await self.eval_regulatory())

        # Cleanup sessions before generating report to get accurate count
        if self._client:
            await self._client.cleanup_sessions()

        # Generate report with accurate cleanup count
        report = self._generate_report()

        # Update cleaned count from actual cleanup result
        if self._client:
            report.sessions_cleaned = self._client.sessions_cleaned_count

        # Print and save
        self._print_report(report)
        report_file = self._save_report(report)
        logger.info(f"Report saved to: {report_file}")

        return report


# =============================================================================
# CLI Entry Point
# =============================================================================

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="SADNxAI LLM Evaluation Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python evals/run_evals.py                           # Run all evaluations
  python evals/run_evals.py --provider claude         # Use Claude provider
  python evals/run_evals.py --category classification # Run only classification
  python evals/run_evals.py --parallel -v             # Parallel with verbose
        """,
    )

    parser.add_argument(
        "--provider",
        choices=["vllm", "claude", "ollama", "mock"],
        default="vllm",
        help="LLM provider to test (default: vllm)",
    )

    parser.add_argument(
        "--model",
        default="",
        help="Specific model name (auto-detected if not specified)",
    )

    parser.add_argument(
        "--category",
        choices=list(CATEGORY_WEIGHTS.keys()),
        help="Run only specific category",
    )

    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="Base URL for chat-service (default: http://localhost:8000)",
    )

    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run test files in parallel for faster execution",
    )

    parser.add_argument(
        "--direct",
        action="store_true",
        help="Test LLM directly without chat-service (TODO: not yet implemented)",
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output",
    )

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)",
    )

    return parser.parse_args()


async def main_async(args: argparse.Namespace) -> int:
    """
    Async main function.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    categories = [args.category] if args.category else None

    async with LLMEvaluator(
        base_url=args.url,
        provider=args.provider,
        model=args.model,
        parallel=args.parallel,
        direct_mode=args.direct,
    ) as evaluator:
        report = await evaluator.run(categories)

    # Exit with error code if failed
    if report.grade in ["D", "F"] or report.critical_failures:
        return 1
    return 0


def main() -> None:
    """CLI entry point."""
    args = parse_args()

    # Setup logging
    log_level = "DEBUG" if args.verbose else args.log_level
    setup_logging(log_level)

    # Run evaluation
    exit_code = asyncio.run(main_async(args))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
