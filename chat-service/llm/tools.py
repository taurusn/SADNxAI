"""
Tool Executor
Handles execution of LLM tool calls
"""

import os
from typing import Dict, Any, Callable

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.models import (
    Session, Classification, GeneralizationConfig,
    MaskingTechnique
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

    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
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
        }

        handler = handlers.get(tool_name)
        if handler is None:
            return {"error": f"Unknown tool: {tool_name}"}

        try:
            return handler(arguments)
        except Exception as e:
            return {"error": str(e)}

    def _handle_classify_columns(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle classify_columns tool call.

        Records the AI's classification decision.
        """
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

        # Build classification
        classification = Classification(
            direct_identifiers=args.get("direct_identifiers", []),
            quasi_identifiers=args.get("quasi_identifiers", []),
            linkage_identifiers=args.get("linkage_identifiers", []),
            date_columns=args.get("date_columns", []),
            sensitive_attributes=args.get("sensitive_attributes", []),
            recommended_techniques=recommended_techniques,
            reasoning=args.get("reasoning", {}),
            generalization_config=gen_config
        )

        # Update session
        self.session.classification = classification

        # Count classified columns
        total_classified = (
            len(classification.direct_identifiers) +
            len(classification.quasi_identifiers) +
            len(classification.linkage_identifiers) +
            len(classification.date_columns) +
            len(classification.sensitive_attributes)
        )

        return {
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

    def _handle_execute_pipeline(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle execute_pipeline tool call.

        Triggers the masking and validation pipeline.
        Also applies any threshold updates if provided.
        """
        confirmed = args.get("confirmed", False)

        if not confirmed:
            return {
                "success": False,
                "error": "Pipeline execution not confirmed. User must explicitly approve."
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
