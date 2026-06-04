# Human Review API
# © 2026 Rebecca
# REST interface for human-in-the-loop decision approval

from flask import Flask, jsonify, request
from human_controlled_orchestrator import HumanControlledOrchestrator, HumanReviewRequest
import json
import os
from datetime import datetime

app = Flask(__name__)
orchestrator = HumanControlledOrchestrator()
LOG_DIR = os.getenv("LOG_DIR", "/logs/review")
os.makedirs(LOG_DIR, exist_ok=True)


@app.route("/health", methods=["GET"])
def health():
    """Health check"""
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})


@app.route("/api/evaluate", methods=["POST"])
def evaluate():
    """
    Evaluate a state and queue for human review if needed.
    
    POST body:
    {
      "state": {...},
      "coherence": 0.95,
      "power": 0.7,
      "elapsed_seconds": 1000.0,
      "consensus_id": "DECISION-0001"
    }
    """
    try:
        data = request.json
        state = data.get("state", {})
        coherence = data.get("coherence", 0.0)
        power = data.get("power", 0.0)
        elapsed_seconds = data.get("elapsed_seconds", 0.0)
        consensus_id = data.get("consensus_id", f"AUTO-{datetime.utcnow().isoformat()}")

        request_obj = orchestrator.evaluate_and_queue_for_review(
            state=state,
            coherence=coherence,
            power=power,
            elapsed_seconds=elapsed_seconds,
            consensus_id=consensus_id,
            timestamp_iso=datetime.utcnow().isoformat(),
        )

        # Log request
        with open(f"{LOG_DIR}/requests.jsonl", "a") as f:
            f.write(json.dumps({"consensus_id": consensus_id, "request": request_obj.to_json()}) + "\n")

        return jsonify({
            "success": True,
            "consensus_id": consensus_id,
            "decision": request_obj.decision,
            "requires_review": request_obj.requires_review,
            "coherence_score": request_obj.coherence_score,
            "message": "Queued for review" if request_obj.requires_review else "Auto-approved"
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/pending", methods=["GET"])
def get_pending():
    """Get all pending review requests"""
    pending = orchestrator.list_pending_reviews()
    return jsonify({
        "count": len(pending),
        "pending": [
            {
                "consensus_id": p.consensus_id,
                "decision": p.decision,
                "coherence_score": p.coherence_score,
                "requires_review": p.requires_review,
                "timestamp": p.timestamp_iso,
            }
            for p in pending
        ]
    }), 200


@app.route("/api/approve/<consensus_id>", methods=["POST"])
def approve(consensus_id):
    """Human approves a decision"""
    notes = request.json.get("notes", "") if request.json else ""
    success = orchestrator.approve_decision(consensus_id, notes)
    
    if success:
        with open(f"{LOG_DIR}/approvals.jsonl", "a") as f:
            f.write(json.dumps({
                "consensus_id": consensus_id,
                "action": "APPROVED",
                "notes": notes,
                "timestamp": datetime.utcnow().isoformat()
            }) + "\n")
        return jsonify({"success": True, "message": f"Approved: {consensus_id}"}), 200
    else:
        return jsonify({"success": False, "error": f"Not found: {consensus_id}"}), 404


@app.route("/api/reject/<consensus_id>", methods=["POST"])
def reject(consensus_id):
    """Human rejects a decision"""
    reason = request.json.get("reason", "No reason provided") if request.json else "No reason provided"
    success = orchestrator.reject_decision(consensus_id, reason)
    
    if success:
        with open(f"{LOG_DIR}/rejections.jsonl", "a") as f:
            f.write(json.dumps({
                "consensus_id": consensus_id,
                "action": "REJECTED",
                "reason": reason,
                "timestamp": datetime.utcnow().isoformat()
            }) + "\n")
        return jsonify({"success": True, "message": f"Rejected: {consensus_id}"}), 200
    else:
        return jsonify({"success": False, "error": f"Not found: {consensus_id}"}), 404


@app.route("/api/summary", methods=["GET"])
def summary():
    """Get orchestrator summary"""
    return jsonify(orchestrator.summary()), 200


@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    """Human dashboard view"""
    summary_data = orchestrator.summary()
    pending = orchestrator.list_pending_reviews()
    
    return jsonify({
        "timestamp": datetime.utcnow().isoformat(),
        "summary": summary_data,
        "pending_count": len(pending),
        "pending_decisions": [
            {
                "consensus_id": p.consensus_id,
                "decision": p.decision,
                "requires_review": p.requires_review,
                "coherence": p.coherence_score,
                "reason": p.reason,
            }
            for p in pending[:20]  # Limit to 20 most recent
        ]
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
