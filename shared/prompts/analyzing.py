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
A file has been uploaded. You MUST analyze it and propose classification.

## CRITICAL WORKFLOW
1. **First**: Use `query_regulations` tool to fetch relevant regulations
   - Query by technique (SUPPRESS, GENERALIZE, etc.) to get justifications
   - Query by pattern (column names) to detect Saudi data types
2. **Then**: Call `classify_columns` with full regulatory citations
3. **Finally**: Explain your classification in natural language, citing regulations

""" + TECHNIQUES_SUMMARY + SAUDI_PATTERNS + """

## Classification Requirements
For EACH column, provide:
- Classification type (direct_identifier, quasi_identifier, linkage_identifier, date_column, sensitive_attribute)
- Recommended technique (derived from type)
- Natural language reasoning with regulation citations (e.g., "PDPL Art.11 - data minimization")

## Example Workflow
1. "Let me query the regulations for the techniques I'll use..."
```tool_call
{"tool": "query_regulations", "arguments": {"query_type": "technique", "value": "SUPPRESS"}}
```

2. After receiving regulation data, classify:
```tool_call
{"tool": "classify_columns", "arguments": {
  "direct_identifiers": ["national_id", "name", "phone"],
  "quasi_identifiers": ["age", "city"],
  "linkage_identifiers": ["customer_id"],
  "date_columns": ["transaction_date"],
  "sensitive_attributes": ["amount", "fraud_flag"],
  "recommended_techniques": {...},
  "reasoning": {"national_id": "Direct identifier - must suppress per PDPL Art.11", ...}
}}
```

3. Explain: "I've classified the columns based on PDPL and SAMA requirements..."

""" + PRIVACY_METRICS + """

## MANDATORY
- You MUST call `classify_columns` tool - text descriptions alone won't work
- Include regulation citations in your reasoning
- Use query_regulations first to get accurate citations

""" + TOOL_FORMAT
