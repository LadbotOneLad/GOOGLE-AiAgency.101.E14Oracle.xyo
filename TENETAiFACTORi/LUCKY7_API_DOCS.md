# LUCKY7-ENGINE Metrics API

## Overview

**Port 6665** — Real-time metrics API for your 12-engine cluster. Exposes phase, power, coherence, RPM, and knock indicators as JSON over HTTP.

## Quick Start

### Run Locally
```bash
docker run -d -p 6665:6665 --name lucky7-api lucky7-metrics-api:latest
```

### Test
```bash
# Health check
curl http://localhost:6665/health

# All engines
curl http://localhost:6665/aggregate

# Single engine
curl http://localhost:6665/metrics/codex-engine-1

# List engines
curl http://localhost:6665/engines
```

## Endpoints

### `GET /health`
Health check. Returns `{"status": "healthy"}`.

### `GET /aggregate`
Aggregated metrics across all engines.

**Response:**
```json
{
  "timestamp": "2026-04-03T23:38:28.134548",
  "engines_active": 12,
  "aggregate": {
    "avg_phase": 0.4332,
    "avg_power": 0.6061,
    "avg_coherence": 0.3947,
    "avg_error": 6.283,
    "knock_rate": 0.0833
  },
  "engines": [...]
}
```

### `GET /metrics?engine=codex-engine-1`
Single engine metrics (query param).

### `GET /metrics/{engine_name}`
Single engine metrics (path param).

**Response:**
```json
{
  "engine": "codex-engine-1",
  "engine_id": "1",
  "tick": 140904,
  "rpm": 5807.3,
  "phase": 0.14,
  "power": 0.935,
  "coherence": 0.694,
  "geometry": 0.0,
  "error": 6.292,
  "knock": true,
  "timestamp": "2026-04-03T23:38:32.338017"
}
```

### `GET /engines`
List all engines.

**Response:**
```json
{
  "total": 12,
  "engines": ["codex-engine-1", "codex-engine-2", ...],
  "api_endpoint": "http://localhost:6665"
}
```

## Metrics Explained

| Field | Range | Meaning |
|-------|-------|---------|
| `phase` | 0-1 | Engine cycle phase (sine-wave position) |
| `power` | 0-1 | Computational power output |
| `coherence` | 0-1 | Internal alignment quality |
| `rpm` | ~5800 | Rotations per minute (cycle speed) |
| `error` | ~6.28 | Phase error magnitude |
| `knock` | bool | Anomaly detection flag |
| `tick` | int | Cycle counter |

## Deployment

### Docker Compose
Add to your compose stack:
```yaml
services:
  lucky7-api:
    image: lucky7-metrics-api:latest
    ports:
      - "6665:6665"
    restart: unless-stopped
```

### Cloud (AWS/GCP/Azure)
```bash
docker tag lucky7-metrics-api:latest yourorg/lucky7-metrics-api:latest
docker push yourorg/lucky7-metrics-api:latest
```

Then deploy container to your cloud platform.

## Next Steps (Phase 2)

- **Add authentication** — API keys for production
- **Add metering** — Request count tracking for billing
- **Add persistence** — Store metrics to database
- **Add dashboards** — Grafana integration

## Files

- `lucky7_api.py` — FastAPI application
- `Dockerfile.lucky7` — Multi-stage production build
- `requirements.txt` — Python dependencies
- `docker-compose-lucky7-api.yml` — Docker Compose template

---

**Status**: Production-ready. Running on `0.0.0.0:6665`. Ready to monetize.
