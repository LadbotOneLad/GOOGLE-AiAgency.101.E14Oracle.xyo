# HC-AOL Quick Reference

## System in 30 Seconds

**HC-AOL = Human-Controlled Autonomous Orchestration Layer**

- You (human) define tasks
- Three engines evaluate them
- You approve or reject
- You authorize submission
- System logs everything

**No autonomous actions. Ever.**

---

## Task Lifecycle

```
1. Human defines task
   ↓
2. System queues for evaluation
   ↓
3. Three rings evaluate
   ↓
4. Human reviews results
   ↓
5. Human approves/rejects
   ↓
6. If approved: Human authorizes submission
   ↓
7. Complete audit trail logged
```

---

## Three Rings

| Ring | Temp | Rejection | Role |
|------|------|-----------|------|
| **Validator** | 0.05 | ~71% | Safety filter |
| **Sovereign** | 0.075 | ~60% | Viability scorer |
| **TENET** | ∞ | 100% hard limits | Boundary enforcer |

**All three must accept for ACCEPT.**

---

## Example Usage

```python
from hc_aol_implementation import HC_AOL_Implementation, HumanTaskDefinition

# 1. Initialize
orch = HC_AOL_Implementation(human_operator="Rebecca")

# 2. Define task
task = HumanTaskDefinition(
    task_id="KAGGLE-001",
    competition_name="Titanic",
    dataset_source="/data/titanic.csv",
    model_search_space={"algorithm": ["rf", "xgb"], "depth": [3, 5, 7]},
    resource_limits={"max_runtime_seconds": 3600, "max_memory_mb": 2048},
    safety_constraints=["no_external_calls", "local_only"],
    human_operator="Rebecca",
    created_at="2026-03-25T12:00:00",
)

# 3. Register
orch.register_human_task_definition(task)

# 4. Evaluate
orch.evaluate_human_task("KAGGLE-001")

# 5. Review
pending = orch.get_human_review_queue()

# 6. Approve
orch.human_approve_for_submission(
    "KAGGLE-001",
    "APPROVE_FOR_SUBMISSION",
    "Looks good"
)

# 7. Authorize submission
orch.human_authorize_submission(
    "KAGGLE-001",
    solution_summary="Random Forest",
    model_parameters={"algorithm": "rf", "depth": 7},
    predicted_score=0.82,
    resource_usage={"runtime": 450, "memory": 512}
)

# 8. Export audit
print(orch.export_audit_trail("KAGGLE-001"))
```

---

## API Endpoints (Flask)

```
POST   /api/task/register
GET    /api/tasks/pending-review
POST   /api/task/<id>/evaluate
POST   /api/task/<id>/approve
POST   /api/task/<id>/authorize-submission
GET    /api/task/<id>/audit-trail
GET    /api/summary
```

---

## Key Files

| File | Purpose |
|------|---------|
| `hc_aol_specification.py` | Core data structures & engine |
| `hc_aol_implementation.py` | Concrete implementation + example |
| `HC-AOL_SPECIFICATION.md` | Full documentation |
| `hc_aol_api.py` | Flask REST API |

---

## Data Flow

```
Human Input
    ↓
Task Definition (complete, explicit)
    ↓
Register in System
    ↓
Three-Ring Consensus Evaluation
    ├─ Validator (safety check)
    ├─ Sovereign (viability score)
    └─ TENET (hard limits)
    ↓
Report to Human
    ↓
Human Review ← CRITICAL CHECKPOINT
    ↓
APPROVE or REJECT
    ↓
If APPROVE:
  ├─ Generate solution candidate
  ├─ Show predicted score
  └─ Wait for human submission auth
    ↓
Human Submits ← CRITICAL CHECKPOINT
    ↓
Complete Audit Trail Logged
```

---

## Guarantees

✓ **Human Authority**  
✓ **No Autonomous Submissions**  
✓ **No Task Creation Bypass**  
✓ **Complete Traceability**  
✓ **Hard Boundary Enforcement**  
✓ **Enterprise Compliance**  

---

## Kaggle/AIcrowd Workflow

```
1. Human: "Solve Kaggle Titanic"
   → Define: algorithm options, parameters, limits
   → Dataset source: /approved/data/titanic.csv
   → Safety: no_external_calls, local_only

2. System: Evaluate options
   → Validator: Is this safe? YES
   → Sovereign: Which model best? XGBoost (score: 0.87)
   → TENET: Within resource limits? YES

3. Human: Review results
   → Read: XGBoost predicted score 0.87
   → See: Uses 450s CPU, 512MB RAM
   → Decide: Approve for submission

4. System: Show submission details
   → Solution: XGBoost(depth=7, lr=0.05)
   → Predicted score: 0.87
   → Resource usage: 450s, 512MB

5. Human: Click "Submit to Kaggle"
   → System formats solution
   → Posts to Kaggle API
   → Logs submission ID and response

6. Audit Trail:
   → Who defined? Rebecca
   → When? 2026-03-25 12:00:00
   → What approved? XGBoost config
   → When submitted? 2026-03-25 12:05:00
   → Result? Submission ID 12345
```

---

## Testing

```bash
python hc_aol_implementation.py
# Runs complete example workflow

python -m pytest hc_aol_tests.py -v
# Runs test suite
```

---

## Deployment

```bash
# Docker
docker build -t hc-aol:latest .
docker run -it hc-aol:latest

# Kubernetes
kubectl apply -f hc-aol-deployment.yaml

# Local
python hc_aol_implementation.py
```

---

## Emergency Stop

If system behaves unexpectedly:

```python
# View all tasks
orch.list_all_tasks()

# View pending human actions
orch.get_human_review_queue()

# Reject task (human override)
orch.human_approve_for_submission(
    task_id="TASK-ID",
    decision="REJECT",
    notes="Halting this task immediately"
)
```

---

## Compliance

For auditors/regulators:

```bash
# View all approvals
cat logs/approvals.jsonl

# View all rejections
cat logs/rejections.jsonl

# View audit trail for specific task
cat logs/audit/TASKID.json

# View system summary
curl http://localhost:8000/api/summary
```

---

**© 2026 Rebecca — HC-AOL v1.0**

**Human-Controlled. Autonomous-Assisted. Always Auditable.**
