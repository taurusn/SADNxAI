#!/usr/bin/env python3
"""
SADNxAI LLM Evaluation Script

Evaluates the LLM's performance on:
1. Column classification accuracy
2. Tool calling correctness
3. Saudi data pattern detection
4. Reasoning quality
5. Regulatory compliance

Usage:
    python evals/run_evals.py                           # Run all evals
    python evals/run_evals.py --provider vllm           # Use vLLM provider
    python evals/run_evals.py --category classification # Run only classification tests
    python evals/run_evals.py --verbose                 # Show detailed output
"""

import argparse
import asyncio
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
import pandas as pd

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@dataclass
class EvalResult:
    """Result of a single evaluation test"""
    test_id: str
    category: str
    description: str
    passed: bool
    score: float
    max_score: float
    details: dict = field(default_factory=dict)
    error: str | None = None


@dataclass
class EvalReport:
    """Complete evaluation report"""
    timestamp: str
    provider: str
    model: str
    total_score: float
    max_score: float
    percentage: float
    grade: str
    results: list[EvalResult]
    category_scores: dict[str, dict]
    critical_failures: list[str]


class LLMEvaluator:
    """Evaluates LLM performance for SADNxAI"""

    WEIGHTS = {
        "classification": 0.40,
        "tool_calling": 0.25,
        "saudi_patterns": 0.15,
        "reasoning": 0.10,
        "regulatory": 0.10,
    }

    GRADE_THRESHOLDS = [
        (90, "A"),
        (80, "B"),
        (70, "C"),
        (60, "D"),
        (0, "F"),
    ]

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        provider: str = "vllm",
        verbose: bool = False,
    ):
        self.base_url = base_url
        self.provider = provider
        self.verbose = verbose
        self.results: list[EvalResult] = []
        self.evals_dir = Path(__file__).parent
        self.data_dir = self.evals_dir / "data"

        # Load expected classifications
        with open(self.evals_dir / "expected_classifications.json") as f:
            self.expected = json.load(f)

    def log(self, msg: str):
        """Print if verbose mode"""
        if self.verbose:
            print(f"  {msg}")

    async def create_session(self, client: httpx.AsyncClient) -> str:
        """Create a new test session"""
        resp = await client.post(f"{self.base_url}/api/sessions")
        resp.raise_for_status()
        return resp.json()["id"]

    async def upload_file(
        self, client: httpx.AsyncClient, session_id: str, file_path: Path
    ) -> dict:
        """Upload a CSV file to a session"""
        with open(file_path, "rb") as f:
            files = {"file": (file_path.name, f, "text/csv")}
            resp = await client.post(
                f"{self.base_url}/api/sessions/{session_id}/upload",
                files=files,
            )
        resp.raise_for_status()
        return resp.json()

    async def send_chat(
        self, client: httpx.AsyncClient, session_id: str, message: str
    ) -> dict:
        """Send a chat message and get response"""
        resp = await client.post(
            f"{self.base_url}/api/sessions/{session_id}/chat",
            json={"message": message},
            timeout=120.0,  # LLM can take time
        )
        resp.raise_for_status()
        return resp.json()

    async def get_session(
        self, client: httpx.AsyncClient, session_id: str
    ) -> dict:
        """Get session details including classification"""
        resp = await client.get(f"{self.base_url}/api/sessions/{session_id}")
        resp.raise_for_status()
        return resp.json()

    def compare_classification(
        self,
        actual: dict,
        expected: dict,
        file_name: str,
    ) -> list[EvalResult]:
        """Compare actual classification with expected"""
        results = []

        # Check each classification category
        for category in [
            "direct_identifiers",
            "quasi_identifiers",
            "linkage_identifiers",
            "date_columns",
            "sensitive_attributes",
        ]:
            expected_cols = set(expected.get(category, []))
            actual_cols = set(actual.get(category, []))

            correct = expected_cols & actual_cols
            missing = expected_cols - actual_cols
            extra = actual_cols - expected_cols

            score = len(correct)
            max_score = len(expected_cols)
            passed = missing == set() and extra == set()

            results.append(EvalResult(
                test_id=f"CLASS-{file_name}-{category}",
                category="classification",
                description=f"{category} classification for {file_name}",
                passed=passed,
                score=score,
                max_score=max_score,
                details={
                    "correct": list(correct),
                    "missing": list(missing),
                    "extra": list(extra),
                },
            ))

            self.log(f"{category}: {score}/{max_score} correct")
            if missing:
                self.log(f"  Missing: {missing}")
            if extra:
                self.log(f"  Extra: {extra}")

        return results

    def check_critical(
        self,
        actual: dict,
        expected: dict,
        file_name: str,
    ) -> list[EvalResult]:
        """Check critical test cases that must pass"""
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
                self.log(f"CRITICAL FAILURE: {col} not classified as direct_identifier")

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
                self.log(f"CRITICAL FAILURE: {col} not classified as sensitive_attribute")

        # Check must_not_be_suppressed
        for col in critical.get("must_not_be_suppressed", []):
            techniques = actual.get("recommended_techniques", {})
            passed = techniques.get(col) != "SUPPRESS"
            results.append(EvalResult(
                test_id=f"CRIT-{file_name}-nosuppress-{col}",
                category="classification",
                description=f"CRITICAL: {col} must NOT be suppressed",
                passed=passed,
                score=1.0 if passed else 0.0,
                max_score=1.0,
                details={"column": col, "actual_technique": techniques.get(col)},
            ))
            if not passed:
                self.log(f"CRITICAL FAILURE: {col} incorrectly marked for SUPPRESS")

        return results

    def check_techniques(
        self,
        actual: dict,
        expected: dict,
        file_name: str,
    ) -> list[EvalResult]:
        """Check recommended techniques match expected"""
        results = []
        expected_tech = expected.get("recommended_techniques", {})
        actual_tech = actual.get("recommended_techniques", {})

        correct = 0
        total = len(expected_tech)

        for col, exp_technique in expected_tech.items():
            act_technique = actual_tech.get(col)
            if act_technique == exp_technique:
                correct += 1
            else:
                self.log(f"Technique mismatch for {col}: expected {exp_technique}, got {act_technique}")

        results.append(EvalResult(
            test_id=f"TECH-{file_name}",
            category="classification",
            description=f"Technique recommendations for {file_name}",
            passed=correct == total,
            score=correct,
            max_score=total,
            details={
                "correct": correct,
                "total": total,
                "mismatches": {
                    col: {"expected": exp, "actual": actual_tech.get(col)}
                    for col, exp in expected_tech.items()
                    if actual_tech.get(col) != exp
                },
            },
        ))

        return results

    async def eval_classification(self) -> list[EvalResult]:
        """Evaluate column classification accuracy"""
        print("\n=== Classification Evaluation ===")
        all_results = []

        async with httpx.AsyncClient() as client:
            for file_name, expected in self.expected.items():
                file_path = self.data_dir / file_name
                if not file_path.exists():
                    print(f"  Skipping {file_name}: file not found")
                    continue

                print(f"\nTesting: {file_name}")

                try:
                    # Create session and upload file
                    session_id = await self.create_session(client)
                    self.log(f"Created session: {session_id}")

                    await self.upload_file(client, session_id, file_path)
                    self.log("File uploaded")

                    # Send initial message to trigger classification
                    await self.send_chat(client, session_id, "Please analyze this file")
                    self.log("Classification requested")

                    # Get session with classification
                    session = await self.get_session(client, session_id)
                    classification = session.get("classification", {})

                    if not classification:
                        all_results.append(EvalResult(
                            test_id=f"CLASS-{file_name}-none",
                            category="classification",
                            description=f"Classification for {file_name}",
                            passed=False,
                            score=0,
                            max_score=1,
                            error="No classification returned",
                        ))
                        continue

                    # Compare classifications
                    results = self.compare_classification(classification, expected, file_name)
                    all_results.extend(results)

                    # Check critical cases
                    critical_results = self.check_critical(classification, expected, file_name)
                    all_results.extend(critical_results)

                    # Check techniques
                    tech_results = self.check_techniques(classification, expected, file_name)
                    all_results.extend(tech_results)

                except httpx.HTTPError as e:
                    all_results.append(EvalResult(
                        test_id=f"CLASS-{file_name}-error",
                        category="classification",
                        description=f"Classification for {file_name}",
                        passed=False,
                        score=0,
                        max_score=1,
                        error=str(e),
                    ))
                except Exception as e:
                    all_results.append(EvalResult(
                        test_id=f"CLASS-{file_name}-error",
                        category="classification",
                        description=f"Classification for {file_name}",
                        passed=False,
                        score=0,
                        max_score=1,
                        error=str(e),
                    ))

        return all_results

    async def eval_tool_calling(self) -> list[EvalResult]:
        """Evaluate tool calling accuracy"""
        print("\n=== Tool Calling Evaluation ===")
        results = []

        async with httpx.AsyncClient() as client:
            # Test 1: Classification tool is called after upload
            print("\nTest: Classification tool called after upload")
            try:
                session_id = await self.create_session(client)
                file_path = self.data_dir / "fraud_detection.csv"
                await self.upload_file(client, session_id, file_path)

                response = await self.send_chat(client, session_id, "Analyze this data")
                session = await self.get_session(client, session_id)

                has_classification = bool(session.get("classification"))
                results.append(EvalResult(
                    test_id="TOOL-001",
                    category="tool_calling",
                    description="classify_columns called after upload",
                    passed=has_classification,
                    score=1.0 if has_classification else 0.0,
                    max_score=1.0,
                ))
                self.log(f"Classification present: {has_classification}")

            except Exception as e:
                results.append(EvalResult(
                    test_id="TOOL-001",
                    category="tool_calling",
                    description="classify_columns called after upload",
                    passed=False,
                    score=0.0,
                    max_score=1.0,
                    error=str(e),
                ))

            # Test 2: Pipeline execution after approval
            print("\nTest: execute_pipeline called after approval")
            try:
                session_id = await self.create_session(client)
                file_path = self.data_dir / "fraud_detection.csv"
                await self.upload_file(client, session_id, file_path)
                await self.send_chat(client, session_id, "Analyze this data")

                # Send approval
                await self.send_chat(client, session_id, "Yes, approved. Proceed with anonymization.")
                session = await self.get_session(client, session_id)

                # Check if pipeline was executed
                status = session.get("status", "")
                pipeline_executed = status in ["masking", "validating", "completed", "failed"]

                results.append(EvalResult(
                    test_id="TOOL-002",
                    category="tool_calling",
                    description="execute_pipeline called after approval",
                    passed=pipeline_executed,
                    score=1.0 if pipeline_executed else 0.0,
                    max_score=1.0,
                    details={"status": status},
                ))
                self.log(f"Pipeline executed: {pipeline_executed} (status: {status})")

            except Exception as e:
                results.append(EvalResult(
                    test_id="TOOL-002",
                    category="tool_calling",
                    description="execute_pipeline called after approval",
                    passed=False,
                    score=0.0,
                    max_score=1.0,
                    error=str(e),
                ))

            # Test 3: No premature pipeline execution
            print("\nTest: No premature pipeline execution")
            try:
                session_id = await self.create_session(client)
                file_path = self.data_dir / "fraud_detection.csv"
                await self.upload_file(client, session_id, file_path)
                await self.send_chat(client, session_id, "Analyze this data")

                # Ask a question without approving
                await self.send_chat(client, session_id, "Can you explain the classification?")
                session = await self.get_session(client, session_id)

                status = session.get("status", "")
                no_premature = status not in ["masking", "validating", "completed", "failed"]

                results.append(EvalResult(
                    test_id="TOOL-003",
                    category="tool_calling",
                    description="No premature pipeline execution",
                    passed=no_premature,
                    score=1.0 if no_premature else 0.0,
                    max_score=1.0,
                    details={"status": status},
                ))
                self.log(f"No premature execution: {no_premature} (status: {status})")

            except Exception as e:
                results.append(EvalResult(
                    test_id="TOOL-003",
                    category="tool_calling",
                    description="No premature pipeline execution",
                    passed=False,
                    score=0.0,
                    max_score=1.0,
                    error=str(e),
                ))

        return results

    async def eval_saudi_patterns(self) -> list[EvalResult]:
        """Evaluate Saudi data pattern detection"""
        print("\n=== Saudi Pattern Detection Evaluation ===")
        results = []

        # Test patterns from the edge_cases.csv
        patterns = [
            ("1098765432", "National ID", "direct_identifiers"),
            ("2123456789", "Iqama", "direct_identifiers"),
            ("+966512345678", "Saudi Phone (+966)", "direct_identifiers"),
            ("0551234567", "Saudi Phone (05)", "direct_identifiers"),
            ("SA0380000000608010167519", "Saudi IBAN", "direct_identifiers"),
        ]

        async with httpx.AsyncClient() as client:
            # Create a test with explicit patterns
            session_id = await self.create_session(client)
            file_path = self.data_dir / "fraud_detection.csv"
            await self.upload_file(client, session_id, file_path)
            await self.send_chat(client, session_id, "Analyze this file")

            session = await self.get_session(client, session_id)
            classification = session.get("classification", {})

            # Check national_id detection
            national_id_detected = "national_id" in classification.get("direct_identifiers", [])
            results.append(EvalResult(
                test_id="SAUDI-001",
                category="saudi_patterns",
                description="National ID pattern detected",
                passed=national_id_detected,
                score=1.0 if national_id_detected else 0.0,
                max_score=1.0,
            ))

            # Check phone detection
            phone_detected = "phone" in classification.get("direct_identifiers", [])
            results.append(EvalResult(
                test_id="SAUDI-002",
                category="saudi_patterns",
                description="Saudi phone pattern detected",
                passed=phone_detected,
                score=1.0 if phone_detected else 0.0,
                max_score=1.0,
            ))

            # Check email detection
            email_detected = "email" in classification.get("direct_identifiers", [])
            results.append(EvalResult(
                test_id="SAUDI-003",
                category="saudi_patterns",
                description="Email pattern detected",
                passed=email_detected,
                score=1.0 if email_detected else 0.0,
                max_score=1.0,
            ))

            # Check city as quasi-identifier
            city_quasi = "city" in classification.get("quasi_identifiers", [])
            results.append(EvalResult(
                test_id="SAUDI-004",
                category="saudi_patterns",
                description="Saudi city recognized as quasi-identifier",
                passed=city_quasi,
                score=1.0 if city_quasi else 0.0,
                max_score=1.0,
            ))

        return results

    async def eval_reasoning(self) -> list[EvalResult]:
        """Evaluate reasoning quality"""
        print("\n=== Reasoning Quality Evaluation ===")
        results = []

        async with httpx.AsyncClient() as client:
            session_id = await self.create_session(client)
            file_path = self.data_dir / "fraud_detection.csv"
            await self.upload_file(client, session_id, file_path)
            await self.send_chat(client, session_id, "Analyze this file")

            session = await self.get_session(client, session_id)
            classification = session.get("classification", {})
            reasoning = classification.get("reasoning", "")

            # Check if reasoning is provided
            has_reasoning = bool(reasoning) and len(reasoning) > 50
            results.append(EvalResult(
                test_id="REASON-001",
                category="reasoning",
                description="Reasoning provided for classification",
                passed=has_reasoning,
                score=1.0 if has_reasoning else 0.0,
                max_score=1.0,
                details={"reasoning_length": len(reasoning) if reasoning else 0},
            ))

            # Check if reasoning mentions key concepts
            reasoning_lower = (reasoning or "").lower()

            mentions_pii = any(term in reasoning_lower for term in ["pii", "personal", "identifier", "sensitive"])
            results.append(EvalResult(
                test_id="REASON-002",
                category="reasoning",
                description="Reasoning mentions privacy concepts",
                passed=mentions_pii,
                score=1.0 if mentions_pii else 0.0,
                max_score=1.0,
            ))

            mentions_technique = any(term in reasoning_lower for term in ["suppress", "generalize", "pseudonymize", "hash", "mask"])
            results.append(EvalResult(
                test_id="REASON-003",
                category="reasoning",
                description="Reasoning mentions anonymization techniques",
                passed=mentions_technique,
                score=1.0 if mentions_technique else 0.0,
                max_score=1.0,
            ))

        return results

    async def eval_regulatory(self) -> list[EvalResult]:
        """Evaluate regulatory compliance references"""
        print("\n=== Regulatory Compliance Evaluation ===")
        results = []

        async with httpx.AsyncClient() as client:
            session_id = await self.create_session(client)
            file_path = self.data_dir / "fraud_detection.csv"
            await self.upload_file(client, session_id, file_path)

            # Ask specifically about regulations
            response = await self.send_chat(
                client, session_id,
                "Analyze this file and explain which PDPL and SAMA regulations apply"
            )

            session = await self.get_session(client, session_id)
            messages = session.get("messages", [])

            # Get the last assistant message
            assistant_msgs = [m for m in messages if m.get("role") == "assistant"]
            last_msg = assistant_msgs[-1].get("content", "") if assistant_msgs else ""
            msg_lower = last_msg.lower()

            # Check for PDPL references
            pdpl_mentioned = "pdpl" in msg_lower or "personal data protection" in msg_lower
            results.append(EvalResult(
                test_id="REG-001",
                category="regulatory",
                description="PDPL referenced in response",
                passed=pdpl_mentioned,
                score=1.0 if pdpl_mentioned else 0.0,
                max_score=1.0,
            ))

            # Check for SAMA references
            sama_mentioned = "sama" in msg_lower or "saudi arabian monetary" in msg_lower
            results.append(EvalResult(
                test_id="REG-002",
                category="regulatory",
                description="SAMA referenced in response",
                passed=sama_mentioned,
                score=1.0 if sama_mentioned else 0.0,
                max_score=1.0,
            ))

            # Check for specific article references
            has_article = "article" in msg_lower or "art." in msg_lower or "section" in msg_lower
            results.append(EvalResult(
                test_id="REG-003",
                category="regulatory",
                description="Specific regulation articles cited",
                passed=has_article,
                score=1.0 if has_article else 0.0,
                max_score=1.0,
            ))

        return results

    def calculate_grade(self, percentage: float) -> str:
        """Calculate letter grade from percentage"""
        for threshold, grade in self.GRADE_THRESHOLDS:
            if percentage >= threshold:
                return grade
        return "F"

    def generate_report(self) -> EvalReport:
        """Generate evaluation report from results"""
        # Calculate category scores
        category_scores = {}
        for category in self.WEIGHTS.keys():
            cat_results = [r for r in self.results if r.category == category]
            if cat_results:
                total = sum(r.score for r in cat_results)
                max_total = sum(r.max_score for r in cat_results)
                percentage = (total / max_total * 100) if max_total > 0 else 0
                category_scores[category] = {
                    "score": total,
                    "max_score": max_total,
                    "percentage": round(percentage, 2),
                    "weight": self.WEIGHTS[category],
                }

        # Calculate weighted total
        weighted_sum = 0
        for category, scores in category_scores.items():
            weighted_sum += scores["percentage"] * self.WEIGHTS[category]

        # Find critical failures
        critical_failures = [
            r.test_id for r in self.results
            if r.test_id.startswith("CRIT-") and not r.passed
        ]

        total_score = sum(r.score for r in self.results)
        max_score = sum(r.max_score for r in self.results)

        return EvalReport(
            timestamp=datetime.now().isoformat(),
            provider=self.provider,
            model="",  # Will be filled from API
            total_score=total_score,
            max_score=max_score,
            percentage=round(weighted_sum, 2),
            grade=self.calculate_grade(weighted_sum),
            results=self.results,
            category_scores=category_scores,
            critical_failures=critical_failures,
        )

    def print_report(self, report: EvalReport):
        """Print evaluation report"""
        print("\n" + "=" * 60)
        print("SADNxAI LLM EVALUATION REPORT")
        print("=" * 60)
        print(f"Timestamp: {report.timestamp}")
        print(f"Provider:  {report.provider}")
        print(f"Grade:     {report.grade} ({report.percentage}%)")
        print()

        print("Category Scores:")
        print("-" * 40)
        for category, scores in report.category_scores.items():
            weight_pct = int(scores["weight"] * 100)
            print(f"  {category:20} {scores['percentage']:5.1f}% (weight: {weight_pct}%)")
        print()

        if report.critical_failures:
            print("CRITICAL FAILURES:")
            print("-" * 40)
            for failure in report.critical_failures:
                print(f"  {failure}")
            print()

        # Show failed tests
        failed = [r for r in report.results if not r.passed]
        if failed:
            print(f"Failed Tests ({len(failed)}):")
            print("-" * 40)
            for r in failed[:10]:  # Show first 10
                print(f"  {r.test_id}: {r.description}")
                if r.error:
                    print(f"    Error: {r.error}")
            if len(failed) > 10:
                print(f"  ... and {len(failed) - 10} more")

        print()
        print("=" * 60)
        if report.grade in ["A", "B"]:
            print("RESULT: PASS - LLM meets production standards")
        elif report.grade == "C":
            print("RESULT: ACCEPTABLE - Minor improvements recommended")
        else:
            print("RESULT: FAIL - LLM does not meet production standards")

        if report.critical_failures:
            print("\nWARNING: Critical failures detected - NOT production ready")
        print("=" * 60)

    async def run(self, categories: list[str] | None = None) -> EvalReport:
        """Run all evaluations"""
        print("Starting SADNxAI LLM Evaluation...")
        print(f"Provider: {self.provider}")
        print(f"Base URL: {self.base_url}")

        # Run selected evaluations
        if categories is None:
            categories = list(self.WEIGHTS.keys())

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

        # Generate and print report
        report = self.generate_report()
        self.print_report(report)

        # Save report to file
        report_path = self.evals_dir / "reports"
        report_path.mkdir(exist_ok=True)

        report_file = report_path / f"eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, "w") as f:
            json.dump({
                "timestamp": report.timestamp,
                "provider": report.provider,
                "percentage": report.percentage,
                "grade": report.grade,
                "category_scores": report.category_scores,
                "critical_failures": report.critical_failures,
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
                    }
                    for r in report.results
                ],
            }, f, indent=2)

        print(f"\nReport saved to: {report_file}")

        return report


def main():
    parser = argparse.ArgumentParser(description="SADNxAI LLM Evaluation")
    parser.add_argument(
        "--provider",
        choices=["vllm", "claude", "ollama", "mock"],
        default="vllm",
        help="LLM provider to test",
    )
    parser.add_argument(
        "--category",
        choices=["classification", "tool_calling", "saudi_patterns", "reasoning", "regulatory"],
        help="Run only specific category",
    )
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="Base URL for chat-service",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output",
    )

    args = parser.parse_args()

    categories = [args.category] if args.category else None

    evaluator = LLMEvaluator(
        base_url=args.url,
        provider=args.provider,
        verbose=args.verbose,
    )

    report = asyncio.run(evaluator.run(categories))

    # Exit with error code if failed
    if report.grade in ["D", "F"] or report.critical_failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
