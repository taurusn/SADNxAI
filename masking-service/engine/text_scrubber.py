"""
Text Scrubber Engine
Scrubs PII from free-text fields like clinical notes
"""

import re
import pandas as pd
from typing import List, Set, Optional


class TextScrubber:
    """
    Scrubs personally identifiable information from free-text columns.

    Detects and redacts:
    - Saudi phone numbers (international and local formats)
    - Email addresses
    - Names (extracted from other columns or provided list)
    - Street addresses
    - Insurance/ID numbers
    """

    def __init__(
        self,
        text_columns: List[str],
        names_to_scrub: Optional[Set[str]] = None,
        replacement: str = "[REDACTED]"
    ):
        """
        Initialize text scrubber.

        Args:
            text_columns: List of column names containing free text
            names_to_scrub: Set of names to scrub from text
            replacement: Replacement string for redacted content
        """
        self.text_columns = text_columns
        self.names_to_scrub = names_to_scrub or set()
        self.replacement = replacement

        # Regex patterns for Saudi Arabia context
        self.patterns = {
            # Saudi phone numbers: +966, 00966, 966, 05x, 5x
            'phone': [
                r'\+966\s*\d{8,9}',           # +966XXXXXXXX
                r'00966\s*\d{8,9}',           # 00966XXXXXXXX
                r'009665\d{8}',               # 009665XXXXXXXX
                r'\b966\s*5\d{8}\b',          # 9665XXXXXXXX
                r'\b05\d{8}\b',               # 05XXXXXXXX
                r'\b5\d{8}\b',                # 5XXXXXXXX (mobile)
            ],
            # Email addresses
            'email': [
                r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            ],
            # Saudi National ID (10 digits starting with 1 or 2)
            'national_id': [
                r'\b[12]\d{9}\b',
            ],
            # Insurance IDs (INS followed by numbers)
            'insurance_id': [
                r'\bINS\d{5,10}\b',
            ],
            # Street addresses (common Saudi patterns)
            'address': [
                r'\b\d+\s+(?:Prince\s+)?(?:King\s+)?[A-Z][a-z]+\s+(?:Road|Street|St|Ave|Avenue|District|Blvd)\b',
                r'\bP\.?O\.?\s*Box\s*\d+\b',
            ],
        }

    def _compile_patterns(self) -> List[re.Pattern]:
        """Compile all regex patterns."""
        compiled = []
        for pattern_list in self.patterns.values():
            for pattern in pattern_list:
                compiled.append(re.compile(pattern, re.IGNORECASE))
        return compiled

    def _build_name_pattern(self) -> Optional[re.Pattern]:
        """Build regex pattern for names."""
        if not self.names_to_scrub:
            return None

        # Escape special regex chars and create alternation
        escaped_names = [re.escape(name) for name in self.names_to_scrub if name]
        if not escaped_names:
            return None

        # Match whole words only
        pattern = r'\b(' + '|'.join(escaped_names) + r')\b'
        return re.compile(pattern, re.IGNORECASE)

    def scrub_text(self, text: str) -> str:
        """
        Scrub PII from a single text string.

        Args:
            text: Input text

        Returns:
            Text with PII redacted
        """
        if pd.isna(text) or not isinstance(text, str):
            return text

        result = text

        # Apply all pattern-based scrubbing
        for pattern in self._compile_patterns():
            result = pattern.sub(self.replacement, result)

        # Apply name scrubbing
        name_pattern = self._build_name_pattern()
        if name_pattern:
            result = name_pattern.sub(self.replacement, result)

        return result

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Scrub PII from specified text columns in dataframe.

        Args:
            df: Input dataframe

        Returns:
            Dataframe with scrubbed text columns
        """
        result = df.copy()

        for col in self.text_columns:
            if col in result.columns:
                result[col] = result[col].apply(self.scrub_text)

        return result

    def get_scrubbed_columns(self, df: pd.DataFrame) -> List[str]:
        """
        Get list of columns that will be scrubbed.

        Args:
            df: Input dataframe

        Returns:
            List of column names that exist and will be scrubbed
        """
        return [col for col in self.text_columns if col in df.columns]

    @staticmethod
    def extract_names_from_column(df: pd.DataFrame, name_column: str) -> Set[str]:
        """
        Extract unique names from a name column for scrubbing in other columns.

        Handles full names by splitting into first and last name components.

        Args:
            df: Input dataframe
            name_column: Column containing names

        Returns:
            Set of name components to scrub
        """
        names = set()

        if name_column not in df.columns:
            return names

        for value in df[name_column].dropna().unique():
            if isinstance(value, str):
                # Add full name
                names.add(value.strip())

                # Split and add components (handles "First Last" and "First Al-Last")
                parts = value.split()
                for part in parts:
                    # Skip common prefixes like "Al-"
                    if part and len(part) > 2 and not part.lower().startswith('al-'):
                        names.add(part.strip())
                    elif part.lower().startswith('al-'):
                        names.add(part.strip())

        return names
