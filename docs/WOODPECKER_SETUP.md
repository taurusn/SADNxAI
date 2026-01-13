# Woodpecker CI/CD Setup for SADNxAI

## Overview

```
GitHub (push to main) 
    ↓ webhook
Cloudflare Tunnel (ci.sadn.site)
    ↓
Woodpecker Server (localhost:8080)
    ↓
Woodpecker Agent → Docker → Rebuild & Deploy
```

## What the Pipeline Does

| Step | Action |
|------|--------|
| **deploy** | Git pull latest code from main |
| **rebuild** | `docker compose down frontend` → `docker compose up -d --build frontend` |

**Trigger:** Push to `main` branch only

---

## Architecture

| Component | URL/Port | Purpose |
|-----------|----------|---------|
| Woodpecker Server | localhost:8080 | CI/CD UI & API |
| Woodpecker Agent | - | Runs pipeline steps |
| Cloudflare Tunnel | ci.sadn.site | External access |

---

## Files

| File | Purpose |
|------|---------|
| `.woodpecker.yml` | Pipeline definition |
| `docker-compose.woodpecker.yml` | Woodpecker server + agent |
| `.env.woodpecker` | GitHub OAuth credentials (gitignored) |

---

## Pipeline Configuration

```yaml
# .woodpecker.yml
when:
  - branch: main
    event: push

steps:
  - name: deploy
    image: alpine/git:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - "D:/IAU/skill forge/Sadn-bank/SADNxAI:/app"
      - "C:/Users/sei/.ssh:/ssh-keys:ro"
    commands:
      - mkdir -p /root/.ssh
      - cp /ssh-keys/* /root/.ssh/
      - chmod 600 /root/.ssh/id_ed25519
      - cd /app
      - git config --global --add safe.directory /app
      - git pull origin main

  - name: rebuild
    image: docker:24-cli
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - "D:/IAU/skill forge/Sadn-bank/SADNxAI:/app"
    commands:
      - cd /app
      - docker compose -p sadnxai down frontend
      - docker compose -p sadnxai up -d --build frontend
```

---

## Setup Steps

### 1. GitHub OAuth App

1. Go to https://github.com/settings/developers
2. Click **New OAuth App**
3. Fill in:
   - **Application name:** `SADNxAI Woodpecker`
   - **Homepage URL:** `https://ci.sadn.site`
   - **Authorization callback URL:** `https://ci.sadn.site/authorize`
4. Save Client ID and Client Secret

### 2. Environment File

```bash
# Create .env.woodpecker
WOODPECKER_GITHUB_CLIENT=<your_client_id>
WOODPECKER_GITHUB_SECRET=<your_client_secret>
WOODPECKER_AGENT_SECRET=$(openssl rand -hex 32)
```

### 3. Cloudflare Tunnel

Add to your tunnel config:
```yaml
- hostname: ci.sadn.site
  service: http://localhost:8080
```

Or via CLI:
```bash
cloudflared tunnel route dns <tunnel-name> ci.sadn.site
```

### 4. Start Woodpecker

```bash
docker compose -f docker-compose.woodpecker.yml --env-file .env.woodpecker up -d
```

### 5. Activate Repository

1. Go to https://ci.sadn.site
2. Login with GitHub
3. Find `taurusn/SADNxAI`
4. Click **Activate**

---

## Commands

```bash
# Start Woodpecker
docker compose -f docker-compose.woodpecker.yml --env-file .env.woodpecker up -d

# Stop Woodpecker
docker compose -f docker-compose.woodpecker.yml down

# View logs
docker logs woodpecker-server
docker logs woodpecker-agent

# Restart
docker compose -f docker-compose.woodpecker.yml --env-file .env.woodpecker restart
```

---

## Troubleshooting

### Pipeline not triggering
- Check webhook in GitHub repo → Settings → Webhooks
- Ensure webhook points to `https://ci.sadn.site/hook`

### SSH/Git pull fails
- Verify SSH key is added to GitHub: https://github.com/settings/keys
- Check SSH key exists: `ls ~/.ssh/id_ed25519`

### Port already allocated
- Use `-p sadnxai` flag with docker compose to use correct project name
- Or manually stop conflicting containers

### Agent not connecting
```bash
docker logs woodpecker-agent
# Should show: "starting Woodpecker agent"
```

---

## Admins

Current admins (can login and manage repos):
- `abdullatifaabdullah`
- `taurusn`

To add more, update `WOODPECKER_ADMIN` in `docker-compose.woodpecker.yml`

---

## URLs

| Service | URL |
|---------|-----|
| Woodpecker CI | https://ci.sadn.site |
| Frontend | https://sadnxai.sadn.site |
| API | https://sadnxaiapi.sadn.site |
