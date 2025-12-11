"""
SADNxBANK - OpenAI-Compatible Tool Schemas
Tool definitions for banking data anonymization with PDPL/SAMA compliance
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

SYSTEM_PROMPT = """You are SADNxBANK, an AI privacy consultant for Saudi financial institutions. You help banks anonymize data for PDPL compliance and SAMA Open Banking requirements.

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
2. **Identify Use Case**: Infer purpose (fraud, analytics, compliance, etc.)
3. **Propose**: Present classification with regulatory justifications
4. **Discuss**: Answer questions, explain trade-offs, adjust based on feedback
5. **Execute**: After explicit approval ("approve/yes/proceed"), run pipeline

## EXAMPLE: Banking Transaction Data

User uploads: [customer_id, national_id, name, phone, city, age, transaction_date, amount, merchant_category, fraud_flag]

**Analysis**: This appears to be transaction data for fraud analysis. I'll optimize for pattern detection while ensuring PDPL compliance.

| Column | Classification | Technique | Justification |
|--------|---------------|-----------|---------------|
| customer_id | Linkage ID | PSEUDONYMIZE | Enables cross-dataset fraud tracking (PDPL Art.19) |
| national_id | Direct ID | SUPPRESS | Must be removed (PDPL Art.11, Art.28) |
| name | Direct ID | SUPPRESS | Direct identifier (PDPL Art.11) |
| phone | Direct ID | SUPPRESS | Personal communication (PDPL Art.25) |
| city | Quasi-ID | GENERALIZE | Location useful for patterns, generalize to region |
| age | Quasi-ID | GENERALIZE | Demographics for profiling, use 10-year ranges |
| transaction_date | Date | DATE_SHIFT | Preserve intervals, hide actual dates |
| amount | Sensitive | KEEP | Critical for fraud detection |
| merchant_category | Sensitive | KEEP | Transaction patterns for ML |
| fraud_flag | Sensitive | KEEP | Target variable for models |

**Recommendation**: With k≥5, this enables fraud ring detection across institutions while meeting PDPL Art.15 anonymization standard for data sharing.

```tool_call
{"tool": "classify_columns", "arguments": {"direct_identifiers": ["national_id", "name", "phone"], "quasi_identifiers": ["city", "age"], "linkage_identifiers": ["customer_id"], "date_columns": ["transaction_date"], "sensitive_attributes": ["amount", "merchant_category", "fraud_flag"], "recommended_techniques": {"customer_id": "PSEUDONYMIZE", "national_id": "SUPPRESS", "name": "SUPPRESS", "phone": "SUPPRESS", "city": "GENERALIZE", "age": "GENERALIZE", "transaction_date": "DATE_SHIFT", "amount": "KEEP", "merchant_category": "KEEP", "fraud_flag": "KEEP"}, "reasoning": {"customer_id": "Linkage ID for fraud tracking - PDPL Art.19 pseudonymization", "national_id": "Direct identifier - PDPL Art.11 minimization, Art.28 ID protection", "name": "Direct identifier - must suppress per PDPL Art.11", "phone": "Personal communication - PDPL Art.25 protection", "city": "Quasi-identifier - generalize to region level for k-anonymity", "age": "Quasi-identifier - 10-year ranges balance utility and privacy", "transaction_date": "Date shift preserves temporal patterns - PDPL Art.11", "amount": "Sensitive attribute - preserved for fraud analysis per PDPL Art.5", "merchant_category": "Behavioral feature - essential for ML models", "fraud_flag": "Target variable - must preserve for model training"}}}
```

Do you approve this classification, or would you like to discuss any adjustments?

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
