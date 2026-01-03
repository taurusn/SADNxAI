# AI ↔ Chat Implementation Fix Plan

## Executive Summary

This plan addresses **23 identified issues** across 6 categories in the AI/Chat implementation. Fixes are ordered by dependency and impact.

---

## Issue Inventory

| Category | Critical | High | Medium | Total |
|----------|----------|------|--------|-------|
| Tool Extraction | 3 | 2 | 1 | 6 |
| Retry & Recovery | 2 | 1 | 0 | 3 |
| State Management | 1 | 2 | 1 | 4 |
| Prompt Engineering | 1 | 2 | 2 | 5 |
| Streaming | 1 | 1 | 1 | 3 |
| Architecture | 0 | 1 | 1 | 2 |
| **Total** | **8** | **9** | **6** | **23** |

---

## Phase 1: Critical Fixes (Stop the Bleeding)

### 1.1 Fix Brace Counting in JSON Extraction

**File:** `chat-service/llm/ollama_adapter.py`
**Lines:** 544-549 (also `adapter.py:293-297`)
**Severity:** CRITICAL

**Current (broken):**
```python
for i, c in enumerate(content[start:], start):
    if c == '{':
        brace_count += 1
    elif c == '}':
        brace_count -= 1
```

**Problem:** Counts braces inside JSON strings. `{"text": "has } here"}` breaks.

**Fix:** Track whether we're inside a quoted string:
```python
def _find_json_end(self, content: str, start: int) -> int:
    """Find end of JSON object respecting strings."""
    brace_count = 0
    in_string = False
    escape_next = False

    for i, c in enumerate(content[start:], start):
        if escape_next:
            escape_next = False
            continue
        if c == '\\' and in_string:
            escape_next = True
            continue
        if c == '"' and not escape_next:
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == '{':
            brace_count += 1
        elif c == '}':
            brace_count -= 1
            if brace_count == 0:
                return i + 1
    return -1  # Unclosed JSON
```

**Apply to:**
- `ollama_adapter.py:544-549` (`_clean_response`)
- `ollama_adapter.py:467-481` (Pattern 3 extraction)
- `adapter.py:293-297` (streaming filter)

---

### 1.2 Fix Retry Condition (Trigger on Missing Tools)

**File:** `chat-service/llm/ollama_adapter.py`
**Lines:** 160-168
**Severity:** CRITICAL

**Current (broken):**
```python
if validation_errors and attempt < max_retries:
    # Retry
```

**Problem:** If LLM outputs text without any tool call, `validation_errors` is empty, no retry happens.

**Fix:** Also retry when tools were expected but not found:
```python
# Determine if we expected a tool call based on session state
expects_tool = session_context and session_context.get("status") in [
    "ANALYZING", "PROPOSED", "DISCUSSING", "FAILED"
]

# Retry if: validation errors OR (expected tools but got none)
should_retry = (
    (validation_errors or (expects_tool and not tool_calls))
    and attempt < max_retries
)

if should_retry:
    error_feedback = validation_errors if validation_errors else [
        "You must call a tool. Use classify_columns, execute_pipeline, or update_thresholds."
    ]
    full_messages.append({"role": "assistant", "content": assistant_message})
    full_messages.append({
        "role": "user",
        "content": f"Error: {error_feedback}. Please respond with a valid tool call."
    })
    continue
```

---

### 1.3 Add Native Tools Support to Streaming

**File:** `chat-service/llm/ollama_adapter.py`
**Lines:** 227-236, 267-286
**Severity:** CRITICAL

**Current (broken):** `chat_stream()` ignores native tools entirely.

**Fix Part A - Add tools to payload (after line 236):**
```python
payload = {
    "model": self.model,
    "messages": full_messages,
    "stream": True,
    "keep_alive": "10m",
    "options": {
        "temperature": 0.1,
        "num_ctx": 24000,
    }
}

# ADD: Native tools support
if self.use_native_tools:
    payload["tools"] = self.tools
```

**Fix Part B - Check native tools before regex (replace lines 267-286):**
```python
if data.get("done", False):
    tool_calls = None

    # Check for native tool calls first
    native_tool_calls = message.get("tool_calls")
    if native_tool_calls and self.use_native_tools:
        tool_calls = []
        for i, tc in enumerate(native_tool_calls):
            func = tc.get("function", {})
            tool_calls.append({
                "id": f"call_{i}",
                "type": "function",
                "function": {
                    "name": func.get("name"),
                    "arguments": json.dumps(func.get("arguments", {}))
                }
            })
        print(f"[LLM Response] Native tool calls: {len(tool_calls)}")
    else:
        # Fallback to regex extraction
        tool_calls = self._extract_tool_calls(full_content)
        print(f"[LLM Response] Regex tool calls: {len(tool_calls) if tool_calls else 0}")

    if tool_calls:
        full_content = self._clean_response(full_content)

    yield {
        "type": "done",
        "content": full_content,
        "tool_calls": tool_calls
    }
    return
```

---

### 1.4 Fix Approval Detection (Word Boundaries)

**File:** `chat-service/core/conversation.py`
**Lines:** 162-175
**Severity:** CRITICAL

**Current (broken):**
```python
for phrase in approval_phrases:
    if phrase in message_lower:  # Substring match!
        return True
```

**Problem:** "disapprove" contains "approve" → false positive.

**Fix:** Use word boundary regex:
```python
import re

def detect_approval(self, message: str) -> bool:
    """Detect if message contains approval intent."""
    message_lower = message.lower().strip()

    # Negative phrases take priority
    rejection_phrases = [
        "don't", "do not", "no", "stop", "wait", "cancel",
        "disapprove", "reject", "hold", "not yet", "change"
    ]
    for phrase in rejection_phrases:
        if re.search(rf'\b{re.escape(phrase)}\b', message_lower):
            return False

    # Check for approval (whole word match)
    approval_phrases = [
        "approve", "approved", "yes", "proceed", "go ahead",
        "execute", "run it", "do it", "let's go", "confirm",
        "agreed", "looks good", "lgtm", "ship it"
    ]
    for phrase in approval_phrases:
        if re.search(rf'\b{re.escape(phrase)}\b', message_lower):
            return True

    return False
```

---

### 1.5 Fix State Validation for Pipeline Execution

**File:** `chat-service/llm/tools.py`
**Lines:** 333-338
**Severity:** CRITICAL

**Current (broken):**
```python
if session.status not in [SessionStatus.APPROVED, SessionStatus.PROPOSED, SessionStatus.DISCUSSING]:
    return {"error": "..."}
```

**Problem:** Allows execution from PROPOSED/DISCUSSING without explicit approval.

**Fix:** Only allow APPROVED state:
```python
if session.status != SessionStatus.APPROVED:
    if session.status in [SessionStatus.PROPOSED, SessionStatus.DISCUSSING]:
        return {
            "error": "Cannot execute pipeline without user approval. "
                     "Please wait for user to confirm with 'approve', 'proceed', or similar.",
            "requires_approval": True
        }
    return {
        "error": f"Cannot execute pipeline in {session.status.value} state. "
                 "Classification and approval required first."
    }
```

---

### 1.6 Add Error Handling for Tool Argument Parsing

**File:** `chat-service/api/routes.py`
**Lines:** 258-262
**Severity:** CRITICAL

**Current (broken):**
```python
args = json.loads(tc["function"]["arguments"])  # Can crash
```

**Fix:**
```python
try:
    args_raw = tc["function"]["arguments"]
    # Handle both string and dict (Claude sends dict, Ollama sends string)
    if isinstance(args_raw, str):
        args = json.loads(args_raw)
    else:
        args = args_raw
except (json.JSONDecodeError, TypeError, KeyError) as e:
    print(f"[Agentic Loop] Failed to parse tool arguments: {e}")
    yield _sse_event("error", {"message": f"Invalid tool arguments: {e}"})
    continue
```

---

### 1.7 Fix Index Calculation in Raw JSON Parsing

**File:** `chat-service/llm/ollama_adapter.py`
**Lines:** 467-481
**Severity:** HIGH

**Current (broken):**
```python
parsed, end_offset = decoder.raw_decode(content, start)
# ...
idx = start + end_offset  # end_offset is relative, not absolute
```

**Fix:**
```python
parsed, end_offset = decoder.raw_decode(content, start)
if "tool" in parsed and "arguments" in parsed:
    matches.append(json.dumps(parsed))
idx = start + end_offset  # This is actually correct - raw_decode returns position relative to start
```

Actually, looking closer - `raw_decode(s, idx)` returns `(obj, end)` where `end` is the index in `s` where parsing stopped. So `end_offset` is already absolute. But the issue is:

```python
idx = start + end_offset  # WRONG - end_offset is already absolute
```

**Correct fix:**
```python
idx = end_offset  # end_offset is the absolute position where parsing ended
```

---

### 1.8 Fix Regex Pattern for Escaped Characters

**File:** `chat-service/llm/ollama_adapter.py`
**Lines:** 459-461
**Severity:** HIGH

**Current (broken):**
```python
pattern2 = r'```(?:json)?\s*\n?(\{[^`]*"tool"[^`]*\})\n?```'
```

**Problem:** `[^`]*` fails if JSON contains backticks.

**Fix:** Use a more robust approach - match the code fence, then parse JSON separately:
```python
# Pattern 2: Find json code blocks
pattern2 = r'```(?:json)?\s*\n?([\s\S]*?)\n?```'
for match in re.findall(pattern2, content, re.DOTALL):
    match = match.strip()
    if '"tool"' in match and match.startswith('{'):
        try:
            parsed = json.loads(match)
            if "tool" in parsed:
                matches.append(match)
        except json.JSONDecodeError:
            continue  # Not valid JSON, skip
```

---

## Phase 2: High Priority Fixes

### 2.1 Add Validation for Threshold Ordering

**File:** `chat-service/llm/tools.py`
**Lines:** 389-402
**Severity:** HIGH

**Current:** No check that minimum ≤ target.

**Fix:**
```python
def _validate_thresholds(self, args: Dict[str, Any]) -> Optional[str]:
    """Validate threshold values and ordering."""
    # Range validation
    validations = [
        ("k_anonymity", 1, 1000),
        ("l_diversity", 1, 100),
        ("t_closeness", 0.0, 1.0),
        ("risk_score", 0, 100),
    ]

    for prefix, min_val, max_val in validations:
        for suffix in ["_minimum", "_target"]:
            key = f"{prefix}{suffix}"
            if key in args:
                val = args[key]
                if not (min_val <= val <= max_val):
                    return f"{key} must be between {min_val} and {max_val}"

    # Ordering validation: minimum <= target
    pairs = [
        ("k_anonymity_minimum", "k_anonymity_target"),
        ("l_diversity_minimum", "l_diversity_target"),
        ("risk_score_maximum", "risk_score_target"),  # Note: risk is inverted
    ]
    for min_key, target_key in pairs:
        if min_key in args and target_key in args:
            if min_key == "risk_score_maximum":
                # Risk: target should be <= maximum
                if args[target_key] > args[min_key]:
                    return f"{target_key} must be <= {min_key}"
            else:
                # Others: minimum should be <= target
                if args[min_key] > args[target_key]:
                    return f"{min_key} must be <= {target_key}"

    # t_closeness: target should be <= maximum (lower is better)
    if "t_closeness_maximum" in args and "t_closeness_target" in args:
        if args["t_closeness_target"] > args["t_closeness_maximum"]:
            return "t_closeness_target must be <= t_closeness_maximum"

    return None  # Valid
```

---

### 2.2 Add Message History Truncation

**File:** `chat-service/core/conversation.py`
**Lines:** 58-76
**Severity:** HIGH

**Current:** Messages grow unbounded.

**Fix:** Add truncation method:
```python
MAX_MESSAGES = 50  # Keep last 50 messages
MAX_CONTEXT_TOKENS = 20000  # Approximate token limit

def _truncate_messages(self, messages: List[Dict]) -> List[Dict]:
    """Truncate message history to fit context window."""
    if len(messages) <= MAX_MESSAGES:
        return messages

    # Always keep first message (often contains important context)
    # and last N messages
    truncated = [messages[0]] + messages[-(MAX_MESSAGES-1):]

    # Add truncation notice
    truncated.insert(1, {
        "role": "system",
        "content": f"[Earlier messages truncated. Showing first and last {MAX_MESSAGES-1} messages.]"
    })

    return truncated

def get_messages_for_llm(self) -> List[Dict]:
    """Build message list for LLM with truncation."""
    messages = self._truncate_messages(self.session.messages)
    # ... rest of existing logic
```

---

### 2.3 Fix Double Serialization of Tool Arguments

**File:** `chat-service/llm/adapter.py`
**Lines:** 110-117
**Severity:** HIGH

**Current (broken):**
```python
"arguments": json.dumps(block.input)  # block.input might already be serialized
```

**Fix:**
```python
# Handle both dict and string inputs
args = block.input
if isinstance(args, dict):
    args = json.dumps(args)
elif not isinstance(args, str):
    args = json.dumps(args)
# If already a string, use as-is

result["tool_calls"].append({
    "id": block.id,
    "type": "function",
    "function": {
        "name": block.name,
        "arguments": args
    }
})
```

---

### 2.4 Add Tool Execution Timeout

**File:** `chat-service/api/routes.py`
**Lines:** 136, 272
**Severity:** HIGH

**Current:** No timeout on tool execution.

**Fix:**
```python
import asyncio

TOOL_TIMEOUT = 30.0  # 30 seconds

try:
    result = await asyncio.wait_for(
        tool_executor.execute(tool_name, args),
        timeout=TOOL_TIMEOUT
    )
except asyncio.TimeoutError:
    result = {"error": f"Tool '{tool_name}' timed out after {TOOL_TIMEOUT}s"}
    print(f"[Agentic Loop] Tool timeout: {tool_name}")
```

---

### 2.5 Log Tool Extraction Details

**File:** `chat-service/llm/ollama_adapter.py`
**Lines:** 445-490
**Severity:** HIGH

**Add logging to diagnose extraction failures:**
```python
def _extract_tool_calls_with_errors(self, content: str) -> Tuple[List, List]:
    """Extract tool calls with detailed logging."""
    matches = []
    validation_errors = []

    # Pattern 1
    p1_matches = re.findall(r'```tool_call\s*\n?(.*?)\n?```', content, re.DOTALL)
    print(f"[Tool Extraction] Pattern 1 (tool_call fence): {len(p1_matches)} matches")
    matches.extend(p1_matches)

    # Pattern 2
    if not matches:
        p2_matches = re.findall(r'```(?:json)?\s*\n?([\s\S]*?)\n?```', content, re.DOTALL)
        p2_valid = [m for m in p2_matches if '"tool"' in m and m.strip().startswith('{')]
        print(f"[Tool Extraction] Pattern 2 (json fence): {len(p2_valid)} matches")
        matches.extend(p2_valid)

    # Pattern 3
    if not matches:
        p3_matches = self._extract_raw_json_tools(content)
        print(f"[Tool Extraction] Pattern 3 (raw JSON): {len(p3_matches)} matches")
        matches.extend(p3_matches)

    print(f"[Tool Extraction] Total matches before validation: {len(matches)}")

    # ... rest of validation logic
```

---

## Phase 3: Prompt Engineering Fixes

### 3.1 Add Negative Examples to System Prompt

**File:** `shared/openai_schema.py`
**Lines:** After 328
**Severity:** HIGH

**Add section:**
```python
## COMMON MISTAKES - DO NOT DO THESE

❌ WRONG - Using example column names:
```tool_call
{"tool": "classify_columns", "arguments": {"direct_identifiers": ["national_id", "customer_name"]}}
```
These are EXAMPLE names. Use the ACTUAL column names from the uploaded file.

❌ WRONG - Reasoning as array:
```tool_call
{"tool": "classify_columns", "arguments": {"reasoning": {"col": ["reason1", "reason2"]}}}
```
Reasoning values must be STRINGS, not arrays.

❌ WRONG - Describing instead of calling:
"I will now classify the columns as follows: national_id is a direct identifier..."
You must output the tool_call block, not describe what you would do.

✅ CORRECT:
```tool_call
{"tool": "classify_columns", "arguments": {"direct_identifiers": ["ActualColumnFromFile"], "reasoning": {"ActualColumnFromFile": "Contains national ID pattern"}}}
```
```

---

### 3.2 Clarify Quasi-Identifier vs Sensitive Attribute

**File:** `shared/openai_schema.py`
**Lines:** 244-260
**Severity:** MEDIUM

**Add clarification:**
```python
## DECISION GUIDE: Quasi-Identifier vs Sensitive Attribute

ASK: "Could this column help RE-IDENTIFY someone when combined with others?"

| Column Type | Re-identification Risk | Classification |
|-------------|----------------------|----------------|
| age, gender, city, occupation | YES - demographic linkage | quasi_identifier |
| transaction_amount, fraud_flag | NO - these are outcomes | sensitive_attribute |
| salary, income_bracket | MAYBE - demographic proxy | quasi_identifier |
| diagnosis, credit_score | NO - analysis targets | sensitive_attribute |

RULE: When unsure, prefer quasi_identifier (safer - will be generalized).
```

---

### 3.3 Add Column Validation Reminder in State Prompts

**File:** `shared/prompts/analyzing.py` (or equivalent)
**Severity:** MEDIUM

**Add:**
```python
CRITICAL VALIDATION:
Before calling classify_columns, verify:
1. Every column name matches EXACTLY what's in the file (case-sensitive)
2. You've classified ALL columns from the file
3. No column appears in multiple categories

The column names from the uploaded file are:
{column_list}

Use ONLY these names. Do not invent or guess column names.
```

---

### 3.4 Strengthen Tool Call Format Instructions

**File:** `shared/openai_schema.py`
**Lines:** 318-327
**Severity:** MEDIUM

**Make format unambiguous:**
```python
## TOOL CALL FORMAT (MANDATORY)

You MUST output tool calls in this EXACT format:

```tool_call
{"tool": "TOOL_NAME", "arguments": {...}}
```

RULES:
1. Use triple backticks with "tool_call" label
2. JSON must be valid (use double quotes, no trailing commas)
3. One tool call per block
4. Do NOT explain the tool call - just output the block
5. The opening ``` and closing ``` must be on their own lines
```

---

### 3.5 Remove Conflicting Instructions

**File:** `shared/openai_schema.py`
**Severity:** MEDIUM

**Current conflicts:**
- Line 278: "Call classify_columns IMMEDIATELY"
- Line 287: "If unsure, classify as sensitive_attributes"

**Fix:** Remove "IMMEDIATELY", add decision process:
```python
WORKFLOW:
1. Read the sample data carefully
2. Identify each column's purpose from the data values
3. Classify based on re-identification risk
4. Call classify_columns with your classification

Take time to analyze. Accuracy > Speed.
```

---

## Phase 4: Architecture Improvements

### 4.1 Add Idempotency to Pipeline Execution

**File:** `chat-service/llm/tools.py`
**Lines:** 321-381
**Severity:** MEDIUM

**Problem:** Multiple execute_pipeline calls can run simultaneously.

**Fix:** Add execution lock:
```python
# In ToolExecutor.__init__
self._pipeline_lock = asyncio.Lock()
self._last_execution_id: Optional[str] = None

async def _handle_execute_pipeline(self, args: Dict[str, Any]) -> Dict[str, Any]:
    async with self._pipeline_lock:
        # Generate execution ID
        execution_id = f"{self.session.id}_{int(time.time())}"

        # Check for duplicate execution
        if self._last_execution_id == execution_id[:len(self._last_execution_id)] if self._last_execution_id else False:
            return {"error": "Pipeline already executing", "duplicate": True}

        self._last_execution_id = execution_id

        # ... rest of execution logic
```

---

### 4.2 Cache Context Building

**File:** `chat-service/core/conversation.py`
**Severity:** MEDIUM

**Problem:** Context rebuilt every turn.

**Fix:** Cache with invalidation:
```python
def __init__(self, session: Session):
    self.session = session
    self._context_cache: Optional[str] = None
    self._context_hash: Optional[str] = None

def _build_context(self) -> str:
    """Build context with caching."""
    # Compute hash of context-relevant state
    state_hash = hashlib.md5(
        f"{self.session.status}{self.session.classification}{self.session.thresholds}".encode()
    ).hexdigest()

    if self._context_hash == state_hash and self._context_cache:
        return self._context_cache

    # Rebuild context
    context = self._build_context_internal()
    self._context_cache = context
    self._context_hash = state_hash
    return context
```

---

## Phase 5: Observability

### 5.1 Structured Logging

**All files**
**Severity:** MEDIUM

**Replace print() with structured logging:**
```python
import structlog

logger = structlog.get_logger()

# Instead of:
print(f"[Tool Extraction] Pattern 1: {len(matches)} matches")

# Use:
logger.info("tool_extraction", pattern=1, matches=len(matches), content_length=len(content))
```

---

### 5.2 Add SSE Error Events

**File:** `chat-service/api/routes.py`
**Severity:** MEDIUM

**Add error event type:**
```python
def _sse_error(error_type: str, message: str, details: Dict = None) -> str:
    """Create SSE error event."""
    return _sse_event("error", {
        "error_type": error_type,
        "message": message,
        "details": details or {}
    })

# Usage:
yield _sse_error("tool_extraction_failed", "No tool calls found in response", {
    "response_length": len(content),
    "patterns_tried": 3
})
```

---

## Implementation Order

```
Week 1: Critical Fixes (Phase 1)
├── Day 1-2: Brace counting fix (1.1) + Retry condition (1.2)
├── Day 3: Native tools streaming (1.3)
├── Day 4: Approval detection (1.4) + State validation (1.5)
└── Day 5: Error handling (1.6) + Index fix (1.7) + Regex fix (1.8)

Week 2: High Priority (Phase 2)
├── Day 1: Threshold validation (2.1)
├── Day 2: Message truncation (2.2)
├── Day 3: Double serialization (2.3) + Timeout (2.4)
└── Day 4-5: Logging (2.5) + Testing

Week 3: Prompts & Architecture (Phase 3-4)
├── Day 1-2: Negative examples (3.1) + Clarifications (3.2, 3.3)
├── Day 3: Format instructions (3.4) + Conflict removal (3.5)
└── Day 4-5: Idempotency (4.1) + Caching (4.2)

Week 4: Observability & Testing (Phase 5)
├── Day 1-2: Structured logging (5.1)
├── Day 3: SSE errors (5.2)
└── Day 4-5: Integration testing + Documentation
```

---

## Success Metrics

| Metric | Current (Est.) | Target |
|--------|----------------|--------|
| Tool extraction success rate | ~60% | >95% |
| False approval triggers | ~5% | <0.1% |
| Pipeline state violations | Possible | Impossible |
| Context overflow crashes | Possible | Impossible |
| Mean time to debug issues | Hours | Minutes |

---

## Testing Strategy

### Unit Tests Needed

```python
# test_brace_counting.py
def test_json_with_brace_in_string():
    content = '{"tool": "x", "args": {"text": "has } brace"}}'
    result = find_json_end(content, 0)
    assert result == len(content)

# test_approval_detection.py
def test_disapprove_not_approval():
    assert detect_approval("I disapprove") == False
    assert detect_approval("approve this") == True

# test_retry_trigger.py
def test_retry_on_missing_tools():
    # Mock LLM returning text instead of tool call
    # Verify retry is triggered
```

### Integration Tests Needed

```python
# test_full_pipeline.py
def test_classify_execute_flow():
    # Upload CSV
    # Verify classification tool called
    # Send approval
    # Verify pipeline executes
    # Verify no state violations
```

---

## Rollback Plan

Each fix is isolated. If issues occur:

1. **Brace counting**: Revert to old logic, accept some JSON failures
2. **Native tools**: Set `OLLAMA_NATIVE_TOOLS=false`
3. **Retry condition**: Revert to validation-only retry
4. **Approval detection**: Revert to substring matching
5. **State validation**: Revert to permissive states

---

## Dependencies

```
1.1 Brace counting     ─┐
1.7 Index calculation   ├─► 1.3 Native tools streaming
1.8 Regex pattern      ─┘

1.2 Retry condition    ─► 2.5 Logging (to debug retry)

1.4 Approval detection ─► 1.5 State validation

3.1-3.5 Prompts        ─► Independent (can do anytime)

4.1-4.2 Architecture   ─► After Phase 1-2 stable
```

---

## Notes

- All fixes preserve backward compatibility
- No database migrations required
- No API contract changes
- Frontend unaffected (SSE events unchanged except new "error" type)
