"""
k-Anonymity Metric
A dataset satisfies k-anonymity if every record is indistinguishable
from at least k-1 other records with respect to quasi-identifiers.
"""

import pandas as pd
from typing import List, Dict


def calculate_k_anonymity(
    df: pd.DataFrame,
    quasi_identifiers: List[str]
) -> Dict:
    """
    Calculate k-anonymity for a dataset.

    k-anonymity is the minimum size of any equivalence class formed
    by the quasi-identifier columns. An equivalence class is a group
    of records that have identical values for all quasi-identifiers.

    Args:
        df: Input dataframe
        quasi_identifiers: List of quasi-identifier column names

    Returns:
        Dict with:
            - k_value: The achieved k-anonymity value
            - equivalence_classes: Number of distinct equivalence classes
            - smallest_class_size: Size of smallest class (= k_value)
            - largest_class_size: Size of largest class
            - mean_class_size: Average class size
            - class_distribution: Dict of class sizes to counts
    """
    # Filter to existing columns
    existing_qi = [col for col in quasi_identifiers if col in df.columns]

    if not existing_qi:
        # No quasi-identifiers means perfect anonymity
        return {
            "k_value": len(df),
            "equivalence_classes": 1,
            "smallest_class_size": len(df),
            "largest_class_size": len(df),
            "mean_class_size": float(len(df)),
            "class_distribution": {len(df): 1}
        }

    # Group by quasi-identifiers and count
    class_sizes = df.groupby(existing_qi, dropna=False).size()

    if len(class_sizes) == 0:
        return {
            "k_value": 0,
            "equivalence_classes": 0,
            "smallest_class_size": 0,
            "largest_class_size": 0,
            "mean_class_size": 0.0,
            "class_distribution": {}
        }

    # Calculate statistics
    k_value = int(class_sizes.min())
    equivalence_classes = len(class_sizes)
    smallest = int(class_sizes.min())
    largest = int(class_sizes.max())
    mean = float(class_sizes.mean())

    # Distribution of class sizes
    distribution = class_sizes.value_counts().to_dict()
    distribution = {int(k): int(v) for k, v in distribution.items()}

    return {
        "k_value": k_value,
        "equivalence_classes": equivalence_classes,
        "smallest_class_size": smallest,
        "largest_class_size": largest,
        "mean_class_size": round(mean, 2),
        "class_distribution": distribution
    }


def get_violating_records(
    df: pd.DataFrame,
    quasi_identifiers: List[str],
    k_threshold: int
) -> pd.DataFrame:
    """
    Get records that violate k-anonymity threshold.

    Args:
        df: Input dataframe
        quasi_identifiers: List of quasi-identifier column names
        k_threshold: Minimum k value required

    Returns:
        DataFrame containing only records in violating equivalence classes
    """
    existing_qi = [col for col in quasi_identifiers if col in df.columns]

    if not existing_qi:
        return pd.DataFrame()

    # Get class sizes
    class_sizes = df.groupby(existing_qi, dropna=False).size()

    # Find classes smaller than k
    violating_classes = class_sizes[class_sizes < k_threshold].index

    if len(violating_classes) == 0:
        return pd.DataFrame()

    # Filter to violating records
    mask = df.set_index(existing_qi).index.isin(violating_classes)
    return df[mask]
