"""
ANALYZING state prompt - full regulatory context for file analysis.
~1,200 tokens
"""

from .base import (
    BASE_CONTEXT, TOOL_FORMAT, TECHNIQUES_SUMMARY,
    SAUDI_PATTERNS, PRIVACY_METRICS
)

ANALYZING_PROMPT = BASE_CONTEXT + """
## Current State: ANALYZING
A file has been uploaded. Analyze it and call `classify_columns` tool.

""" + TECHNIQUES_SUMMARY + SAUDI_PATTERNS + """

## Classification Categories
| Category | Technique | Examples |
|----------|-----------|----------|
| direct_identifier | SUPPRESS | national_id, name, phone, email, iban |
| quasi_identifier | GENERALIZE | age, city, gender, occupation |
| linkage_identifier | PSEUDONYMIZE | customer_id, account_id, transaction_id |
| date_column | DATE_SHIFT | transaction_date, dob, created_at |
| sensitive_attribute | KEEP | amount, transaction_amount, fraud_flag, score |

## Your Task
1. Count ALL columns in CURRENT FILE section - you must classify every single one
2. Classify each column into one of the 5 categories above
3. Call `classify_columns` tool - EVERY column must appear in exactly one category
4. If unsure about a column, put it in sensitive_attributes (KEEP)
5. Ask user if they approve

""" + PRIVACY_METRICS + """

## Requirements
- Call `classify_columns` tool with all columns from the file
- Include reasoning with regulation citations (PDPL Art.11, Art.15, SAMA 2.6.2, etc.)
- Do NOT just describe - actually call the tool

""" + TOOL_FORMAT
