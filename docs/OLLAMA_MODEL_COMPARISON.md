# Ollama Model Comparison for Tool Calling

> Last Updated: 2025-01-10

This document summarizes our research on Ollama models for reliable tool/function calling in SADNxAI.

## Current Issue

SADNxAI uses **5 tools** for the agentic loop:
- `classify_columns`
- `execute_pipeline`
- `update_thresholds`
- `query_regulations`
- `get_current_thresholds`

## Model Analysis

### Ministral 3B (ministral-3:14b) - BROKEN

**Status**: Does not work with >2 tools

**Issue**: Known Ollama bug - [Issue #13328](https://github.com/ollama/ollama/issues/13328)

When using more than 2 tools:
- Model describes what it would do in natural language
- Never outputs actual tool calls
- Stream ends without `done=True` in some cases

**Example failure**:
```
I'll classify the columns in your CSV file...
[describes classification but never calls classify_columns]
```

### Qwen2.5 (qwen2.5:7b, qwen2.5:14b)

**Status**: Unreliable

**Issues**:
1. **Empty responses** - Sometimes returns empty content with no tool calls
2. **Hallucinated tool calls** - Invents tools that don't exist
3. **Partial JSON** - Tool call arguments sometimes truncated
4. **Context sensitivity** - Performance degrades with longer conversations

**References**:
- [Ollama Issue #7695](https://github.com/ollama/ollama/issues/7695) - Tool calling issues
- [Ollama Issue #8389](https://github.com/ollama/ollama/issues/8389) - Empty responses

### GLM4 (glm4:9b)

**Status**: Template incompatible

**Issues**:
1. **Chat template mismatch** - Ollama's default template doesn't match GLM4's expected format
2. **Tool format different** - GLM4 expects different tool definition schema
3. **No official Ollama support** - Community model with varying quality

**Workaround**: Would require custom Modelfile with correct template (complex)

### Llama 3.1 8B Instruct

**Status**: RECOMMENDED

**Why it works**:
- Native function calling support in architecture
- Well-tested in Ollama
- Reliable with multiple tools (5+)
- Good balance of speed and capability

**Model**: `llama3.1:8b-instruct`

### Qwen3 (qwen3:8b)

**Status**: Good alternative

**Improvements over Qwen2.5**:
- Better tool calling reliability
- Improved JSON formatting
- Less hallucination

**Model**: `qwen3:8b`

### Mistral Nemo 12B

**Status**: Good alternative

**Strengths**:
- Excellent instruction following
- Reliable tool calling
- Good reasoning

**Model**: `mistral-nemo:12b`

## Recommendation Table

| Model | Size | Tool Calling | Speed | Recommendation |
|-------|------|--------------|-------|----------------|
| llama3.1:8b-instruct | 8B | Excellent | Fast | **Best Choice** |
| qwen3:8b | 8B | Good | Fast | Alternative |
| mistral-nemo:12b | 12B | Good | Medium | Alternative |
| qwen2.5:14b | 14B | Poor | Slow | Not Recommended |
| ministral-3:14b | 14B | Broken (>2 tools) | Slow | Do Not Use |
| glm4:9b | 9B | Incompatible | Medium | Do Not Use |

## Migration Steps

1. Pull new model:
   ```bash
   docker exec ollama ollama pull llama3.1:8b-instruct
   ```

2. Update environment variable:
   ```env
   OLLAMA_MODEL=llama3.1:8b-instruct
   ```

3. Restart chat-service:
   ```bash
   docker compose restart chat-service
   ```

4. Test with a new session and file upload

## Testing Tool Calling

Quick test to verify model works:

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.1:8b-instruct",
  "messages": [{"role": "user", "content": "What is 2+2?"}],
  "tools": [
    {"type": "function", "function": {"name": "add", "parameters": {"type": "object", "properties": {"a": {"type": "number"}, "b": {"type": "number"}}}}},
    {"type": "function", "function": {"name": "subtract", "parameters": {"type": "object", "properties": {"a": {"type": "number"}, "b": {"type": "number"}}}}},
    {"type": "function", "function": {"name": "multiply", "parameters": {"type": "object", "properties": {"a": {"type": "number"}, "b": {"type": "number"}}}}},
    {"type": "function", "function": {"name": "divide", "parameters": {"type": "object", "properties": {"a": {"type": "number"}, "b": {"type": "number"}}}}},
    {"type": "function", "function": {"name": "power", "parameters": {"type": "object", "properties": {"a": {"type": "number"}, "b": {"type": "number"}}}}}
  ],
  "stream": false
}'
```

Expected: Response should include `"tool_calls"` with `add` function.

## References

- [Ollama Tool Calling Documentation](https://ollama.com/blog/tool-support)
- [Ollama Issue #13328](https://github.com/ollama/ollama/issues/13328) - Ministral >2 tools bug
- [Ollama Issue #7695](https://github.com/ollama/ollama/issues/7695) - Qwen2.5 tool issues
- [Ollama Issue #8389](https://github.com/ollama/ollama/issues/8389) - Empty response bug
