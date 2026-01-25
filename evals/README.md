# SADNxAI LLM Evaluation Framework

A comprehensive evaluation suite for assessing LLM performance in the SADNxAI data anonymization platform.

## Overview

This framework evaluates the LLM's ability to:

| Dimension | Weight | Description |
|-----------|--------|-------------|
| **Classification** | 40% | Correctly categorize columns (direct/quasi/linkage/date/sensitive) |
| **Tool Calling** | 25% | Use correct tools at correct times |
| **Saudi Patterns** | 15% | Detect Saudi-specific data (National ID, IBAN, phone) |
| **Reasoning** | 10% | Provide quality explanations |
| **Regulatory** | 10% | Reference PDPL/SAMA regulations |

## Quick Start

### Prerequisites

```bash
# Services must be running
docker compose up -d

# Wait for services to be healthy
curl http://localhost:8000/api/sessions
```

### Run Evaluations

```bash
# Run all evaluations
python evals/run_evals.py

# Run with verbose output
python evals/run_evals.py -v

# Run specific category
python evals/run_evals.py --category classification

# Run with parallel execution (faster)
python evals/run_evals.py --parallel

# Test specific provider
python evals/run_evals.py --provider vllm
python evals/run_evals.py --provider claude
```

## Example Output

```
============================================================
SADNxAI LLM EVALUATION REPORT
============================================================
Timestamp:  2025-01-25T10:30:00
Provider:   vllm
Model:      meta-llama/Llama-3.1-8B-Instruct
Duration:   45000ms
Grade:      B (85.5%)

Category Scores:
----------------------------------------
  classification       ████████████████░░░░  87.5% (w:40%)
  tool_calling         ██████████████████░░  90.0% (w:25%)
  saudi_patterns       ████████████████░░░░  80.0% (w:15%)
  reasoning            ███████████████░░░░░  75.0% (w:10%)
  regulatory           █████████████████░░░  85.0% (w:10%)

Summary: 42/50 tests passed
Sessions: 15 created, 15 cleaned

============================================================
RESULT: PASS - LLM meets production standards
============================================================
```

## Grading Scale

| Grade | Score | Meaning |
|-------|-------|---------|
| **A** | 90%+ | Production ready |
| **B** | 80-89% | Good, minor improvements needed |
| **C** | 70-79% | Acceptable |
| **D** | 60-69% | Below standard |
| **F** | <60% | Not production ready |

## Critical Tests

These tests **must pass** for production deployment:

| Test ID | Description | Failure Impact |
|---------|-------------|----------------|
| `CRIT-*-direct-national_id` | National ID → direct_identifiers | PII exposure |
| `CRIT-*-direct-phone` | Phone → direct_identifiers | PII exposure |
| `CRIT-*-direct-email` | Email → direct_identifiers | PII exposure |
| `CRIT-*-sensitive-fraud_flag` | fraud_flag → sensitive_attributes | Utility loss |
| `CRIT-*-nosuppress-transaction_amount` | Amount NOT suppressed | Utility loss |

If **any** critical test fails, the grade is automatically `F` regardless of score.

## Directory Structure

```
evals/
├── README.md                     # This file
├── criteria.md                   # Detailed test case specifications
├── run_evals.py                  # Main evaluation script
├── expected_classifications.json # Ground truth for all test files
├── __init__.py
├── data/                         # Test CSV files
│   ├── fraud_detection.csv       # Fraud detection use case
│   ├── open_banking.csv          # Open banking use case
│   ├── healthcare.csv            # Healthcare records
│   ├── customer_data.csv         # General customer data
│   └── edge_cases.csv            # Edge cases (naming variations)
└── reports/                      # Generated evaluation reports
    └── eval_vllm_20250125_103000.json
```

## Test Categories

### 1. Classification Tests

Tests correct categorization of columns:

- **Direct Identifiers**: national_id, phone, email, IBAN, name
- **Quasi-Identifiers**: age, city, gender, occupation
- **Linkage Identifiers**: customer_id, account_id, patient_id
- **Date Columns**: transaction_date, birth_date, created_at
- **Sensitive Attributes**: amount, fraud_flag, diagnosis

### 2. Tool Calling Tests

Tests correct tool usage:

- `TOOL-001`: classify_columns called after upload
- `TOOL-002`: execute_pipeline called after approval
- `TOOL-003`: No premature pipeline execution
- `TOOL-004`: update_thresholds works correctly
- `TOOL-005`: update_classification works correctly

### 3. Saudi Pattern Tests

Tests Saudi-specific data detection:

- `SAUDI-001`: National ID (10 digits starting with 1)
- `SAUDI-002`: Saudi phone (+966, 05)
- `SAUDI-003`: Email addresses
- `SAUDI-004-006`: Quasi-identifiers (city, age, gender)
- `SAUDI-007`: Saudi IBAN (SA + 22 digits)

### 4. Reasoning Tests

Tests explanation quality:

- `REASON-001`: Reasoning provided (>50 chars)
- `REASON-002`: Mentions privacy concepts
- `REASON-003`: Mentions techniques (suppress, generalize, etc.)
- `REASON-004`: Specific to the data (mentions actual columns)

### 5. Regulatory Tests

Tests compliance references:

- `REG-001`: PDPL referenced
- `REG-002`: SAMA referenced
- `REG-003`: Specific articles cited
- `REG-004`: Domain-relevant regulations

## Adding New Test Cases

### 1. Add Test Data

Create a new CSV file in `evals/data/`:

```csv
customer_id,national_id,age,city,amount
CUST-001,1098765432,35,Riyadh,5000.00
```

### 2. Add Expected Classification

Update `expected_classifications.json`:

```json
{
  "my_new_test.csv": {
    "direct_identifiers": ["national_id"],
    "quasi_identifiers": ["age", "city"],
    "linkage_identifiers": ["customer_id"],
    "date_columns": [],
    "sensitive_attributes": ["amount"],
    "recommended_techniques": {
      "national_id": "SUPPRESS",
      "age": "GENERALIZE",
      "city": "GENERALIZE",
      "customer_id": "PSEUDONYMIZE",
      "amount": "KEEP"
    },
    "critical_checks": {
      "must_be_direct": ["national_id"],
      "must_be_sensitive": ["amount"],
      "must_not_be_suppressed": ["amount", "customer_id"]
    }
  }
}
```

### 3. Run Tests

```bash
python evals/run_evals.py --category classification -v
```

## CLI Options

| Option | Description |
|--------|-------------|
| `--provider` | LLM provider: vllm, claude, ollama, mock |
| `--model` | Specific model name |
| `--category` | Run only: classification, tool_calling, saudi_patterns, reasoning, regulatory |
| `--url` | Chat service URL (default: http://localhost:8000) |
| `--parallel` | Run test files in parallel |
| `--direct` | Direct LLM mode (no services needed) - WIP |
| `-v, --verbose` | Verbose output |
| `--log-level` | DEBUG, INFO, WARNING, ERROR |

## CI Integration

The script exits with code 1 if:
- Grade is D or F
- Any critical test fails

Example GitHub Actions:

```yaml
- name: Run LLM Evaluations
  run: |
    docker compose up -d
    sleep 60  # Wait for services
    python evals/run_evals.py --provider vllm
```

## Report Format

Reports are saved to `evals/reports/` as JSON:

```json
{
  "timestamp": "2025-01-25T10:30:00",
  "provider": "vllm",
  "model": "meta-llama/Llama-3.1-8B-Instruct",
  "percentage": 85.5,
  "grade": "B",
  "duration_ms": 45000,
  "category_scores": {
    "classification": {"score": 35, "max_score": 40, "percentage": 87.5, "weight": 0.4}
  },
  "critical_failures": [],
  "summary": {
    "total_tests": 50,
    "passed": 42,
    "failed": 8,
    "errors": 0
  },
  "results": [...]
}
```

## Troubleshooting

### Services Not Available

```
ERROR: Services not available at http://localhost:8000
```

**Fix**: Start services with `docker compose up -d` and wait for health check.

### Timeout Errors

**Fix**: Increase timeout or check if vLLM is loaded:
```bash
docker compose logs vllm | grep "ready"
```

### Low Scores

1. Check which tests failed in the report
2. Review LLM logs: `docker compose logs chat-service`
3. Consider using a different model (llama3.1:8b recommended for tool calling)

## Development

### Running Tests Locally

```bash
# Install dependencies
pip install -r evals/requirements.txt

# Run with debug logging
python evals/run_evals.py -v --log-level DEBUG
```

### Code Structure

```python
# Main classes
APIClient          # HTTP client with retry logic
LLMEvaluator       # Main evaluation engine
EvalResult         # Single test result
EvalReport         # Aggregated report

# Key methods
eval_classification()  # Test column classification
eval_tool_calling()    # Test tool usage
eval_saudi_patterns()  # Test Saudi data detection
eval_reasoning()       # Test explanation quality
eval_regulatory()      # Test compliance references
```
