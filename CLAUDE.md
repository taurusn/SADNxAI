# SADNxAI - Data Anonymization Platform

## Project Overview
SADNxAI (SADN x AI) is a Saudi-focused data anonymization platform for banking and financial institutions. It uses a local Small Language Model (SLM) to guide users through anonymizing sensitive datasets while preserving data utility, ensuring compliance with PDPL (Personal Data Protection Law) and SAMA (Saudi Arabian Monetary Authority) regulations.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Docker Compose Network                         │
├─────────────┬──────────────┬──────────────┬──────────────┬─────────────┤
│  Frontend   │ Chat Service │   Masking    │  Validation  │   Ollama    │
│  (Next.js)  │  (FastAPI)   │   Service    │   Service    │   (GPU)     │
│   :3000     │    :8000     │    :8001     │    :8002     │   :11434    │
└──────┬──────┴──────┬───────┴──────┬───────┴──────┬───────┴──────┬──────┘
       │             │              │              │              │
       │             ▼              │              │              │
       │        ┌─────────┐        │              │              │
       │        │  Redis  │        │              │              │
       │        │  :6379  │        │              │              │
       │        └─────────┘        │              │              │
       │             │              │              │              │
       ▼             ▼              ▼              ▼              │
┌──────────────────────────────────────────────────────────────────────────┐
│                         Shared Storage Volume                            │
│  /storage/input  │  /storage/staging  │  /storage/output  │  /reports   │
└──────────────────────────────────────────────────────────────────────────┘
```

## Services

| Service | Port | Description |
|---------|------|-------------|
| frontend | 3000 | Next.js chat UI with React, TailwindCSS |
| chat-service | 8000 | Main API, LLM orchestration, session management |
| masking-service | 8001 | Data anonymization engine (suppress, generalize, pseudonymize, date-shift) |
| validation-service | 8002 | Privacy metrics (k-anonymity, l-diversity, t-closeness) & PDF reports |
| ollama | 11434 | Local SLM with GPU support (qwen2.5:14b) |
| redis | 6379 | Session storage |

## Key Files

### Chat Service (`chat-service/`)
| File | Purpose |
|------|---------|
| `main.py` | FastAPI app entry, CORS config |
| `api/routes.py` | REST endpoints: sessions, upload, chat, thresholds, downloads |
| `core/conversation.py` | Conversation state machine, approval detection |
| `core/session.py` | Session CRUD with Redis |
| `llm/adapter.py` | LLM provider abstraction (Ollama/Claude/Mock) |
| `llm/ollama_adapter.py` | Ollama integration with tool calling, retry logic |
| `llm/tools.py` | Tool executor for classify_columns, execute_pipeline, update_thresholds |
| `pipeline/executor.py` | Orchestrates masking → validation → report flow |

### Masking Service (`masking-service/`)
| File | Purpose |
|------|---------|
| `api/routes.py` | `/mask` endpoint |
| `engine/suppressor.py` | Remove direct identifiers (name, national_id, phone) |
| `engine/generalizer.py` | Generalize quasi-identifiers with Saudi location hierarchies |
| `engine/pseudonymizer.py` | HMAC-SHA256 hashing for linkage IDs |
| `engine/date_shifter.py` | Random date offset preserving intervals |
| `engine/text_scrubber.py` | PII detection and redaction in free text |

### Validation Service (`validation-service/`)
| File | Purpose |
|------|---------|
| `api/routes.py` | `/validate` and `/report` endpoints |
| `metrics/k_anonymity.py` | k-anonymity calculation |
| `metrics/l_diversity.py` | l-diversity calculation |
| `metrics/t_closeness.py` | t-closeness calculation (Earth Mover's Distance) |
| `report/generator.py` | PDF report generation with ReportLab |

### Shared (`shared/`)
| File | Purpose |
|------|---------|
| `models.py` | Pydantic models: Session, Classification, Thresholds, etc. |
| `openai_schema.py` | System prompt and tool definitions for LLM |
| `regulations.py` | PDPL/SAMA article mappings, Saudi data patterns |

### Frontend (`frontend/`)
| File | Purpose |
|------|---------|
| `app/page.tsx` | Main page layout |
| `components/ChatArea.tsx` | Message display, validation results, download buttons |
| `components/FileUpload.tsx` | CSV upload component |
| `components/MessageInput.tsx` | Chat input |
| `components/Sidebar.tsx` | Session list |
| `lib/api.ts` | API client |
| `lib/store.ts` | Zustand state management |

## Running the Project

```bash
# Start all services (with GPU support)
docker compose up -d

# Rebuild specific service after changes
docker compose up --build -d chat-service

# Check logs
docker compose logs -f chat-service
docker compose logs -f ollama

# Pull the model (if not already pulled)
docker exec ollama ollama pull qwen2.5:14b

# Check GPU usage inside Ollama
docker exec ollama nvidia-smi
```

## Environment Variables

```env
# LLM Configuration
LLM_PROVIDER=ollama              # 'ollama' or 'claude'
OLLAMA_MODEL=qwen2.5:14b         # Model to use (14b recommended for tool calling)
OLLAMA_URL=http://ollama:11434   # Ollama service URL
OLLAMA_NATIVE_TOOLS=false        # Use Ollama's native function calling (experimental)
LLM_MOCK_MODE=false              # true for testing without LLM
ANTHROPIC_API_KEY=               # Only if using Claude

# Service URLs
REDIS_URL=redis://redis:6379/0
MASKING_SERVICE_URL=http://masking-service:8001
VALIDATION_SERVICE_URL=http://validation-service:8002

# Storage
STORAGE_PATH=/storage
```

## Pipeline Flow & Session States

```
IDLE → [upload CSV] → ANALYZING → [LLM classifies] → PROPOSED
  → [user discusses] → DISCUSSING → [user approves] → APPROVED
  → [masking starts] → MASKING → [validation] → VALIDATING
  → COMPLETED (if passed) or FAILED (if metrics fail)
```

### Approval Detection
The system detects approval with phrases: "approve", "yes", "proceed", "go ahead", "execute", "confirm", "lgtm", "ship it"

## Tool Call Format

The SLM outputs tool calls in this format:
```
```tool_call
{"tool": "classify_columns", "arguments": {...}}
```
```

### Available Tools
| Tool | Purpose | Required Args |
|------|---------|---------------|
| `classify_columns` | Record column classification | direct_identifiers, quasi_identifiers, linkage_identifiers, date_columns, sensitive_attributes, recommended_techniques, reasoning |
| `execute_pipeline` | Run anonymization (after approval) | confirmed: true |
| `update_thresholds` | Modify privacy thresholds | k_anonymity_*, l_diversity_*, t_closeness_*, risk_score_* |

## Masking Techniques

| Technique | Applied To | Description |
|-----------|------------|-------------|
| SUPPRESS | Direct identifiers | Complete removal (national_id, name, phone, email, IBAN) |
| GENERALIZE | Quasi-identifiers | Hierarchical generalization (age→ranges, city→province→region) |
| PSEUDONYMIZE | Linkage identifiers | HMAC-SHA256 with session salt (customer_id, account_id) |
| DATE_SHIFT | Date columns | Random offset ±365 days preserving intervals |
| TEXT_SCRUB | Sensitive text | PII detection and [REDACTED] replacement |
| KEEP | Sensitive attributes | Preserved for analysis (amount, fraud_flag) |

### Generalization Levels (0-3)
- **Age**: 0=exact, 1=5-year range, 2=10-year range, 3=Child/Adult/Senior
- **Location**: 0=city, 1=province, 2=region, 3=Saudi Arabia
- **Date**: 0=exact, 1=week, 2=month, 3=quarter

## Privacy Metrics

| Metric | Default Threshold | Description |
|--------|-------------------|-------------|
| k-anonymity | min=5, target=10 | Each record indistinguishable from k-1 others |
| l-diversity | min=2, target=3 | Sensitive values diverse within groups |
| t-closeness | max=0.2, target=0.15 | Distribution similarity (lower=better) |
| Risk Score | max=20%, target=10% | Composite weighted score |

## Regulatory Compliance

### PDPL Articles (Personal Data Protection Law)
- **Art. 11**: Data minimization - only collect minimum necessary
- **Art. 15**: Disclosure permitted only with consent OR anonymized form
- **Art. 19**: Implement technical measures for data protection
- **Art. 24**: Credit data requires explicit consent
- **Art. 29**: Cross-border transfers require adequate protection

### SAMA Requirements
- **Section 2.6.2**: Personal data must be secured in Saudi facilities, PCI compliant
- **Section 2.6.3**: Third-party sharing requires consent OR anonymized data
- **Open Banking**: Secure data sharing with licensed TPPs

### Saudi Data Patterns (Auto-detected)
| Pattern | Regex | Classification |
|---------|-------|----------------|
| National ID | `^1\d{9}$` | Direct (SUPPRESS) |
| Iqama | `^2\d{9}$` | Direct (SUPPRESS) |
| Phone | `^(\+966|05)\d{8}$` | Direct (SUPPRESS) |
| IBAN | `^SA\d{22}$` | Direct (SUPPRESS) |
| Card PAN | `^\d{16}$` | Direct (SUPPRESS) |

## GPU Support

The docker-compose.yml is configured for NVIDIA GPU acceleration:
```yaml
ollama:
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: all
            capabilities: [gpu]
```

To verify GPU is working:
```bash
docker exec ollama nvidia-smi
# Look for "GPU memory" being used when model is loaded
```

## Known Issues & Solutions

### 1. Slow LLM Responses
- **Cause**: Model not loaded or running on CPU
- **Solution**: Check GPU access with `docker exec ollama nvidia-smi`
- **Optimizations in code**: `keep_alive: "10m"`, persistent HTTP client

### 2. Tool Calling Issues
- **Cause**: Smaller models don't reliably follow tool call format
- **Symptom**: LLM describes actions in text instead of JSON tool calls
- **Solution**: Use qwen2.5:14b (better tool calling than 3b), retry logic in `ollama_adapter.py`

### 3. Context Truncation
- **Cause**: Prompt exceeds context window
- **Solution**: `num_ctx: 24000` in ollama options, compact system prompt

### 4. Validation Failures
- **Cause**: Insufficient generalization for k-anonymity
- **Solution**: Increase generalization levels or adjust thresholds via chat

## API Endpoints

### Sessions
- `POST /api/sessions` - Create new session
- `GET /api/sessions` - List sessions
- `GET /api/sessions/{id}` - Get session details
- `DELETE /api/sessions/{id}` - Delete session

### Chat & Files
- `POST /api/sessions/{id}/upload` - Upload CSV
- `POST /api/sessions/{id}/chat` - Send message
- `PATCH /api/sessions/{id}/thresholds` - Update thresholds

### Downloads
- `GET /api/sessions/{id}/download/data` - Download anonymized CSV
- `GET /api/sessions/{id}/download/report` - Download PDF report

## Development

### Local Development (without Docker)
```bash
# Backend services
cd chat-service && uvicorn main:app --reload --port 8000
cd masking-service && uvicorn main:app --reload --port 8001
cd validation-service && uvicorn main:app --reload --port 8002

# Frontend
cd frontend && npm run dev

# Run Ollama natively with GPU
ollama serve
ollama pull qwen2.5:14b
```

### Testing
```bash
python test_all.py
```
