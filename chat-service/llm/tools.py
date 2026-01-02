"""
Tool Executor
Handles execution of LLM tool calls
"""

import os
import asyncio
from typing import Dict, Any, Callable, Optional

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.models import (
    Session, Classification, GeneralizationConfig,
    MaskingTechnique, RegulationRef, SessionStatus
)


class ToolExecutor:
    """
    Executes tool calls from the LLM.

    Tools:
    - classify_columns: Records column classification
    - execute_pipeline: Triggers masking/validation pipeline
    - update_thresholds: Updates privacy thresholds
    """

    def __init__(self, session: Session, pipeline_callback: Callable = None):
        """
        Initialize tool executor.

        Args:
            session: Current session
            pipeline_callback: Callback function to execute pipeline
        """
        self.session = session
        self.pipeline_callback = pipeline_callback

    async def execute(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool call.

        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments

        Returns:
            Tool result dict
        """
        handlers = {
            "classify_columns": self._handle_classify_columns,
            "execute_pipeline": self._handle_execute_pipeline,
            "update_thresholds": self._handle_update_thresholds,
            "query_regulations": self._handle_query_regulations,
        }

        handler = handlers.get(tool_name)
        if handler is None:
            return {"error": f"Unknown tool: {tool_name}"}

        try:
            result = handler(arguments)
            # If handler returns a coroutine, await it
            if asyncio.iscoroutine(result):
                return await result
            return result
        except Exception as e:
            return {"error": str(e)}

    async def _handle_classify_columns(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle classify_columns tool call.

        Records the AI's classification decision and saves to PostgreSQL.
        Supports incremental merge - LLM can send only missing columns on retry.
        """
        # Merge with existing partial classification if present
        existing = self.session.classification
        if existing:
            print("[Column Validation] Merging with existing partial classification")
            # Merge lists (new columns added to existing)
            for category in ["direct_identifiers", "quasi_identifiers", "linkage_identifiers", "date_columns", "sensitive_attributes"]:
                existing_list = getattr(existing, category, []) or []
                new_list = args.get(category, [])
                # Combine and dedupe while preserving order
                merged = list(existing_list)
                for col in new_list:
                    if col not in merged:
                        merged.append(col)
                args[category] = merged

            # Merge dicts (recommended_techniques, reasoning, regulation_refs)
            for dict_field in ["recommended_techniques", "reasoning", "regulation_refs"]:
                existing_dict = getattr(existing, dict_field, {}) or {}
                # Convert enum values to strings for recommended_techniques
                if dict_field == "recommended_techniques" and existing_dict:
                    existing_dict = {k: v.value if hasattr(v, 'value') else v for k, v in existing_dict.items()}
                new_dict = args.get(dict_field, {})
                merged_dict = {**existing_dict, **new_dict}  # New values override
                args[dict_field] = merged_dict

        # Validate that all classified columns exist in the actual file
        actual_columns = set(self.session.columns or [])
        print(f"[Column Validation] Session columns: {self.session.columns}")
        print(f"[Column Validation] Actual columns set: {actual_columns}")

        all_classified_cols = (
            args.get("direct_identifiers", []) +
            args.get("quasi_identifiers", []) +
            args.get("linkage_identifiers", []) +
            args.get("date_columns", []) +
            args.get("sensitive_attributes", [])
        )
        print(f"[Column Validation] LLM classified (after merge): {all_classified_cols}")

        if actual_columns:
            invalid_cols = [col for col in all_classified_cols if col not in actual_columns]
            print(f"[Column Validation] Invalid columns: {invalid_cols}")
            if invalid_cols:
                return {
                    "success": False,
                    "error": f"Column(s) not found in file: {invalid_cols}. Available columns: {list(actual_columns)}"
                }

            # Check that ALL columns from file are classified
            all_classified_set = set(all_classified_cols)
            unclassified = actual_columns - all_classified_set
            print(f"[Column Validation] Unclassified columns: {unclassified}")
            if unclassified:
                # Save partial classification for next merge attempt
                self._save_partial_classification(args)
                unclassified_list = list(unclassified)
                return {
                    "success": False,
                    "error": f"Columns NOT classified: {unclassified_list}. "
                             f"Look at the Sample Data values for these columns and classify them. "
                             f"If unsure, add them to 'sensitive_attributes' (KEEP). "
                             f"Send ONLY these {len(unclassified_list)} columns - they will merge with your previous classification."
                }
        else:
            print("[Column Validation] WARNING: No columns in session, skipping validation")

        # Build generalization config
        gen_config_args = args.get("generalization_config", {})
        gen_config = GeneralizationConfig(
            age_level=gen_config_args.get("age_level", 1),
            location_level=gen_config_args.get("location_level", 1),
            date_level=gen_config_args.get("date_level", 1)
        )

        # Convert string techniques to enum
        recommended_techniques = {}
        for col, tech in args.get("recommended_techniques", {}).items():
            try:
                recommended_techniques[col] = MaskingTechnique(tech)
            except ValueError:
                recommended_techniques[col] = MaskingTechnique.KEEP

        # Convert regulation_refs to RegulationRef objects
        raw_regulation_refs = args.get("regulation_refs", {})
        regulation_refs = {}
        for col, refs in raw_regulation_refs.items():
            regulation_refs[col] = [
                RegulationRef(
                    regulation_id=ref.get("regulation_id", ""),
                    relevance=ref.get("relevance", "")
                )
                for ref in refs if isinstance(ref, dict)
            ]

        # Normalize reasoning - handle both string and array formats
        reasoning = args.get("reasoning", {})
        for col, val in reasoning.items():
            if isinstance(val, list):
                reasoning[col] = " ".join(str(v) for v in val)
            elif not isinstance(val, str):
                reasoning[col] = str(val)
        args["reasoning"] = reasoning

        # Build classification
        classification = Classification(
            direct_identifiers=args.get("direct_identifiers", []),
            quasi_identifiers=args.get("quasi_identifiers", []),
            linkage_identifiers=args.get("linkage_identifiers", []),
            date_columns=args.get("date_columns", []),
            sensitive_attributes=args.get("sensitive_attributes", []),
            recommended_techniques=recommended_techniques,
            reasoning=args.get("reasoning", {}),
            regulation_refs=regulation_refs,
            generalization_config=gen_config
        )

        # Update session
        self.session.classification = classification

        # Use already extracted values for DB save
        reasoning = args.get("reasoning", {})

        # Build classifications list for PostgreSQL
        # Map classification categories to type IDs
        db_classifications = []
        category_mappings = [
            ("direct_identifiers", "direct_identifier", 0),
            ("quasi_identifiers", "quasi_identifier", gen_config.age_level),  # Use age_level as default
            ("linkage_identifiers", "linkage_identifier", 0),
            ("date_columns", "date_column", gen_config.date_level),
            ("sensitive_attributes", "sensitive_attribute", 0),
        ]

        for category, type_id, default_gen_level in category_mappings:
            columns = args.get(category, [])
            for col in columns:
                # Determine generalization level based on column type
                gen_level = default_gen_level
                if category == "quasi_identifiers":
                    # Check if it's a location column
                    col_lower = col.lower()
                    if any(loc in col_lower for loc in ["city", "region", "province", "location", "address"]):
                        gen_level = gen_config.location_level

                db_classifications.append({
                    "column_name": col,
                    "classification_type_id": type_id,
                    "reasoning": reasoning.get(col, ""),
                    "generalization_level": gen_level,
                    "regulation_refs": raw_regulation_refs.get(col, [])
                })

        # Save to PostgreSQL
        db_save_result = None
        if db_classifications:
            db_save_result = await self._save_classifications_to_db(db_classifications)

        # Count classified columns
        total_classified = (
            len(classification.direct_identifiers) +
            len(classification.quasi_identifiers) +
            len(classification.linkage_identifiers) +
            len(classification.date_columns) +
            len(classification.sensitive_attributes)
        )

        result = {
            "success": True,
            "message": f"Classification recorded for {total_classified} columns",
            "classification": {
                "direct_identifiers": classification.direct_identifiers,
                "quasi_identifiers": classification.quasi_identifiers,
                "linkage_identifiers": classification.linkage_identifiers,
                "date_columns": classification.date_columns,
                "sensitive_attributes": classification.sensitive_attributes
            }
        }

        if db_save_result:
            result["db_saved"] = db_save_result.get("success", False)
            if not db_save_result.get("success"):
                result["db_error"] = db_save_result.get("error")

        return result

    def _save_partial_classification(self, args: Dict[str, Any]) -> None:
        """
        Save partial classification to session for incremental merge on retry.
        This allows the LLM to send only missing columns in subsequent calls.
        """
        gen_config_args = args.get("generalization_config", {})
        gen_config = GeneralizationConfig(
            age_level=gen_config_args.get("age_level", 1),
            location_level=gen_config_args.get("location_level", 1),
            date_level=gen_config_args.get("date_level", 1)
        )

        # Convert string techniques to enum
        recommended_techniques = {}
        for col, tech in args.get("recommended_techniques", {}).items():
            try:
                recommended_techniques[col] = MaskingTechnique(tech)
            except ValueError:
                recommended_techniques[col] = MaskingTechnique.KEEP

        self.session.classification = Classification(
            direct_identifiers=args.get("direct_identifiers", []),
            quasi_identifiers=args.get("quasi_identifiers", []),
            linkage_identifiers=args.get("linkage_identifiers", []),
            date_columns=args.get("date_columns", []),
            sensitive_attributes=args.get("sensitive_attributes", []),
            recommended_techniques=recommended_techniques,
            reasoning=args.get("reasoning", {}),
            regulation_refs={},  # Skip complex conversion for partial save
            generalization_config=gen_config
        )
        print(f"[Column Validation] Saved partial classification with {len(args.get('direct_identifiers', []) + args.get('quasi_identifiers', []) + args.get('linkage_identifiers', []) + args.get('date_columns', []) + args.get('sensitive_attributes', []))} columns")

    async def _save_classifications_to_db(self, classifications: list) -> Dict[str, Any]:
        """Save classifications to PostgreSQL database"""
        from shared.database import Database
        from uuid import UUID

        try:
            job_id = UUID(self.session.id)
            # Ensure job exists
            job = await Database.get_job(job_id)
            if not job:
                await Database.create_job(job_id, self.session.title)

            # Save classifications
            saved = await Database.save_classifications(job_id, classifications)
            return {
                "success": True,
                "saved_count": len(saved)
            }
        except Exception as e:
            print(f"Failed to save classifications to DB: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _handle_execute_pipeline(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle execute_pipeline tool call.

        Triggers the masking and validation pipeline.
        Also applies any threshold updates if provided.
        """
        # If the LLM called this tool, it means confirmation was given
        # Default to True since calling execute_pipeline implies approval
        confirmed = args.get("confirmed", True)

        # Verify session is in approved state before executing pipeline
        allowed_states = [SessionStatus.APPROVED, SessionStatus.PROPOSED, SessionStatus.DISCUSSING]
        if self.session.status not in allowed_states:
            return {
                "success": False,
                "error": f"Pipeline can only run after user approval. Current status: {self.session.status}"
            }

        if self.session.classification is None:
            return {
                "success": False,
                "error": "No classification set. Please classify columns first."
            }

        if self.session.file_path is None:
            return {
                "success": False,
                "error": "No file uploaded. Please upload a CSV file first."
            }

        # Apply any threshold updates that were passed alongside execute_pipeline
        threshold_keys = [
            "k_anonymity_minimum", "k_anonymity_target",
            "l_diversity_minimum", "l_diversity_target",
            "t_closeness_minimum", "t_closeness_target",
            "risk_score_minimum", "risk_score_target"
        ]
        threshold_args = {k: v for k, v in args.items() if k in threshold_keys}
        if threshold_args:
            self._handle_update_thresholds(threshold_args)

        # If callback provided, execute pipeline
        if self.pipeline_callback:
            try:
                result = self.pipeline_callback(self.session)
                return {
                    "success": True,
                    "message": "Pipeline execution started",
                    "result": result
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Pipeline execution failed: {str(e)}"
                }

        return {
            "success": True,
            "message": "Pipeline execution triggered (callback not provided)"
        }

    def _handle_update_thresholds(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle update_thresholds tool call.

        Updates privacy thresholds based on user requirements.
        """
        # Validate threshold ranges
        errors = []
        for key in ["k_anonymity_minimum", "k_anonymity_target"]:
            if key in args and args[key] < 1:
                errors.append(f"{key} must be at least 1")
        for key in ["l_diversity_minimum", "l_diversity_target"]:
            if key in args and args[key] < 1:
                errors.append(f"{key} must be at least 1")
        for key in ["t_closeness_minimum", "t_closeness_target"]:
            if key in args and (args[key] < 0 or args[key] > 1):
                errors.append(f"{key} must be between 0 and 1")
        for key in ["risk_score_minimum", "risk_score_target"]:
            if key in args and (args[key] < 0 or args[key] > 100):
                errors.append(f"{key} must be between 0 and 100")

        if errors:
            return {"success": False, "error": "; ".join(errors)}

        current = self.session.thresholds
        changes = []

        # Update k-anonymity
        if "k_anonymity_minimum" in args:
            current.k_anonymity.minimum = args["k_anonymity_minimum"]
            changes.append(f"k-anonymity minimum: {args['k_anonymity_minimum']}")
        if "k_anonymity_target" in args:
            current.k_anonymity.target = args["k_anonymity_target"]
            changes.append(f"k-anonymity target: {args['k_anonymity_target']}")

        # Update l-diversity
        if "l_diversity_minimum" in args:
            current.l_diversity.minimum = args["l_diversity_minimum"]
            changes.append(f"l-diversity minimum: {args['l_diversity_minimum']}")
        if "l_diversity_target" in args:
            current.l_diversity.target = args["l_diversity_target"]
            changes.append(f"l-diversity target: {args['l_diversity_target']}")

        # Update t-closeness
        if "t_closeness_minimum" in args:
            current.t_closeness.minimum = args["t_closeness_minimum"]
            changes.append(f"t-closeness threshold: {args['t_closeness_minimum']}")
        if "t_closeness_target" in args:
            current.t_closeness.target = args["t_closeness_target"]
            changes.append(f"t-closeness target: {args['t_closeness_target']}")

        # Update risk score
        if "risk_score_minimum" in args:
            current.risk_score.minimum = args["risk_score_minimum"]
            changes.append(f"risk score max: {args['risk_score_minimum']}%")
        if "risk_score_target" in args:
            current.risk_score.target = args["risk_score_target"]
            changes.append(f"risk score target: {args['risk_score_target']}%")

        self.session.thresholds = current

        return {
            "success": True,
            "message": f"Updated thresholds: {', '.join(changes) if changes else 'No changes'}",
            "thresholds": {
                "k_anonymity": {"minimum": current.k_anonymity.minimum, "target": current.k_anonymity.target},
                "l_diversity": {"minimum": current.l_diversity.minimum, "target": current.l_diversity.target},
                "t_closeness": {"minimum": current.t_closeness.minimum, "target": current.t_closeness.target},
                "risk_score": {"minimum": current.risk_score.minimum, "target": current.risk_score.target}
            }
        }

    async def _handle_query_regulations(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle query_regulations tool call.

        Queries the regulation database and returns relevant PDPL/SAMA articles.
        """
        from shared.database import Database

        query_type = args.get("query_type", "")
        value = args.get("value", "")

        # Handle case where LLM passes a list instead of string
        if isinstance(value, list):
            value = ",".join(str(v) for v in value)

        if not query_type or not value:
            return {
                "success": False,
                "error": "Both query_type and value are required"
            }

        try:
            if query_type == "technique":
                results = await Database.query_regulations_by_technique(value)
            elif query_type == "classification_type":
                results = await Database.query_regulations_by_classification_type(value)
            elif query_type == "search":
                results = await Database.search_regulations(value)
            elif query_type == "by_ids":
                ids = [id.strip() for id in value.split(",")]
                results = await Database.query_regulations_by_ids(ids)
            elif query_type == "pattern":
                result = await Database.detect_saudi_pattern(value)
                results = [result] if result else []
            else:
                return {
                    "success": False,
                    "error": f"Unknown query_type: {query_type}. Valid types: technique, classification_type, search, by_ids, pattern"
                }

            return {
                "success": True,
                "query_type": query_type,
                "value": value,
                "regulations": results,
                "count": len(results)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Database query failed: {str(e)}"
            }
