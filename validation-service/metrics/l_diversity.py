"""
l-Diversity Metric
A dataset satisfies l-diversity if every equivalence class has
at least l distinct values for the sensitive attribute.
"""

import pandas as pd
from typing import List, Dict


def calculate_l_diversity(
    df: pd.DataFrame,
    quasi_identifiers: List[str],
    sensitive_attributes: List[str]
) -> Dict:
    """
    Calculate l-diversity for a dataset.

    l-diversity ensures that each equivalence class (defined by
    quasi-identifiers) contains at least l distinct values for
    each sensitive attribute.

    Args:
        df: Input dataframe
        quasi_identifiers: List of quasi-identifier column names
        sensitive_attributes: List of sensitive attribute column names

    Returns:
        Dict with:
            - l_value: The achieved l-diversity value (minimum across all)
            - per_attribute: Dict of l-values per sensitive attribute
            - equivalence_classes: Number of distinct equivalence classes
            - diversity_distribution: Distribution of diversity values
    """
    existing_qi = [col for col in quasi_identifiers if col in df.columns]
    existing_sa = [col for col in sensitive_attributes if col in df.columns]

    # Handle edge cases
    if not existing_sa:
        return {
            "l_value": float('inf'),
            "per_attribute": {},
            "equivalence_classes": 0,
            "diversity_distribution": {},
            "message": "No sensitive attributes found"
        }

    if not existing_qi:
        # No quasi-identifiers means entire dataset is one class
        per_attr = {}
        for sa in existing_sa:
            per_attr[sa] = int(df[sa].nunique())
        l_value = min(per_attr.values()) if per_attr else 0
        return {
            "l_value": l_value,
            "per_attribute": per_attr,
            "equivalence_classes": 1,
            "diversity_distribution": {l_value: 1}
        }

    # Calculate l-diversity per attribute
    per_attribute = {}
    all_diversities = []

    for sa in existing_sa:
        # Count distinct sensitive values per equivalence class
        diversity_per_class = df.groupby(existing_qi, dropna=False)[sa].nunique()
        min_diversity = int(diversity_per_class.min()) if len(diversity_per_class) > 0 else 0
        per_attribute[sa] = min_diversity
        all_diversities.extend(diversity_per_class.tolist())

    # Overall l-value is minimum across all attributes
    l_value = min(per_attribute.values()) if per_attribute else 0

    # Calculate distribution
    if all_diversities:
        diversity_series = pd.Series(all_diversities)
        distribution = diversity_series.value_counts().to_dict()
        distribution = {int(k): int(v) for k, v in distribution.items()}
    else:
        distribution = {}

    equivalence_classes = len(df.groupby(existing_qi, dropna=False)) if existing_qi else 1

    return {
        "l_value": l_value,
        "per_attribute": per_attribute,
        "equivalence_classes": equivalence_classes,
        "diversity_distribution": distribution
    }


def get_low_diversity_classes(
    df: pd.DataFrame,
    quasi_identifiers: List[str],
    sensitive_attributes: List[str],
    l_threshold: int
) -> List[Dict]:
    """
    Find equivalence classes with diversity below threshold.

    Args:
        df: Input dataframe
        quasi_identifiers: List of quasi-identifier column names
        sensitive_attributes: List of sensitive attribute column names
        l_threshold: Minimum l value required

    Returns:
        List of dicts describing violating classes
    """
    existing_qi = [col for col in quasi_identifiers if col in df.columns]
    existing_sa = [col for col in sensitive_attributes if col in df.columns]

    if not existing_qi or not existing_sa:
        return []

    violations = []

    for sa in existing_sa:
        grouped = df.groupby(existing_qi, dropna=False)
        for name, group in grouped:
            diversity = group[sa].nunique()
            if diversity < l_threshold:
                violations.append({
                    "quasi_identifier_values": dict(zip(existing_qi, name if isinstance(name, tuple) else [name])),
                    "sensitive_attribute": sa,
                    "diversity": diversity,
                    "record_count": len(group)
                })

    return violations
