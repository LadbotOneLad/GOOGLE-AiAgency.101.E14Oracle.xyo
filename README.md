<<<<<<< HEAD
# E14 Oracle — Cosmological Decision Engine

[![Docker](https://img.shields.io/badge/Docker-Enabled-blue?logo=docker)](https://hub.docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://www.python.org/)
[![GitHub](https://img.shields.io/badge/GitHub-LadbotOneLad/AiFACTORi-black?logo=github)](https://github.com/LadbotOneLad/AiFACTORi)

A production-grade Python system for phase-space convergence detection, Merkle consensus validation, and real-time decision orchestration across 14 synchronized engines.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose (or Python 3.11+)
- Git

### Docker (Recommended)

```bash
git clone https://github.com/LadbotOneLad/AiFACTORi.git
cd AiFACTORi
docker-compose up -d
docker-compose logs -f
```

### Local Python

```bash
git clone https://github.com/LadbotOneLad/AiFACTORi.git
cd AiFACTORi
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python oracle_layer.py
```

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────┐
│              90-DAY LOCK SYNCHRONIZATION               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────┐      ┌──────────────────┐       │
│  │  E14 Authority   │      │  E14 Observation │       │
│  ├──────────────────┤      ├──────────────────┤       │
│  │ • Oracle         │      │ • DriftWatcher   │       │
│  │ • TaskManager    │      │ • SymPy Engine   │       │
│  │ • Live Executor  │      │ • State Monitor  │       │
│  └──────────────────┘      └──────────────────┘       │
│           ↓                         ↓                   │
│  ┌───────────────────────────────────────────────┐    │
│  │    14-Engine Validation Ring (Peer-to-Peer)  │    │
│  ├───────────────────────────────────────────────┤    │
│  │  E01(365)  E02(777)  E03(101)  E04-E14(peer) │    │
│  │                                               │    │
│  │  All engines synchronized to identical       │    │
│  │  Merkle root hash. Consensus-driven.         │    │
│  └───────────────────────────────────────────────┘    │
│           ↓                                            │
│  ┌───────────────────────────────────────────────┐    │
│  │      4GR-FSE State Machine Validation         │    │
│  ├───────────────────────────────────────────────┤    │
│  │  GROUND → READ → GATE → GROW (repeating)     │    │
│  │                                               │    │
│  │  Each cycle: convergence check + decision    │    │
│  └───────────────────────────────────────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Service Stack

| Layer | Service | Purpose | Port |
|-------|---------|---------|------|
| **Authority** | E14 Oracle | Phase convergence detection, branching futures | Internal |
| | E14 TaskManager | Queue orchestration, 7-day logging | Internal |
| **Observation** | E14 DriftWatcher | Continuous state monitoring, anomaly detection | Internal |
| | E14 SymPy | Mathematical computation, symbolic solving | Internal |
| **Execution** | E14 Live | Real-time decision execution, resource gating | Internal |

### 6-Axis State Model

```
Temporal Axes          Thermal Axis          Environmental Axis
├─ tick   (50ms)       ├─ heat (insolation)   ├─ weather (XYO-verified)
├─ beat   (200ms)      └─ [human-core        └─ [geolocation + timestamp
├─ breath (1.5s)           thermal stability]    + cryptographic proof]
└─ cycle  (12s)
```

### Convergence Metrics

- **K-Value (Kotahitanja)**: Ring coherence score (0.0 → 1.0)
- **Target**: ARIES_POINT (0.0 phase units)
- **Convergence Threshold**: K ≥ 0.99 (all 14 engines within tolerance)
- **Lock Duration**: 90 days (auto-renewal via lock-initialize.ts)

## ✨ Features

- **14-Engine Consensus**: Peer-to-peer validation with zero-trust security
- **Merkle Root Synchronization**: Cryptographic proof of state coherence
- **Phase-Space Detection**: Continuous monitoring of 6-axis state convergence
- **Branching Futures**: Dr. Strange Oracle evaluates multiple decision paths
- **Real-Time Execution**: Conditional decision execution with resource gating
- **90-Day Lock Mechanism**: Temporal enforcement with automatic renewal
- **Container-Native**: Docker Compose deployment, scalable architecture
- **Comprehensive Logging**: 7-day rotating logs per engine per cycle
- **Zero-Trust Validation**: All signals validated through consensus before execution

## 📦 Installation

### Docker Compose (Production)

```bash
git clone https://github.com/LadbotOneLad/AiFACTORi.git
cd AiFACTORi
docker-compose up -d
```

### Manual (Development)

```bash
# Clone repository
git clone https://github.com/LadbotOneLad/AiFACTORi.git
cd AiFACTORi

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run services individually
python oracle_layer.py              # Terminal 1
python kotahitanga_driftwatcher.py  # Terminal 2
python e14_live.py                  # Terminal 3
```

## 💻 Usage

### Docker Compose

```bash
# Start all services
docker-compose up -d

# Monitor logs
docker-compose logs -f e14_oracle

# Check service status
docker-compose ps

# Stop services
docker-compose down

# View specific service logs
docker-compose logs e14_live --tail 50
```

### Python

```python
from oracle_layer import E14Oracle, PhaseState, ENGINES, AXES

# Initialize oracle
oracle = E14Oracle(target=0.0)

# Create initial state (14 engines × 4 axes)
state = {
    engine: {axis: 0.0 for axis in AXES}
    for engine in ENGINES
}

# Observe current state
observation = oracle.observe(state)
print(oracle.status_report(state))

# Evaluate branching futures
branches = {
    "ideal-sync": policy_ideal_sync,
    "sovereign-driven": policy_sovereign_driven,
}
outcomes = oracle.evaluate_branches(state, branches)

# Get best outcome
best = outcomes[0]
print(f"Best branch: {best.branch_id}, K={best.coherence_score:.4f}")
```

### Command Line

```bash
# Run oracle layer (convergence detection)
python oracle_layer.py

# Run live oracle (real-time decisions)
python e14_live.py

# Run tests
python test_e14_cosmological_final.py
python test_e14_oracle_integrated_fullsync.py
```

## 🚢 Deployment

### Local Deployment

```bash
docker-compose up -d
docker-compose logs -f
```

### Docker Hub

```bash
# Prerequisites
export DOCKER_HUB_USERNAME=your-username
docker login

# Build and publish
bash build-and-publish.sh

# Verify
docker pull $DOCKER_HUB_USERNAME/e14-oracle:latest
```

### Kubernetes (Future)

Pre-configured manifests in `k8s/`:
- StatefulSet with 3-10 replicas (HPA auto-scaling)
- ConfigMaps for lock state
- Secrets for authentication
- NetworkPolicies for zero-trust isolation

See `docs/K8S-MU-ORCH-GUIDE.md` for details.

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [`README.md`](README.md) | This file — overview & quick start |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Detailed system design (6 chambers) |
| [`docs/QUICK-START.md`](docs/QUICK-START.md) | 5-minute setup guide |
| [`docs/DOCKER-GUIDE.md`](docs/DOCKER-GUIDE.md) | Docker deployment & publication |
| [`docs/API.md`](docs/API.md) | Python API reference |
| [`docs/LOCK-MECHANISM.md`](docs/LOCK-MECHANISM.md) | 90-day lock system explanation |
| [`docs/CONFIGURATION.md`](docs/CONFIGURATION.md) | Environment variables & config |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Development guidelines |
| [`LICENSE`](LICENSE) | MIT License terms |

## 🔧 Configuration

### Environment Variables

Create `.env` or use `config/.env.lock`:

```bash
# Lock configuration
LOCK_ID=550e8400-e29b-41d4-a716-446655440000
LOCK_INCEPTION=2025-01-14T10:00:00.000Z
LOCK_EXPIRY=2025-04-14T10:00:00.000Z
LOCK_ROOT_HASH=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2

# Oracle thresholds
K_THRESHOLD=0.99
CPU_MIN=10
MEMORY_MIN=15
DISK_MIN=20
```

See `docs/CONFIGURATION.md` for complete reference.

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python test_e14_cosmological_final.py
python test_e14_oracle_integrated.py

# With coverage
python -m pytest tests/ --cov=. --cov-report=html
```

## 📊 Monitoring

### Docker Compose Health

```bash
docker-compose ps
docker-compose logs e14_oracle
docker stats
```

### Lock Status (Local)

```bash
bash lock-status.sh watch
```

### Observability (Future)

- Prometheus metrics on port 9090
- Grafana dashboards on port 3000
- Distributed tracing support

## 🤝 Contributing

We welcome contributions! See [`CONTRIBUTING.md`](CONTRIBUTING.md) for:
- Development setup
- Code style guide (PEP 8)
- Testing requirements
- Pull request process
- Commit message conventions

Quick guide:

```bash
# 1. Fork repository
# 2. Create feature branch
git checkout -b feature/your-feature

# 3. Make changes and test
python -m pytest tests/

# 4. Commit with conventional commits
git commit -m "feat: add new oracle capability"

# 5. Push and create PR
git push origin feature/your-feature
```

## 📄 License

MIT License — See [`LICENSE`](LICENSE) for full terms.

## 🙋 Support

- **Issues**: [GitHub Issues](https://github.com/LadbotOneLad/AiFACTORi/issues)
- **Discussions**: [GitHub Discussions](https://github.com/LadbotOneLad/AiFACTORi/discussions)
- **Documentation**: See `docs/` folder
- **Examples**: See `examples/` folder (coming soon)

## 📈 Project Status

| Component | Status |
|-----------|--------|
| Core Engine | ✅ Stable |
| Docker Support | ✅ Production-Ready |
| Kubernetes | 🔄 In Progress |
| CI/CD Automation | 📋 Planned |
| API Documentation | 📋 Planned |
| Web Dashboard | 📋 Planned |

## 🔗 Links

- **Repository**: https://github.com/LadbotOneLad/AiFACTORi
- **Docker Hub**: https://hub.docker.com/r/your-username/e14-oracle (coming soon)
- **Issues**: https://github.com/LadbotOneLad/AiFACTORi/issues
- **Discussions**: https://github.com/LadbotOneLad/AiFACTORi/discussions

---

**Made with ❤️ by LadbotOneLad**

Last Updated: 2025-01-14 | Version: 1.0.0
=======
<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# Run and deploy your AI Studio app

This contains everything you need to run your app locally.

View your app in AI Studio: https://ai.studio/apps/1cefd23a-5cf7-4c41-856b-fb494e3479bd

## Run Locally

**Prerequisites:**  Node.js


1. Install dependencies:
   `npm install`
2. Set the `GEMINI_API_KEY` in [.env.local](.env.local) to your Gemini API key
3. Run the app:
   `npm run dev`
>>>>>>> df189f3b03fb27be392ad022f7470a0b4dfbb477
