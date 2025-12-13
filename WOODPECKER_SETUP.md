# Woodpecker CI Setup for SADNxAI

## Overview

```
GitHub (push) → Webhook → Cloudflare Tunnel (ci.sadn.site) → Woodpecker → Deploy
```

**Pipeline behavior:**
- All branches: Lint + type-check (frontend & backend)
- main only: git pull + docker compose restart

---

## Step 1: Create GitHub OAuth App

1. Go to https://github.com/settings/developers
2. Click **"New OAuth App"**
3. Fill in:
   - **Application name**: `SADNxAI Woodpecker`
   - **Homepage URL**: `https://ci.sadn.site`
   - **Authorization callback URL**: `https://ci.sadn.site/authorize`
4. Click **"Register application"**
5. Copy the **Client ID**
6. Click **"Generate a new client secret"** and copy it

---

## Step 2: Configure Cloudflare Tunnel

Add a new public hostname in your Cloudflare Tunnel config:

**Option A: Cloudflare Dashboard**
1. Go to Zero Trust → Networks → Tunnels
2. Select your tunnel → Public Hostname
3. Add:
   - Subdomain: `ci`
   - Domain: `sadn.site`
   - Service: `http://localhost:8080`

**Option B: Config file (if using config.yml)**
```yaml
ingress:
  # Existing services...
  - hostname: sadnxai.sadn.site
    service: http://localhost:3000
  - hostname: sadnxaiapi.sadn.site
    service: http://localhost:8000

  # Add Woodpecker
  - hostname: ci.sadn.site
    service: http://localhost:8080

  - service: http_status:404
```

Restart the tunnel after changes:
```bash
cloudflared tunnel run <your-tunnel-name>
```

---

## Step 3: Create Environment File

```bash
cd "/d/IAU/skill forge/Sadn-bank/SADNxAI"

# Generate agent secret
openssl rand -hex 32

# Create env file
cp .env.woodpecker.example .env.woodpecker
```

Edit `.env.woodpecker`:
```env
WOODPECKER_GITHUB_CLIENT=<your_client_id>
WOODPECKER_GITHUB_SECRET=<your_client_secret>
WOODPECKER_AGENT_SECRET=<generated_secret>
```

---

## Step 4: Start Woodpecker

```bash
# Start Woodpecker server and agent
docker compose -f docker-compose.woodpecker.yml --env-file .env.woodpecker up -d

# Check logs
docker logs woodpecker-server
docker logs woodpecker-agent
```

---

## Step 5: Activate the Repository

1. Open https://ci.sadn.site
2. Login with GitHub (authorize the OAuth app)
3. You'll see your repositories
4. Find `taurusn/SADNxAI` and click **"Activate"**
5. Woodpecker will add a webhook to your GitHub repo

---

## Step 6: Test the Pipeline

```bash
# Make a small change and push
git add .
git commit -m "test: trigger CI pipeline"
git push origin main
```

Check https://ci.sadn.site to see the pipeline run.

---

## Pipeline Details

### What runs on every branch:
| Step | Image | What it does |
|------|-------|--------------|
| lint-frontend | node:20-alpine | `npm run lint` |
| typecheck-frontend | node:20-alpine | `npx tsc --noEmit` |
| lint-backend | python:3.11-slim | `ruff check` on all services |

### What runs only on main:
| Step | Image | What it does |
|------|-------|--------------|
| deploy | docker:24-cli | `git pull` + `docker compose up -d --build` |
| notify-success | alpine | Print deployment URLs |

---

## Troubleshooting

### Webhook not triggering
1. Go to GitHub repo → Settings → Webhooks
2. Check if webhook exists (should point to `https://ci.sadn.site/hook`)
3. Check "Recent Deliveries" for errors

### Agent not connecting
```bash
docker logs woodpecker-agent
# Should show: "successfully connected to server"
```

### Pipeline stuck
```bash
# Restart agent
docker restart woodpecker-agent
```

### Permission denied during deploy
The agent needs access to Docker socket and project directory. Check volumes in `docker-compose.woodpecker.yml`.

---

## Files Created

| File | Purpose |
|------|---------|
| `docker-compose.woodpecker.yml` | Woodpecker server + agent |
| `.woodpecker.yml` | Pipeline definition |
| `.env.woodpecker.example` | Environment template |
| `.env.woodpecker` | Your actual credentials (gitignored) |
