"""
t-Closeness Metric
A dataset satisfies t-closeness if the distribution of sensitive
attributes in each equivalence class is within distance t from
the global distribution.
"""

import pandas as pd
import numpy as np
from typing import List, Dict


def earth_movers_distance(p: np.ndarray, q: np.ndarray) -> float:
    """
    Calculate Earth Mover's Distance (EMD) for categorical distributions.

    For categorical data, EMD equals half the L1 distance (total variation).

    Args:
        p: First probability distribution
        q: Second probability distribution

    Returns:
        EMD value between 0 and 1
    """
    return 0.5 * np.sum(np.abs(p - q))


def calculate_t_closeness(
    df: pd.DataFrame,
    quasi_identifiers: List[str],
    sensitive_attributes: List[str]
) -> Dict:
    """
    Calculate t-closeness for a dataset.

    t-closeness measures the maximum distance between the distribution
    of sensitive attribute values in any equivalence class and the
    global distribution.

    Args:
        df: Input dataframe
        quasi_identifiers: List of quasi-identifier column names
        sensitive_attributes: List of sensitive attribute column names

    Returns:
        Dict with:
            - t_value: The achieved t-closeness value (max EMD)
            - per_attribute: Dict of t-values per sensitive attribute
            - equivalence_classes: Number of distinct equivalence classes
            - class_distances: List of EMD values per class
    """
    existing_qi = [col for col in quasi_identifiers if col in df.columns]
    existing_sa = [col for col in sensitive_attributes if col in df.columns]

    # Handle edge cases
    if not existing_sa:
        return {
            "t_value": 0.0,
            "per_attribute": {},
            "equivalence_classes": 0,
            "class_distances": [],
            "message": "No sensitive attributes found"
        }

    if not existing_qi:
        # No quasi-identifiers means entire dataset is one class
        # Distribution equals global distribution, so t=0
        return {
            "t_value": 0.0,
            "per_attribute": {sa: 0.0 for sa in existing_sa},
            "equivalence_classes": 1,
            "class_distances": [0.0]
        }

    per_attribute = {}
    all_distances = []

    for sa in existing_sa:
        # Calculate global distribution
        global_dist = df[sa].value_counts(normalize=True)
        all_values = global_dist.index.tolist()

        # Calculate EMD for each equivalence class
        max_emd = 0.0
        class_emds = []

        grouped = df.groupby(existing_qi, dropna=False)

        for name, group in grouped:
            # Local distribution
            local_dist = group[sa].value_counts(normalize=True)

            # Align distributions (ensure same categories)
            p = np.array([global_dist.get(v, 0) for v in all_values])
            q = np.array([local_dist.get(v, 0) for v in all_values])

            # Calculate EMD
            emd = earth_movers_distance(p, q)
            class_emds.append(emd)
            max_emd = max(max_emd, emd)

        per_attribute[sa] = round(max_emd, 4)
        all_distances.extend(class_emds)

    # Overall t-value is maximum across all attributes
    t_value = max(per_attribute.values()) if per_attribute else 0.0

    equivalence_classes = len(df.groupby(existing_qi, dropna=False)) if existing_qi else 1

    return {
        "t_value": round(t_value, 4),
        "per_attribute": per_attribute,
        "equivalence_classes": equivalence_classes,
        "mean_distance": round(np.mean(all_distances), 4) if all_distances else 0.0,
        "max_distance": round(max(all_distances), 4) if all_distances else 0.0
    }


def get_high_distance_classes(
    df: pd.DataFrame,
    quasi_identifiers: List[str],
    sensitive_attributes: List[str],
    t_threshold: float
) -> List[Dict]:
    """
    Find equivalence classes with EMD above threshold.

    Args:
        df: Input dataframe
        quasi_identifiers: List of quasi-identifier column names
        sensitive_attributes: List of sensitive attribute column names
        t_threshold: Maximum t value allowed

    Returns:
        List of dicts describing violating classes
    """
    existing_qi = [col for col in quasi_identifiers if col in df.columns]
    existing_sa = [col for col in sensitive_attributes if col in df.columns]

    if not existing_qi or not existing_sa:
        return []

    violations = []

    for sa in existing_sa:
        # Global distribution
        global_dist = df[sa].value_counts(normalize=True)
        all_values = global_dist.index.tolist()

        grouped = df.groupby(existing_qi, dropna=False)

        for name, group in grouped:
            local_dist = group[sa].value_counts(normalize=True)

            p = np.array([global_dist.get(v, 0) for v in all_values])
            q = np.array([local_dist.get(v, 0) for v in all_values])

            emd = earth_movers_distance(p, q)

            if emd > t_threshold:
                violations.append({
                    "quasi_identifier_values": dict(zip(existing_qi, name if isinstance(name, tuple) else [name])),
                    "sensitive_attribute": sa,
                    "emd": round(emd, 4),
                    "record_count": len(group)
                })

    return violations
