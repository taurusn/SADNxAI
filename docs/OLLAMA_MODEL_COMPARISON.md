# Ollama Model Comparison for Tool Calling

This document compares different Ollama models for native tool/function calling reliability in SADNxAI.

## Current Issues (2025-01-10)

### Ministral-3:14b

**Status**: NOT RECOMMENDED for tool calling

| Issue | Description | Source |
|-------|-------------|--------|
| >2 tools fails | Tool calling doesn't work if more than 2 tools attached | [Issue #13328](https://github.com/ollama/ollama/issues/13328) |
| Silent quit | Model generates text then quits without calling tools | [Issue #13328](https://github.com/ollama/ollama/issues/13328) |
| Multiple tool calls | Template doesn't handle multiple tool calls properly | [Issue #13334](https://github.com/ollama/ollama/issues/13334) |

**Symptoms observed in SADNxAI**:
- Model outputs 1200+ tokens describing what it will do
- Never actually makes the tool call
- Stream ends without `done=True`
- SADNxAI has 5 tools, triggering the >2 tools bug

---

### Qwen2.5

**Status**: HAS ISSUES - consider Qwen3 instead

| Issue | Description | Source |
|-------|-------------|--------|
| Empty responses | Returns empty content with tools | [Issue #10899](https://github.com/ollama/ollama/issues/10899) |
| Tools not recognized | No access to tools/functions | [Issue #8588](https://github.com/ollama/ollama/issues/8588) |
| Schema hallucination | Returns wrong JSON, doesn't follow tool schema | [Issue #7051](https://github.com/ollama/ollama/issues/7051) |
| Silent failures | Tool calls fail silently | [Issue #2728](https://github.com/anomalyco/opencode/issues/2728) |

---

### GLM4

**Status**: NOT RECOMMENDED - template incompatibility

| Issue | Description | Source |
|-------|-------------|--------|
| XML format unsupported | GLM4 uses XML-style tool calls, Ollama doesn't support | [Issue #6505](https://github.com/ollama/ollama/issues/6505) |
| JSON workaround | Can use JSON format but degraded performance | [GLM-4.6](https://ollama.com/MichelRosselli/GLM-4.6) |

---

## Recommended Models

### Tier 1: Most Reliable

| Model | Size | RAM | Reliability | Notes |
|-------|------|-----|-------------|-------|
| `llama3.1:8b-instruct` | 8B | 8GB+ | ⭐⭐⭐⭐⭐ | Best overall, official Ollama support |
| `qwen3:8b` | 8B | 8GB+ | ⭐⭐⭐⭐ | Used in Ollama docs, fixes Qwen2.5 issues |

### Tier 2: Good Alternatives

| Model | Size | RAM | Reliability | Notes |
|-------|------|-----|-------------|-------|
| `mistral-nemo:12b` | 12B | 12GB+ | ⭐⭐⭐⭐ | Good for tool calling |
| `mistral:7b-instruct` | 7B | 8GB+ | ⭐⭐⭐⭐ | Lower resources, reliable |
| `dolphin3:8b-llama3.1` | 8B | 8GB+ | ⭐⭐⭐⭐ | Agentic/function calling focus |

### Tier 3: Specialized

| Model | Size | RAM | Reliability | Notes |
|-------|------|-----|-------------|-------|
| `functiongemma` | 270M | 1GB | ⭐⭐⭐ | Tiny, specialized for function calling |

---

## Configuration

### Switching Models

Update `docker-compose.yml` or `.env`:

```bash
# Option 1: Environment variable
OLLAMA_MODEL=llama3.1:8b-instruct

# Option 2: In docker-compose.yml
environment:
  - OLLAMA_MODEL=llama3.1:8b-instruct
```

### Pull the model first:

```bash
docker exec ollama ollama pull llama3.1:8b-instruct
```

### Disable Native Tools (Fallback)

If native tool calling fails, use regex-based extraction:

```bash
OLLAMA_NATIVE_TOOLS=false
```

This uses markdown code block format instead:
~~~
```tool_call
{"tool": "classify_columns", "arguments": {...}}
```
~~~

---

## Best Practices

1. **Context Window**: Use 32k+ for better tool calling performance
   ```bash
   OLLAMA_NUM_CTX=32000
   ```

2. **Keep Model Loaded**: Reduce cold start latency
   ```bash
   OLLAMA_KEEP_ALIVE=10m
   ```

3. **Test Before Deploy**: Verify tool calling works with your specific use case

4. **Monitor Logs**: Watch for these warning signs:
   - "No tool calls, final response" when tool was expected
   - Stream ending without `done=True`
   - Empty content after many tokens streamed

---

## Sources

- [Ollama Tool Calling Docs](https://docs.ollama.com/capabilities/tool-calling)
- [Ollama Tools Models List](https://ollama.com/search?c=tools)
- [Top Ollama Models for Function Calling 2025](https://collabnix.com/best-ollama-models-for-function-calling-tools-complete-guide-2025/)
- [Ollama Tool Support Blog](https://ollama.com/blog/tool-support)

---

## Changelog

- **2025-01-10**: Initial document after investigating Ministral tool calling issues
