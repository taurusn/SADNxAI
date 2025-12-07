"""
Pseudonymizer Engine
Applies consistent HMAC-SHA256 hashing to linkage identifiers
"""

import pandas as pd
import hmac
import hashlib
from typing import List, Dict, Optional


class Pseudonymizer:
    """
    Pseudonymizes linkage identifier columns using HMAC-SHA256.

    Linkage identifiers (MRN, patient_id, record_id) need consistent
    replacement so that records can still be linked across tables
    while preventing re-identification.

    Features:
    - Deterministic: Same input always produces same output
    - Secure: HMAC-SHA256 with secret salt prevents rainbow table attacks
    - Configurable: Can use different prefixes per column type
    """

    def __init__(
        self,
        linkage_columns: List[str],
        salt: str,
        hash_length: int = 12,
        prefixes: Optional[Dict[str, str]] = None
    ):
        """
        Initialize pseudonymizer.

        Args:
            linkage_columns: List of linkage identifier column names
            salt: Secret salt for HMAC (must be kept secret)
            hash_length: Length of hash to use (default 12 chars)
            prefixes: Optional dict mapping column names to prefixes
                     e.g., {'mrn': 'MRN-', 'patient_id': 'PID-'}
        """
        self.linkage_columns = linkage_columns
        self.salt = salt.encode('utf-8')
        self.hash_length = hash_length
        self.prefixes = prefixes or {}
        self._cache: Dict[str, str] = {}

    def _pseudonymize_value(self, value: str, column: str) -> str:
        """
        Generate pseudonym for a single value.

        Args:
            value: Original value to pseudonymize
            column: Column name (for prefix lookup)

        Returns:
            Pseudonymized value
        """
        if pd.isna(value) or value == '':
            return value

        # Create cache key
        cache_key = f"{column}:{value}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Generate HMAC-SHA256
        val_str = str(value)
        message = f"{column}:{val_str}".encode('utf-8')
        hash_bytes = hmac.new(self.salt, message, hashlib.sha256).hexdigest()

        # Take first N characters
        hash_short = hash_bytes[:self.hash_length].upper()

        # Add prefix if configured
        prefix = self.prefixes.get(column, '')
        result = f"{prefix}{hash_short}"

        # Cache result
        self._cache[cache_key] = result

        return result

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply pseudonymization to linkage identifier columns.

        Args:
            df: Input dataframe

        Returns:
            Dataframe with pseudonymized linkage identifiers
        """
        result = df.copy()

        # Find existing columns
        existing_columns = [col for col in self.linkage_columns if col in df.columns]

        for col in existing_columns:
            result[col] = df[col].apply(lambda x: self._pseudonymize_value(x, col))

        return result

    def get_pseudonymized_columns(self, df: pd.DataFrame) -> List[str]:
        """
        Get list of columns that were actually pseudonymized.

        Args:
            df: Input dataframe

        Returns:
            List of column names that exist and will be pseudonymized
        """
        return [col for col in self.linkage_columns if col in df.columns]

    def get_mapping(self) -> Dict[str, str]:
        """
        Get the mapping of original values to pseudonyms.

        Returns:
            Dict mapping "column:original" to pseudonym
        """
        return self._cache.copy()

    def clear_cache(self):
        """Clear the pseudonym cache."""
        self._cache.clear()
