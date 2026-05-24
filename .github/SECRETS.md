# GitHub Actions Secrets Setup

This project uses SSH for secure deployments. Configure these repository secrets:

## Required Secrets

Add these in: **Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Description |
|---|---|
| `DEPLOY_SSH_KEY` | Your private SSH key (ed25519 format) |
| `DEPLOY_HOST` | Server hostname or IP (SSH port: 777) |
| `DEPLOY_USER` | SSH username |
| `DOCKERHUB_USERNAME` | Docker Hub username (for docker-push.yml) |
| `DOCKERHUB_TOKEN` | Docker Hub access token (for docker-push.yml) |

## SSH Key Setup

1. **Use your existing ed25519 key:**
   ```bash
   cat ~/.ssh/id_ed25519 | base64
   ```
   Paste the output as `DEPLOY_SSH_KEY` secret value.

2. **Or generate a new deployment key:**
   ```bash
   ssh-keygen -t ed25519 -f ~/.ssh/deploy_key -C "kcufsihtliametihs001@example.com" -N ""
   cat ~/.ssh/deploy_key | base64
   ```

3. **Add public key to server:**
   ```bash
   ssh-copy-id -i ~/.ssh/deploy_key user@server
   ```
   Or manually append `deploy_key.pub` to `~/.ssh/authorized_keys` on the target server.

## Workflows Included

- **docker-build.yml** - Builds & tests on PR/push
- **docker-push.yml** - Pushes to Docker Hub on main branch
- **deploy.yml** - Deploys container to production server via SSH

---

**Security Notes:**
- Never commit private keys to the repository
- Secrets are masked in GitHub Actions logs
- SSH keys are cleaned up after deployment
- Use different keys for different environments (dev/staging/prod)
