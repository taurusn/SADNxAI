"""
Generalizer Engine
Applies generalization hierarchies to quasi-identifiers
"""

import pandas as pd
import re
from typing import List, Dict, Optional, Any


# Saudi Arabia location hierarchies
SAUDI_CITIES_TO_PROVINCE = {
    # Eastern Province
    "dammam": "Eastern Province",
    "dhahran": "Eastern Province",
    "khobar": "Eastern Province",
    "al khobar": "Eastern Province",
    "jubail": "Eastern Province",
    "qatif": "Eastern Province",
    "hofuf": "Eastern Province",
    "al hofuf": "Eastern Province",
    "al ahsa": "Eastern Province",
    "ras tanura": "Eastern Province",

    # Riyadh Province
    "riyadh": "Riyadh Province",
    "diriyah": "Riyadh Province",
    "kharj": "Riyadh Province",
    "al kharj": "Riyadh Province",
    "majmaah": "Riyadh Province",

    # Makkah Province
    "mecca": "Makkah Province",
    "makkah": "Makkah Province",
    "jeddah": "Makkah Province",
    "taif": "Makkah Province",
    "rabigh": "Makkah Province",

    # Madinah Province
    "medina": "Madinah Province",
    "madinah": "Madinah Province",
    "yanbu": "Madinah Province",

    # Qassim Province
    "buraidah": "Qassim Province",
    "unaizah": "Qassim Province",

    # Asir Province
    "abha": "Asir Province",
    "khamis mushait": "Asir Province",

    # Tabuk Province
    "tabuk": "Tabuk Province",

    # Hail Province
    "hail": "Hail Province",

    # Northern Borders
    "arar": "Northern Borders Province",

    # Jazan Province
    "jazan": "Jazan Province",
    "jizan": "Jazan Province",

    # Najran Province
    "najran": "Najran Province",

    # Al Bahah Province
    "al bahah": "Al Bahah Province",
    "bahah": "Al Bahah Province",

    # Al Jawf Province
    "sakakah": "Al Jawf Province",
}

PROVINCE_TO_REGION = {
    "Eastern Province": "Eastern",
    "Riyadh Province": "Central",
    "Makkah Province": "Western",
    "Madinah Province": "Western",
    "Qassim Province": "Central",
    "Asir Province": "Southern",
    "Tabuk Province": "Northern",
    "Hail Province": "Northern",
    "Northern Borders Province": "Northern",
    "Jazan Province": "Southern",
    "Najran Province": "Southern",
    "Al Bahah Province": "Southern",
    "Al Jawf Province": "Northern",
}


class Generalizer:
    """
    Generalizes quasi-identifier columns using hierarchies.

    Supports:
    - Age: exact → 5yr range → 10yr range → category
    - Location: city → province → region → country
    - Date: exact → week → month → quarter
    - Generic: value → first N chars → category
    """

    def __init__(
        self,
        quasi_identifiers: List[str],
        age_level: int = 1,
        location_level: int = 1,
        date_level: int = 1,
        column_types: Optional[Dict[str, str]] = None
    ):
        """
        Initialize generalizer.

        Args:
            quasi_identifiers: List of quasi-identifier column names
            age_level: Generalization level for age (0-3)
            location_level: Generalization level for location (0-3)
            date_level: Generalization level for dates (0-3)
            column_types: Optional dict mapping column names to types
                         ('age', 'location', 'date', 'gender', 'zipcode', 'generic')
        """
        self.quasi_identifiers = quasi_identifiers
        self.age_level = age_level
        self.location_level = location_level
        self.date_level = date_level
        self.column_types = column_types or {}

    def _detect_column_type(self, col_name: str, sample_values: pd.Series) -> str:
        """
        Auto-detect column type based on name and values.

        Args:
            col_name: Column name
            sample_values: Sample of column values

        Returns:
            Detected type: 'age', 'location', 'date', 'gender', 'zipcode', 'generic'
        """
        col_lower = col_name.lower()

        # Check by column name patterns
        if any(x in col_lower for x in ['age', 'عمر']):
            return 'age'
        if any(x in col_lower for x in ['city', 'location', 'address', 'مدينة', 'province', 'region']):
            return 'location'
        if any(x in col_lower for x in ['gender', 'sex', 'جنس']):
            return 'gender'
        if any(x in col_lower for x in ['zip', 'postal', 'رمز']):
            return 'zipcode'
        if any(x in col_lower for x in ['date', 'تاريخ']) and not pd.api.types.is_datetime64_any_dtype(sample_values):
            return 'date'

        # Check by value patterns
        non_null = sample_values.dropna()
        if len(non_null) > 0:
            # Check if numeric (potential age)
            if pd.api.types.is_numeric_dtype(non_null):
                if non_null.min() >= 0 and non_null.max() <= 120:
                    return 'age'

            # Check if looks like city names
            sample_str = str(non_null.iloc[0]).lower() if len(non_null) > 0 else ""
            if sample_str in SAUDI_CITIES_TO_PROVINCE:
                return 'location'

        return 'generic'

    def _generalize_age(self, age: Any, level: int) -> str:
        """
        Generalize age value.

        Level 0: 34
        Level 1: 30-34 (5-year range)
        Level 2: 30-39 (10-year range)
        Level 3: Adult/Child/Senior
        """
        if pd.isna(age):
            return None

        try:
            age_int = int(float(age))
        except (ValueError, TypeError):
            return str(age)

        if level == 0:
            return str(age_int)
        elif level == 1:
            # 5-year range
            lower = (age_int // 5) * 5
            upper = lower + 4
            return f"{lower}-{upper}"
        elif level == 2:
            # 10-year range
            lower = (age_int // 10) * 10
            upper = lower + 9
            return f"{lower}-{upper}"
        else:
            # Category
            if age_int < 18:
                return "Child"
            elif age_int < 65:
                return "Adult"
            else:
                return "Senior"

    def _generalize_location(self, location: Any, level: int) -> str:
        """
        Generalize location value.

        Level 0: Dammam (city)
        Level 1: Eastern Province
        Level 2: Eastern (region)
        Level 3: Saudi Arabia
        """
        if pd.isna(location):
            return None

        loc_str = str(location).strip().lower()

        if level == 0:
            return str(location)
        elif level == 1:
            # City to Province
            return SAUDI_CITIES_TO_PROVINCE.get(loc_str, str(location))
        elif level == 2:
            # City to Region
            province = SAUDI_CITIES_TO_PROVINCE.get(loc_str, None)
            if province:
                return PROVINCE_TO_REGION.get(province, province)
            # Maybe it's already a province
            return PROVINCE_TO_REGION.get(str(location), str(location))
        else:
            # Country level
            return "Saudi Arabia"

    def _generalize_date(self, date_val: Any, level: int) -> str:
        """
        Generalize date value.

        Level 0: 2024-03-15
        Level 1: 2024-W11 (week)
        Level 2: 2024-03 (month)
        Level 3: 2024-Q1 (quarter)
        """
        if pd.isna(date_val):
            return None

        try:
            if isinstance(date_val, str):
                dt = pd.to_datetime(date_val)
            else:
                dt = pd.Timestamp(date_val)
        except Exception:
            return str(date_val)

        if level == 0:
            return dt.strftime('%Y-%m-%d')
        elif level == 1:
            # ISO week
            return f"{dt.year}-W{dt.isocalendar()[1]:02d}"
        elif level == 2:
            # Month
            return dt.strftime('%Y-%m')
        else:
            # Quarter
            quarter = (dt.month - 1) // 3 + 1
            return f"{dt.year}-Q{quarter}"

    def _generalize_zipcode(self, zipcode: Any, level: int) -> str:
        """
        Generalize zipcode by truncating digits.

        Level 0: 12345
        Level 1: 1234*
        Level 2: 123**
        Level 3: 12***
        """
        if pd.isna(zipcode):
            return None

        zip_str = str(zipcode).strip()
        # Remove non-digits
        digits = re.sub(r'\D', '', zip_str)

        if level == 0:
            return zip_str
        elif level == 1 and len(digits) > 1:
            return digits[:-1] + '*'
        elif level == 2 and len(digits) > 2:
            return digits[:-2] + '**'
        else:
            return digits[:2] + '*' * max(0, len(digits) - 2)

    def _generalize_gender(self, gender: Any, level: int) -> str:
        """
        Generalize gender.

        Level 0-2: Keep original (M/F or Male/Female)
        Level 3: * (suppress)
        """
        if pd.isna(gender):
            return None

        if level >= 3:
            return "*"
        return str(gender)

    def _generalize_generic(self, value: Any, level: int) -> str:
        """
        Generic generalization by truncation.

        Level 0: Full value
        Level 1: First 75% of chars
        Level 2: First 50% of chars
        Level 3: First char + *
        """
        if pd.isna(value):
            return None

        val_str = str(value)

        if level == 0:
            return val_str
        elif level == 1:
            keep = max(1, int(len(val_str) * 0.75))
            return val_str[:keep] + '*' * (len(val_str) - keep)
        elif level == 2:
            keep = max(1, int(len(val_str) * 0.5))
            return val_str[:keep] + '*' * (len(val_str) - keep)
        else:
            return val_str[0] + '*' * max(0, len(val_str) - 1) if val_str else '*'

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply generalization to quasi-identifier columns.

        Args:
            df: Input dataframe

        Returns:
            Dataframe with generalized quasi-identifiers
        """
        result = df.copy()

        # Find existing columns
        existing_columns = [col for col in self.quasi_identifiers if col in df.columns]

        for col in existing_columns:
            # Determine column type
            col_type = self.column_types.get(col) or self._detect_column_type(col, df[col])

            # Apply appropriate generalization
            if col_type == 'age':
                result[col] = df[col].apply(lambda x: self._generalize_age(x, self.age_level))
            elif col_type == 'location':
                result[col] = df[col].apply(lambda x: self._generalize_location(x, self.location_level))
            elif col_type == 'date':
                result[col] = df[col].apply(lambda x: self._generalize_date(x, self.date_level))
            elif col_type == 'zipcode':
                result[col] = df[col].apply(lambda x: self._generalize_zipcode(x, self.location_level))
            elif col_type == 'gender':
                result[col] = df[col].apply(lambda x: self._generalize_gender(x, self.location_level))
            else:
                result[col] = df[col].apply(lambda x: self._generalize_generic(x, self.location_level))

        return result

    def get_generalized_columns(self, df: pd.DataFrame) -> List[str]:
        """
        Get list of columns that were actually generalized.

        Args:
            df: Input dataframe

        Returns:
            List of column names that exist and will be generalized
        """
        return [col for col in self.quasi_identifiers if col in df.columns]
