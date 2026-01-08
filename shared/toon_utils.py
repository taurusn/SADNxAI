"""
SADNxAI - TOON Encoding Utilities
Token-Oriented Object Notation for efficient LLM prompts

TOON reduces token usage by 55-60% for tabular/structured data
while maintaining LLM comprehension accuracy.
"""

import os
import json
from typing import Any, Dict, List, Optional

# Check if TOON is enabled via environment variable
TOON_ENABLED = os.getenv("TOON_ENABLED", "false").lower() == "true"

# Try to import toons library
try:
    import toons
    TOON_AVAILABLE = True
except ImportError:
    TOON_AVAILABLE = False
    if TOON_ENABLED:
        print("[TOON] Warning: toons library not installed, falling back to JSON")


def encode_data(data: Any, force_json: bool = False) -> str:
    """
    Encode data to TOON format if enabled, otherwise JSON.

    Args:
        data: Data to encode (list, dict, etc.)
        force_json: Force JSON output regardless of TOON setting

    Returns:
        Encoded string (TOON or JSON)
    """
    if force_json or not TOON_ENABLED or not TOON_AVAILABLE:
        return json.dumps(data, ensure_ascii=False, default=str)

    try:
        return toons.dumps(data)
    except Exception as e:
        print(f"[TOON] Encoding failed, falling back to JSON: {e}")
        return json.dumps(data, ensure_ascii=False, default=str)


def decode_data(encoded: str) -> Any:
    """
    Decode data from TOON or JSON format.
    Auto-detects format based on content.

    Args:
        encoded: Encoded string

    Returns:
        Decoded data
    """
    if not encoded:
        return None

    # Try JSON first (most common case)
    try:
        return json.loads(encoded)
    except json.JSONDecodeError:
        pass

    # Try TOON if available
    if TOON_AVAILABLE:
        try:
            return toons.loads(encoded)
        except Exception:
            pass

    # Return as-is if all parsing fails
    return encoded


def format_sample_data_for_prompt(sample_data: List[Dict], max_rows: int = 5) -> str:
    """
    Format sample data for LLM prompt in the most efficient format.

    With TOON enabled:
    ```
    [5,]{id,name,city,age}
    1,Ahmed,Riyadh,35
    2,Sara,Jeddah,28
    ```

    With JSON fallback:
    ```
    [{"id": 1, "name": "Ahmed", ...}, ...]
    ```

    Args:
        sample_data: List of row dictionaries
        max_rows: Maximum rows to include (default: 5)

    Returns:
        Formatted string for prompt
    """
    if not sample_data:
        return "No sample data available"

    # Limit rows and truncate long values
    truncated_data = []
    for row in sample_data[:max_rows]:
        truncated_row = {}
        for key, value in row.items():
            str_val = str(value) if value is not None else ""
            # Truncate long values to 30 chars
            truncated_row[key] = str_val[:30] + "..." if len(str_val) > 30 else str_val
        truncated_data.append(truncated_row)

    return encode_data(truncated_data)


def format_classification_for_prompt(classification: Dict) -> str:
    """
    Format classification context for LLM prompt.

    Args:
        classification: Classification dictionary with categories

    Returns:
        Formatted string for prompt
    """
    if not classification:
        return "No classification available"

    # Create compact representation
    compact = {
        "direct_ids": classification.get("direct_identifiers", []),
        "quasi_ids": classification.get("quasi_identifiers", []),
        "linkage_ids": classification.get("linkage_identifiers", []),
        "dates": classification.get("date_columns", []),
        "sensitive": classification.get("sensitive_attributes", []),
    }

    # Only include techniques if present
    if classification.get("recommended_techniques"):
        compact["techniques"] = classification["recommended_techniques"]

    return encode_data(compact)


def format_validation_for_prompt(validation: Dict) -> str:
    """
    Format validation results for LLM prompt.

    Args:
        validation: Validation result dictionary

    Returns:
        Formatted string for prompt
    """
    if not validation:
        return "No validation results available"

    # Handle both dict formats (direct metrics or nested)
    if isinstance(validation, dict):
        # Check if it's the nested format with 'metrics' key
        if "metrics" in validation:
            metrics = validation["metrics"]
        else:
            metrics = validation

        # Create compact representation
        compact = {}
        for name, data in metrics.items():
            if isinstance(data, dict):
                compact[name] = {
                    "val": data.get("value", "?"),
                    "thresh": data.get("threshold", "?"),
                    "ok": data.get("passed", False)
                }
            else:
                compact[name] = data

        return encode_data(compact)

    return encode_data(validation)


def format_thresholds_for_prompt(thresholds: Dict) -> str:
    """
    Format threshold settings for LLM prompt.

    Args:
        thresholds: Thresholds dictionary

    Returns:
        Formatted string for prompt
    """
    if not thresholds:
        return "Default thresholds"

    return encode_data(thresholds)


def get_format_info() -> str:
    """
    Return information about the current encoding format for system prompt.
    Helps LLM understand the data format being used.

    Returns:
        Format description string or empty string if JSON
    """
    if TOON_ENABLED and TOON_AVAILABLE:
        return (
            "Data is provided in TOON format (Token-Oriented Object Notation) for efficiency. "
            "TOON uses a compact tabular format: header row with column names, "
            "followed by data rows with comma-separated values."
        )
    return ""


def is_toon_enabled() -> bool:
    """Check if TOON encoding is currently enabled and available."""
    return TOON_ENABLED and TOON_AVAILABLE


def get_toon_status() -> Dict[str, Any]:
    """
    Get detailed TOON status for debugging/monitoring.

    Returns:
        Status dictionary with enabled, available, and library info
    """
    status = {
        "enabled": TOON_ENABLED,
        "available": TOON_AVAILABLE,
        "active": TOON_ENABLED and TOON_AVAILABLE,
    }

    if TOON_AVAILABLE:
        try:
            status["version"] = getattr(toons, "__version__", "unknown")
        except Exception:
            status["version"] = "unknown"

    return status
