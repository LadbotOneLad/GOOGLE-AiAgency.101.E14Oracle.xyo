"""
MCP Audit Server - HTTP/WebSocket server for enhanced MCP suite with full auditing
"""

import json
import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

from mcp_suite_v2_enhanced import (
    EnhancedMCPRouter,
    ServiceType,
    SecurityError,
)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize enhanced router
router = EnhancedMCPRouter()

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": list(router.services.keys()),
    }), 200


@app.route('/metrics', methods=['GET'])
def metrics():
    """System metrics endpoint"""
    return jsonify({
        "total_requests": len(router.audit_logger.audit_logs),
        "audit_logs": len(router.audit_logger.audit_logs),
        "alerts": len(router.alert_manager.alerts),
        "timestamp": datetime.utcnow().isoformat(),
    }), 200


@app.route('/audit', methods=['GET'])
def get_audit_logs():
    """Get audit logs with optional filtering"""
    service = request.args.get('service')
    hours = int(request.args.get('hours', 24))
    limit = int(request.args.get('limit', 100))
    
    logs = [
        r.to_dict() for r in router.audit_logger.audit_logs
        if (not service or r.service == service)
    ][-limit:]
    
    return jsonify({
        "total": len(logs),
        "logs": logs,
        "filters": {"service": service, "hours": hours, "limit": limit},
    }), 200


@app.route('/audit/export', methods=['GET'])
def export_audit():
    """Export audit logs"""
    format_type = request.args.get('format', 'json')
    
    export_data = router.audit_logger.export_audit(format_type)
    
    return jsonify({
        "format": format_type,
        "data": export_data,
        "timestamp": datetime.utcnow().isoformat(),
    }), 200


@app.route('/alerts', methods=['GET'])
def get_alerts():
    """Get active alerts"""
    severity = request.args.get('severity')
    status = request.args.get('status', 'open')
    
    alerts = [
        a for a in router.alert_manager.alerts
        if (not severity or a['severity'] == severity) and a['status'] == status
    ]
    
    return jsonify({
        "total": len(alerts),
        "alerts": alerts,
    }), 200


@app.route('/alerts/<alert_id>/resolve', methods=['POST'])
def resolve_alert(alert_id):
    """Resolve an alert"""
    data = request.get_json()
    resolution = data.get('resolution', 'Manually resolved')
    
    asyncio.run(
        router.alert_manager.resolve_alert(alert_id, resolution)
    )
    
    return jsonify({
        "alert_id": alert_id,
        "status": "resolved",
        "timestamp": datetime.utcnow().isoformat(),
    }), 200


@app.route('/validate/<service>/<method>', methods=['POST'])
def validate_call(service, method):
    """Validate a service call without executing"""
    params = request.get_json()
    
    try:
        validation = asyncio.run(
            router.validator.validate_input(service, method, params)
        )
        
        compliance = asyncio.run(
            router.compliance_checker.check_compliance(service, method, params)
        )
        
        return jsonify({
            "service": service,
            "method": method,
            "validation": {
                "passed": validation.passed,
                "score": validation.score,
                "checks": validation.checks,
            },
            "compliance": {
                "passed": compliance.passed,
                "score": compliance.score,
                "checks": compliance.checks,
            },
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/risk/<service>/<method>', methods=['POST'])
def assess_risk(service, method):
    """Assess risk of a service call"""
    params = request.get_json()
    
    try:
        risk = asyncio.run(
            router.risk_analyzer.assess_risk(service, method, params)
        )
        
        return jsonify({
            "service": service,
            "method": method,
            "risk_level": risk.risk_level,
            "risk_score": risk.risk_score,
            "threats": risk.threats,
            "mitigations": risk.mitigations,
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/anomalies/<service>', methods=['GET'])
def get_anomalies(service):
    """Get detected anomalies for a service"""
    metrics = request.args.to_dict()
    
    try:
        anomalies = asyncio.run(
            router.anomaly_detector.detect_anomalies(service, metrics)
        )
        
        return jsonify({
            "service": service,
            "anomalies_detected": len(anomalies) > 0,
            "anomalies": anomalies,
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/performance/<service>', methods=['GET'])
def get_performance(service):
    """Get performance analytics for a service"""
    logs = [
        r for r in router.audit_logger.audit_logs
        if r.service == service
    ]
    
    execution_times = [r.execution_time_ms for r in logs]
    
    if not execution_times:
        return jsonify({"error": f"No data for {service}"}), 404
    
    perf = asyncio.run(
        router.perf_analyzer.analyze_performance(service, execution_times)
    )
    
    return jsonify({
        "service": service,
        "metrics": perf,
        "sample_size": len(execution_times),
    }), 200


@app.route('/lineage/<data_id>', methods=['GET'])
def get_lineage(data_id):
    """Get data lineage for a data ID"""
    lineage = asyncio.run(
        router.lineage_tracker.get_lineage(data_id)
    )
    
    return jsonify({
        "data_id": data_id,
        "lineage": lineage,
    }), 200


@app.route('/call/<service>/<method>', methods=['POST'])
def call_service(service, method):
    """Execute a service call through MCP with full audit trail"""
    
    request_id = str(uuid.uuid4())
    user_id = request.headers.get('X-User-ID', 'anonymous')
    params = request.get_json() or {}
    
    try:
        service_type = ServiceType[service.upper()]
    except KeyError:
        return jsonify({"error": f"Unknown service: {service}"}), 400
    
    try:
        result = asyncio.run(
            router.call(
                service_type=service_type,
                method=method,
                request_id=request_id,
                user_id=user_id,
                **params
            )
        )
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
    
    except Exception as e:
        logger.exception(f"Error calling {service}.{method}")
        return jsonify({
            "request_id": request_id,
            "success": False,
            "error": str(e),
        }), 500


@app.route('/call', methods=['POST'])
def call_generic():
    """Generic MCP call endpoint"""
    
    data = request.get_json()
    service_str = data.get('service', '').upper()
    method = data.get('method')
    params = data.get('params', {})
    request_id = data.get('request_id', str(uuid.uuid4()))
    user_id = request.headers.get('X-User-ID', 'anonymous')
    
    if not service_str or not method:
        return jsonify({
            "error": "Missing 'service' or 'method'"
        }), 400
    
    try:
        service_type = ServiceType[service_str]
    except KeyError:
        return jsonify({"error": f"Unknown service: {service_str}"}), 400
    
    result = asyncio.run(
        router.call(
            service_type=service_type,
            method=method,
            request_id=request_id,
            user_id=user_id,
            **params
        )
    )
    
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code


@app.route('/status', methods=['GET'])
def status():
    """System status endpoint"""
    total_logs = len(router.audit_logger.audit_logs)
    success_logs = len([l for l in router.audit_logger.audit_logs if l.status == "success"])
    failure_logs = len([l for l in router.audit_logger.audit_logs if l.status == "failure"])
    open_alerts = len([a for a in router.alert_manager.alerts if a['status'] == 'open'])
    
    success_rate = (success_logs / total_logs * 100) if total_logs > 0 else 0
    
    return jsonify({
        "timestamp": datetime.utcnow().isoformat(),
        "audit_stats": {
            "total_calls": total_logs,
            "successful": success_logs,
            "failed": failure_logs,
            "success_rate": f"{success_rate:.2f}%",
        },
        "alerts": {
            "open": open_alerts,
            "total": len(router.alert_manager.alerts),
        },
        "services": list(router.services.keys()),
    }), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    logger.info("Starting MCP Audit Server v2...")
    logger.info("Available endpoints:")
    logger.info("  GET  /health - System health")
    logger.info("  GET  /metrics - System metrics")
    logger.info("  GET  /status - System status")
    logger.info("  GET  /audit - Audit logs")
    logger.info("  GET  /alerts - Active alerts")
    logger.info("  POST /call/{service}/{method} - Execute service call")
    logger.info("  POST /validate/{service}/{method} - Validate without executing")
    logger.info("  POST /risk/{service}/{method} - Risk assessment")
    logger.info("  GET  /performance/{service} - Performance analytics")
    
    app.run(
        host='0.0.0.0',
        port=8888,
        debug=False,
        threaded=True,
    )
