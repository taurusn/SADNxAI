"""
Suppressor Engine
Removes direct identifier columns entirely from the dataset
"""

import pandas as pd
from typing import List


class Suppressor:
    """
    Suppresses (removes) direct identifier columns.

    Direct identifiers are columns that can uniquely identify an individual
    on their own, such as national ID, phone number, email, full name.
    """

    def __init__(self, columns_to_suppress: List[str]):
        """
        Initialize suppressor with columns to remove.

        Args:
            columns_to_suppress: List of column names to drop
        """
        self.columns_to_suppress = columns_to_suppress

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove specified columns from the dataframe.

        Args:
            df: Input dataframe

        Returns:
            Dataframe with suppressed columns removed
        """
        # Find which columns actually exist in the dataframe
        existing_columns = [col for col in self.columns_to_suppress if col in df.columns]

        if not existing_columns:
            return df

        # Drop the columns
        result = df.drop(columns=existing_columns)

        return result

    def get_suppressed_columns(self, df: pd.DataFrame) -> List[str]:
        """
        Get list of columns that were actually suppressed.

        Args:
            df: Input dataframe

        Returns:
            List of column names that exist and will be suppressed
        """
        return [col for col in self.columns_to_suppress if col in df.columns]
