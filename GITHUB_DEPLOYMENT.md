# 🚀 GITHUB DEPLOYMENT — AiFACTORi v1.0

## Prerequisites

- [x] GitHub account: `LadbotOneLad`
- [x] Git installed locally
- [x] Docker & Docker Compose (for local deployment)
- [x] SSH key configured OR GitHub Personal Access Token

## Repository Information

```
Owner:       LadbotOneLad
Repository:  AiFACTORi
URL:         https://github.com/LadbotOneLad/AiFACTORi.git
SSH:         git@github.com:LadbotOneLad/AiFACTORi.git
Visibility:  Public
```

## Current Local Status

```
Branch:      main
Commits:     3
Files:       Core deployment files staged
Status:      Ready to push
```

## Push Instructions

### Option 1: HTTPS (Recommended for CI/CD)

```bash
git remote add origin https://github.com/LadbotOneLad/AiFACTORi.git
git branch -M main
git push -u origin main
```

When prompted, use your GitHub **Personal Access Token** (not password):
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Create token with scopes: `repo`, `admin:repo_hook`
3. Paste token when prompted for password

### Option 2: SSH (Recommended for local development)

```bash
# Generate SSH key (if needed)
ssh-keygen -t ed25519 -C "aifactori@tenetaiagency.dev"

# Add public key to GitHub
# Settings → SSH and GPG keys → New SSH key
cat ~/.ssh/id_ed25519.pub | pbcopy  # macOS
# OR
cat ~/.ssh/id_ed25519.pub | xclip -selection clipboard  # Linux

# Then push
git remote add origin git@github.com:LadbotOneLad/AiFACTORi.git
git branch -M main
git push -u origin main
```

### Option 3: GitHub CLI

```bash
# Authenticate
gh auth login
# Follow prompts (HTTPS or SSH)

# Clone & push
gh repo clone LadbotOneLad/AiFACTORi
cd AiFACTORi
git push -u origin main
```

---

## What's Being Pushed

### Core Files
- ✅ `README.md` — Full system overview
- ✅ `QUICKSTART.md` — 3-command deployment
- ✅ `ARCHITECTURE_INDEX.md` — Five chambers guide
- ✅ `docker-compose-90DAY-LOCK.yml` — Full stack deployment
- ✅ `Dockerfile`, `Dockerfile.4gr`, `Dockerfile.thymus` — Container images
- ✅ `package.json`, `requirements.txt` — Dependencies

### Cyberpunk Documentation (Five Chambers)
- ✅ `.cipher/ARCHITECTURE.md` — Core philosophy & design
- ✅ `.sanctum/DEPLOYMENT.md` — Launch procedures
- ✅ `.oracle/DIAGNOSTICS.md` — Monitoring & debugging
- ✅ `.codex_vault/SECRETS.md` — Configuration & secrets
- ✅ `.nexus/INFRASTRUCTURE.md` — Integration & networking

### Configuration Files
- ✅ `.gitignore` — Ignore generated files
- ✅ `.dockerignore` — Optimize Docker builds
- ✅ `.env.lock` — Environment variables (committed, but sanitized)
- ✅ `k8s-lock-deployment.yaml` — Kubernetes manifests
- ✅ `lock-metadata.json` — Complete lock state

### Scripts & Utilities
- ✅ `lock-status.sh` — Real-time monitoring
- ✅ `lock-initialize.ts` — Lock renewal (every 90 days)
- ✅ `lock-init-node.js` — Node.js lock renewal alternative

### GitHub Workflows
- ✅ `.github/workflows/deploy.yml` — CI/CD pipeline
- ✅ `.github/workflows/docker-build.yml` — Build on push
- ✅ `.github/workflows/docker-push.yml` — Push to Docker Hub

---

## Post-Push Checklist

### On GitHub Repository

- [ ] Verify all files are visible
- [ ] Check commit history (3 commits)
- [ ] Confirm branch is `main`
- [ ] Set branch protection rules (Settings → Branches)
  - [ ] Require pull request reviews
  - [ ] Require status checks to pass
  - [ ] Dismiss stale reviews

### GitHub Settings

- [ ] Update repository description:
  ```
  14-engine sovereign AI architecture with 90-day lock, 
  zero-trust immune system, and cryptographic Merkle root validation
  ```

- [ ] Add topics:
  ```
  aifactori, ai-agents, docker, kubernetes, zero-trust, 
  sovereign-ai, multi-agent, cyberpunk, architecture
  ```

- [ ] Configure GitHub Actions (Settings → Actions)
  - [ ] Allow all actions
  - [ ] Set workflow permissions to "Read and write"

- [ ] Set up Secrets (Settings → Secrets and variables → Actions)
  ```
  DOCKER_USERNAME = [your-docker-hub-username]
  DOCKER_PASSWORD = [your-docker-hub-token]
  KUBECONFIG = [base64-encoded-k8s-config, optional]
  ```

### Visibility & Access

- [ ] Set repository visibility (Public for open-source)
- [ ] Add collaborators if needed (Settings → Collaborators)
- [ ] Configure deploy keys for CD (Settings → Deploy keys)

---

## GitHub Pages (Optional Documentation Site)

Enable GitHub Pages for live documentation:

```bash
# In Settings → Pages
# Source: Deploy from a branch
# Branch: main
# Folder: docs/ (or /)
```

Then access at: `https://ladbotodelad.github.io/AiFACTORi/`

---

## CI/CD Pipeline

Once pushed, GitHub Actions will:

1. **On every push to `main`**:
   - Build Docker images
   - Run tests (if any)
   - Push to Docker Hub (if configured)
   - Deploy to Kubernetes (if configured)

2. **Docker Hub**:
   - Images available as: `docker pull ladbotodelad/aifactori:latest`
   - Automatic builds from GitHub repo

3. **Kubernetes Deployment**:
   - Triggered by GitHub Actions workflow
   - Requires `KUBECONFIG` secret configured

---

## Public Access

Once deployed to GitHub:

```bash
# Anyone can clone
git clone https://github.com/LadbotOneLad/AiFACTORi.git

# Or with GitHub CLI
gh repo clone LadbotOneLad/AiFACTORi

# Docker images available globally
docker pull ladbotodelad/aifactori:latest
docker pull ladbotodelad/aifactori-engine-4gr:latest
docker pull ladbotodelad/aifactori-thymus:latest
```

---

## Security Considerations

⚠️ **Before pushing to public repo:**

- [ ] Remove any real credentials from `.env.lock`
- [ ] Strip sensitive data from `.gitignore`
- [ ] Review all files for hardcoded secrets
- [ ] Use GitHub Secrets for environment variables
- [ ] Enable branch protection
- [ ] Configure code scanning (Settings → Security)

✅ **These are already safe:**
- Lock metadata (not security-critical)
- Docker configurations (publicly acceptable)
- Kubernetes manifests (sanitized examples)

---

## Rollback Procedure

If something goes wrong after push:

```bash
# View commit history
git log --oneline

# Revert last commit (keeps history)
git revert HEAD
git push origin main

# OR: Force reset to previous commit (destructive)
git reset --hard HEAD~1
git push -f origin main  # ⚠️ Only if you're certain
```

---

## Next Steps

1. **Complete the push** (choose Option 1, 2, or 3 above)
2. **Verify on GitHub** (check all files are there)
3. **Configure GitHub Actions secrets** (if using CI/CD)
4. **Test local deployment** (run the 3 QUICKSTART commands)
5. **Update GitHub description & topics**
6. **Share publicly** (announce on social media, etc.)

---

## Support Resources

- **GitHub Docs**: https://docs.github.com/
- **Git Push Troubleshooting**: https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository
- **GitHub Actions**: https://docs.github.com/en/actions
- **Docker Hub**: https://docs.docker.com/docker-hub/

---

**Status**: Ready for GitHub deployment  
**Commits**: 3 staged and ready  
**Files**: ~50+ (core + documentation)  
**Estimated size**: ~50MB (with images)

🚀 **You are ready to go live!**
