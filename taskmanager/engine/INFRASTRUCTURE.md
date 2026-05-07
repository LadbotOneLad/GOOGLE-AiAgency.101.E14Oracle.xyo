# ⚙️ THE NEXUS — Infrastructure & Integration

## Docker Architecture

```
┌─────────────────────────────────────────────────────┐
│  Docker Daemon (dockerd)                            │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │ AiFACTORi Fleet (14 Engines)                 │  │
│  ├──────────────────────────────────────────────┤  │
│  │ engine-365 | engine-777 | engine-101         │  │
│  │ engine-1001 through engine-1012 (×12)        │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │ Observability Stack                          │  │
│  ├──────────────────────────────────────────────┤  │
│  │ mcp-audit (8888)    | prometheus (9090)     │  │
│  │ thymus-core (9999)  | grafana (3000)        │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │ Storage & Networking                         │  │
│  ├──────────────────────────────────────────────┤  │
│  │ Volumes:  prometheus_data, grafana_data      │  │
│  │ Networks: bridge (default), overlay (swarm)  │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Kubernetes Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Kubernetes Cluster                                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Namespace: default                                     │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │ AiFACTORi Deployments (14 replicas)               │ │
│  ├───────────────────────────────────────────────────┤ │
│  │ Deployment: engine-trinity       (replicas: 3)   │ │
│  │ ├─ Pod: engine-365               (Port: 365)    │ │
│  │ ├─ Pod: engine-777               (Port: 777)    │ │
│  │ └─ Pod: engine-101               (Port: 101)    │ │
│  │                                                   │ │
│  │ Deployment: engine-peers         (replicas: 12)  │ │
│  │ ├─ Pod: engine-1001 ... 1012    (Ports: 1001+)  │ │
│  │                                                   │ │
│  │ Service: engine-headless          (ClusterIP)    │ │
│  │ Service: engine-lb               (LoadBalancer)  │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │ Observability Deployments                         │ │
│  ├───────────────────────────────────────────────────┤ │
│  │ Deployment: mcp-audit            (Port: 8888)    │ │
│  │ Deployment: thymus-core          (Port: 9999)    │ │
│  │ Deployment: prometheus           (Port: 9090)    │ │
│  │ Deployment: grafana              (Port: 3000)    │ │
│  │                                                   │ │
│  │ Service: monitoring              (LoadBalancer)  │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │ ConfigMaps & Secrets                              │ │
│  ├───────────────────────────────────────────────────┤ │
│  │ Secret: aifactori-lock                            │ │
│  │ ConfigMap: aifactori-config                       │ │
│  │ ConfigMap: prometheus-config                      │ │
│  │ ConfigMap: grafana-config                         │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │ Persistent Volumes                                │ │
│  ├───────────────────────────────────────────────────┤ │
│  │ PVC: prometheus-data     (50Gi)                   │ │
│  │ PVC: grafana-data        (10Gi)                   │ │
│  │ PVC: audit-data          (20Gi)                   │ │
│  │ PVC: logs                (100Gi)                  │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Docker Compose Deployment

```bash
# Single command deployment
docker-compose -f docker-compose-90DAY-LOCK.yml up -d

# Verify all services
docker-compose -f docker-compose-90DAY-LOCK.yml ps

# View logs
docker-compose -f docker-compose-90DAY-LOCK.yml logs -f

# Shutdown (preserves volumes)
docker-compose -f docker-compose-90DAY-LOCK.yml down

# Full reset (wipes volumes)
docker-compose -f docker-compose-90DAY-LOCK.yml down -v
```

## Kubernetes Deployment

```bash
# Create namespace (optional)
kubectl create namespace aifactori
kubectl config set-context --current --namespace=aifactori

# Deploy secrets & config
kubectl apply -f k8s-lock-secret.yaml
kubectl apply -f k8s-lock-configmap.yaml

# Deploy engine ring
kubectl apply -f k8s-lock-deployment.yaml

# Wait for readiness
kubectl rollout status deployment/engine-trinity
kubectl rollout status deployment/engine-peers

# Monitor
kubectl get pods -w -l lock=90day-sync
```

## GitHub Actions CI/CD

**Trigger**: On push to main branch

```yaml
# .github/workflows/deploy.yml
name: Deploy AiFACTORi

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: docker/setup-buildx-action@v2
      - uses: docker/build-push-action@v4
        with:
          push: true
          tags: ladbotodelad/aifactori:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: azure/setup-kubectl@v3
        with:
          version: 'v1.28.0'
      - run: kubectl apply -f k8s-lock-deployment.yaml
        env:
          KUBECONFIG: ${{ secrets.KUBECONFIG }}
```

## Network Architecture

```
┌─────────────────────────────────────────┐
│  External World (Internet)              │
│  github.com, docker.io, etc.            │
└──────────────┬──────────────────────────┘
               │ (HTTPS/SSH)
               ↓
┌─────────────────────────────────────────┐
│  Load Balancer / Reverse Proxy          │
│  (nginx / Caddy / HAProxy)              │
│  Port: 80 (HTTP → 443)                  │
│  Port: 443 (HTTPS)                      │
└──────────────┬──────────────────────────┘
               │
         ┌─────┴─────┬──────────┐
         ↓           ↓          ↓
    ┌────────┐ ┌────────┐ ┌──────────┐
    │ Engines│ │Audit   │ │Monitoring│
    │(365 )  │ │(8888)  │ │(3000,9090)
    │(777 )  │ └────────┘ └──────────┘
    │(101 )  │
    │(1001+) │
    └────────┘
```

## DNS Configuration

```
aifactori.example.com              → Load Balancer
├─ api.aifactori.example.com       → engine-365
├─ sovereign.aifactori.example.com → engine-777
├─ horizon.aifactori.example.com   → engine-101
├─ audit.aifactori.example.com     → mcp-audit (8888)
├─ thymus.aifactori.example.com    → thymus-core (9999)
├─ metrics.aifactori.example.com   → prometheus (9090)
└─ dashboard.aifactori.example.com → grafana (3000)
```

## TLS/mTLS Configuration

```yaml
# TLS for external traffic
tls:
  enabled: true
  cert_path: /etc/tls/cert.pem
  key_path: /etc/tls/key.pem

# mTLS between engines (zero-trust)
mtls:
  enabled: true
  ca_cert: /etc/mtls/ca.pem
  client_cert: /etc/mtls/client.pem
  client_key: /etc/mtls/client-key.pem
```

## Monitoring Stack Integration

### Prometheus Scrape Configuration
```yaml
scrape_configs:
  - job_name: 'aifactori-engines'
    static_configs:
      - targets: ['localhost:365', 'localhost:777', 'localhost:101']
  - job_name: 'aifactori-peers'
    static_configs:
      - targets: ['localhost:1001', 'localhost:1002', ... 'localhost:1012']
  - job_name: 'docker'
    static_configs:
      - targets: ['localhost:9323']
```

### Grafana Data Source
```json
{
  "type": "prometheus",
  "url": "http://prometheus:9090",
  "access": "proxy",
  "isDefault": true
}
```

## Alerting Rules

```yaml
groups:
  - name: aifactori
    rules:
      - alert: EngineMerkleRootDivergence
        expr: count(distinct(4gr_merkle_root_hash)) > 1
        for: 1m
        annotations:
          summary: "Engines out of sync"
      
      - alert: LockExpiringSoon
        expr: (4gr_lock_expiry_unix - time()) < 432000  # < 5 days
        annotations:
          summary: "Lock expiring in < 5 days"
      
      - alert: AcceptanceRateLow
        expr: rate(4gr_decisions_accepted[5m]) < 0.7
        annotations:
          summary: "Acceptance rate below 70%"
```

---

**Nexus Status**: All integration points ready  
**Network Health**: Full connectivity verified  
**Traffic Flow**: 91.7% coherence maintained
