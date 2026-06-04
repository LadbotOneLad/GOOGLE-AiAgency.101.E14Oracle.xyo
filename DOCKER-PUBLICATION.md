# 🐳 Docker Publication Guide — AiFACTORi + E14

> **Build, test, and publish production-grade containers to Docker Hub**

---

## 📋 Prerequisites

```bash
# 1. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 2. Create Docker Hub Account
# Visit: https://hub.docker.com/signup
# Choose username (e.g., ladbotodelad)

# 3. Login to Docker Hub
docker login
# Prompt: Username → [your-username]
# Prompt: Password → [your-token]
# (Generate token at https://hub.docker.com/settings/security)
```

---

## 🔨 Build Docker Images

### Option 1: Automated Script (Recommended)

```bash
# Make script executable
chmod +x build-and-publish.sh

# Run build
./build-and-publish.sh

# Prompts:
# - Docker Hub username
# - Version number
# - Confirmation to push
```

### Option 2: Manual Build

```bash
# AiFACTORi Engine
docker build \
  -f Dockerfile.aifactori \
  -t ladbotodelad/aifactori-engine:2.0 \
  -t ladbotodelad/aifactori-engine:latest \
  .

# E14 Oracle
docker build \
  -f Dockerfile.e14-oracle \
  -t ladbotodelad/e14-oracle:2.0 \
  -t ladbotodelad/e14-oracle:latest \
  .

# Verify builds
docker images | grep aifactori
docker images | grep e14
```

---

## ✅ Test Images Locally

### Test AiFACTORi Engine

```bash
# Run single engine
docker run -d \
  --name test-engine-365 \
  -e ENGINE_ID=365 \
  -e ENGINE_ROLE=validator \
  -p 365:365 \
  ladbotodelad/aifactori-engine:latest

# Check health
docker logs test-engine-365
curl http://localhost:365/4gr/health

# Stop
docker stop test-engine-365
docker rm test-engine-365
```

### Test E14 Oracle

```bash
# Run oracle
docker run -d \
  --name test-oracle \
  -e MODE=LOCKED \
  -e LOCK_DURATION_DAYS=90 \
  -p 8001:8001 \
  ladbotodelad/e14-oracle:latest

# Check health
docker logs test-oracle
curl http://localhost:8001/health

# Stop
docker stop test-oracle
docker rm test-oracle
```

---

## 📤 Publish to Docker Hub

### Option 1: Automated Push

```bash
./build-and-publish.sh
# Includes login, build, and push
```

### Option 2: Manual Push

```bash
# AiFACTORi Engine
docker push ladbotodelad/aifactori-engine:2.0
docker push ladbotodelad/aifactori-engine:latest

# E14 Oracle
docker push ladbotodelad/e14-oracle:2.0
docker push ladbotodelad/e14-oracle:latest
```

### Verify Push Success

```bash
# Visit Docker Hub
https://hub.docker.com/r/ladbotodelad/aifactori-engine
https://hub.docker.com/r/ladbotodelad/e14-oracle

# Pull from Docker Hub (public)
docker pull ladbotodelad/aifactori-engine:latest
docker pull ladbotodelad/e14-oracle:latest
```

---

## 🎯 Image Details

### AiFACTORi Engine Image

```yaml
Name:           aifactori-engine
Version:        2.0
Lock Cycle:     2
Base Image:     python:3.11-slim
Size:           ~450MB
Ports:          365, 777, 101, 1001-1012
User:           aifactori (non-root)
Health Check:   /4gr/health endpoint

Environment:
  LOCK_METADATA_PATH=/app/lock/metadata.json
  LOG_DIR=/logs
  PYTHONUNBUFFERED=1

Tags:
  ladbotodelad/aifactori-engine:2.0
  ladbotodelad/aifactori-engine:latest
  ladbotodelad/aifactori-engine:cycle-2

Repository:
  https://hub.docker.com/r/ladbotodelad/aifactori-engine
```

### E14 Oracle Image

```yaml
Name:           e14-oracle
Version:        1.0
Lock Cycle:     2
Base Image:     python:3.11-slim
Size:           ~380MB
Port:           8001
User:           oracle (non-root)
Health Check:   /health endpoint

Environment:
  ORACLE_MODE=LOCKED
  LOCK_DURATION_DAYS=90
  AIFACTORI_INTEGRATION=enabled
  FLASK_ENV=production
  LOG_DIR=/logs

Tags:
  ladbotodelad/e14-oracle:1.0
  ladbotodelad/e14-oracle:latest
  ladbotodelad/e14-oracle:cycle-2

Repository:
  https://hub.docker.com/r/ladbotodelad/e14-oracle
```

---

## 🚀 Deploy from Docker Hub

### Pull Latest Images

```bash
docker pull ladbotodelad/aifactori-engine:latest
docker pull ladbotodelad/e14-oracle:latest
docker pull prom/prometheus:latest
docker pull grafana/grafana:latest
```

### Run Full Stack

```bash
# Create docker-compose-publish.yml with:
version: "3.9"
services:
  engine-365:
    image: ladbotodelad/aifactori-engine:latest
    environment:
      - ENGINE_ID=365
      - ENGINE_ROLE=validator
    ports:
      - "365:365"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:365/4gr/health"]
      interval: 30s

  oracle:
    image: ladbotodelad/e14-oracle:latest
    environment:
      - MODE=LOCKED
    ports:
      - "8001:8001"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"

# Deploy
docker-compose -f docker-compose-publish.yml up -d

# Verify
docker-compose -f docker-compose-publish.yml ps
```

---

## 📊 Docker Hub Repository Setup

### Repository Settings

1. **Visit**: https://hub.docker.com/settings/security
2. **Generate Access Token**:
   - Click "New Access Token"
   - Name: "AiFACTORi CI/CD"
   - Permissions: Read, Write, Delete
   - Copy token (one-time display)

3. **Docker Login**:
   ```bash
   docker login -u ladbotodelad -p [your-token]
   ```

### Repository Description

```
🌌 AiFACTORi: Sovereign Multi-Agent Architecture

14-engine cryptographic validation system with 90-day lock mechanism, 
zero-trust immune system, and 91.7% coherence (Kotahitanja).

Features:
✅ 14 Synchronized Engines
✅ Merkle Root Consensus
✅ 4GR-FSE State Machine
✅ Zero-Trust Validation
✅ 90-Day Lock Window
✅ Production-Ready
✅ Full Observability

Deploy: docker pull ladbotodelad/aifactori-engine:latest
Docs: https://github.com/LadbotOneLad/AiFACTORi
```

---

## 🔒 Security Best Practices

### Image Security

```bash
# 1. Scan for vulnerabilities
docker scan ladbotodelad/aifactori-engine:latest

# 2. Non-root user (already configured)
# User: aifactori / oracle (UID: 1000)

# 3. Read-only lock metadata
# Permission: 444 (read-only for user)

# 4. Health checks built-in
# Every image has healthcheck configured

# 5. Minimal base image
# python:3.11-slim (no unnecessary packages)

# 6. .dockerignore configured
# Excludes sensitive files, test files, docs
```

### Registry Security

```bash
# 1. Enable two-factor authentication
# Docker Hub → Account Settings → Security

# 2. Use access tokens (not passwords)
# Docs: https://docs.docker.com/docker-hub/access-tokens/

# 3. Limit token permissions
# Read, Write, Delete only when needed

# 4. Rotate tokens regularly
# Every 90 days with lock renewal cycle
```

---

## 📈 Monitoring Pushed Images

### Check Image Details

```bash
# List tags
curl https://hub.docker.com/v2/repositories/ladbotodelad/aifactori-engine/tags

# Pull stats (on Docker Hub UI)
# Repository → Tags → View pull statistics

# Latest pulls per day/week/month visible on Docker Hub
```

### Update docker-compose to use published images

```yaml
services:
  engine-365:
    image: ladbotodelad/aifactori-engine:latest
    # Instead of: image: aifactori/engine-4gr:latest

  oracle:
    image: ladbotodelad/e14-oracle:latest
    # Instead of: image: e14/oracle:stable
```

---

## 🎯 CI/CD Integration (GitHub Actions)

### Automatic Build & Publish

```yaml
# .github/workflows/docker-publish.yml
name: Docker Build & Publish

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build & Push AiFACTORi
        uses: docker/build-push-action@v4
        with:
          file: ./Dockerfile.aifactori
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/aifactori-engine:latest
            ${{ secrets.DOCKER_USERNAME }}/aifactori-engine:${{ github.sha }}
      
      - name: Build & Push E14
        uses: docker/build-push-action@v4
        with:
          file: ./Dockerfile.e14-oracle
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/e14-oracle:latest
            ${{ secrets.DOCKER_USERNAME }}/e14-oracle:${{ github.sha }}
```

### GitHub Secrets Setup

```
Settings → Secrets and variables → Actions → New repository secret

DOCKER_USERNAME=ladbotodelad
DOCKER_PASSWORD=[your-access-token]
```

---

## 📦 Version Management

### Semantic Versioning

```
Format: MAJOR.MINOR.PATCH

Current:
  AiFACTORi Engine: 2.0.0
  E14 Oracle: 1.0.0

Tags on Docker Hub:
  2.0.0           (exact version)
  2.0             (minor version)
  2               (major version)
  latest          (always latest stable)
  cycle-2         (lock cycle tag)

Tagging strategy:
  docker tag ladbotodelad/aifactori-engine:2.0.0 ladbotodelad/aifactori-engine:2.0
  docker tag ladbotodelad/aifactori-engine:2.0 ladbotodelad/aifactori-engine:latest
```

---

## ✅ Deployment Checklist

- [ ] Docker installed locally
- [ ] Docker Hub account created
- [ ] Access token generated
- [ ] `docker login` successful
- [ ] Dockerfile.aifactori reviewed
- [ ] Dockerfile.e14-oracle reviewed
- [ ] .dockerignore configured
- [ ] build-and-publish.sh is executable
- [ ] Local images build successfully
- [ ] Local test containers run
- [ ] Images pushed to Docker Hub
- [ ] Docker Hub repositories public
- [ ] Images pullable: `docker pull ladbotodelad/aifactori-engine:latest`
- [ ] docker-compose updated to use published images
- [ ] Full stack deploys from published images
- [ ] GitHub Actions workflows configured
- [ ] All systems operational

---

## 🎉 Publication Success Indicators

```
✅ Images appear on Docker Hub
✅ Pull count increases
✅ GitHub Actions builds automatically
✅ docker-compose deploys from registry
✅ All health checks pass
✅ Metrics visible in Prometheus
✅ Logs appear in observability stack
✅ Zero security warnings
✅ Full 19-service stack operational
```

---

## 📍 Final Commands

```bash
# Build locally
./build-and-publish.sh

# Or manually
docker build -f Dockerfile.aifactori -t ladbotodelad/aifactori-engine:2.0 .
docker build -f Dockerfile.e14-oracle -t ladbotodelad/e14-oracle:1.0 .

# Push to Docker Hub
docker push ladbotodelad/aifactori-engine:2.0
docker push ladbotodelad/e14-oracle:1.0

# Deploy from public registry
docker-compose -f docker-compose-e14-integration.yml up -d

# Verify
docker ps
curl http://localhost:365/4gr/health
curl http://localhost:8001/health
```

---

**Status**: READY FOR PUBLICATION ✅  
**Images**: Production-grade  
**Security**: Best practices applied  
**Observability**: Full telemetry included  

**Your containers are ready to be shared with the world!** 🚀
