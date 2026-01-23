#!/bin/bash
#
# SADNxAI RunPod Startup Script
# Run this after every pod restart
#

set -e

echo "=============================================="
echo "  SADNxAI RunPod Startup Script"
echo "=============================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
HF_TOKEN="${HF_TOKEN:-your_huggingface_token_here}"
VLLM_API_KEY="${VLLM_API_KEY:-token-sadnxai}"
DB_PASSWORD="${DB_PASSWORD:-sadnxai_secure_pass}"

# Step 1: Restore symlinks
echo -e "${YELLOW}[1/8] Restoring symlinks...${NC}"
ln -sf /workspace/SADNxAI /root/SADNxAI 2>/dev/null || true
ln -sf /workspace/.cache/huggingface /root/.cache/huggingface 2>/dev/null || true
mkdir -p /root/.cache 2>/dev/null || true
ln -sf /workspace/.npm /root/.npm 2>/dev/null || true
ln -sf /workspace/storage /storage 2>/dev/null || true

# Restore SSH keys
if [ -f /workspace/id_ed25519 ]; then
    mkdir -p ~/.ssh
    cp /workspace/id_ed25519* ~/.ssh/
    chmod 600 ~/.ssh/id_ed25519
    echo -e "${GREEN}  SSH keys restored${NC}"
fi

# Step 2: Stop conflicting services
echo -e "${YELLOW}[2/8] Stopping conflicting services...${NC}"
service nginx stop 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true
pkill -f "next" 2>/dev/null || true
pkill -f "vllm" 2>/dev/null || true
sleep 2

# Step 3: Start infrastructure
echo -e "${YELLOW}[3/8] Starting infrastructure...${NC}"
redis-server --daemonize yes
service postgresql start
sleep 2

# Check Redis
if redis-cli ping | grep -q "PONG"; then
    echo -e "${GREEN}  Redis: OK${NC}"
else
    echo -e "${RED}  Redis: FAILED${NC}"
    exit 1
fi

# Check PostgreSQL
if service postgresql status | grep -q "online"; then
    echo -e "${GREEN}  PostgreSQL: OK${NC}"
else
    echo -e "${RED}  PostgreSQL: FAILED${NC}"
    exit 1
fi

# Step 4: Start vLLM
echo -e "${YELLOW}[4/8] Starting vLLM (this takes ~60 seconds)...${NC}"
export HF_HOME=/workspace/.cache/huggingface
export HF_TOKEN=$HF_TOKEN
export HUGGING_FACE_HUB_TOKEN=$HF_TOKEN

nohup vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --host 0.0.0.0 --port 8080 \
  --enable-auto-tool-choice \
  --tool-call-parser llama3_json \
  --max-model-len 32000 \
  --gpu-memory-utilization 0.9 \
  --api-key $VLLM_API_KEY \
  > /tmp/vllm.log 2>&1 &

# Wait for vLLM to be ready
echo "  Waiting for model to load..."
for i in {1..120}; do
    if curl -s -H "Authorization: Bearer $VLLM_API_KEY" http://localhost:8080/v1/models | grep -q "Llama"; then
        echo -e "${GREEN}  vLLM: OK${NC}"
        break
    fi
    if [ $i -eq 120 ]; then
        echo -e "${RED}  vLLM: TIMEOUT (check /tmp/vllm.log)${NC}"
        exit 1
    fi
    sleep 1
    echo -ne "  Loading: $i/120 seconds\r"
done

# Step 5: Start backend services
echo -e "${YELLOW}[5/8] Starting backend services...${NC}"

export LLM_PROVIDER=vllm
export VLLM_URL=http://localhost:8080
export VLLM_API_KEY=$VLLM_API_KEY
export VLLM_MODEL=meta-llama/Llama-3.1-8B-Instruct
export REDIS_URL=redis://localhost:6379/0
export DATABASE_URL=postgresql://sadnxai:${DB_PASSWORD}@localhost:5432/sadnxai
export MASKING_SERVICE_URL=http://localhost:8001
export VALIDATION_SERVICE_URL=http://localhost:8002
export STORAGE_PATH=/storage

# Masking Service
cd /workspace/SADNxAI/masking-service
PYTHONPATH=/workspace/SADNxAI:/workspace/SADNxAI/masking-service \
nohup python -m uvicorn main:app --host 0.0.0.0 --port 8001 > /tmp/masking.log 2>&1 &

# Validation Service
cd /workspace/SADNxAI/validation-service
PYTHONPATH=/workspace/SADNxAI:/workspace/SADNxAI/validation-service \
nohup python -m uvicorn main:app --host 0.0.0.0 --port 8002 > /tmp/validation.log 2>&1 &

# Chat Service
cd /workspace/SADNxAI/chat-service
PYTHONPATH=/workspace/SADNxAI:/workspace/SADNxAI/chat-service \
nohup python -m uvicorn main:app --host 0.0.0.0 --port 8000 > /tmp/chat.log 2>&1 &

sleep 5

# Check services
for port in 8000 8001 8002; do
    if curl -s http://localhost:$port/health | grep -q "healthy"; then
        echo -e "${GREEN}  Port $port: OK${NC}"
    else
        echo -e "${RED}  Port $port: FAILED${NC}"
    fi
done

# Step 6: Start Cloudflare tunnel for backend
echo -e "${YELLOW}[6/8] Starting backend tunnel...${NC}"
nohup cloudflared tunnel --url http://localhost:8000 > /tmp/cf-backend.log 2>&1 &
sleep 10
BACKEND_URL=$(grep -o "https://[^ ]*trycloudflare.com" /tmp/cf-backend.log | head -1)
if [ -n "$BACKEND_URL" ]; then
    echo -e "${GREEN}  Backend tunnel: $BACKEND_URL${NC}"
else
    echo -e "${RED}  Backend tunnel: FAILED${NC}"
    exit 1
fi

# Step 7: Start frontend with tunnel URL
echo -e "${YELLOW}[7/8] Starting frontend...${NC}"
cd /workspace/SADNxAI/frontend
NEXT_PUBLIC_API_URL=${BACKEND_URL}/api \
nohup npm run dev > /tmp/frontend.log 2>&1 &
sleep 8

if ss -tlnp | grep -q ":3000"; then
    echo -e "${GREEN}  Frontend: OK${NC}"
else
    echo -e "${RED}  Frontend: FAILED${NC}"
fi

# Step 8: Start Cloudflare tunnel for frontend
echo -e "${YELLOW}[8/8] Starting frontend tunnel...${NC}"
nohup cloudflared tunnel --url http://localhost:3000 > /tmp/cf-frontend.log 2>&1 &
sleep 10
FRONTEND_URL=$(grep -o "https://[^ ]*trycloudflare.com" /tmp/cf-frontend.log | head -1)

# Final status
echo ""
echo "=============================================="
echo -e "${GREEN}  SADNxAI is LIVE!${NC}"
echo "=============================================="
echo ""
echo "  Access the app:"
echo -e "  ${GREEN}$FRONTEND_URL${NC}"
echo ""
echo "  Backend API:"
echo "  $BACKEND_URL"
echo ""
echo "  Service Status:"
ss -tlnp | grep -E "3000|8000|8001|8002|8080|6379" | awk '{print "  " $1 " " $4}'
echo ""
echo "  Logs:"
echo "  tail -f /tmp/vllm.log"
echo "  tail -f /tmp/chat.log"
echo "  tail -f /tmp/frontend.log"
echo "=============================================="

# Save URLs to file for reference
cat > /tmp/sadnxai-urls.txt << EOF
FRONTEND_URL=$FRONTEND_URL
BACKEND_URL=$BACKEND_URL
EOF

echo ""
echo "URLs saved to /tmp/sadnxai-urls.txt"
