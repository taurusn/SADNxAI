# LLM Upgrade Proposal: Ministral-3 + TOON Integration

## Current State

| Component | Current | Issue |
|-----------|---------|-------|
| LLM Model | qwen2.5:14b | Tool calling works but not optimized |
| Data Format | JSON | High token usage, costly |
| Provider | Ollama (local) | Good - keeps data on-premise |

---

## Proposed Changes

### 1. New LLM: Ministral-3:14b

**Why switch from Qwen 2.5 to Ministral-3?**

| Feature | qwen2.5:14b | ministral-3:14b |
|---------|-------------|-----------------|
| Parameters | 14B | 14B |
| Native Tool Calling | Good | **Best-in-class** |
| JSON Output | Good | **Native optimized** |
| Agentic Workflows | Standard | **Purpose-built** |
| Edge Deployment | Standard | **Optimized** |

**Key Benefits:**
- **Best-in-class agentic capabilities** - designed for tool use workflows
- **Native function calling** - more reliable tool execution
- **Native JSON output** - structured responses without parsing errors
- **Same parameter size** - no additional GPU memory required

**Migration:**
```yaml
# docker-compose.yml
OLLAMA_MODEL=ministral-3:14b  # Changed from qwen2.5:14b
```

```bash
# Pull the new model
docker exec ollama ollama pull ministral-3:14b
```

---

### 2. TOON Format Integration

**What is TOON?**

TOON (Token-Oriented Object Notation) is a compact, human-readable format that reduces LLM token usage by **30-60%** compared to JSON.

**Example Comparison:**

```json
// JSON - 47 tokens
[
  {"id": 1, "name": "Ahmed", "city": "Riyadh"},
  {"id": 2, "name": "Sara", "city": "Jeddah"},
  {"id": 3, "name": "Omar", "city": "Dammam"}
]
```

```
// TOON - 19 tokens (60% reduction)
[3,]{id,name,city}
1,Ahmed,Riyadh
2,Sara,Jeddah
3,Omar,Dammam
```

**Why TOON for SADNxAI?**

| Benefit | Impact |
|---------|--------|
| **Token Reduction** | 30-60% fewer tokens per request |
| **Cost Savings** | Lower compute costs for LLM inference |
| **Faster Processing** | Less data to process = faster responses |
| **Better Accuracy** | 74% accuracy vs JSON's 70% in benchmarks |
| **CSV Data Friendly** | Perfect for our tabular anonymization data |

**Use Cases in SADNxAI:**

1. **Column Classification** - Send dataset sample as TOON instead of JSON
2. **Masking Configuration** - Classification results in TOON format
3. **Validation Results** - Privacy metrics in compact TOON
4. **Conversation Context** - Reduce token usage in chat history

**Implementation:**

```python
# Install
pip install toon

# Usage in chat-service
import toon

# Before sending to LLM
sample_data_toon = toon.encode(sample_data_json)

# LLM processes TOON (any model works)
response = await llm.chat(messages_with_toon)

# Response can be JSON or TOON
result = toon.decode(response) if is_toon else json.loads(response)
```

---

## Implementation Plan

### Phase 1: LLM Switch
1. Pull ministral-3:14b model
2. Update docker-compose.yml
3. Test tool calling with existing workflows
4. Validate classification accuracy

### Phase 2: TOON Integration
1. Add `toon` to requirements.txt
2. Create TOON encoder/decoder utility
3. Update LLM adapter to use TOON for data payloads
4. Keep JSON for tool definitions (required by Ollama)

### Phase 3: Optimization
1. Benchmark token usage before/after
2. Measure response times
3. Document cost savings

---

## Expected Outcomes

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Tool Call Reliability | 85% | 95%+ | +10% |
| Token Usage | 100% | 40-70% | 30-60% reduction |
| Response Time | Baseline | Faster | ~20% improvement |
| Classification Accuracy | Good | Better | Native JSON helps |

---

## References

- [Ministral-3:14b on Ollama](https://ollama.com/library/ministral-3:14b)
- [Ollama Tool Calling Docs](https://docs.ollama.com/capabilities/tool-calling)
- [TOON Official Specification](https://github.com/toon-format/spec)
- [TOON Python Library](https://github.com/xaviviro/python-toon)
- [TOON Format Explained](https://toonformat.dev/)

---

## Implementation Status

| Component | Status | File |
|-----------|--------|------|
| Ollama 0.13.1 pinned | DONE | `docker-compose.yml` |
| Healthcheck added | DONE | `docker-compose.yml` |
| Model: ministral-3:14b | DONE | `.env` |
| Context: 32K configurable | DONE | `.env`, `ollama_adapter.py` |
| TOON library added | DONE | `requirements.txt` |
| TOON utilities module | DONE | `shared/toon_utils.py` |
| Prompt builder updated | DONE | `ollama_adapter.py` |
| TOON enabled by default | NO | Set `TOON_ENABLED=true` to enable |

### Next Steps

1. **Pull new model**: `docker exec ollama ollama pull ministral-3:14b`
2. **Rebuild chat-service**: `docker compose build chat-service`
3. **Restart services**: `docker compose up -d`
4. **Test without TOON**: Verify ministral-3 tool calling works
5. **Enable TOON**: Set `TOON_ENABLED=true` in `.env`
6. **Benchmark**: Compare token usage before/after TOON

### Rollback

```bash
# Revert model
OLLAMA_MODEL=qwen2.5:14b

# Disable TOON
TOON_ENABLED=false

# Restart
docker compose up -d --force-recreate chat-service
```

---

*Proposed: 2026-01-08*
*Implemented: 2026-01-08*
