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

---

## Code Review Findings (2025-12-31)

### Critical Issues Summary

| Severity | Count | Description |
|----------|-------|-------------|
| Critical | 19 | Security vulnerabilities, critical bugs |
| High | 33 | Authentication, path traversal, performance |
| Medium | 50 | Error handling, edge cases, code quality |
| Low | 34 | Documentation, minor improvements |

---

### Security Vulnerabilities

#### 1. CORS Allow All Origins (CRITICAL)
**Files:** `masking-service/main.py:27`, `validation-service/main.py:27`
```python
# PROBLEM: Allows any website to attack APIs
allow_origins=["*"]

# FIX: Restrict to known origins
allow_origins=[
    "http://localhost:3000",
    "https://sadnxai.sadn.site",
]
```

#### 2. No Authentication (CRITICAL)
**Files:** All API endpoints in `chat-service/api/routes.py`
- No JWT, API key, or session authentication
- Anyone can create, read, delete sessions
- **Fix:** Implement JWT middleware

#### 3. Path Traversal Risk (HIGH)
**File:** `validation-service/api/routes.py:117-119`
```python
# PROBLEM: No validation that path is under /storage
if not os.path.exists(request.input_path):
    raise HTTPException(...)

# FIX: Add path validation
if not os.path.abspath(request.input_path).startswith(STORAGE_PATH):
    raise HTTPException(status_code=400, detail="Invalid path")
```

#### 4. Exposed Database Ports (HIGH)
**File:** `docker-compose.yml:77, 90`
```yaml
# PROBLEM: Redis and PostgreSQL exposed to network
ports:
  - "5432:5432"  # Remove or restrict to 127.0.0.1:5432:5432
  - "6379:6379"  # Remove or restrict
```

#### 5. Prompt Injection Possible (MEDIUM)
**File:** `chat-service/api/routes.py:558`
- User messages appended directly without sanitization
- **Fix:** Add input validation and system-level guardrails

---

### Critical Bugs

#### 1. Terminal Tool Never Executes in Streaming (CRITICAL)
**File:** `chat-service/api/routes.py:127-133`
```python
# PROBLEM: execute_pipeline tool detected but never executed
if tool_name in terminal_tools:
    yield _sse_event("terminal_tool", {...})
    should_break = True
    continue  # Tool skipped, never runs!

# FIX: Execute the tool before breaking
if tool_name in terminal_tools:
    result = await tool_executor.execute(tool_name, tool_args)
    yield _sse_event("tool_result", {"result": result})
    should_break = True
```

#### 2. Generalizer Uses Wrong Parameter (CRITICAL)
**File:** `masking-service/engine/generalizer.py:361-365`
```python
# PROBLEM: Zipcode/gender/generic use age_level instead of correct level
result[col] = df[col].apply(lambda x: self._generalize_zipcode(x, self.age_level))  # WRONG
result[col] = df[col].apply(lambda x: self._generalize_gender(x, self.age_level))   # WRONG

# FIX: Use appropriate level for each type
result[col] = df[col].apply(lambda x: self._generalize_zipcode(x, self.location_level))
```

#### 3. Race Conditions in Session Updates (HIGH)
**File:** `chat-service/api/routes.py:521-530`
- Session modified in async generator, updates can interleave
- **Fix:** Add per-session locking or transaction-based updates

#### 4. Memory Leak - Polling Interval (HIGH)
**File:** `frontend/lib/store.ts:361`
```typescript
// PROBLEM: Interval never cleaned up on component unmount
const interval = setInterval(async () => {...}, 2000);

// FIX: Clear interval in useEffect cleanup
useEffect(() => {
  return () => {
    if (pollingInterval) clearInterval(pollingInterval);
  };
}, []);
```

---

### Performance Issues

#### 1. Regex Recompiled Every Call (HIGH)
**File:** `masking-service/engine/text_scrubber.py:109`
```python
# PROBLEM: Patterns compiled on every scrub_text() call
for pattern in self._compile_patterns():  # Called every time!

# FIX: Compile once in __init__
def __init__(self, ...):
    self._compiled_patterns = self._compile_patterns()
```

#### 2. t-closeness Recalculates Global Distribution (MEDIUM)
**File:** `validation-service/metrics/t_closeness.py:88-104`
```python
# PROBLEM: Recalculates inside loop (O(n*k) instead of O(n))
for class_key, class_df in grouped:
    global_dist = df[sa].value_counts(normalize=True)  # Redundant!

# FIX: Pre-calculate before loop
global_dist = df[sa].value_counts(normalize=True)
for class_key, class_df in grouped:
    # Use pre-calculated global_dist
```

#### 3. No Request Debouncing (MEDIUM)
**File:** `frontend/lib/store.ts:365-393`
- Polling every 2s without checking if previous request finished
- **Fix:** Add request tracking or use AbortController

---

### Missing Features

#### 1. IBAN Detection Pattern Missing
**File:** `masking-service/engine/text_scrubber.py`
```python
# ADD: IBAN pattern for SAMA compliance
'iban': [r'\bSA\d{22}\b']
```

#### 2. File Size Validation Missing
**File:** `frontend/components/FileUpload.tsx:28`
```typescript
// PROBLEM: Says "max 100MB" but no validation
if (file && file.name.endsWith('.csv')) {
    setSelectedFile(file);  // No size check!
}

// FIX: Add size validation
if (file && file.name.endsWith('.csv') && file.size <= 100 * 1024 * 1024) {
    setSelectedFile(file);
}
```

#### 3. Redis Password Missing
**File:** `docker-compose.yml:74-85`
```yaml
# FIX: Add password authentication
redis:
  command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
```

---

### Compliance Risks

| Regulation | Risk | Issue |
|------------|------|-------|
| PDPL Art. 15 | HIGH | Missing IBAN pattern could leave financial data exposed |
| PDPL Art. 19 | MEDIUM | No authentication means unauthorized data access |
| SAMA 2.6.2 | HIGH | Exposed database ports violate secure facility requirements |

---

### Recommended Priority Fixes

#### Week 1 (Critical)
- [ ] Fix CORS policies on masking/validation services
- [ ] Remove exposed database ports in docker-compose
- [ ] Add Redis password authentication
- [ ] Fix generalizer parameter bug (lines 361-365)
- [ ] Fix streaming terminal tool execution

#### Week 2 (High)
- [ ] Implement JWT authentication
- [ ] Fix path traversal in validation service
- [ ] Add file size/MIME validation in frontend
- [ ] Cache regex patterns in text scrubber
- [ ] Add IBAN detection pattern

#### Week 3 (Medium)
- [ ] Fix memory leaks in frontend polling
- [ ] Optimize t-closeness calculation
- [ ] Add comprehensive error handling
- [ ] Add resource limits to Docker services
- [ ] Implement proper logging

---

### Architecture Recommendations

1. **Add Authentication Layer**
   - JWT tokens for API authentication
   - Session validation middleware
   - Rate limiting (slowapi)

2. **Improve Error Handling**
   - Catch specific exceptions, not generic `Exception`
   - Don't expose internal error details to clients
   - Add structured logging

3. **Enhance Security**
   - Network isolation between services
   - Remove all exposed ports except frontend
   - Use Docker secrets for credentials

4. **Performance Optimization**
   - Pre-compile regex patterns
   - Pre-calculate global distributions
   - Add request debouncing
   - Implement caching where appropriate

---

## Tier-by-Tier Architecture Analysis (2025-12-31)

### Architecture Maturity Assessment

| Dimension | Score | Notes |
|-----------|-------|-------|
| Modularity | 8/10 | Clean service boundaries, composable engines |
| Scalability | 5/10 | No rate limiting, small pools, single-instance design |
| Security | 4/10 | CORS issues, SQL injection, no auth |
| Maintainability | 7/10 | Good typing, some code duplication in streaming |
| Observability | 3/10 | Console.log only, no structured logging |
| Testability | 4/10 | No visible tests, tight coupling in some areas |

---

### TIER 1: DATABASE LAYER

#### PostgreSQL Schema (10 tables, 3NF normalized)

```
REFERENCE TABLES                          DATA TABLES
├─ techniques (6 types)                   ├─ jobs (main entity)
├─ classification_types (5)               ├─ classifications_on_jobs
├─ validations (4 metrics)                ├─ validation_on_jobs
├─ regulations (PDPL/SAMA)                └─ classification_regulations
├─ saudi_patterns (7 regex)
└─ technique_regulations (junction)
```

**Key Files:**
- `db/init/001_schema.sql` - Table definitions, indexes, constraints
- `db/init/002_seed_data.sql` - Reference data (techniques, patterns)
- `shared/database.py` - asyncpg connection pooling, queries
- `shared/models.py` - Pydantic models for serialization

**Strengths:**
- UUID primary keys for distributed systems
- JSONB for flexible data (thresholds, sample_data)
- Full-text search index on regulations
- Cascade deletion on job cleanup

**Critical Issues:**

| Issue | File:Line | Impact |
|-------|-----------|--------|
| SQL Injection | `database.py:187-206` | Dynamic column names not validated |
| No Session TTL | `session.py:71` | Redis memory grows unbounded |
| Small Pool | `database.py:26-33` | min=2, max=10 insufficient |
| VARCHAR(500) | `schema.sql:81` | Windows paths can exceed limit |

**Fix for SQL Injection:**
```python
# database.py:187-206
ALLOWED_FIELDS = {'status', 'thresholds', 'masked_path', 'report_path'}
if key not in ALLOWED_FIELDS:
    raise ValueError(f"Invalid field: {key}")
```

**Fix for Redis TTL:**
```python
# session.py:71
TTL_SECONDS = 7776000  # 90 days
self.redis.setex(key, TTL_SECONDS, session_json)
```

#### Redis Session Storage

```python
# Key patterns
session:{uuid}  → Full Session JSON (up to 100KB)
sessions        → Sorted set by timestamp

# Missing features
- No TTL (sessions never expire)
- No tenant isolation
- No compression
```

---

### TIER 2: BACKEND SERVICES

#### Service Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                    CHAT SERVICE (8000)                          │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ routes.py → Session CRUD, Upload, Chat, Downloads      │    │
│  │ llm/adapter.py → Ollama/Claude/Mock switching          │    │
│  │ llm/tools.py → classify_columns, execute_pipeline      │    │
│  │ pipeline/executor.py → Masking → Validation → Report   │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────┬──────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ MASKING (8001)│ │VALIDATION(8002│ │ OLLAMA (11434)│
│ 5 Engines:    │ │ 3 Metrics:    │ │ qwen2.5:14b   │
│ - Suppressor  │ │ - k-anonymity │ │ GPU-accel     │
│ - Generalizer │ │ - l-diversity │ │               │
│ - Pseudonymize│ │ - t-closeness │ │               │
│ - DateShifter │ │ + PDF Reports │ │               │
│ - TextScrubber│ │               │ │               │
└───────────────┘ └───────────────┘ └───────────────┘
```

#### Agentic Loop Flow

```
User Message → Chat Endpoint
                    │
    ┌───────────────┴───────────────┐
    │  AGENTIC LOOP (max 10 iter)   │
    │  1. Build context             │
    │  2. Call LLM with tools       │
    │  3. Stream tokens (SSE)       │
    │  4. Execute tool if called    │
    │  5. Break on terminal tool    │
    └───────────────┬───────────────┘
                    │
        (if execute_pipeline)
                    ▼
    ┌───────────────────────────────┐
    │     PIPELINE EXECUTION        │
    │  masking → validation → PDF   │
    └───────────────────────────────┘
```

#### Inter-Service Contracts

| Route | Method | Payload | Response |
|-------|--------|---------|----------|
| `/mask` | POST | job_id, file_path, classification, salt | output_path, techniques_applied |
| `/validate` | POST | job_id, file_path, QIs, SAs, thresholds | passed, metrics, remediation |
| `/report` | POST | job_id, session, validation_result | report_path |

**Strengths:**
- Provider-agnostic LLM (Ollama/Claude/Mock)
- SSE streaming with 2KB padding for proxies
- Modular masking engines
- Saudi-specific location hierarchies

**Critical Issues:**

| Issue | File:Line | Impact |
|-------|-----------|--------|
| Terminal tool not executed | `routes.py:127-133` | Pipeline never runs via streaming |
| No transaction consistency | `executor.py:48-149` | No rollback if validation fails after masking |
| CORS allows all | `masking/main.py:27` | Any website can attack APIs |
| Generalizer wrong param | `generalizer.py:361-365` | Zipcode uses age_level |

---

### TIER 3: FRONTEND

#### Component Hierarchy

```
RootLayout (Server)
  └─ page.tsx (Client)
      ├─ Sidebar
      │   ├─ Session list
      │   └─ New Chat button
      └─ ChatArea
          ├─ Status header + Downloads
          ├─ Messages (ReactMarkdown)
          ├─ Streaming indicators
          ├─ Validation result grid
          ├─ FileUpload (when empty)
          └─ MessageInput
```

#### State Management (Zustand)

```typescript
interface AppState {
  sessions: Session[]              // All sessions
  currentSession: SessionDetail    // Active session

  isLoading: boolean               // List loading
  isSending: boolean               // Message sending
  error: string | null             // Error toast

  streamingContent: string         // Token buffer
  streamingStatus: 'thinking'|'streaming'|'tool'|'pipeline'
  currentTool: string              // Tool being executed
  pendingMessages: string[]        // Completed iterations

  pollingInterval: NodeJS.Timeout  // 2s polling during processing
}
```

#### Streaming Event Flow

```
api.sendMessageStream(sessionId, message, onEvent)
                    │
    ┌───────────────┴───────────────┐
    │       SSE Event Processing     │
    ├────────────────────────────────┤
    │ 'thinking'   → Show indicator  │
    │ 'text_delta' → Append tokens   │
    │ 'tool_call'  → Save pending    │
    │ 'tool_result'→ Clear tool      │
    │ 'done'       → Convert to msg  │
    └────────────────────────────────┘
```

**Key Files:**
- `lib/store.ts` - Zustand store (406 lines)
- `lib/api.ts` - API client with SSE (252 lines)
- `components/ChatArea.tsx` - Message display
- `components/FileUpload.tsx` - Drag-drop upload

**Strengths:**
- TypeScript strict mode
- Optimistic UI updates
- Callback-based streaming
- Smart API URL routing (relative in prod)

**Critical Issues:**

| Issue | File:Line | Impact |
|-------|-----------|--------|
| Memory leak | `store.ts:361` | Polling interval never cleared |
| Double API call | `store.ts:343-344` | selectSession + loadSessions per message |
| No file validation | `FileUpload.tsx:28` | Size/MIME not checked |
| No mobile layout | All components | Fixed 288px sidebar |

---

### Cross-Tier Data Flow

```
FRONTEND                 BACKEND                    DATABASE
────────                 ───────                    ────────

Upload CSV ───────────→ Save /storage ───────────→ Redis Session
                        Parse columns

Stream Events ←──────── LLM classifies ──────────→ PostgreSQL
(SSE tokens)            via tool call              classifications

Show Classification
"Do you approve?" ←────

User: "yes" ──────────→ execute_pipeline
                        ├→ Masking Service
Stream Progress ←───────┤   (5 techniques)
"Masking..."            │
                        ├→ Validation Service ───→ validation_on_jobs
Stream Progress ←───────┤   (3 metrics)
"Validating..."         │
                        ├→ Report Service
Stream Progress ←───────┤   (PDF generation)
"Generating..."         │

Show Results ←────────── Update session ─────────→ Redis final state
- Metrics grid
- Download buttons
```

---

### Database Schema Reference

```sql
-- Core job tracking
CREATE TABLE jobs (
  id UUID PRIMARY KEY,
  title VARCHAR(500),
  status VARCHAR(50),           -- IDLE/ANALYZING/MASKING/etc.
  file_path VARCHAR(500),
  masked_path VARCHAR(500),
  report_path VARCHAR(500),
  columns JSONB,                -- Column names array
  sample_data JSONB,            -- First 10 rows
  thresholds JSONB,             -- k/l/t/risk thresholds
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Per-column classifications
CREATE TABLE classifications_on_jobs (
  id SERIAL PRIMARY KEY,
  job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
  column_name VARCHAR(255),
  classification_type_id VARCHAR(50),
  reasoning TEXT,
  generalization_level INTEGER DEFAULT 1,
  UNIQUE(job_id, column_name)
);

-- Validation results
CREATE TABLE validation_on_jobs (
  id SERIAL PRIMARY KEY,
  job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
  validation_id VARCHAR(50),    -- k_anonymity/l_diversity/etc.
  value FLOAT,
  threshold_used FLOAT,
  passed BOOLEAN,
  details JSONB,
  UNIQUE(job_id, validation_id)
);

-- Indexes
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_created ON jobs(created_at DESC);
CREATE INDEX idx_classifications_job ON classifications_on_jobs(job_id);
CREATE INDEX idx_validation_job ON validation_on_jobs(job_id);
CREATE INDEX idx_regulations_fts ON regulations
  USING GIN(to_tsvector('english', full_text || ' ' || title));
```

---

### Recommended Architecture Improvements

#### Phase 1: Security Hardening
```yaml
# docker-compose.yml changes
redis:
  command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
  ports: []  # Remove exposed port

postgres:
  ports: []  # Remove exposed port

masking-service:
  environment:
    - ALLOWED_ORIGINS=http://localhost:3000,https://sadnxai.sadn.site
```

#### Phase 2: Observability
```python
# Add to all services
import structlog
logger = structlog.get_logger()

# Replace print() with
logger.info("pipeline_started", job_id=job_id, status="masking")
logger.error("validation_failed", job_id=job_id, metrics=failed_metrics)
```

#### Phase 3: Scalability
```yaml
# Add resource limits
services:
  chat-service:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

#### Phase 4: Testing
```bash
# Add test structure
tests/
├── unit/
│   ├── test_suppressor.py
│   ├── test_generalizer.py
│   └── test_k_anonymity.py
├── integration/
│   ├── test_pipeline.py
│   └── test_streaming.py
└── e2e/
    └── test_full_flow.py
```

---

## User ↔ LLM Flow Analysis (2025-12-31)

### Flow Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           USER ↔ LLM FLOW                                    │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   USER INPUT                                                                 │
│       │                                                                      │
│       ▼                                                                      │
│   ┌─────────────────────┐                                                    │
│   │  MessageInput.tsx   │ ⚠ No sanitization, no max length                  │
│   │  (Frontend)         │ ⚠ Race condition on rapid Enter                   │
│   └──────────┬──────────┘                                                    │
│              │                                                               │
│              ▼                                                               │
│   ┌─────────────────────┐                                                    │
│   │     api.ts          │ ⚠ Silent SSE parse errors                         │
│   │  sendMessageStream  │ ⚠ No reconnection logic                           │
│   │                     │ ⚠ No stream timeout                               │
│   └──────────┬──────────┘                                                    │
│              │ fetch() with ReadableStream                                   │
│              ▼                                                               │
│   ┌─────────────────────┐                                                    │
│   │   routes.py:554     │ ✓ SSE with 2KB padding                            │
│   │   POST /chat        │ ⚠ nonlocal session mutation                       │
│   └──────────┬──────────┘                                                    │
│              │                                                               │
│              ▼                                                               │
│   ┌─────────────────────┐                                                    │
│   │  conversation.py    │ ⚠ Incomplete state transitions                    │
│   │  State Machine      │ ⚠ Approval detection gaps                         │
│   │                     │ ⚠ Context becomes stale                           │
│   └──────────┬──────────┘                                                    │
│              │                                                               │
│              ▼                                                               │
│   ┌─────────────────────┐                                                    │
│   │   adapter.py        │ ⚠ Event loop antipattern                          │
│   │   LLM Abstraction   │ ⚠ Async/sync mixing bug                           │
│   └──────────┬──────────┘                                                    │
│              │                                                               │
│              ▼                                                               │
│   ┌─────────────────────┐                                                    │
│   │ ollama_adapter.py   │ ⚠ HTTP client not cleaned                         │
│   │ Tool Call Parsing   │ ⚠ Brace counting bug                              │
│   │                     │ ⚠ Stale response after retries                    │
│   └──────────┬──────────┘                                                    │
│              │ POST /api/chat (streaming)                                    │
│              ▼                                                               │
│   ┌─────────────────────┐                                                    │
│   │     OLLAMA          │ ✓ GPU accelerated                                 │
│   │   qwen2.5:14b       │ ✓ 24K context window                              │
│   └──────────┬──────────┘                                                    │
│              │                                                               │
│              ▼                                                               │
│   ┌─────────────────────┐                                                    │
│   │    tools.py         │ ⚠ No column validation                            │
│   │  Tool Executor      │ ⚠ No state check before pipeline                  │
│   │                     │ ⚠ DB errors ignored                               │
│   └──────────┬──────────┘                                                    │
│              │                                                               │
│              ▼                                                               │
│   ┌─────────────────────┐                                                    │
│   │   session.py        │ ⚠ No optimistic locking                           │
│   │   Redis CRUD        │ ⚠ Race conditions on updates                      │
│   │                     │ ⚠ Message ordering corruption                     │
│   └──────────┬──────────┘                                                    │
│              │                                                               │
│              ▼                                                               │
│   ┌─────────────────────┐                                                    │
│   │    store.ts         │ ⚠ Optimistic update failures                      │
│   │   Zustand State     │ ⚠ Stream cancellation missing                     │
│   │                     │ ⚠ Memory leak (polling)                           │
│   └──────────┬──────────┘                                                    │
│              │                                                               │
│              ▼                                                               │
│   ┌─────────────────────┐                                                    │
│   │   ChatArea.tsx      │ ⚠ XSS via ReactMarkdown                           │
│   │   Message Render    │ ⚠ Key prop using index                            │
│   └──────────┴──────────┘                                                    │
│              │                                                               │
│              ▼                                                               │
│         USER OUTPUT                                                          │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

### Issues Summary

| Severity | Count | Categories |
|----------|-------|------------|
| **CRITICAL** | 12 | Race conditions, data loss, security |
| **HIGH** | 9 | Resource leaks, silent failures |
| **MEDIUM** | 8 | Logic errors, UX issues |
| **LOW** | 3 | Minor improvements |

---

### CRITICAL Issues

#### 1. Session State Race Conditions (DATA LOSS)

**Files:**
- `session.py:96-114` - No optimistic locking
- `session.py:158-174` - Message ordering corruption
- `routes.py:494, 555` - Closure mutation without sync

```python
# PROBLEM: session.py:96-114
# Concurrent requests overwrite each other (read-modify-write)
def update_session(self, session: Session) -> Session:
    session.updated_at = datetime.utcnow()
    key = f"{self.session_prefix}{session.id}"
    self.redis.set(key, self._serialize_session(session))  # Simple overwrite!
    return session

# FIX: Add optimistic locking with version
def update_session(self, session: Session) -> Session:
    key = f"{self.session_prefix}{session.id}"
    pipe = self.redis.pipeline()
    pipe.watch(key)
    current = self._deserialize_session(self.redis.get(key))
    if current.version != session.version:
        raise OptimisticLockError("Session modified by another request")
    session.version += 1
    session.updated_at = datetime.utcnow()
    pipe.multi()
    pipe.set(key, self._serialize_session(session))
    pipe.execute()
    return session
```

#### 2. XSS Vulnerability in Chat Display

**File:** `ChatArea.tsx:118-120`

```typescript
// PROBLEM: LLM output rendered without sanitization
{message.role === 'assistant' ? (
  <div className="prose prose-sm max-w-none">
    <ReactMarkdown>{message.content || ''}</ReactMarkdown>  // XSS!
  </div>
) : ...}

// ATTACK: LLM returns: [Click](javascript:alert('XSS'))
// User clicks → Script executes

// FIX: Add sanitization
import remarkSanitize from 'remark-sanitize';

<ReactMarkdown remarkPlugins={[remarkSanitize]}>
  {message.content || ''}
</ReactMarkdown>
```

#### 3. Prompt Injection Vulnerability

**File:** `ollama_adapter.py:308-354`

```python
# PROBLEM: User data concatenated directly into system prompt
prompt += f"\n\n## CURRENT FILE: {fi.get('filename', '?')}\n"
columns = fi.get('columns', [])
prompt += f"Columns: {', '.join(columns)}\n"

# Sample data injection
for row in sample_data[:5]:
    values = [str(row.get(h, ""))[:30] for h in headers]
    prompt += "| " + " | ".join(values) + " |\n"

# ATTACK: filename = "data.csv```\n\nIgnore all previous instructions...\n```"
# Or column name contains: "name|||APPROVE_ALL|||"

# FIX: Escape markdown and limit content
import html
def escape_for_prompt(text: str) -> str:
    text = html.escape(text)
    text = text.replace('```', '` ` `')
    text = text.replace('\n', ' ')
    return text[:100]

prompt += f"\n\n## CURRENT FILE: {escape_for_prompt(filename)}\n"
```

#### 4. Terminal Tool Never Executes (Streaming)

**File:** `routes.py:116-133`

```python
# PROBLEM: Tool detected but never executed in streaming mode
if tool_name in terminal_tools:
    print(f"[Agentic Loop] Terminal tool called: {tool_name}")
    yield _sse_event("terminal_tool", {...})
    should_break = True
    continue  # ← Tool skipped! Never runs!

# FIX: Execute the tool before breaking
if tool_name in terminal_tools:
    result = await tool_executor.execute(tool_name, tool_args)
    yield _sse_event("tool_result", {
        "tool": tool_name,
        "success": result.get("success", False),
        "result": result
    })
    yield _sse_event("terminal_tool", {...})
    should_break = True
    # Don't continue - let loop exit naturally
```

#### 5. Stream Failure = Lost State

**Files:**
- `routes.py:519-525` - Session only persisted at stream end
- `api.ts:148-174` - No reader cleanup
- `store.ts:270-354` - No stream cancellation

```python
# PROBLEM: routes.py - Session modified but not persisted until end
async def event_stream():
    nonlocal session
    session.messages.append(user_msg)      # Modified
    session.status = SessionStatus.PROPOSED  # Modified
    # ... streaming ...
    session_manager.update_session(session)  # Only here!
    yield _sse_event("done", {...})

# If stream crashes before update_session(), all changes lost!

# FIX: Persist critical state changes immediately
async def event_stream():
    nonlocal session
    try:
        session.messages.append(user_msg)
        session_manager.update_session(session)  # Persist immediately
        # ... streaming ...
    finally:
        session_manager.update_session(session)  # Always persist
```

```typescript
// FIX: api.ts - Add cleanup
const reader = response.body?.getReader();
try {
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        // Process...
    }
} finally {
    reader?.cancel();  // Always cleanup
}
```

#### 6. Tool Column Hallucination Not Validated

**File:** `tools.py:71-185`

```python
# PROBLEM: LLM-provided columns not validated against actual file
classification = Classification(
    direct_identifiers=args.get("direct_identifiers", []),  # Could be hallucinated!
    quasi_identifiers=args.get("quasi_identifiers", []),
    # ...
)

# If LLM hallucinates "customer_name" but file has "name":
# → Masking skips the real "name" column
# → Data NOT anonymized! Privacy violation!

# FIX: Validate columns exist
actual_columns = set(self.session.columns or [])
for col_list in [args.get("direct_identifiers", []),
                 args.get("quasi_identifiers", []),
                 args.get("linkage_identifiers", []),
                 args.get("date_columns", []),
                 args.get("sensitive_attributes", [])]:
    for col in col_list:
        if col not in actual_columns:
            return {
                "success": False,
                "error": f"Column '{col}' not found in file. Available: {list(actual_columns)}"
            }
```

---

### HIGH Severity Issues

| # | Issue | File:Line | Fix |
|---|-------|-----------|-----|
| 1 | HTTP client never closed | `ollama_adapter.py:30-36` | Add `__aenter__`/`__aexit__` |
| 2 | Event loop antipattern | `adapter.py:176-181` | Use `asyncio.run()` |
| 3 | No error SSE event type | `routes.py:74-139` | Add `yield _sse_event("error", ...)` |
| 4 | Silent SSE parse errors | `api.ts:166-171` | Propagate to error handler |
| 5 | No stream timeout | `api.ts:148-174` | Add `setTimeout` guard |
| 6 | Incomplete SSE buffer | `api.ts:209-211` | Process remaining buffer |
| 7 | Stale response after retries | `ollama_adapter.py:192-195` | Return latest response |
| 8 | Async/sync mixing | `adapter.py:159` | Use `asyncio.to_thread()` |
| 9 | No Redis TTL | `session.py:71` | Add 90-day expiration |

---

### State Machine Issues

```
Current Transitions (conversation.py:177-202):

IDLE ──upload──► ANALYZING ──propose──► PROPOSED ──approve──► APPROVED
                                            │                    │
                                       ──discuss──►         mask_start
                                            │                    │
                                            ▼                    ▼
                                       DISCUSSING           MASKING
                                            │                    │
                                       ──approve──►         mask_done
                                                                 │
                                                                 ▼
                                         FAILED ◄──fail── VALIDATING ──pass──► COMPLETED
                                            │
                                       ──retry──► (not implemented!)

MISSING TRANSITIONS:
❌ No cancel/abort from any state
❌ No error handling for MASKING failures
❌ No "retry" handler implemented
❌ Pipeline can run without APPROVED status (tools.py:223-233)
❌ No transition for threshold updates
```

**Fix:** Complete state transition matrix in `conversation.py`:

```python
transitions = {
    # Existing transitions...

    # Missing transitions
    (SessionStatus.MASKING, "error"): SessionStatus.FAILED,
    (SessionStatus.VALIDATING, "error"): SessionStatus.FAILED,
    (SessionStatus.FAILED, "retry"): SessionStatus.PROPOSED,
    (SessionStatus.PROPOSED, "cancel"): SessionStatus.IDLE,
    (SessionStatus.DISCUSSING, "cancel"): SessionStatus.IDLE,
    (SessionStatus.MASKING, "cancel"): SessionStatus.FAILED,
}
```

---

### SSE Streaming Protocol Issues

#### Backend Generation

**File:** `routes.py:41-46`

```python
# PROBLEM: Malformed padding format
def _sse_event(event_type: str, data: Dict[str, Any]) -> str:
    event_json = json.dumps({'type': event_type, **data})
    padding = ":" + " " * 2048 + "\n"  # Extra newline breaks SSE
    return f"data: {event_json}\n\n{padding}"

# FIX: Correct SSE comment format
def _sse_event(event_type: str, data: Dict[str, Any]) -> str:
    event_json = json.dumps({'type': event_type, **data})
    padding = ":" + " " * 2048  # No trailing newline
    return f"data: {event_json}\n\n{padding}\n"
```

#### Frontend Consumption

**File:** `api.ts:148-174`

```typescript
// PROBLEMS:
// 1. No cleanup on exit
// 2. No timeout detection
// 3. No reconnection logic

// FIX: Add comprehensive error handling
async function streamWithRetry(
    url: string,
    options: RequestInit,
    onEvent: (e: StreamEvent) => void,
    maxRetries = 3
) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 120000);

    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal
        });

        const reader = response.body?.getReader();
        if (!reader) throw new Error('No response body');

        try {
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                // Process...
            }
        } finally {
            reader.cancel();
        }
    } finally {
        clearTimeout(timeout);
    }
}
```

#### Event Types Analysis

| Event | Generated | Handled | Status |
|-------|-----------|---------|--------|
| `text_delta` | ✓ routes.py:77 | ✓ store.ts:176 | Working |
| `tool_call` | ✓ routes.py:125 | ✓ store.ts:183 | Working |
| `tool_result` | ✓ routes.py:139 | ✓ store.ts:197 | Working |
| `done` | ✓ routes.py:527 | ✓ store.ts:208 | Working |
| `error` | ❌ NOT GENERATED | ❌ | **Missing!** |
| `validation_result` | ❌ NOT GENERATED | ❌ | **Missing!** |

---

### Tool Calling Flow Issues

#### Parse Issues (ollama_adapter.py:436-524)

```python
# PROBLEM: Brace counting doesn't handle strings
for i, c in enumerate(content[start:], start):
    if c == '{':
        brace_count += 1
    elif c == '}':
        brace_count -= 1
        if brace_count == 0:
            end = i + 1
            break

# If JSON contains: {"reasoning": "use { brackets }"}
# Brace count becomes wrong → parsing fails

# FIX: Use proper JSON parsing
import json
def extract_tool_calls(content: str) -> List[dict]:
    results = []
    decoder = json.JSONDecoder()
    idx = 0
    while idx < len(content):
        try:
            if content[idx:idx+7] == '{"tool"':
                obj, end_idx = decoder.raw_decode(content, idx)
                results.append(obj)
                idx = end_idx
            else:
                idx += 1
        except json.JSONDecodeError:
            idx += 1
    return results
```

#### Execute Issues (tools.py)

| Tool | Issue | Line | Fix |
|------|-------|------|-----|
| `classify_columns` | No column validation | 71-185 | Validate against file columns |
| `execute_pipeline` | No status check | 223-233 | Require APPROVED status |
| `update_thresholds` | No range validation | 276-281 | Validate k≥1, l≥1, 0≤t≤1 |
| All tools | DB errors silently ignored | 156-183 | Return error if DB save fails |

---

### LLM Adapter Issues

#### Event Loop Antipattern

**File:** `adapter.py:176-181`

```python
# PROBLEM: Creates/destroys event loop per call
def chat(self, messages: List[Dict]) -> Dict[str, Any]:
    import asyncio
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(self.ollama_adapter.chat(messages))
    finally:
        loop.close()  # Memory overhead, thread safety issues

# FIX: Use asyncio.run() or force async throughout
def chat(self, messages: List[Dict]) -> Dict[str, Any]:
    return asyncio.run(self.chat_async(messages))

# Or better: Use async/await throughout the stack
```

#### Async/Sync Mixing

**File:** `adapter.py:159`

```python
# PROBLEM: Calling sync from async blocks event loop
async def chat_async(...) -> Dict[str, Any]:
    if self.mock_mode:
        return self._mock_response(messages)
    if self.ollama_adapter:
        return await self.ollama_adapter.chat(messages, session_context)
    return self.chat(messages)  # ← SYNC call in async context!

# FIX: Use asyncio.to_thread() for sync calls
async def chat_async(...) -> Dict[str, Any]:
    if self.mock_mode:
        return await asyncio.to_thread(self._mock_response, messages)
    if self.ollama_adapter:
        return await self.ollama_adapter.chat(messages, session_context)
    return await asyncio.to_thread(self.chat, messages)
```

---

### Frontend State Issues

#### Optimistic Update Failure

**File:** `store.ts:253-268`

```typescript
// PROBLEM: Optimistic message stays if request fails
const userMessage: Message = { role: 'user', content: message };
set({
    currentSession: {
        ...currentSession,
        messages: [...currentSession.messages, userMessage],  // Added
    },
    isSending: true,
});

try {
    await api.sendMessageStream(...);
} catch (err) {
    set({
        error: (err as Error).message,
        isSending: false,
        // userMessage still in messages! Ghost message!
    });
}

// FIX: Remove optimistic message on failure
} catch (err) {
    set((state) => ({
        error: (err as Error).message,
        isSending: false,
        currentSession: state.currentSession ? {
            ...state.currentSession,
            messages: state.currentSession.messages.slice(0, -1)  // Remove last
        } : null
    }));
}
```

#### Stream Cancellation Missing

**File:** `store.ts:87-103`

```typescript
// PROBLEM: Switching sessions doesn't cancel active stream
selectSession: async (sessionId: string) => {
    get().stopPolling();  // Only stops polling, not streaming!
    set({ isLoading: true, currentSessionId: sessionId });
    // Old stream still fires events to wrong session!
}

// FIX: Add AbortController
interface AppState {
    streamController: AbortController | null;
}

sendMessage: async (sessionId: string, message: string) => {
    const controller = new AbortController();
    set({ streamController: controller });

    try {
        await api.sendMessageStream(sessionId, message, onEvent, controller.signal);
    } finally {
        set({ streamController: null });
    }
}

selectSession: async (sessionId: string) => {
    get().streamController?.abort();  // Cancel active stream
    get().stopPolling();
    // ...
}
```

---

### Recommended Priority Fixes

#### P0 - Fix Today (Critical Security/Data Loss)
1. Add Redis WATCH/MULTI/EXEC for atomic session updates
2. Add `remark-sanitize` to ReactMarkdown for XSS prevention
3. Escape user data in system prompt builder
4. Execute terminal tools before `continue` in streaming loop
5. Validate column names against actual file columns

#### P1 - Fix This Week (High Impact)
6. Add try/finally with `reader.cancel()` in frontend streaming
7. Add `error` event type for backend failures
8. Add AbortController for stream cancellation on session switch
9. Add session version field for optimistic locking
10. Close HTTP client properly in adapter

#### P2 - Fix This Sprint (Medium Priority)
11. Complete state transition matrix with cancel/retry
12. Add stream timeout detection (120s)
13. Implement exponential backoff reconnection
14. Add threshold range validation (k≥1, l≥1, 0≤t≤1)
15. Rebuild context after ALL tool executions, not just classify

---

### Test Cases for Flow Validation

```python
# tests/integration/test_user_llm_flow.py

async def test_concurrent_session_updates():
    """Verify no data loss with concurrent updates"""
    session = await create_session()

    # Simulate concurrent requests
    tasks = [
        update_session(session.id, {"status": "ANALYZING"}),
        add_message(session.id, {"role": "user", "content": "test"}),
    ]
    await asyncio.gather(*tasks)

    result = await get_session(session.id)
    assert result.status == "ANALYZING"
    assert len(result.messages) == 1

async def test_stream_interruption_recovery():
    """Verify state persisted on stream failure"""
    session = await create_session()

    # Start streaming, then abort mid-stream
    with pytest.raises(ConnectionError):
        async for event in stream_with_abort(session.id, abort_after=5):
            pass

    # State should be persisted
    result = await get_session(session.id)
    assert result.messages  # Should have partial messages

async def test_column_validation():
    """Verify hallucinated columns are rejected"""
    session = await upload_file("test.csv")  # Has columns: id, name, age

    result = await classify_columns(session.id, {
        "direct_identifiers": ["customer_id"],  # Doesn't exist!
    })

    assert result["success"] == False
    assert "customer_id" in result["error"]
    assert "not found" in result["error"]
```
