# 🗝️ THE CODEX VAULT — Secrets & Configuration

## Encryption Keys (KEEP SECURE)

```
⚠️ WARNING: This vault contains cryptographic material.
   Never commit secrets to public repositories.
   Use GitHub Secrets or HashiCorp Vault for production.
```

## Environment Variables (.env.lock)

The master incantation that controls all 14 engines:

```bash
# Lock Parameters
LOCK_ID="550e8400-e29b-41d4-a716-446655440000"
LOCK_INCEPTION="2025-01-14T10:00:00.000Z"
LOCK_EXPIRY="2025-04-14T10:00:00.000Z"
LOCK_STATUS="ACTIVE"

# Wobble Constants (Frozen)
WOBBLE_TIER0=0.05
WOBBLE_TIER1=0.075
WOBBLE_TIER2=0.15

# Merkle Root (Immutable)
MERKLE_ROOT="[computed at lock initialization]"

# Engine Configuration
ENGINE_COUNT=14
CORE_ENGINES=3
PEER_ENGINES=12

# Port Allocations
PORT_ENGINE_365=365
PORT_ENGINE_777=777
PORT_ENGINE_101=101
PORT_ENGINE_1001_1012="1001-1012"

# Service Ports
PORT_MCP_AUDIT=8888
PORT_THYMUS=9999
PORT_PROMETHEUS=9090
PORT_GRAFANA=3000

# Resource Limits
CPUS_PER_ENGINE=0.8
MEMORY_PER_ENGINE=512M
CPUS_AUDIT=1.0
MEMORY_AUDIT=1G
CPUS_THYMUS=1.0
MEMORY_THYMUS=1G
```

## Kubernetes Secrets (k8s-lock-secret.yaml)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: aifactori-lock
  namespace: default
type: Opaque
data:
  lock-id: NTUwZTg0MDAtZTI5Yi00MWQ0LWE3MTYtNDQ2NjU1NDQwMDAw
  lock-expiry: MjAyNS0wNC0xNFQxMDowMDowMC4wMDBa
  merkle-root: "[base64-encoded]"
  wobble-tier0: MC4wNQ==
  wobble-tier1: MC4wNzU=
  wobble-tier2: MC4xNQ==
```

Deploy with:
```bash
kubectl apply -f k8s-lock-secret.yaml
```

## Kubernetes ConfigMap (k8s-lock-configmap.yaml)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: aifactori-config
  namespace: default
data:
  docker-compose.yml: |
    version: "3.9"
    services:
      engine:
        image: aifactori/engine-4gr:latest
        # ... [full config]
  
  lock-metadata.json: |
    {
      "lock_id": "550e8400-e29b-41d4-a716-446655440000",
      "inception": "2025-01-14T10:00:00.000Z",
      "expiry": "2025-04-14T10:00:00.000Z",
      "engines": [
        {
          "name": "engine-365",
          "port": 365,
          "role": "validator",
          "tier": "tier-0"
        },
        # ... [all 14 engines]
      ]
    }
```

Deploy with:
```bash
kubectl apply -f k8s-lock-configmap.yaml
```

## Password Vault

### Docker Hub Credentials
```
Username: [your-docker-username]
Password: [your-docker-password]
Registry: docker.io
```

Login:
```bash
docker login -u [username] -p [password]
```

### GitHub Personal Access Token
```
Token: ghp_[64-char-token]
Scopes: repo, admin:repo_hook, admin:org_hook
Expiry: [as configured]
```

Use:
```bash
git clone https://[token]@github.com/LadbotOneLad/AiFACTORi.git
# OR
export GITHUB_TOKEN=[token]
gh repo clone LadbotOneLad/AiFACTORi
```

### SSH Keys (Git)
```bash
# Generate if needed
ssh-keygen -t ed25519 -C "aifactori@tenetaiagency.dev"

# Add to GitHub
cat ~/.ssh/id_ed25519.pub | pbcopy  # macOS
cat ~/.ssh/id_ed25519.pub | xclip -selection clipboard  # Linux

# Use in git
git clone git@github.com:LadbotOneLad/AiFACTORi.git
```

## Database Credentials (If Used)

```yaml
postgres:
  host: postgres-service
  port: 5432
  username: aifactori_user
  password: [strong-random-password]
  database: aifactori_lock_state
  ssl: true

redis:
  host: redis-service
  port: 6379
  password: [strong-random-password]
  db: 0
```

## API Keys & Tokens

```
Prometheus Auth: [basic-auth-token]
Grafana Admin:   admin@aifactori.dev / [password]
MCP Audit Key:   [uuid-based-key]
Thymus Token:    [jwt-bearer-token]
```

## TLS/SSL Certificates

```bash
# Generate self-signed (development)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365

# Mount in Docker
volumes:
  - ./certs/cert.pem:/app/certs/cert.pem
  - ./certs/key.pem:/app/certs/key.pem
```

## GitHub Actions Secrets

Configure these in: Settings → Secrets and variables → Actions

```
DOCKER_USERNAME:        [docker-hub-username]
DOCKER_PASSWORD:        [docker-hub-password]
GITHUB_TOKEN:           [auto-created-by-github]
KUBECONFIG:             [base64-encoded-k8s-config]
LOCK_METADATA_PROD:     [production-lock-json]
SLACK_WEBHOOK:          [optional-notifications]
```

## Secure Practices

1. **Never commit secrets** to git (use .gitignore)
2. **Rotate credentials** every 90 days (aligns with lock window)
3. **Use environment variables** instead of hardcoded values
4. **Enable 2FA** on GitHub account
5. **Audit access logs** regularly
6. **Use least privilege** for all service accounts
7. **Encrypt at rest** (secrets management tool)
8. **Encrypt in transit** (TLS/mTLS)

## Secret Rotation Checklist

Every 90 days when lock expires:

- [ ] Regenerate LOCK_ID
- [ ] Update LOCK_EXPIRY
- [ ] Rotate GitHub PAT
- [ ] Rotate Docker Hub credentials
- [ ] Refresh Kubernetes secrets
- [ ] Update GitHub Actions secrets
- [ ] Rotate any database passwords
- [ ] Review and revoke unused tokens

---

**Vault Status**: Secured and encrypted  
**Key Rotation**: Synchronized with 90-day lock  
**Access Control**: Zero-trust verified
