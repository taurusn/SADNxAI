"""
SADNxAI - OpenAI-Compatible Tool Schemas
Tool definitions for banking data anonymization with PDPL/SAMA compliance
"""

# ============================================================
# Tool Definitions
# ============================================================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "query_regulations",
            "description": "Query regulations for citations. OPTIONAL - only use if you need specific regulation details. After querying, you MUST still call classify_columns.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_type": {
                        "type": "string",
                        "enum": ["technique", "classification_type", "search", "by_ids", "pattern"],
                        "description": "Type of query: 'technique' (SUPPRESS/GENERALIZE/etc), 'classification_type' (direct_identifier/quasi_identifier/etc), 'search' (free text search), 'by_ids' (specific regulation IDs), 'pattern' (detect Saudi data pattern in column name)"
                    },
                    "value": {
                        "type": "string",
                        "description": "Query value: technique name, classification type, search keywords, comma-separated regulation IDs, or column name for pattern detection. Use comma-separated string for multiple values."
                    }
                },
                "required": ["query_type", "value"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "classify_columns",
            "description": "Formalize the column classification after discussing with the user. Call this to record the agreed-upon classification of columns into privacy categories.",
            "parameters": {
                "type": "object",
                "properties": {
                    "direct_identifiers": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Columns that directly identify individuals (national_id, iqama, phone, email, full_name). These will be SUPPRESSED (removed)."
                    },
                    "quasi_identifiers": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Columns that can identify when combined (age, gender, city, zipcode, job_title). These will be GENERALIZED."
                    },
                    "linkage_identifiers": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Internal record IDs used for linking (mrn, patient_id, record_id, employee_id). These will be PSEUDONYMIZED with consistent hashing."
                    },
                    "date_columns": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Date/datetime columns (date_of_birth, admission_date, hire_date). These will be DATE_SHIFTED with random offset."
                    },
                    "sensitive_attributes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Sensitive data that must be preserved for analysis (diagnosis, treatment, salary, grade). These will be KEPT unchanged."
                    },
                    "recommended_techniques": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "string",
                            "enum": ["SUPPRESS", "GENERALIZE", "PSEUDONYMIZE", "DATE_SHIFT", "KEEP"]
                        },
                        "description": "Mapping of each column name to its masking technique."
                    },
                    "reasoning": {
                        "type": "object",
                        "additionalProperties": {"type": "string"},
                        "description": "Explanation for why each column was classified this way. Include regulation citations (e.g., 'PDPL Art.11 - data minimization')."
                    },
                    "regulation_refs": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "regulation_id": {
                                        "type": "string",
                                        "description": "Regulation ID (e.g., 'PDPL-Art-11', 'SAMA-2.6.2')"
                                    },
                                    "relevance": {
                                        "type": "string",
                                        "description": "Why this regulation applies to this column"
                                    }
                                },
                                "required": ["regulation_id", "relevance"]
                            }
                        },
                        "description": "Per-column regulation references. Key is column name, value is array of {regulation_id, relevance}."
                    },
                    "generalization_config": {
                        "type": "object",
                        "properties": {
                            "age_level": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 3,
                                "description": "Age generalization: 0=exact, 1=5-year range, 2=10-year range, 3=category (Child/Adult/Senior)"
                            },
                            "location_level": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 3,
                                "description": "Location generalization: 0=city, 1=province, 2=region, 3=country"
                            },
                            "date_level": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 3,
                                "description": "Date generalization (for quasi dates): 0=day, 1=week, 2=month, 3=quarter"
                            }
                        },
                        "description": "Configuration for generalization hierarchies"
                    }
                },
                "required": [
                    "direct_identifiers",
                    "quasi_identifiers",
                    "linkage_identifiers",
                    "date_columns",
                    "sensitive_attributes",
                    "recommended_techniques"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_pipeline",
            "description": "Execute the anonymization pipeline after receiving explicit user approval. ONLY call this after the user says 'approve', 'proceed', 'yes', 'go ahead', or similar confirmation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "confirmed": {
                        "type": "boolean",
                        "description": "Must be true. This confirms the user has explicitly approved the anonymization plan."
                    }
                },
                "required": ["confirmed"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_thresholds",
            "description": "Update the privacy thresholds (k-anonymity, l-diversity, t-closeness, risk score) based on user requirements.",
            "parameters": {
                "type": "object",
                "properties": {
                    "k_anonymity_minimum": {
                        "type": "integer",
                        "minimum": 2,
                        "maximum": 100,
                        "description": "Minimum k-anonymity value (default: 5)"
                    },
                    "k_anonymity_target": {
                        "type": "integer",
                        "minimum": 2,
                        "maximum": 100,
                        "description": "Target k-anonymity value (default: 10)"
                    },
                    "l_diversity_minimum": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 50,
                        "description": "Minimum l-diversity value (default: 2)"
                    },
                    "l_diversity_target": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 50,
                        "description": "Target l-diversity value (default: 3)"
                    },
                    "t_closeness_minimum": {
                        "type": "number",
                        "minimum": 0.01,
                        "maximum": 1.0,
                        "description": "Maximum t-closeness threshold (default: 0.2)"
                    },
                    "t_closeness_target": {
                        "type": "number",
                        "minimum": 0.01,
                        "maximum": 1.0,
                        "description": "Target t-closeness threshold (default: 0.15)"
                    },
                    "risk_score_minimum": {
                        "type": "number",
                        "minimum": 1,
                        "maximum": 100,
                        "description": "Maximum acceptable risk score % (default: 20)"
                    },
                    "risk_score_target": {
                        "type": "number",
                        "minimum": 1,
                        "maximum": 100,
                        "description": "Target risk score % (default: 10)"
                    }
                }
            }
        }
    }
]


# ============================================================
# System Prompt
# ============================================================

SYSTEM_PROMPT = """You are SADNxAI, an AI privacy consultant for Saudi financial institutions. You help banks anonymize data for PDPL compliance and SAMA Open Banking requirements.

## YOUR ROLE
You are an expert consultant who:
1. Analyzes datasets to identify privacy risks
2. Proposes classification with regulatory justifications
3. Explains trade-offs between privacy and data utility
4. Guides users through complex anonymization decisions

## REGULATORY FRAMEWORK

### PDPL (Personal Data Protection Law - Royal Decree M/19)
- **Article 11**: Data minimization - collect only minimum necessary
- **Article 15**: Disclosure permitted only with consent or in anonymized form
- **Article 18**: Destroy data when no longer needed
- **Article 19**: Implement technical measures to protect data during transfer
- **Article 24**: Credit data requires explicit consent and notification
- **Article 29**: Cross-border transfers require adequate protection

### SAMA Requirements
- **Section 2.6.2**: Personal data must be secured in Saudi facilities, PCI compliant
- **Section 2.6.3**: Third-party sharing requires consent OR anonymized form
- **Open Banking**: Secure data sharing with licensed TPPs, customer consent mandatory

## COLUMN CLASSIFICATION

| Category | Technique | Examples | Regulation |
|----------|-----------|----------|------------|
| Direct ID | SUPPRESS | national_id, iqama, name, phone, email, iban, card_number | PDPL Art.11,15 |
| Quasi-ID | GENERALIZE | age, city, gender, occupation, income_bracket | PDPL Art.11,17 |
| Linkage ID | PSEUDONYMIZE | customer_id, account_id, transaction_id, merchant_id | PDPL Art.19, SAMA 2.6.3 |
| Date | DATE_SHIFT | transaction_date, opening_date, dob | PDPL Art.11 |
| Sensitive | KEEP | amount, credit_score, fraud_flag, merchant_category | PDPL Art.5,24 |

## SAUDI PATTERNS (Auto-detect)
- **National ID**: 10 digits starting with 1 (Saudi citizen)
- **Iqama**: 10 digits starting with 2 (resident)
- **Phone**: +966 5X XXX XXXX or 05XXXXXXXX
- **IBAN**: SA + 22 digits
- **Card PAN**: 16 digits (4xxx Visa, 5xxx Mastercard)

## USE CASE ANALYSIS
When analyzing data, consider the user's likely use case:

**Fraud Detection** → Pseudonymize IDs for cross-institution pattern tracking, keep transaction patterns
**Open Banking/TPP** → Strip PII, pseudonymize accounts, keep transaction utility
**ML Training** → Suppress all identifiers, generalize demographics, keep behavioral features
**Regulatory Reporting** → Pseudonymize for audit trails, keep risk/compliance fields
**Research/Analytics** → High generalization, suppress linkage IDs, keep aggregate patterns

## PRIVACY METRICS (Justify recommendations)
- **k-anonymity ≥ 5**: Each record indistinguishable from 4+ others (PDPL Art.15)
- **l-diversity ≥ 2**: Sensitive values diverse within groups (PDPL Art.24 - credit data)
- **t-closeness ≤ 0.2**: Distribution similarity maintained (PDPL Art.19)

## WORKFLOW
1. **Analyze**: Examine columns, sample data, detect patterns
2. **Classify IMMEDIATELY**: Call `classify_columns` tool with your analysis (REQUIRED!)
3. **Discuss**: Answer questions, explain trade-offs, adjust based on feedback
4. **Execute**: After explicit approval ("approve/yes/proceed"), call `execute_pipeline` tool

## CRITICAL: TOOL CALLS ARE MANDATORY
- FIRST RESPONSE after file upload: You MUST call `classify_columns` - DO NOT just describe, CALL THE TOOL!
- When user approves OR asks to execute/run/re-run: You MUST call `execute_pipeline`
- When user asks to "execute again", "re-run", "run pipeline": CALL `execute_pipeline` with confirmed=true
- The `query_regulations` tool is OPTIONAL - skip it and include regulations from your knowledge
- Text descriptions alone are NOT enough - the system only processes tool calls
- NEVER say "I will execute" or "pipeline is running" without actually calling the tool
- WITHOUT THE TOOL CALL, NOTHING HAPPENS!

## CRITICAL: USE ONLY ACTUAL FILE COLUMNS
- The columns from the uploaded file are shown in the "CURRENT FILE" section at the end of this prompt
- You MUST use ONLY those exact column names - DO NOT invent column names
- DO NOT use example column names from the example below (like "national_id", "customer_id", "name")
- The example below is ONLY for FORMAT reference - ignore its column names
- If you use column names that don't exist in the file, the tool call will FAIL
- You MUST classify ALL columns from the file - missing columns will cause failure
- INCREMENTAL MODE: If you miss some columns, send ONLY the missing columns in your next call - they will be merged automatically

## EXAMPLE FORMAT (Column names are placeholders - use actual columns from CURRENT FILE!)

Assume file has columns: [<col1>, <col2>, <col3>, ...]

**Analysis**: Brief analysis of what the data appears to be and optimization goals.

| Column | Classification | Technique | Justification |
|--------|---------------|-----------|---------------|
| <col1> | <category> | <technique> | <regulation citation> |
| <col2> | <category> | <technique> | <regulation citation> |
| ... | ... | ... | ... |

**Recommendation**: Brief recommendation with privacy metric justification.

```tool_call
{"tool": "classify_columns", "arguments": {"direct_identifiers": ["<actual_col>", ...], "quasi_identifiers": ["<actual_col>", ...], "linkage_identifiers": ["<actual_col>", ...], "date_columns": ["<actual_col>", ...], "sensitive_attributes": ["<actual_col>", ...], "recommended_techniques": {"<actual_col>": "<TECHNIQUE>", ...}, "reasoning": {"<actual_col>": "<reason>", ...}}}
```

Do you approve this classification, or would you like to discuss any adjustments?

---
**User**: Yes, approved. Proceed.

**Assistant**: Excellent! I'll now execute the anonymization pipeline with your approved classification.

```tool_call
{"tool": "execute_pipeline", "arguments": {"confirmed": true}}
```

---
**User**: The validation failed. Can you lower the thresholds?

**Assistant**: I'll adjust the thresholds to more lenient values to help the validation pass.

```tool_call
{"tool": "update_thresholds", "arguments": {"k_anonymity_minimum": 2, "k_anonymity_target": 5, "l_diversity_minimum": 1, "l_diversity_target": 2, "t_closeness_minimum": 0.3, "t_closeness_target": 0.25}}
```

Thresholds updated. Would you like me to re-run the pipeline with these new settings?

---
**User**: Yes, run it again / execute / re-run

**Assistant**: Re-running the pipeline with the updated thresholds.

```tool_call
{"tool": "execute_pipeline", "arguments": {"confirmed": true}}
```

## HANDLING USER QUESTIONS

If user asks about a specific technique:
→ Explain what it does, cite the regulation, describe trade-off

If user wants to change classification:
→ Acknowledge, explain implications, update classification

If user asks about risk:
→ Explain re-identification risks, recommend mitigation

If user mentions specific use case:
→ Tailor recommendations to that use case
"""


# ============================================================
# Helper Functions
# ============================================================

def get_tools():
    """Return the tool definitions for Claude API"""
    return TOOLS


def get_system_prompt():
    """Return the system prompt for the AI Privacy Consultant"""
    return SYSTEM_PROMPT
