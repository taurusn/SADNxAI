"""
Date Shifter Engine
Applies random but consistent date offsets to preserve temporal relationships
"""

import pandas as pd
import numpy as np
import hashlib
from datetime import timedelta
from typing import List, Optional


class DateShifter:
    """
    Shifts date columns by a random but consistent offset per record.

    The offset is determined by hashing a combination of the salt and
    row index, ensuring:
    1. Same row always gets same offset (reproducible)
    2. Different rows get different offsets
    3. Temporal relationships within a record are preserved
    """

    def __init__(
        self,
        date_columns: List[str],
        salt: str,
        min_days: int = -365,
        max_days: int = 365,
        preserve_year: bool = False
    ):
        """
        Initialize date shifter.

        Args:
            date_columns: List of date column names to shift
            salt: Secret salt for deterministic offset generation
            min_days: Minimum days to shift (negative = past)
            max_days: Maximum days to shift (positive = future)
            preserve_year: If True, only shift within the same year
        """
        self.date_columns = date_columns
        self.salt = salt
        self.min_days = min_days
        self.max_days = max_days
        self.preserve_year = preserve_year
        self._offset_cache = {}

    def _get_offset_for_row(self, row_index: int) -> int:
        """
        Generate deterministic offset for a row.

        Args:
            row_index: Index of the row

        Returns:
            Number of days to shift (can be negative)
        """
        if row_index in self._offset_cache:
            return self._offset_cache[row_index]

        # Create deterministic hash from salt + row index
        hash_input = f"{self.salt}:{row_index}".encode('utf-8')
        hash_value = hashlib.sha256(hash_input).hexdigest()

        # Convert first 8 hex chars to integer
        hash_int = int(hash_value[:8], 16)

        # Map to offset range
        range_size = self.max_days - self.min_days
        offset = self.min_days + (hash_int % (range_size + 1))

        self._offset_cache[row_index] = offset
        return offset

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply date shifting to specified columns.

        Args:
            df: Input dataframe

        Returns:
            Dataframe with shifted dates
        """
        result = df.copy()

        # Find existing date columns
        existing_columns = [col for col in self.date_columns if col in df.columns]

        if not existing_columns:
            return result

        # Convert columns to datetime if not already
        for col in existing_columns:
            if not pd.api.types.is_datetime64_any_dtype(result[col]):
                result[col] = pd.to_datetime(result[col], errors='coerce')

        # Apply shifts
        for idx in result.index:
            offset_days = self._get_offset_for_row(idx)
            offset = timedelta(days=offset_days)

            for col in existing_columns:
                if pd.notna(result.at[idx, col]):
                    original_date = result.at[idx, col]
                    new_date = original_date + offset

                    # If preserving year, adjust offset to stay within same year
                    if self.preserve_year:
                        if new_date.year != original_date.year:
                            # Shift in opposite direction to stay in year
                            if new_date.year > original_date.year:
                                new_date = original_date - timedelta(days=abs(offset_days))
                            else:
                                new_date = original_date + timedelta(days=abs(offset_days))

                            # If still outside year, just set to mid-year
                            if new_date.year != original_date.year:
                                new_date = original_date

                    result.at[idx, col] = new_date

        return result

    def get_shifted_columns(self, df: pd.DataFrame) -> List[str]:
        """
        Get list of columns that were actually shifted.

        Args:
            df: Input dataframe

        Returns:
            List of column names that exist and will be shifted
        """
        return [col for col in self.date_columns if col in df.columns]
