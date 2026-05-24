# Codex 6.65: Human-Controlled System

## Overview

**Codex 6.65: codebecslucky7 Edition** with **human-in-the-loop decision approval**.

This system runs three parallel consensus rings (Inner Validator, Sovereign, TENET) that evaluate states and queue decisions for **human review before execution**.

### Architecture

```
State Input
    ↓
Three-Ring Consensus (Inner → Sovereign → TENET)
    ↓
Decision + Review Request
    ↓
Human Review API (Flask)
    ↓
Approve / Reject (Human chooses)
    ↓
Audit Trail Logged
```

**Key**: All decisions wait for human approval. No autonomous execution.

---

## Running the System

### Option 1: Docker Compose (Recommended)

```bash
# Build and start
docker compose -f docker-compose.human-controlled.yml up -d

# Check status
docker compose logs -f

# Access review API
curl http://localhost:8000/api/dashboard
```

### Option 2: Local Python

```bash
# Install dependencies
pip install flask pydantic

# Start review API
python review_api.py

# In another terminal: send evaluations
python human_controlled_orchestrator.py
```

---

## Three-Ring Consensus

### Inner Validator Ring (T=0.05)
- **Target rejection rate**: ~71%
- **Role**: High-frequency filter (membrane)
- **Checks**: Coherence > threshold, Power stability

### Sovereign Ring (T=0.075)
- **Target rejection rate**: ~60%
- **Role**: Policy enforcement
- **Checks**: Geometry alignment (within 2π ± 0.15)

### TENET Horizon (T=∞)
- **Target rejection rate**: 100% on violations
- **Role**: Hard boundary enforcement
- **Checks**: Drift ≤ 1.0, Time ≤ 86400s, Coherence sane

**Consensus**: All three must accept for final ACCEPT.

---

## Human Review API

### Evaluate a State

```bash
curl -X POST http://localhost:8000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "state": {
      "phase": 0.5,
      "power": 0.7,
      "geom_ratio": 6.28,
      "geom_error": 0.05
    },
    "coherence": 0.95,
    "power": 0.7,
    "elapsed_seconds": 1000.0,
    "consensus_id": "DECISION-0001"
  }'
```

Response:
```json
{
  "success": true,
  "consensus_id": "DECISION-0001",
  "decision": "ACCEPT",
  "requires_review": false,
  "coherence_score": 0.95,
  "message": "Auto-approved"
}
```

### Get Pending Reviews

```bash
curl http://localhost:8000/api/pending
```

Response:
```json
{
  "count": 2,
  "pending": [
    {
      "consensus_id": "DECISION-0005",
      "decision": "ACCEPT",
      "coherence_score": 0.08,
      "requires_review": true,
      "timestamp": "2026-03-25T12:00:00"
    }
  ]
}
```

### Approve a Decision

```bash
curl -X POST http://localhost:8000/api/approve/DECISION-0005 \
  -H "Content-Type: application/json" \
  -d '{"notes": "Approved after manual verification"}'
```

### Reject a Decision

```bash
curl -X POST http://localhost:8000/api/reject/DECISION-0005 \
  -H "Content-Type: application/json" \
  -d '{"reason": "Coherence too low for this use case"}'
```

### View Dashboard

```bash
curl http://localhost:8000/api/dashboard
```

---

## Audit Trail

All decisions are logged:

- **Requests**: `/logs/review/requests.jsonl`
- **Approvals**: `/logs/review/approvals.jsonl`
- **Rejections**: `/logs/review/rejections.jsonl`

Each line is JSON:
```json
{
  "consensus_id": "DECISION-0001",
  "action": "APPROVED",
  "notes": "...",
  "timestamp": "2026-03-25T12:00:00"
}
```

---

## Integration with Kaggle/AIcrowd

### Workflow

1. **Fetch challenge** from Kaggle/AIcrowd API
2. **Format as state** using `challenge_adapter.py`
3. **POST to `/api/evaluate`** with state
4. **Human reviews** in dashboard
5. **Human approves** via `/api/approve/<consensus_id>`
6. **System formats** and **submits** solution

Example:

```python
# fetch_and_submit_challenge.py
import requests
from challenge_adapter import KaggleAdapter

adapter = KaggleAdapter(api_key="...")
challenge = adapter.fetch_challenges()[0]
state = adapter.format_challenge_as_state(challenge)

# Send to human review
response = requests.post(
    "http://human-review-api:8000/api/evaluate",
    json={
        "state": state,
        "coherence": 0.9,
        "power": 0.75,
        "elapsed_seconds": 1000.0,
        "consensus_id": challenge["id"]
    }
)

decision = response.json()
print(f"Decision: {decision['decision']}")
print(f"Requires review: {decision['requires_review']}")

# Wait for human approval (check /api/pending periodically)
# Then submit solution...
```

---

## Key Features

✓ **Human-controlled**: Every decision waits for human approval  
✓ **Transparent**: All logic is auditable and logged  
✓ **Three-ring consensus**: Multiple validation layers  
✓ **Auto-review**: Flags borderline decisions for human attention  
✓ **Audit trail**: Complete record of all decisions and approvals  
✓ **REST API**: Easy integration with external systems  
✓ **Containerized**: Docker Compose for easy deployment  

---

## Monitoring

### Metrics Endpoint

```bash
curl http://localhost:8000/api/summary
```

Response:
```json
{
  "pending_reviews": 2,
  "approved": 45,
  "rejected": 3,
  "total_processed": 48,
  "inner_ring_metrics": {
    "temperature": 0.05,
    "target_rejection": 0.71,
    "actual_rejection": 0.68,
    "processed": 1000
  },
  "sovereign_ring_metrics": {
    "temperature": 0.075,
    "target_rejection": 0.6,
    "actual_rejection": 0.58,
    "processed": 1000
  },
  "tenet_ring_metrics": {
    "temperature": Infinity,
    "hard_boundary": true,
    "processed": 1000
  }
}
```

---

## Security Notes

- **No autonomous submission**: All decisions require human approval
- **Audit logging**: Every action is recorded
- **API restricted**: Use reverse proxy (nginx) in production with auth
- **Log retention**: Keep approval logs for compliance

---

## Next Steps

1. Deploy locally: `docker compose -f docker-compose.human-controlled.yml up -d`
2. Test API: `curl http://localhost:8000/api/health`
3. Send evaluation: `POST /api/evaluate`
4. Approve/reject: `POST /api/approve/<id>`
5. Integrate with Kaggle: Implement `challenge_adapter.py`
6. Deploy to cloud: Use same compose file on VM

---

**© 2026 Rebecca — Codex 6.65: codebecslucky7 Edition**

Human-controlled. Transparent. Auditable.
