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
| `api/websocket.py` | WebSocket endpoint for real-time chat streaming |
| `core/conversation.py` | Conversation state machine, approval detection |
| `core/session.py` | Session CRUD with Redis |
| `core/ws_manager.py` | WebSocket connection manager per session |
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
| `components/ChatArea.tsx` | Message display, validation results, download buttons, WS indicator |
| `components/FileUpload.tsx` | CSV upload component |
| `components/MessageInput.tsx` | Chat input |
| `components/Sidebar.tsx` | Session list |
| `lib/api.ts` | API client (REST + SSE) |
| `lib/store.ts` | Zustand state management with WebSocket integration |
| `lib/websocket.ts` | WebSocket manager singleton with auto-reconnect |

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

---

## Code Review Findings (2025-12-31)

| Severity | Count | Key Issues |
|----------|-------|------------|
| Critical | 19 | CORS *, no auth, SQL injection |
| High | 33 | Path traversal, exposed ports, race conditions |
| Medium | 50 | Error handling, edge cases |
| Low | 34 | Documentation |

### Security (Production)

| Issue | File | Status |
|-------|------|--------|
| CORS allow all | `masking/main.py:27`, `validation/main.py:27` | TODO |
| No authentication | `routes.py` (all endpoints) | TODO |
| Path traversal | `validation/routes.py:117` | TODO |
| Exposed DB ports | `docker-compose.yml:77,90` | TODO |
| No Redis password | `docker-compose.yml` | TODO |

### Logic Bugs (Fixed 2025-01-01)

| Issue | File | Status |
|-------|------|--------|
| Generalizer wrong param | `generalizer.py:360-365` | ✅ FIXED |
| No column validation | `tools.py:71-185` | ✅ FIXED |
| Brace counting in JSON | `ollama_adapter.py:463-483` | ✅ FIXED |
| No pipeline status check | `tools.py:223-233` | ✅ FIXED |
| No threshold validation | `tools.py:276-281` | ✅ FIXED |
| SSE buffer not processed | `api.ts:156-174` | ✅ FIXED |

### Performance (TODO)

| Issue | File |
|-------|------|
| Regex recompiled every call | `text_scrubber.py:109` |
| t-closeness recalculates in loop | `t_closeness.py:88-104` |
| No request debouncing | `store.ts:365-393` |
| Polling interval memory leak | `store.ts:361` |

### Missing Features (TODO)

| Feature | File |
|---------|------|
| IBAN pattern in text scrubber | `text_scrubber.py` |
| File size validation | `FileUpload.tsx:28` |

---

## Architecture Overview

| Dimension | Score | Notes |
|-----------|-------|-------|
| Modularity | 8/10 | Clean service boundaries |
| Scalability | 5/10 | Single-instance design |
| Security | 4/10 | CORS issues, no auth |
| Maintainability | 7/10 | Good typing |
| Observability | 3/10 | Console.log only |

### Database Layer

**PostgreSQL** (10 tables, 3NF): `jobs`, `classifications_on_jobs`, `validation_on_jobs`, `regulations`, `saudi_patterns`

**Redis**: `session:{uuid}` → Full Session JSON, `sessions` → Sorted set by timestamp

**Key Files**: `db/init/*.sql`, `shared/database.py`, `shared/models.py`

### Backend Services

```
CHAT SERVICE (8000)
  routes.py → Session CRUD, Upload, Chat
  llm/adapter.py → Ollama/Claude/Mock
  llm/tools.py → classify_columns, execute_pipeline
  pipeline/executor.py → Masking → Validation → Report
        │
        ├→ MASKING (8001): Suppressor, Generalizer, Pseudonymizer, DateShifter, TextScrubber
        ├→ VALIDATION (8002): k-anonymity, l-diversity, t-closeness, PDF Reports
        └→ OLLAMA (11434): qwen2.5:14b GPU-accelerated
```

### Agentic Loop

```
User Message → AGENTIC LOOP (max 10 iter)
  1. Build context
  2. Call LLM with tools
  3. Stream tokens (SSE)
  4. Execute tool if called
  5. Break on terminal tool → execute_pipeline → masking → validation → PDF
```

### Inter-Service Contracts

| Route | Payload | Response |
|-------|---------|----------|
| `POST /mask` | job_id, file_path, classification | output_path |
| `POST /validate` | job_id, file_path, QIs, SAs, thresholds | passed, metrics |
| `POST /report` | job_id, session, validation_result | report_path |

### Frontend (Next.js + Zustand)

```
page.tsx → Sidebar (sessions) + ChatArea (messages, streaming, validation grid)
```

**SSE Events**: `thinking`, `text_delta`, `tool_call`, `tool_result`, `done`

### Data Flow

```
Upload CSV → Redis Session → LLM classifies → PostgreSQL
User approves → Masking → Validation → PDF → Download buttons
```

### Core Tables

```sql
jobs (id UUID, title, status, file_path, columns JSONB, thresholds JSONB)
classifications_on_jobs (job_id, column_name, classification_type_id, reasoning)
validation_on_jobs (job_id, validation_id, value, passed, details JSONB)
```

---

## Production Roadmap (TODO)

1. **Security**: CORS restrictions, JWT auth, Redis password, path validation
2. **Observability**: Structured logging (structlog), error SSE events
3. **Scalability**: Resource limits, connection pooling, Redis TTL
4. **Testing**: Unit tests for engines, integration tests for pipeline

---

## WebSocket Implementation (2025-01-10)

### Overview

Replaced polling-based session updates with real-time WebSocket communication. The frontend now maintains a persistent bidirectional connection to the chat-service for streaming LLM responses and session state updates.

### New Files

| File | Purpose |
|------|---------|
| `chat-service/core/ws_manager.py` | Connection manager - tracks WebSocket connections per session, thread-safe with asyncio lock |
| `chat-service/api/websocket.py` | WebSocket endpoint `/api/ws/{session_id}` - full agentic loop implementation |
| `frontend/lib/websocket.ts` | WebSocket manager singleton - auto-reconnect, exponential backoff, message queue |

### Modified Files

| File | Changes |
|------|---------|
| `chat-service/main.py` | Added WebSocket router import and inclusion |
| `frontend/lib/store.ts` | Replaced SSE with WebSocket for chat, removed polling, added `wsConnected` state |
| `frontend/components/ChatArea.tsx` | Added WebSocket connection indicator (green/red dot) |

### WebSocket Protocol

**Client → Server:**
```json
{
  "type": "chat" | "ping" | "get_session",
  "payload": { "message": "..." },
  "id": "correlation-id"
}
```

**Server → Client:**
```json
{
  "type": "connected" | "session" | "token" | "thinking" | "tool_start" | "tool_end" | "pipeline_start" | "pipeline_progress" | "message" | "done" | "error" | "pong",
  "payload": { ... },
  "id": "correlation-id",
  "timestamp": 1234567890.123
}
```

### Key Features

- **Auto-reconnect**: Exponential backoff (1s, 2s, 4s... up to 30s), max 10 attempts
- **Message queue**: Messages queued when offline, flushed on reconnect
- **Heartbeat**: Ping/pong every 30 seconds to keep connection alive
- **SSE fallback**: Falls back to SSE when WebSocket fails
- **Session persistence**: Messages stored in Redis, available on reconnect

### Deployment

After code changes, rebuild and restart services:
```bash
docker compose up --build -d chat-service frontend
```

---

## Investigation Findings (2025-01-10)

### Issue: LLM Hallucinating Error Message

**Symptom**: When user said "proceed" to approve classification, the LLM output:
```
Error: {"error":"unexpected end of JSON input"}
```
Instead of calling `execute_pipeline` tool.

**Root Cause**: The LLM (ministral-3:14b) hallucinated an error message in its text response instead of making a proper tool call. This is a model behavior issue where smaller models don't reliably follow tool call format.

**Solution**: Use qwen2.5:14b or Claude for more reliable tool calling. The retry logic in `ollama_adapter.py` helps but cannot fully solve model-level issues.

### Issue: Race Condition - Handlers Set Up After Connect

**Symptom**: New chat text box not appearing, missing session state

**Root Cause**: In `store.ts`, `setupWebSocketHandlers()` was called AFTER `wsManager.connect()`, causing the initial `session` event to be missed.

**Fix**: Setup handlers BEFORE connecting, add `refreshSession()` after connect as safety net:
```typescript
selectSession: async (sessionId: string) => {
  setupWebSocketHandlers(set, get); // BEFORE connect
  await wsManager.connect(sessionId);
  wsManager.refreshSession(); // Safety net
}
```

### Issue: Handlers Cleared When Switching Sessions

**Symptom**: Clicking one chat opens another, sidebar selection bugged

**Root Cause**: `connect()` internally called `disconnect()` which cleared newly set up handlers

**Fix**: Created separate `closeConnection()` method that closes socket but preserves handlers:
```typescript
private closeConnection(): void {
  // Closes socket but KEEPS handlers
}

disconnect(): void {
  this.closeConnection();
  this.clearHandlers(); // Also clears handlers
}
```

### Issue: Empty Message Bubbles ("Loading Clouds")

**Symptom**: Empty assistant message bubbles appearing in UI

**Root Cause**: Native tool calling may return `tool_calls` with empty `content`. Backend stored empty assistant messages, frontend rendered them as bubbles.

**Fix** (commit 33feece):
- Backend: Skip storing empty assistant messages in session
- Frontend: Filter out empty messages when rendering
- Frontend: Don't add empty messages on 'done' event

### Known Issues (TODO)

| Issue | Description | Status |
|-------|-------------|--------|
| WebSocket error 1006 | Connection rejected if new code not deployed | Deploy required |
| LLM tool call reliability | Smaller models don't reliably follow tool format | Use qwen2.5:14b+ |
| No WebSocket auth | WebSocket connections not authenticated | TODO |
| Connection indicator | Red dot shown when WS fails, may confuse users | Consider better UX |
