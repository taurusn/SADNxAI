# LLM Evaluation Criteria for SADNxAI

## Overview

This document defines the evaluation criteria for assessing the LLM's performance in the SADNxAI data anonymization platform. The LLM acts as a privacy consultant, classifying data columns and guiding users through the anonymization process.

---

## 1. Column Classification Accuracy (40% weight)

### 1.1 Direct Identifiers (SUPPRESS)

**Definition**: Data that directly identifies an individual and must be completely removed.

| Test Case | Column Name | Sample Data | Expected Classification | Technique |
|-----------|-------------|-------------|------------------------|-----------|
| DI-001 | national_id | 1098765432 | direct_identifiers | SUPPRESS |
| DI-002 | iqama_number | 2123456789 | direct_identifiers | SUPPRESS |
| DI-003 | full_name | "Ahmed Al-Rashid" | direct_identifiers | SUPPRESS |
| DI-004 | phone_number | +966512345678 | direct_identifiers | SUPPRESS |
| DI-005 | mobile | 0551234567 | direct_identifiers | SUPPRESS |
| DI-006 | email | user@example.com | direct_identifiers | SUPPRESS |
| DI-007 | iban | SA0380000000608010167519 | direct_identifiers | SUPPRESS |
| DI-008 | card_number | 4111111111111111 | direct_identifiers | SUPPRESS |
| DI-009 | passport_no | A12345678 | direct_identifiers | SUPPRESS |
| DI-010 | address | "123 King Fahd Rd, Riyadh" | direct_identifiers | SUPPRESS |

**Scoring**:
- Correct classification: 1 point
- Wrong classification: 0 points
- Missing classification: 0 points

### 1.2 Quasi-Identifiers (GENERALIZE)

**Definition**: Data that can identify individuals when combined with other data.

| Test Case | Column Name | Sample Data | Expected Classification | Technique |
|-----------|-------------|-------------|------------------------|-----------|
| QI-001 | age | 35 | quasi_identifiers | GENERALIZE |
| QI-002 | birth_year | 1989 | quasi_identifiers | GENERALIZE |
| QI-003 | city | "Riyadh" | quasi_identifiers | GENERALIZE |
| QI-004 | region | "Central" | quasi_identifiers | GENERALIZE |
| QI-005 | gender | "M" | quasi_identifiers | GENERALIZE |
| QI-006 | occupation | "Engineer" | quasi_identifiers | GENERALIZE |
| QI-007 | employer_type | "Private" | quasi_identifiers | GENERALIZE |
| QI-008 | zip_code | 12345 | quasi_identifiers | GENERALIZE |
| QI-009 | marital_status | "Married" | quasi_identifiers | GENERALIZE |
| QI-010 | education_level | "Bachelor" | quasi_identifiers | GENERALIZE |

**Scoring**: Same as above

### 1.3 Linkage Identifiers (PSEUDONYMIZE)

**Definition**: IDs used for record linkage that should be hashed, not removed.

| Test Case | Column Name | Sample Data | Expected Classification | Technique |
|-----------|-------------|-------------|------------------------|-----------|
| LI-001 | customer_id | "CUST-12345" | linkage_identifiers | PSEUDONYMIZE |
| LI-002 | account_id | "ACC-98765" | linkage_identifiers | PSEUDONYMIZE |
| LI-003 | patient_id | "PAT-54321" | linkage_identifiers | PSEUDONYMIZE |
| LI-004 | member_id | "MEM-11111" | linkage_identifiers | PSEUDONYMIZE |
| LI-005 | transaction_id | "TXN-99999" | linkage_identifiers | PSEUDONYMIZE |
| LI-006 | loan_id | "LOAN-77777" | linkage_identifiers | PSEUDONYMIZE |
| LI-007 | policy_id | "POL-88888" | linkage_identifiers | PSEUDONYMIZE |
| LI-008 | case_id | "CASE-66666" | linkage_identifiers | PSEUDONYMIZE |
| LI-009 | user_id | "USR-44444" | linkage_identifiers | PSEUDONYMIZE |
| LI-010 | employee_id | "EMP-33333" | linkage_identifiers | PSEUDONYMIZE |

### 1.4 Date Columns (DATE_SHIFT)

**Definition**: Date/time fields that should be shifted to preserve temporal relationships.

| Test Case | Column Name | Sample Data | Expected Classification | Technique |
|-----------|-------------|-------------|------------------------|-----------|
| DC-001 | transaction_date | "2024-01-15" | date_columns | DATE_SHIFT |
| DC-002 | birth_date | "1989-05-20" | date_columns | DATE_SHIFT |
| DC-003 | created_at | "2024-01-01T10:30:00" | date_columns | DATE_SHIFT |
| DC-004 | admission_date | "2024-02-10" | date_columns | DATE_SHIFT |
| DC-005 | discharge_date | "2024-02-15" | date_columns | DATE_SHIFT |
| DC-006 | account_open_date | "2020-06-01" | date_columns | DATE_SHIFT |
| DC-007 | last_login | "2024-01-20T14:22:00" | date_columns | DATE_SHIFT |
| DC-008 | registration_date | "2023-03-15" | date_columns | DATE_SHIFT |

### 1.5 Sensitive Attributes (KEEP)

**Definition**: Data needed for analysis that should be preserved unchanged.

| Test Case | Column Name | Sample Data | Expected Classification | Technique |
|-----------|-------------|-------------|------------------------|-----------|
| SA-001 | transaction_amount | 5000.00 | sensitive_attributes | KEEP |
| SA-002 | fraud_flag | 1 | sensitive_attributes | KEEP |
| SA-003 | is_fraud | "Yes" | sensitive_attributes | KEEP |
| SA-004 | risk_score | 0.85 | sensitive_attributes | KEEP |
| SA-005 | diagnosis | "Diabetes" | sensitive_attributes | KEEP |
| SA-006 | loan_amount | 100000 | sensitive_attributes | KEEP |
| SA-007 | credit_score | 750 | sensitive_attributes | KEEP |
| SA-008 | account_balance | 25000.50 | sensitive_attributes | KEEP |
| SA-009 | claim_amount | 15000 | sensitive_attributes | KEEP |
| SA-010 | payment_status | "Completed" | sensitive_attributes | KEEP |

---

## 2. Tool Calling Accuracy (25% weight)

### 2.1 Tool Call Format

| Test Case | Description | Expected Behavior | Score |
|-----------|-------------|-------------------|-------|
| TC-001 | Valid classify_columns call | All required fields present | 1 |
| TC-002 | Valid execute_pipeline call | confirmed=true | 1 |
| TC-003 | Valid update_thresholds call | Valid ranges | 1 |
| TC-004 | Missing required field | Error returned | 1 |
| TC-005 | Invalid column names | Error with column list | 1 |

### 2.2 Tool Call Timing

| Test Case | State | User Message | Expected Tool | Score |
|-----------|-------|--------------|---------------|-------|
| TT-001 | ANALYZING | (file uploaded) | classify_columns | 1 |
| TT-002 | PROPOSED | "yes, proceed" | execute_pipeline | 1 |
| TT-003 | PROPOSED | "change age to sensitive" | update_classification | 1 |
| TT-004 | PROPOSED | "increase k to 10" | update_thresholds | 1 |
| TT-005 | DISCUSSING | "approved" | execute_pipeline | 1 |

### 2.3 No Hallucinated Tools

| Test Case | Description | Expected Behavior | Score |
|-----------|-------------|-------------------|-------|
| TH-001 | LLM should not invent tools | Only use defined tools | 1 |
| TH-002 | LLM should not hallucinate errors | Real errors only | 1 |
| TH-003 | LLM should not skip tool calls | Call tools when needed | 1 |

---

## 3. Saudi Data Pattern Detection (15% weight)

### 3.1 Pattern Recognition

| Test Case | Pattern | Sample | Expected Detection | Score |
|-----------|---------|--------|-------------------|-------|
| SP-001 | National ID | 1098765432 | Direct identifier | 1 |
| SP-002 | Iqama | 2123456789 | Direct identifier | 1 |
| SP-003 | Saudi Phone (+966) | +966512345678 | Direct identifier | 1 |
| SP-004 | Saudi Phone (05) | 0551234567 | Direct identifier | 1 |
| SP-005 | Saudi IBAN | SA0380000000608010167519 | Direct identifier | 1 |
| SP-006 | Card PAN (16 digits) | 4111111111111111 | Direct identifier | 1 |
| SP-007 | Commercial Registration | 1010123456 | Linkage identifier | 1 |

### 3.2 Saudi Location Hierarchy

| Test Case | City | Province | Region | Score |
|-----------|------|----------|--------|-------|
| SL-001 | Riyadh | Riyadh Province | Central | 1 |
| SL-002 | Jeddah | Makkah Province | Western | 1 |
| SL-003 | Dammam | Eastern Province | Eastern | 1 |
| SL-004 | Abha | Asir Province | Southern | 1 |
| SL-005 | Tabuk | Tabuk Province | Northern | 1 |

---

## 4. Reasoning Quality (10% weight)

### 4.1 Explanation Completeness

| Test Case | Requirement | Example | Score |
|-----------|-------------|---------|-------|
| RQ-001 | Explains WHY column is classified | "national_id contains 10-digit numbers starting with 1, indicating Saudi National ID" | 1 |
| RQ-002 | References data patterns | "Values match Saudi phone format (+966...)" | 1 |
| RQ-003 | Mentions privacy impact | "Direct identifier - can uniquely identify individuals" | 1 |
| RQ-004 | Suggests appropriate technique | "Should be SUPPRESSED to prevent identification" | 1 |

### 4.2 Reasoning Accuracy

| Test Case | Scenario | Expected Reasoning | Score |
|-----------|----------|-------------------|-------|
| RA-001 | Fraud detection use case | "Fraud_Flag kept for ML model training" | 1 |
| RA-002 | Open banking use case | "Account data pseudonymized for TPP sharing" | 1 |
| RA-003 | Healthcare use case | "Diagnosis kept per PDPL Article 23" | 1 |

---

## 5. Regulatory Compliance (10% weight)

### 5.1 PDPL Article References

| Test Case | Technique | Expected PDPL Articles | Score |
|-----------|-----------|----------------------|-------|
| RC-001 | SUPPRESS | Art. 11, 15, 18 | 1 |
| RC-002 | GENERALIZE | Art. 11, 17, 19 | 1 |
| RC-003 | PSEUDONYMIZE | Art. 15, 19, 31 | 1 |
| RC-004 | DATE_SHIFT | Art. 11, 19 | 1 |
| RC-005 | KEEP (sensitive) | Art. 5, 23, 24 | 1 |

### 5.2 SAMA Requirement References

| Test Case | Data Type | Expected SAMA Reference | Score |
|-----------|-----------|------------------------|-------|
| RS-001 | Card data | BCT/15631, PCI-DSS | 1 |
| RS-002 | IBAN | Section 2.6.2 | 1 |
| RS-003 | Third-party sharing | Section 2.6.3 | 1 |
| RS-004 | Open banking | Open Banking Framework | 1 |

---

## Scoring Rubric

### Overall Score Calculation

```
Total Score = (Classification × 0.40) + (Tool Calling × 0.25) +
              (Saudi Patterns × 0.15) + (Reasoning × 0.10) +
              (Regulatory × 0.10)
```

### Grade Thresholds

| Grade | Score Range | Description |
|-------|-------------|-------------|
| A | 90-100% | Excellent - Production ready |
| B | 80-89% | Good - Minor improvements needed |
| C | 70-79% | Acceptable - Some gaps |
| D | 60-69% | Below standard - Significant issues |
| F | <60% | Failing - Not suitable for production |

---

## Critical Test Cases (Must Pass)

These test cases are critical for production deployment:

| ID | Description | Failure Impact |
|----|-------------|----------------|
| CRIT-001 | National ID classified as direct_identifier | PII exposure |
| CRIT-002 | Phone number classified as direct_identifier | PII exposure |
| CRIT-003 | IBAN classified as direct_identifier | Financial data exposure |
| CRIT-004 | Fraud_Flag NOT classified as direct_identifier | Utility loss |
| CRIT-005 | Transaction_Amount NOT hashed | Utility loss |
| CRIT-006 | All columns must be classified | Incomplete anonymization |
| CRIT-007 | Tool calls use correct format | Pipeline failure |
| CRIT-008 | execute_pipeline only after approval | Unauthorized execution |

**Policy**: If ANY critical test case fails, the LLM is not suitable for production use with that configuration.

---

## Test Data Files

Test CSV files are located in `evals/data/`:

- `fraud_detection.csv` - Fraud detection use case
- `open_banking.csv` - Open banking use case
- `healthcare.csv` - Healthcare/medical records
- `customer_data.csv` - General customer data
- `edge_cases.csv` - Edge cases and ambiguous columns
