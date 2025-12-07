#!/bin/bash
# SADNxAI - Ollama Model Initialization Script
# This script pulls the required model after Ollama container starts

set -e

# Configuration
OLLAMA_HOST="${OLLAMA_HOST:-localhost}"
OLLAMA_PORT="${OLLAMA_PORT:-11434}"
MODEL="${OLLAMA_MODEL:-qwen2.5:3b}"

OLLAMA_URL="http://${OLLAMA_HOST}:${OLLAMA_PORT}"

echo "=============================================="
echo "SADNxAI - Ollama Model Initialization"
echo "=============================================="
echo "Ollama URL: ${OLLAMA_URL}"
echo "Model: ${MODEL}"
echo ""

# Wait for Ollama to be ready
echo "Waiting for Ollama to be ready..."
MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s "${OLLAMA_URL}/api/tags" > /dev/null 2>&1; then
        echo "Ollama is ready!"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "  Attempt ${RETRY_COUNT}/${MAX_RETRIES}..."
    sleep 2
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo "ERROR: Ollama failed to start after ${MAX_RETRIES} attempts"
    exit 1
fi

# Check if model already exists
echo ""
echo "Checking if model '${MODEL}' is already downloaded..."
MODELS=$(curl -s "${OLLAMA_URL}/api/tags" | grep -o '"name":"[^"]*"' | grep -o '[^"]*:[^"]*' || true)

if echo "$MODELS" | grep -q "^${MODEL}$"; then
    echo "Model '${MODEL}' is already available!"
else
    echo "Model '${MODEL}' not found. Pulling..."
    echo ""

    # Pull the model
    curl -X POST "${OLLAMA_URL}/api/pull" \
        -H "Content-Type: application/json" \
        -d "{\"name\": \"${MODEL}\"}" \
        --no-buffer 2>&1 | while read -r line; do
            # Parse progress from JSON response
            STATUS=$(echo "$line" | grep -o '"status":"[^"]*"' | cut -d'"' -f4 || true)
            if [ -n "$STATUS" ]; then
                echo "  $STATUS"
            fi
        done

    echo ""
    echo "Model pull complete!"
fi

# Verify model is available
echo ""
echo "Verifying model..."
FINAL_CHECK=$(curl -s "${OLLAMA_URL}/api/tags" | grep -o "\"${MODEL}\"" || true)

if [ -n "$FINAL_CHECK" ]; then
    echo "SUCCESS: Model '${MODEL}' is ready for use!"
else
    # Try without version tag
    MODEL_BASE=$(echo "$MODEL" | cut -d':' -f1)
    FINAL_CHECK=$(curl -s "${OLLAMA_URL}/api/tags" | grep -o "\"${MODEL_BASE}" || true)
    if [ -n "$FINAL_CHECK" ]; then
        echo "SUCCESS: Model '${MODEL}' is ready for use!"
    else
        echo "WARNING: Could not verify model. It may still work."
    fi
fi

echo ""
echo "=============================================="
echo "Initialization complete!"
echo "=============================================="
