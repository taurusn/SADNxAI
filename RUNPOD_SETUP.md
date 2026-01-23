# SADNxAI RunPod Deployment Guide

Complete guide for deploying SADNxAI on RunPod GPU servers.

## Overview

SADNxAI is a Saudi-focused Data Anonymization Platform for banking/financial institutions. It uses AI (LLM) to guide users through anonymizing sensitive datasets while ensuring PDPL & SAMA compliance.

### Architecture

| Service | Port | Technology | Purpose |
|---------|------|------------|---------|
| Frontend | 3000 | Next.js 14 | Chat UI with WebSocket streaming |
| Chat Service | 8000 | FastAPI | LLM orchestration, session management |
| Masking Service | 8001 | FastAPI | Anonymization engine (5 techniques) |
| Validation Service | 8002 | FastAPI | Privacy metrics (k-anonymity, l-diversity, t-closeness) |
| Redis | 6379 | Redis | Session storage |
| PostgreSQL | 5432 | PostgreSQL 14 | Classifications, regulations, audit |
| vLLM | 8080 | vLLM | LLM inference (Llama 3.1 8B) |

---

## Prerequisites

### RunPod Configuration
- **GPU**: RTX 4090 (24GB VRAM) or better
- **Template**: Ubuntu 22.04 with CUDA
- **Disk**: 20GB root + 50GB workspace volume
- **Ports**: Expose 3000, 8000, 8001, 8002, 8080

### Required Tokens
- **HuggingFace Token**: For Llama 3.1 8B (gated model)
  - Get from: https://huggingface.co/settings/tokens
  - Accept license at: https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct

---

## Initial Setup (First Run Only)

### 1. Install System Dependencies

```bash
apt-get update && apt-get install -y \
  redis-server \
  postgresql \
  postgresql-contrib \
  git
```

### 2. Setup SSH Keys (for GitHub)

```bash
ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/id_ed25519 -N ""

# Copy to workspace for persistence
cp ~/.ssh/id_ed25519* /workspace/

# Display public key to add to GitHub
cat ~/.ssh/id_ed25519.pub
```

Add the public key to: https://github.com/settings/keys

### 3. Clone Repository

```bash
cd /workspace
git clone git@github.com:taurusn/SADNxAI.git

# Create symlink from root
ln -sf /workspace/SADNxAI /root/SADNxAI
```

### 4. Setup Persistent Storage

```bash
# HuggingFace cache (for model weights ~16GB)
mkdir -p /workspace/.cache/huggingface
ln -sf /workspace/.cache/huggingface /root/.cache/huggingface

# NPM cache
mkdir -p /workspace/.npm
ln -sf /workspace/.npm /root/.npm

# Application storage
mkdir -p /workspace/storage/{input,staging,output,reports}
ln -sf /workspace/storage /storage
```

### 5. Setup PostgreSQL Database

```bash
service postgresql start

# Create user and database
su - postgres -c "psql -c \"CREATE USER sadnxai WITH PASSWORD 'sadnxai_secure_pass';\""
su - postgres -c "psql -c \"CREATE DATABASE sadnxai OWNER sadnxai;\""
su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE sadnxai TO sadnxai;\""

# Load schema (copy to temp for permissions)
cp /workspace/SADNxAI/db/init/*.sql /tmp/
chmod 644 /tmp/*.sql
su - postgres -c "psql -d sadnxai -f /tmp/001_schema.sql"
su - postgres -c "psql -d sadnxai -f /tmp/002_seed_data.sql"
```

### 6. Install Python Dependencies

```bash
cd /workspace/SADNxAI
pip install -r chat-service/requirements.txt
pip install -r masking-service/requirements.txt
pip install -r validation-service/requirements.txt
pip install vllm
```

### 7. Install Frontend Dependencies

```bash
cd /workspace/SADNxAI/frontend
npm install --legacy-peer-deps
```

### 8. Install Cloudflared

```bash
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
  -O /usr/local/bin/cloudflared
chmod +x /usr/local/bin/cloudflared
```

---

## Quick Start (Every Restart)

### Option A: Use the Startup Script

```bash
/workspace/SADNxAI/scripts/runpod-start.sh
```

### Option B: Manual Startup

#### 1. Restore Symlinks & SSH

```bash
# Restore symlinks
ln -sf /workspace/SADNxAI /root/SADNxAI
ln -sf /workspace/.cache/huggingface /root/.cache/huggingface
ln -sf /workspace/.npm /root/.npm
ln -sf /workspace/storage /storage

# Restore SSH keys
cp /workspace/id_ed25519* ~/.ssh/
chmod 600 ~/.ssh/id_ed25519
```

#### 2. Start Infrastructure

```bash
# Stop nginx (it conflicts with our ports)
service nginx stop

# Start Redis
redis-server --daemonize yes

# Start PostgreSQL
service postgresql start
```

#### 3. Start vLLM (GPU LLM Server)

```bash
export HF_HOME=/workspace/.cache/huggingface
export HF_TOKEN=your_huggingface_token_here
export HUGGING_FACE_HUB_TOKEN=$HF_TOKEN

nohup vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --host 0.0.0.0 --port 8080 \
  --enable-auto-tool-choice \
  --tool-call-parser llama3_json \
  --max-model-len 32000 \
  --gpu-memory-utilization 0.9 \
  --api-key token-sadnxai \
  > /tmp/vllm.log 2>&1 &

# Wait for model to load (~60 seconds)
echo "Waiting for vLLM to load model..."
sleep 60
tail -5 /tmp/vllm.log
```

#### 4. Start Backend Services

```bash
# Environment variables
export LLM_PROVIDER=vllm
export VLLM_URL=http://localhost:8080
export VLLM_API_KEY=token-sadnxai
export VLLM_MODEL=meta-llama/Llama-3.1-8B-Instruct
export REDIS_URL=redis://localhost:6379/0
export DATABASE_URL=postgresql://sadnxai:sadnxai_secure_pass@localhost:5432/sadnxai
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

sleep 3
echo "Backend services started"
```

#### 5. Start Frontend

```bash
cd /workspace/SADNxAI/frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api \
nohup npm run dev > /tmp/frontend.log 2>&1 &

sleep 5
echo "Frontend started on port 3000"
```

#### 6. Create Cloudflare Tunnels

```bash
# Backend tunnel
nohup cloudflared tunnel --url http://localhost:8000 > /tmp/cf-backend.log 2>&1 &
sleep 8
BACKEND_URL=$(grep -o "https://[^ ]*trycloudflare.com" /tmp/cf-backend.log | head -1)
echo "Backend URL: $BACKEND_URL"

# Restart frontend with backend tunnel URL
pkill -f "next"
sleep 2
cd /workspace/SADNxAI/frontend
NEXT_PUBLIC_API_URL=${BACKEND_URL}/api \
nohup npm run dev > /tmp/frontend.log 2>&1 &
sleep 5

# Frontend tunnel
nohup cloudflared tunnel --url http://localhost:3000 > /tmp/cf-frontend.log 2>&1 &
sleep 8
FRONTEND_URL=$(grep -o "https://[^ ]*trycloudflare.com" /tmp/cf-frontend.log | head -1)

echo ""
echo "=============================================="
echo "  SADNxAI is LIVE!"
echo "=============================================="
echo "  Frontend: $FRONTEND_URL"
echo "  Backend:  $BACKEND_URL"
echo "=============================================="
```

---

## Troubleshooting

### Common Issues

#### 1. CORS Errors
The chat service needs CORS configured for cloudflare tunnels. Check `chat-service/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.trycloudflare\.com|http://localhost:.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
```

#### 2. Port Already in Use
```bash
# Check what's using a port
ss -tlnp | grep <port>

# Kill process on port
fuser -k <port>/tcp
```

#### 3. vLLM Out of Memory
Reduce model length or GPU memory utilization:
```bash
--max-model-len 16000 \
--gpu-memory-utilization 0.8
```

#### 4. Disk Space Issues
Move caches to workspace:
```bash
# Check disk usage
df -h / /workspace

# Move HuggingFace cache
mv /root/.cache/huggingface/* /workspace/.cache/huggingface/
ln -sf /workspace/.cache/huggingface /root/.cache/huggingface
```

#### 5. Module Not Found Errors
Set PYTHONPATH correctly:
```bash
export PYTHONPATH=/workspace/SADNxAI:/workspace/SADNxAI/<service-name>
```

#### 6. Nginx Conflicts
Stop nginx as it uses ports 8001:
```bash
service nginx stop
```

### Check Service Status

```bash
# All services
ss -tlnp | grep -E "3000|8000|8001|8002|8080|6379|5432"

# Service logs
tail -f /tmp/vllm.log
tail -f /tmp/chat.log
tail -f /tmp/masking.log
tail -f /tmp/validation.log
tail -f /tmp/frontend.log
tail -f /tmp/cf-backend.log
tail -f /tmp/cf-frontend.log

# Health checks
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:8002/health
curl -H "Authorization: Bearer token-sadnxai" http://localhost:8080/v1/models
redis-cli ping
```

---

## Workspace Structure

```
/workspace/
├── SADNxAI/                    # Project repository
│   ├── chat-service/           # FastAPI chat orchestration
│   ├── masking-service/        # Anonymization engine
│   ├── validation-service/     # Privacy metrics
│   ├── frontend/               # Next.js UI
│   ├── shared/                 # Shared models
│   ├── db/                     # Database schemas
│   └── scripts/                # Utility scripts
├── .cache/
│   └── huggingface/            # Model weights (~16GB)
├── .npm/                       # NPM cache
├── storage/                    # Application data
│   ├── input/                  # Uploaded CSV files
│   ├── staging/                # Processing files
│   ├── output/                 # Anonymized outputs
│   └── reports/                # PDF reports
├── id_ed25519                  # SSH private key
└── id_ed25519.pub              # SSH public key
```

---

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `vllm` | LLM provider (vllm, ollama, claude) |
| `VLLM_URL` | `http://localhost:8080` | vLLM server URL |
| `VLLM_API_KEY` | `token-sadnxai` | vLLM API key |
| `VLLM_MODEL` | `meta-llama/Llama-3.1-8B-Instruct` | Model name |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection |
| `DATABASE_URL` | `postgresql://...` | PostgreSQL connection |
| `MASKING_SERVICE_URL` | `http://localhost:8001` | Masking service |
| `VALIDATION_SERVICE_URL` | `http://localhost:8002` | Validation service |
| `STORAGE_PATH` | `/storage` | File storage path |
| `HF_TOKEN` | - | HuggingFace token |
| `HF_HOME` | `/workspace/.cache/huggingface` | HF cache directory |

---

## Security Notes

1. **HuggingFace Token**: Keep `HF_TOKEN` secure, don't commit to git
2. **Database Password**: Change default password in production
3. **vLLM API Key**: Use a strong API key in production
4. **Cloudflare Tunnels**: URLs are temporary; use named tunnels for permanent URLs
5. **SSH Keys**: Keep private key secure, back up to secure location
