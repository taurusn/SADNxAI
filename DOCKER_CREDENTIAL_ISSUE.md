# Docker Credential Issue Report

## Issue Summary

**Error Message:**
```
error getting credentials - err: exit status 1, out: `A specified logon session does not exist. It may already have been terminated.`
```

**Impact:** Unable to pull Docker images (including `ollama/ollama:latest`) via SSH session on Windows.

---

## Environment

| Component | Details |
|-----------|---------|
| **OS** | Windows 11 Pro (Build 22631) |
| **Docker Desktop** | v29.1.2 |
| **Access Method** | SSH (OpenSSH for Windows) |
| **Shell** | Git Bash / WSL |

---

## Root Cause Analysis

### Primary Cause: Windows Credential Store + SSH Session Incompatibility

The Docker credential helper (`docker-credential-desktop.exe`) uses the **Windows Credential Manager** to store and retrieve Docker registry credentials. This credential store is tied to the **Windows logon session**.

**The Problem:**
- SSH sessions on Windows run in a **different logon session context** (Session 0 or a service session)
- The Windows Credential Manager is not accessible from these sessions
- When Docker tries to authenticate (even for public images), it calls the credential helper
- The credential helper fails because it cannot access the user's credential store

### Technical Flow

```
User (SSH) → docker pull → docker-credential-desktop.exe → Windows Credential Manager
                                        ↓
                            FAILS: "logon session does not exist"
```

### GitHub Issue Reference

This is a known issue documented at: https://github.com/docker/cli/issues/2682

---

## Symptoms

1. `docker pull` fails for ANY image (public or private)
2. `docker login` fails with same error
3. Error occurs ONLY via SSH - works fine in local GUI terminal
4. Error persists even after:
   - Restarting Docker Desktop
   - Restarting the PC
   - Signing out/in of Docker Hub

---

## What We Tried (Troubleshooting Log)

### Attempt 1: Remove `credsStore` from config.json
```json
{
  "auths": {},
  "currentContext": "desktop-linux"
}
```
**Result:** ❌ Failed - Docker Desktop overwrites config on restart

### Attempt 2: Set empty `credsStore`
```json
{
  "auths": {},
  "credsStore": "",
  "currentContext": "desktop-linux"
}
```
**Result:** ❌ Failed - Still tries to use credential helper

### Attempt 3: Make config.json read-only
```bash
chmod 444 ~/.docker/config.json
```
**Result:** ❌ Failed - Docker has config cached in memory

### Attempt 4: Rename credential helper executable
```bash
mv docker-credential-desktop.exe docker-credential-desktop.exe.disabled
```
**Result:** ⚠️ Partial - Breaks Docker Desktop startup

### Attempt 5: Restart Docker Desktop
```bash
docker desktop restart
```
**Result:** ❌ Failed - Config gets reset, issue persists

### Attempt 6: Restart PC
**Result:** ❌ Failed - SSH session still in different logon context

### Attempt 7: Use `wincred` credential store
```json
{
  "auths": {},
  "credsStore": "wincred",
  "currentContext": "desktop-linux"
}
```
**Result:** ⏳ Pending verification

---

## Solutions

### Solution 1: Use Non-Elevated Local Terminal (Best)

If you have physical/RDP access to the machine:
1. Open regular PowerShell or CMD (NOT as Administrator)
2. Run `docker pull` commands there
3. SSH sessions can then use the pulled images

### Solution 2: Use `wincred` Credential Store

Edit `~/.docker/config.json`:
```json
{
  "auths": {},
  "credsStore": "wincred",
  "currentContext": "desktop-linux"
}
```

Then restart Docker Desktop from the GUI (not via SSH).

### Solution 3: Pre-pull Images via GUI

1. Open Docker Desktop GUI
2. Use the search/pull feature to download images
3. SSH sessions can then use existing images

### Solution 4: Use Docker in WSL2

If using WSL2 backend:
```bash
# From WSL2 terminal (not Windows SSH)
docker pull ollama/ollama:latest
```

### Solution 5: Install Ollama Natively (For This Project)

Since this project specifically needs Ollama:
1. Download Ollama from https://ollama.com/download
2. Install natively on Windows
3. Update `docker-compose.yml` to use `host.docker.internal:11434`
4. Removes Docker dependency for Ollama entirely

---

## Recommended Fix for SADNxAI Project

### Option A: Native Ollama Installation

```yaml
# docker-compose.yml - Comment out ollama service
# ollama:
#   image: ollama/ollama:latest
#   ...

# Update chat-service environment:
environment:
  - OLLAMA_URL=http://host.docker.internal:11434
```

### Option B: Pre-pull via GUI

1. Open Docker Desktop on the Windows machine
2. Pull `ollama/ollama:latest` via GUI or local terminal
3. Then use `docker compose up` via SSH

---

## Prevention

### For Future SSH Docker Usage on Windows:

1. **Always pre-pull images** via local terminal before SSH sessions
2. **Consider using WSL2** for Docker operations
3. **Use GitHub Actions / CI** for builds instead of SSH
4. **Configure credential helper** to use `wincred` instead of `desktop`

### Docker Desktop Settings

In Docker Desktop → Settings → Docker Engine, you can add:
```json
{
  "features": {
    "containerd-snapshotter": false
  }
}
```

---

## Related Issues & Resources

- [Docker CLI Issue #2682](https://github.com/docker/cli/issues/2682) - Original bug report
- [Docker Desktop Windows SSH](https://docs.docker.com/desktop/faqs/windowsfaqs/) - Official FAQ
- [Windows Credential Manager](https://support.microsoft.com/en-us/windows/accessing-credential-manager-1b5c916a-6a16-889f-8581-fc16e8165ac0) - Microsoft Docs

---

## Status

| Item | Status |
|------|--------|
| Issue Identified | ✅ Complete |
| Root Cause Found | ✅ Windows SSH + Credential Store |
| Workaround Available | ✅ Multiple options |
| Permanent Fix | ❌ Requires Microsoft/Docker fix |

---

## Appendix: Full Error Log

```
$ docker pull ollama/ollama:latest
error getting credentials - err: exit status 1, out: `A specified logon session does not exist. It may already have been terminated.`

$ docker login
error getting credentials - err: exit status 1, out: `A specified logon session does not exist. It may already have been terminated.`

$ echo "test" | docker-credential-desktop.exe get
A specified logon session does not exist. It may already have been terminated.
```

---

*Report generated: 2025-12-08*
*Project: SADNxAI*
