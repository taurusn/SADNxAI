#!/bin/bash
#
# SADNxAI RunPod First-Time Setup Script
# Run this ONCE when creating a new RunPod instance
#

set -e

echo "=============================================="
echo "  SADNxAI First-Time Setup"
echo "=============================================="

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if already set up
if [ -f /workspace/.sadnxai-setup-complete ]; then
    echo -e "${YELLOW}Setup already completed. Run runpod-start.sh instead.${NC}"
    exit 0
fi

# Step 1: Install system dependencies
echo -e "${YELLOW}[1/7] Installing system dependencies...${NC}"
apt-get update -qq
apt-get install -y -qq redis-server postgresql postgresql-contrib git
echo -e "${GREEN}  Done${NC}"

# Step 2: Install cloudflared
echo -e "${YELLOW}[2/7] Installing cloudflared...${NC}"
if [ ! -f /usr/local/bin/cloudflared ]; then
    wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
      -O /usr/local/bin/cloudflared
    chmod +x /usr/local/bin/cloudflared
fi
echo -e "${GREEN}  Done${NC}"

# Step 3: Setup persistent storage
echo -e "${YELLOW}[3/7] Setting up persistent storage...${NC}"
mkdir -p /workspace/.cache/huggingface
mkdir -p /workspace/.npm
mkdir -p /workspace/storage/{input,staging,output,reports}

# Create symlinks
mkdir -p /root/.cache
ln -sf /workspace/.cache/huggingface /root/.cache/huggingface
ln -sf /workspace/.npm /root/.npm
ln -sf /workspace/storage /storage
ln -sf /workspace/SADNxAI /root/SADNxAI
echo -e "${GREEN}  Done${NC}"

# Step 4: Setup PostgreSQL
echo -e "${YELLOW}[4/7] Setting up PostgreSQL...${NC}"
service postgresql start
sleep 2

su - postgres -c "psql -c \"CREATE USER sadnxai WITH PASSWORD 'sadnxai_secure_pass';\"" 2>/dev/null || true
su - postgres -c "psql -c \"CREATE DATABASE sadnxai OWNER sadnxai;\"" 2>/dev/null || true
su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE sadnxai TO sadnxai;\""

# Load schema
cp /workspace/SADNxAI/db/init/*.sql /tmp/
chmod 644 /tmp/*.sql
su - postgres -c "psql -d sadnxai -f /tmp/001_schema.sql" 2>/dev/null || true
su - postgres -c "psql -d sadnxai -f /tmp/002_seed_data.sql" 2>/dev/null || true
echo -e "${GREEN}  Done${NC}"

# Step 5: Install Python dependencies
echo -e "${YELLOW}[5/7] Installing Python dependencies (this may take a few minutes)...${NC}"
cd /workspace/SADNxAI
pip install -q -r chat-service/requirements.txt
pip install -q -r masking-service/requirements.txt
pip install -q -r validation-service/requirements.txt
pip install -q vllm
echo -e "${GREEN}  Done${NC}"

# Step 6: Install frontend dependencies
echo -e "${YELLOW}[6/7] Installing frontend dependencies...${NC}"
cd /workspace/SADNxAI/frontend
npm install --legacy-peer-deps --silent
echo -e "${GREEN}  Done${NC}"

# Step 7: Pre-download LLM model
echo -e "${YELLOW}[7/7] Pre-downloading Llama 3.1 8B model...${NC}"
export HF_HOME=/workspace/.cache/huggingface
export HF_TOKEN=${HF_TOKEN:-your_huggingface_token_here}
export HUGGING_FACE_HUB_TOKEN=$HF_TOKEN

python -c "
from huggingface_hub import snapshot_download
snapshot_download('meta-llama/Llama-3.1-8B-Instruct', cache_dir='/workspace/.cache/huggingface')
print('Model downloaded successfully')
" 2>/dev/null || echo "Model will be downloaded on first vLLM start"
echo -e "${GREEN}  Done${NC}"

# Mark setup as complete
touch /workspace/.sadnxai-setup-complete

echo ""
echo "=============================================="
echo -e "${GREEN}  First-time setup complete!${NC}"
echo "=============================================="
echo ""
echo "  Next steps:"
echo "  1. Run: /workspace/SADNxAI/scripts/runpod-start.sh"
echo ""
echo "  Or for future restarts, just run:"
echo "  /workspace/SADNxAI/scripts/runpod-start.sh"
echo ""
