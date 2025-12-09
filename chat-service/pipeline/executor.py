"""
Pipeline Executor
Orchestrates masking and validation services
"""

import os
import uuid
import httpx
from typing import Dict, Any

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.models import Session, ValidationResult, MetricResult, RemediationSuggestion


class PipelineExecutor:
    """
    Orchestrates the anonymization pipeline.

    Steps:
    1. Call masking service to anonymize data
    2. Call validation service to check privacy metrics
    3. Generate PDF report
    4. Move final output to output directory
    """

    def __init__(
        self,
        masking_url: str = None,
        validation_url: str = None,
        storage_path: str = None
    ):
        """
        Initialize pipeline executor.

        Args:
            masking_url: URL of masking service
            validation_url: URL of validation service
            storage_path: Base storage path
        """
        self.masking_url = masking_url or os.getenv("MASKING_SERVICE_URL", "http://localhost:8001")
        self.validation_url = validation_url or os.getenv("VALIDATION_SERVICE_URL", "http://localhost:8002")
        self.storage_path = storage_path or os.getenv("STORAGE_PATH", "/storage")

    async def execute(self, session: Session) -> Dict[str, Any]:
        """
        Execute the full anonymization pipeline.

        Args:
            session: Session with classification and file info

        Returns:
            Dict with results including:
                - masked_path: Path to anonymized CSV
                - validation_result: Validation metrics
                - report_path: Path to PDF report (if validation passed)
        """
        job_id = str(uuid.uuid4())
        salt = str(uuid.uuid4())  # Generate unique salt for this job

        result = {
            "job_id": job_id,
            "masked_path": None,
            "validation_result": None,
            "report_path": None,
            "error": None
        }

        try:
            # Step 1: Masking
            masking_result = await self._call_masking_service(
                job_id=job_id,
                input_path=session.file_path,
                classification=session.classification,
                salt=salt
            )

            if "error" in masking_result:
                result["error"] = f"Masking failed: {masking_result['error']}"
                return result

            result["masked_path"] = masking_result["output_path"]

            # Step 2: Validation
            validation_result = await self._call_validation_service(
                job_id=job_id,
                input_path=masking_result["output_path"],
                quasi_identifiers=session.classification.quasi_identifiers,
                sensitive_attributes=session.classification.sensitive_attributes,
                thresholds=session.thresholds
            )

            if "error" in validation_result:
                result["error"] = f"Validation failed: {validation_result['error']}"
                return result

            # Convert to ValidationResult model
            result["validation_result"] = ValidationResult(
                passed=validation_result["passed"],
                metrics={
                    k: MetricResult(**v) for k, v in validation_result["metrics"].items()
                },
                failed_metrics=validation_result["failed_metrics"],
                remediation_suggestions=[
                    RemediationSuggestion(**s) for s in validation_result.get("remediation_suggestions", [])
                ]
            )

            # Step 3: Generate report (if validation passed or for all completions)
            report_result = await self._call_report_service(
                job_id=job_id,
                session=session,
                validation_result=validation_result
            )

            if "error" not in report_result:
                result["report_path"] = report_result["report_path"]

            # Step 4: Move to output if passed
            if validation_result["passed"]:
                output_path = await self._move_to_output(
                    job_id=job_id,
                    masked_path=masking_result["output_path"],
                    original_filename=session.title
                )
                result["output_path"] = output_path

        except Exception as e:
            result["error"] = str(e)

        return result

    async def _call_masking_service(
        self,
        job_id: str,
        input_path: str,
        classification: Any,
        salt: str
    ) -> Dict[str, Any]:
        """Call masking service to anonymize data."""
        async with httpx.AsyncClient(timeout=300.0) as client:
            try:
                response = await client.post(
                    f"{self.masking_url}/mask",
                    json={
                        "job_id": job_id,
                        "input_path": input_path,
                        "classification": classification.model_dump(),
                        "salt": salt
                    }
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                return {"error": str(e)}

    async def _call_validation_service(
        self,
        job_id: str,
        input_path: str,
        quasi_identifiers: list,
        sensitive_attributes: list,
        thresholds: Any
    ) -> Dict[str, Any]:
        """Call validation service to check privacy metrics."""
        async with httpx.AsyncClient(timeout=300.0) as client:
            try:
                response = await client.post(
                    f"{self.validation_url}/validate",
                    json={
                        "job_id": job_id,
                        "input_path": input_path,
                        "quasi_identifiers": quasi_identifiers,
                        "sensitive_attributes": sensitive_attributes,
                        "thresholds": thresholds.model_dump()
                    }
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                return {"error": str(e)}

    async def _call_report_service(
        self,
        job_id: str,
        session: Session,
        validation_result: Dict
    ) -> Dict[str, Any]:
        """Call validation service to generate PDF report."""
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                response = await client.post(
                    f"{self.validation_url}/report",
                    json={
                        "job_id": job_id,
                        "session": session.model_dump(mode="json"),
                        "validation_result": validation_result
                    }
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                return {"error": str(e)}

    async def _move_to_output(
        self,
        job_id: str,
        masked_path: str,
        original_filename: str
    ) -> str:
        """Move masked file to output directory with proper naming."""
        import shutil

        # Generate output filename
        base_name = os.path.splitext(original_filename)[0]
        output_filename = f"{base_name}_anonymized.csv"
        output_dir = os.path.join(self.storage_path, "output")
        output_path = os.path.join(output_dir, output_filename)

        # Ensure directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Copy file
        shutil.copy2(masked_path, output_path)

        return output_path
