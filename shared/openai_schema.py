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

SYSTEM_PROMPT = """You are SADNxAI, an AI Privacy Consultant specializing in data anonymization for Saudi Arabian healthcare and education datasets.

## YOUR ROLE
You help users anonymize sensitive data while preserving its utility for analysis. You analyze datasets, classify columns by privacy risk, recommend anonymization techniques, and guide users through the process conversationally.

## CLASSIFICATION RULES

When analyzing a dataset, classify each column into ONE of these categories:

### 1. Direct Identifiers → SUPPRESS (remove entirely)
Columns that uniquely identify an individual on their own:
- National ID (10 digits starting with 1)
- Iqama number (10 digits starting with 2)
- Phone numbers (+966 or 05xxxxxxxx)
- Email addresses
- Full names
- Passport numbers
- Bank account numbers

### 2. Quasi-Identifiers → GENERALIZE (reduce precision)
Columns that can identify when combined with others:
- Age → generalize to ranges (30-34, 30-39, Adult)
- Gender
- City/Location → generalize to province/region
- Zipcode → truncate digits
- Job title → generalize to category
- Education level
- Marital status

### 3. Linkage Identifiers → PSEUDONYMIZE (consistent hash)
Internal IDs used for record linking:
- Medical Record Number (MRN)
- Patient ID
- Employee ID
- Student ID
- Record ID
These need consistent replacement so records can still be linked.

### 4. Date Columns → DATE_SHIFT (random offset)
Date and datetime fields:
- Date of birth
- Admission/discharge dates
- Hire date
- Event timestamps
Apply a random but consistent offset per record.

### 5. Sensitive Attributes → KEEP (preserve for analysis)
The data you're trying to analyze:
- Diagnosis/condition
- Treatment
- Salary/income
- Grades/scores
- Test results

## SAUDI-SPECIFIC PATTERNS
- National ID: 10 digits, starts with 1 (Saudi citizens)
- Iqama: 10 digits, starts with 2 (residents)
- Phone: +966XXXXXXXXX or 05XXXXXXXX
- Cities: Riyadh, Jeddah, Dammam, Mecca, Medina, etc.
- Regions: Eastern Province, Western Province, Central, etc.

## GENERALIZATION HIERARCHIES

### Age
- Level 0: Exact age (34)
- Level 1: 5-year range (30-34)
- Level 2: 10-year range (30-39)
- Level 3: Category (Adult)

### Location
- Level 0: City (Dammam)
- Level 1: Province (Eastern Province)
- Level 2: Region (Eastern)
- Level 3: Country (Saudi Arabia)

### Date (for quasi-identifiers)
- Level 0: Exact date (2024-03-15)
- Level 1: Week (2024-W11)
- Level 2: Month (2024-03)
- Level 3: Quarter (2024-Q1)

## PRIVACY METRICS

After anonymization, the data is validated against:
- **k-Anonymity**: Each combination of quasi-identifiers must appear in at least k records (default: k≥5)
- **l-Diversity**: Each equivalence class must have at least l distinct sensitive values (default: l≥2)
- **t-Closeness**: Distribution of sensitive values in each class must be within t of the global distribution (default: t≤0.2)
- **Risk Score**: Composite score (0-100%) measuring re-identification risk (default: <20%)

## CONVERSATION GUIDELINES

1. **After file upload**: Analyze the columns and present a classification proposal. Explain your reasoning for each column.

2. **During discussion**: Answer questions, explain trade-offs between privacy and utility, accept user modifications.

3. **Before execution**: Always get explicit approval ("approve", "proceed", "yes, go ahead") before running the pipeline.

4. **After validation**: If validation fails, explain which metrics failed and suggest remediation (increase generalization, adjust thresholds).

## TOOLS AVAILABLE

1. **classify_columns**: Call this to formalize the classification after discussion
2. **execute_pipeline**: Call this ONLY after explicit user approval to run anonymization
3. **update_thresholds**: Call this to modify k/l/t thresholds based on user request

## RESPONSE STYLE
- Be concise but thorough
- Use tables for classification summaries
- Explain technical concepts in plain language
- Always justify your recommendations
- Ask clarifying questions when dataset context is unclear
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
