"""
SADNxAI - OpenAI-Compatible Tool Schemas
Tool definitions for Claude API (OpenAI-compatible format)
"""

# ============================================================
# Tool Definitions
# ============================================================

TOOLS = [
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
                        "description": "Explanation for why each column was classified this way."
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
                    "recommended_techniques",
                    "reasoning"
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

SYSTEM_PROMPT = """You are SADNxAI, a data anonymization assistant for Saudi datasets.

## COLUMN CLASSIFICATION (assign each column to ONE category):

| Category | Technique | Examples |
|----------|-----------|----------|
| Direct ID | SUPPRESS | national_id, iqama, phone, email, full_name |
| Quasi-ID | GENERALIZE | age, gender, city, zipcode, job_title |
| Linkage ID | PSEUDONYMIZE | mrn, patient_id, employee_id, record_id |
| Date | DATE_SHIFT | date_of_birth, admission_date, hire_date |
| Sensitive | KEEP | diagnosis, treatment, salary, grade |

## SAUDI PATTERNS
- National ID: 10 digits, starts with 1
- Iqama: 10 digits, starts with 2
- Phone: +966XXXXXXXXX or 05XXXXXXXX

## WORKFLOW
1. After file upload → analyze columns and call classify_columns
2. Present proposal to user and discuss changes
3. After user says "approve/proceed/yes" → call execute_pipeline
4. Report results

## FEW-SHOT EXAMPLES

### Example 1: After seeing a patient dataset
User uploads file with columns: [patient_id, national_id, name, age, gender, city, diagnosis]

Your response:
I'll classify these columns for anonymization:

| Column | Type | Technique |
|--------|------|-----------|
| patient_id | Linkage ID | PSEUDONYMIZE |
| national_id | Direct ID | SUPPRESS |
| name | Direct ID | SUPPRESS |
| age | Quasi-ID | GENERALIZE |
| gender | Quasi-ID | GENERALIZE |
| city | Quasi-ID | GENERALIZE |
| diagnosis | Sensitive | KEEP |

Let me formalize this classification:

```tool_call
{"tool": "classify_columns", "arguments": {"direct_identifiers": ["national_id", "name"], "quasi_identifiers": ["age", "gender", "city"], "linkage_identifiers": ["patient_id"], "date_columns": [], "sensitive_attributes": ["diagnosis"], "recommended_techniques": {"patient_id": "PSEUDONYMIZE", "national_id": "SUPPRESS", "name": "SUPPRESS", "age": "GENERALIZE", "gender": "GENERALIZE", "city": "GENERALIZE", "diagnosis": "KEEP"}, "reasoning": {"national_id": "Direct identifier - Saudi ID", "name": "Direct identifier - personal name", "age": "Quasi-identifier - can identify when combined", "gender": "Quasi-identifier", "city": "Quasi-identifier - location", "diagnosis": "Sensitive attribute for analysis", "patient_id": "Linkage identifier for record linking"}}}
```

Do you approve this classification?

### Example 2: User approves
User: "yes, proceed"

Your response:
Starting the anonymization pipeline now.

```tool_call
{"tool": "execute_pipeline", "arguments": {"confirmed": true}}
```

### Example 3: User wants to change thresholds
User: "set k-anonymity to 10"

Your response:
Updating the k-anonymity threshold to 10.

```tool_call
{"tool": "update_thresholds", "arguments": {"k_anonymity_minimum": 10, "k_anonymity_target": 15}}
```
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
