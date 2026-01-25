# SADNxAI LLM Evaluation Framework

This directory contains evaluation criteria, test cases, and scripts for assessing the LLM component of SADNxAI.

## Evaluation Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Classification Accuracy | 40% | Correct categorization of columns |
| Tool Calling | 25% | Proper tool call format and execution |
| Saudi Pattern Detection | 15% | Recognition of Saudi-specific data |
| Reasoning Quality | 10% | Explanations for decisions |
| Regulatory Compliance | 10% | Correct PDPL/SAMA references |

## Quick Start

```bash
# Run all evaluations
python evals/run_evals.py

# Run specific evaluation
python evals/run_evals.py --category classification

# Run with specific LLM provider
python evals/run_evals.py --provider vllm
python evals/run_evals.py --provider claude
python evals/run_evals.py --provider ollama
```

## Test Categories

1. **Classification Tests** (`test_classification.json`)
2. **Tool Calling Tests** (`test_tool_calling.json`)
3. **Saudi Patterns Tests** (`test_saudi_patterns.json`)
4. **Edge Cases Tests** (`test_edge_cases.json`)

## Scoring

- **Pass**: Score >= 80%
- **Acceptable**: Score >= 60%
- **Fail**: Score < 60%
