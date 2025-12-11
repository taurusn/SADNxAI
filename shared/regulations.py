"""
SADNxBANK - Saudi Regulatory Mappings
PDPL, SAMA Open Banking, and NDMO compliance references
"""

# ============================================================
# PDPL Article Mappings (Royal Decree M/19, Sept 2021)
# ============================================================

PDPL_ARTICLES = {
    "Article 5": {
        "title": "Consent & Processing",
        "text": "Processing personal data requires data subject consent. Purpose cannot change without consent.",
        "applies_to": ["all_processing", "consent_management"]
    },
    "Article 10": {
        "title": "Data Collection Sources",
        "text": "Direct collection from data subject preferred. Collection from other sources requires consent or legal basis.",
        "applies_to": ["data_collection", "third_party_data"]
    },
    "Article 11": {
        "title": "Data Minimization",
        "text": "Data must be limited to the minimum amount necessary. Controllers must cease collection and destroy data when no longer needed.",
        "applies_to": ["SUPPRESS", "data_retention"]
    },
    "Article 15": {
        "title": "Disclosure Restrictions",
        "text": "Disclosure permitted only with consent, from public sources, for public entity requests, vital interests, in anonymized form, or legitimate interests (excluding sensitive data).",
        "applies_to": ["data_sharing", "anonymization"]
    },
    "Article 17": {
        "title": "Data Correction",
        "text": "Controllers must correct inaccurate data and notify all entities that received it.",
        "applies_to": ["data_accuracy", "GENERALIZE"]
    },
    "Article 18": {
        "title": "Data Destruction",
        "text": "Data must be destroyed without undue delay when no longer necessary for processing purpose.",
        "applies_to": ["SUPPRESS", "data_retention"]
    },
    "Article 19": {
        "title": "Security Measures",
        "text": "Controllers must implement all necessary organizational, administrative, and technical measures to protect personal data during transfer.",
        "applies_to": ["PSEUDONYMIZE", "encryption", "data_transfer"]
    },
    "Article 23": {
        "title": "Health Data",
        "text": "Health data requires additional controls. Access restricted to minimum employees necessary. Processing limited to minimum extent.",
        "applies_to": ["sensitive_data", "health_records"]
    },
    "Article 24": {
        "title": "Credit Data",
        "text": "Credit data requires explicit consent verification. Data subjects must be notified of disclosure requests.",
        "applies_to": ["financial_data", "credit_scoring"]
    },
    "Article 29": {
        "title": "Cross-Border Transfers",
        "text": "Transfers require adequate protection level. Must be limited to minimum amount necessary. No prejudice to national security or vital interests.",
        "applies_to": ["data_transfer", "international"]
    },
    "Article 31": {
        "title": "Records Maintenance",
        "text": "Controllers must maintain processing activity records including purpose, data categories, recipients, and cross-border transfers.",
        "applies_to": ["audit_trail", "compliance"]
    }
}

# ============================================================
# SAMA Open Banking Requirements
# ============================================================

SAMA_REQUIREMENTS = {
    "Section 2.6.1": {
        "title": "Data Collection",
        "text": "Issuer bears responsibility for collecting primary cardholder data regardless of service providers involved.",
        "applies_to": ["data_collection", "accountability"]
    },
    "Section 2.6.2": {
        "title": "Data Storage",
        "text": "Personal information must be secured in Saudi Arabia facilities. Must comply with PCI standards.",
        "applies_to": ["data_residency", "encryption"]
    },
    "Section 2.6.3": {
        "title": "Data Sharing & Consent",
        "text": "Third-party use requires prior written consent except for legal obligations or anonymized data.",
        "applies_to": ["data_sharing", "anonymization", "consent"]
    },
    "Open Banking Framework": {
        "title": "Secure Data Sharing",
        "text": "Enable customers to share financial data securely with licensed third-party providers. Customer consent is mandatory.",
        "applies_to": ["open_banking", "TPP", "consent"]
    },
    "BCT/15631": {
        "title": "Card Regulations",
        "text": "Data protection requirements for payment card operations effective May 2012.",
        "applies_to": ["card_data", "PCI"]
    }
}

# ============================================================
# NDMO Standards
# ============================================================

NDMO_STANDARDS = {
    "Data Classification": {
        "title": "Classification Framework",
        "text": "Data must be classified against defined confidentiality levels. Classification is prerequisite for data sharing.",
        "applies_to": ["classification", "sensitivity_levels"]
    },
    "Personal Data Protection": {
        "title": "Protection Domain",
        "text": "Data controllers must obtain NDMO approval before sharing personal data outside Kingdom.",
        "applies_to": ["cross_border", "approval"]
    },
    "Data Accuracy": {
        "title": "Accuracy Requirements",
        "text": "Controller must ensure personal data is accurate, integral, updated, and used only for collection purpose.",
        "applies_to": ["data_quality", "purpose_limitation"]
    }
}

# ============================================================
# Technique to Regulation Mapping
# ============================================================

TECHNIQUE_REGULATIONS = {
    "SUPPRESS": {
        "justification": "Removal of direct identifiers to prevent individual identification",
        "pdpl_articles": ["Article 11", "Article 15", "Article 18"],
        "sama_sections": ["Section 2.6.3"],
        "rationale": "PDPL Article 11 mandates data minimization - collecting only minimum necessary. Article 15 permits disclosure only in anonymized form. Article 18 requires destruction when no longer needed."
    },
    "GENERALIZE": {
        "justification": "Reducing precision of quasi-identifiers to achieve k-anonymity",
        "pdpl_articles": ["Article 11", "Article 17", "Article 19"],
        "sama_sections": ["Section 2.6.2"],
        "rationale": "PDPL Article 11 requires minimum data necessary. Generalization preserves analytical utility while reducing re-identification risk per Article 19 security measures."
    },
    "PSEUDONYMIZE": {
        "justification": "Replacing identifiers with consistent cryptographic hashes for linkage without identification",
        "pdpl_articles": ["Article 15", "Article 19", "Article 31"],
        "sama_sections": ["Section 2.6.3", "Open Banking Framework"],
        "rationale": "PDPL Article 15 permits processing for legitimate interests with safeguards. Article 19 requires technical measures. SAMA Open Banking requires secure data sharing with TPPs."
    },
    "DATE_SHIFT": {
        "justification": "Applying uniform random offset to dates preserving temporal intervals",
        "pdpl_articles": ["Article 11", "Article 19"],
        "sama_sections": ["Section 2.6.2"],
        "rationale": "Preserves analytical patterns (seasonality, intervals) while preventing identification through date correlation. Meets Article 11 minimization and Article 19 security."
    },
    "KEEP": {
        "justification": "Preserving sensitive attributes for analytical utility",
        "pdpl_articles": ["Article 5", "Article 23", "Article 24"],
        "sama_sections": ["Open Banking Framework"],
        "rationale": "Sensitive attributes (salary, diagnosis, credit score) are preserved as they provide analytical value. Protection achieved through suppression/generalization of identifiers per PDPL Article 5 consent framework."
    }
}

# ============================================================
# Privacy Metrics to Regulation Mapping
# ============================================================

METRIC_REGULATIONS = {
    "k_anonymity": {
        "description": "Each record indistinguishable from at least k-1 others",
        "pdpl_articles": ["Article 15", "Article 19"],
        "rationale": "PDPL Article 15 permits anonymized disclosure. k-anonymity ensures individuals cannot be singled out, meeting Article 19 technical protection requirements.",
        "recommended_minimum": 5,
        "sama_alignment": "Aligns with SAMA data protection principles for preventing individual identification"
    },
    "l_diversity": {
        "description": "Each equivalence class has at least l distinct sensitive values",
        "pdpl_articles": ["Article 23", "Article 24"],
        "rationale": "Prevents attribute disclosure attacks. Critical for health data (Article 23) and credit data (Article 24) where sensitive values must not be inferable.",
        "recommended_minimum": 2,
        "sama_alignment": "Protects sensitive financial attributes from inference"
    },
    "t_closeness": {
        "description": "Distribution of sensitive attributes in each class within t of overall distribution",
        "pdpl_articles": ["Article 11", "Article 19"],
        "rationale": "Prevents statistical inference attacks. Ensures generalization doesn't create skewed distributions revealing sensitive information.",
        "recommended_maximum": 0.2,
        "sama_alignment": "Ensures statistical integrity while maintaining privacy"
    }
}

# ============================================================
# Saudi Data Patterns
# ============================================================

SAUDI_PATTERNS = {
    "national_id": {
        "pattern": r"^1\d{9}$",
        "description": "Saudi National ID (10 digits starting with 1)",
        "classification": "direct_identifier",
        "technique": "SUPPRESS",
        "pdpl_reference": "Article 28 prohibits copying identifying documents except by law"
    },
    "iqama": {
        "pattern": r"^2\d{9}$",
        "description": "Resident ID/Iqama (10 digits starting with 2)",
        "classification": "direct_identifier",
        "technique": "SUPPRESS",
        "pdpl_reference": "Article 28 - identifying document protection"
    },
    "saudi_phone": {
        "pattern": r"^(\+966|00966|966)?0?5\d{8}$",
        "description": "Saudi mobile number (+966 5X XXX XXXX)",
        "classification": "direct_identifier",
        "technique": "SUPPRESS",
        "pdpl_reference": "Article 25 - personal communication means protection"
    },
    "saudi_iban": {
        "pattern": r"^SA\d{22}$",
        "description": "Saudi IBAN (SA + 22 digits)",
        "classification": "direct_identifier",
        "technique": "SUPPRESS",
        "sama_reference": "Section 2.6.2 - payment account protection"
    },
    "card_number": {
        "pattern": r"^\d{16}$",
        "description": "Payment card number (16 digits)",
        "classification": "direct_identifier",
        "technique": "SUPPRESS",
        "sama_reference": "BCT/15631, PCI-DSS compliance required"
    },
    "commercial_registration": {
        "pattern": r"^\d{10}$",
        "description": "Commercial Registration (CR) number",
        "classification": "linkage_identifier",
        "technique": "PSEUDONYMIZE",
        "pdpl_reference": "Article 31 - business entity records"
    },
    "email": {
        "pattern": r"^[\w\.-]+@[\w\.-]+\.\w+$",
        "description": "Email address",
        "classification": "direct_identifier",
        "technique": "SUPPRESS",
        "pdpl_reference": "Article 25 - personal communication protection"
    }
}

# ============================================================
# Banking-Specific Classifications
# ============================================================

BANKING_COLUMN_HINTS = {
    # Direct Identifiers (SUPPRESS)
    "direct_identifiers": [
        "national_id", "iqama", "iqama_number", "id_number", "passport",
        "full_name", "name", "customer_name", "account_holder",
        "phone", "mobile", "telephone", "contact_number",
        "email", "email_address",
        "iban", "account_number", "card_number", "card_pan",
        "address", "street", "postal_code"
    ],
    # Quasi-Identifiers (GENERALIZE)
    "quasi_identifiers": [
        "age", "date_of_birth", "dob", "birth_year",
        "gender", "sex",
        "city", "region", "province", "district", "nationality",
        "occupation", "job_title", "employer", "industry",
        "income_bracket", "salary_range",
        "account_type", "product_type", "segment"
    ],
    # Linkage Identifiers (PSEUDONYMIZE)
    "linkage_identifiers": [
        "customer_id", "client_id", "account_id", "user_id",
        "transaction_id", "reference_number", "merchant_id",
        "branch_id", "employee_id", "cr_number"
    ],
    # Date Columns (DATE_SHIFT)
    "date_columns": [
        "transaction_date", "opening_date", "closing_date",
        "registration_date", "last_activity", "created_at",
        "maturity_date", "due_date", "payment_date"
    ],
    # Sensitive Attributes (KEEP)
    "sensitive_attributes": [
        "transaction_amount", "balance", "credit_limit",
        "credit_score", "risk_rating", "fraud_flag",
        "merchant_category", "transaction_type", "channel",
        "loan_amount", "interest_rate", "tenure"
    ]
}

# ============================================================
# Use Case Templates
# ============================================================

USE_CASE_TEMPLATES = {
    "fraud_detection": {
        "description": "Cross-institution fraud pattern sharing",
        "priority_columns": {
            "pseudonymize": ["customer_id", "account_id", "merchant_id"],
            "keep": ["transaction_amount", "merchant_category", "fraud_flag", "transaction_type"],
            "generalize": ["city", "age"],
            "suppress": ["name", "national_id", "iban", "phone"]
        },
        "rationale": "Pseudonymized IDs enable pattern tracking across institutions without exposing identity. Transaction patterns preserved for ML models.",
        "regulations": ["SAMA Open Banking Framework", "PDPL Article 15", "PDPL Article 19"]
    },
    "open_banking_tpp": {
        "description": "Data sharing with licensed third-party providers",
        "priority_columns": {
            "pseudonymize": ["customer_id", "account_id"],
            "keep": ["transaction_amount", "balance", "merchant_category"],
            "generalize": ["transaction_date", "city"],
            "suppress": ["name", "national_id", "phone", "email", "iban"]
        },
        "rationale": "TPPs need transaction data for services but not PII. SAMA requires customer consent and data minimization.",
        "regulations": ["SAMA Section 2.6.3", "PDPL Article 5", "PDPL Article 11"]
    },
    "ml_model_training": {
        "description": "Training fraud/risk models on historical data",
        "priority_columns": {
            "suppress": ["name", "national_id", "iban", "phone", "email", "address"],
            "pseudonymize": ["customer_id"],
            "keep": ["transaction_amount", "credit_score", "fraud_flag", "risk_rating", "merchant_category"],
            "generalize": ["age", "city", "income_bracket"]
        },
        "rationale": "Models need behavioral patterns not identities. Generalized demographics provide context without re-identification risk.",
        "regulations": ["PDPL Article 11", "PDPL Article 19", "NDMO Data Classification"]
    },
    "regulatory_reporting": {
        "description": "SAMA/central bank compliance reports",
        "priority_columns": {
            "pseudonymize": ["customer_id", "account_id", "transaction_id"],
            "keep": ["transaction_amount", "transaction_type", "currency", "risk_rating"],
            "generalize": ["transaction_date"],
            "suppress": ["name", "phone", "email"]
        },
        "rationale": "Regulators need transaction patterns and risk data. Pseudonymized IDs enable audit trails without exposing customers.",
        "regulations": ["PDPL Article 31", "SAMA BCT/15631"]
    },
    "research_analytics": {
        "description": "Internal analytics or academic research sharing",
        "priority_columns": {
            "suppress": ["name", "national_id", "iban", "phone", "email", "customer_id"],
            "generalize": ["age", "city", "transaction_date", "transaction_amount"],
            "keep": ["merchant_category", "transaction_type", "product_type"]
        },
        "rationale": "Research needs aggregate patterns not individual records. High generalization ensures k-anonymity.",
        "regulations": ["PDPL Article 15", "PDPL Article 29", "NDMO Data Classification"]
    }
}


def get_technique_justification(technique: str) -> dict:
    """Get regulatory justification for a masking technique"""
    return TECHNIQUE_REGULATIONS.get(technique, {})


def get_metric_justification(metric: str) -> dict:
    """Get regulatory justification for a privacy metric"""
    return METRIC_REGULATIONS.get(metric, {})


def get_column_classification_hint(column_name: str) -> tuple:
    """Suggest classification based on column name patterns"""
    col_lower = column_name.lower().replace(" ", "_").replace("-", "_")

    for category, keywords in BANKING_COLUMN_HINTS.items():
        for keyword in keywords:
            if keyword in col_lower or col_lower in keyword:
                technique_map = {
                    "direct_identifiers": "SUPPRESS",
                    "quasi_identifiers": "GENERALIZE",
                    "linkage_identifiers": "PSEUDONYMIZE",
                    "date_columns": "DATE_SHIFT",
                    "sensitive_attributes": "KEEP"
                }
                return category, technique_map.get(category, "KEEP")

    return None, None


def detect_saudi_pattern(value: str) -> dict:
    """Detect if a value matches Saudi-specific patterns"""
    import re
    for pattern_name, pattern_info in SAUDI_PATTERNS.items():
        if re.match(pattern_info["pattern"], str(value)):
            return {
                "pattern": pattern_name,
                "classification": pattern_info["classification"],
                "technique": pattern_info["technique"],
                "reference": pattern_info.get("pdpl_reference") or pattern_info.get("sama_reference")
            }
    return None
