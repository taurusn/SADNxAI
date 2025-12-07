# SADNxAI - Data Anonymization Platform

## Project Overview
SADNxAI is a Saudi-focused data anonymization platform that uses a local Small Language Model (SLM) to guide users through anonymizing sensitive datasets while preserving data utility.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Frontend   │────▶│ Chat Service │────▶│  Ollama (SLM)   │
│  (Next.js)  │     │  (FastAPI)   │     │  qwen2.5:3b     │
└─────────────┘     └──────┬───────┘     └─────────────────┘
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
        ┌──────────┐ ┌──────────┐ ┌───────┐
        │ Masking  │ │Validation│ │ Redis │
        │ Service  │ │ Service  │ │       │
        └──────────┘ └──────────┘ └───────┘
```

## Services

| Service | Port | Description |
|---------|------|-------------|
| frontend | 3000 | Next.js chat UI |
| chat-service | 8000 | Main API, LLM orchestration |
| masking-service | 8001 | Data anonymization engine |
| validation-service | 8002 | Privacy metrics & PDF reports |
| ollama | 11434 | Local SLM (qwen2.5:3b) |
| redis | 6379 | Session storage |

## Key Files

### Chat Service
- `chat-service/llm/ollama_adapter.py` - Ollama integration with tool calling
- `chat-service/llm/adapter.py` - LLM provider switching (Ollama/Claude/Mock)
- `chat-service/api/routes.py` - API endpoints
- `chat-service/core/conversation.py` - Conversation state management

### Masking Service
- `masking-service/engine/` - Anonymization techniques:
  - `suppressor.py` - Remove direct identifiers
  - `generalizer.py` - Generalize quasi-identifiers
  - `pseudonymizer.py` - Replace with consistent hashes
  - `date_shifter.py` - Shift dates randomly

### Validation Service
- `validation-service/metrics/` - Privacy metrics:
  - `k_anonymity.py` - k-anonymity calculation
  - `l_diversity.py` - l-diversity calculation
  - `t_closeness.py` - t-closeness calculation
- `validation-service/report/generator.py` - PDF report generation

### Shared
- `shared/models.py` - Pydantic models for all services
- `shared/openai_schema.py` - System prompt and tool definitions

## Running the Project

```bash
# Start all services
docker compose up -d

# Rebuild after changes
docker compose up --build -d chat-service

# Check logs
docker compose logs --tail=50 chat-service
docker compose logs --tail=30 ollama
```

## Known Issues & Solutions

### 1. Slow LLM Responses
- **Cause**: CPU inference with 3B model
- **Solution**: Optimizations in `ollama_adapter.py`:
  - `keep_alive: "10m"` - keeps model loaded
  - Persistent HTTP client
  - `timeout: 240s` for long requests

### 2. Tool Calling Issues
- **Cause**: qwen2.5:3b doesn't reliably follow tool call format
- **Symptom**: LLM describes actions in text instead of JSON tool calls
- **Solution Options**:
  1. Switch to larger model (qwen2.5:7b)
  2. Improve prompt with more examples
  3. Use Ollama's native function calling

### 3. Context Truncation
- **Cause**: Prompt exceeds context window
- **Solution**: Set `num_ctx: 4096` in ollama options

## Pipeline Flow

```
IDLE → UPLOAD → ANALYZING → PROPOSED → APPROVED → MASKING → VALIDATING → COMPLETED
                    │            │
                    │            └─ User says "approve"
                    └─ LLM calls classify_columns tool
```

## Environment Variables

```env
LLM_PROVIDER=ollama          # or 'claude'
OLLAMA_MODEL=qwen2.5:3b      # model to use
LLM_MOCK_MODE=false          # true for testing
ANTHROPIC_API_KEY=           # only if using Claude
```

## Tool Call Format (for SLM)

The SLM should output tool calls like:
```
```tool_call
{"tool": "classify_columns", "arguments": {...}}
```
```

Tools available:
- `classify_columns` - Classify columns by privacy risk
- `execute_pipeline` - Run anonymization after approval
- `update_thresholds` - Modify privacy thresholds

## Data Flow

1. User uploads CSV → stored in `/storage/input/`
2. Chat service sends 5 sample rows + columns to LLM
3. LLM classifies columns → stored in session
4. User approves → LLM calls execute_pipeline
5. Masking service anonymizes data → `/storage/staging/`
6. Validation service checks metrics → `/storage/output/`
7. PDF report generated → `/storage/reports/`
