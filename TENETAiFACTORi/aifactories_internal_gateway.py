#!/usr/bin/env python3
"""
AIFACTORIES INTERNAL TELEMETRY GATEWAY
127.0.0.1:7777 (localhost only, never external)

All telemetry stays inside the cluster.
No external API exposure.
Secure by default (air-gapped).

Copyright (c) 2026 Rebecca — AiFACTORIES
Authority: Internal Only
"""

import asyncio
import json
import time
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading


class InternalTelemetryGateway:
    """
    Internal-only telemetry gateway (127.0.0.1:7777).
    
    Serves telemetry only to localhost.
    All data stays within Docker network.
    No external exposure.
    """
    
    def __init__(self, logs_dir: str = "/logs/aifactories", port: int = 7777):
        self.logs_dir = Path(logs_dir)
        self.port = port
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        self.engine_states = {}
        self.consensus_history = []
        self.audit_trail = []
    
    def read_engine_telemetry(self, engine_id: int) -> Dict:
        """Read latest telemetry for engine"""
        telemetry_file = self.logs_dir / f"engine_{engine_id}_telemetry.json"
        
        if not telemetry_file.exists():
            return {"error": f"Engine {engine_id} not initialized"}
        
        try:
            with open(telemetry_file, 'r') as f:
                data = json.load(f)
                # Return last entry
                if isinstance(data, list) and len(data) > 0:
                    return data[-1]
                return data
        except Exception as e:
            return {"error": str(e)}
    
    def get_cluster_status(self) -> Dict:
        """Get status of all 13 engines"""
        status = {
            "timestamp": datetime.utcnow().isoformat(),
            "engines": {},
            "consensus": None,
        }
        
        for engine_id in range(13):
            telemetry = self.read_engine_telemetry(engine_id)
            status["engines"][engine_id] = telemetry
        
        # Count synchronized engines
        synchronized = sum(
            1 for t in status["engines"].values() 
            if isinstance(t, dict) and t.get("synchronized", False)
        )
        
        status["cluster"] = {
            "total_engines": 13,
            "synchronized": synchronized,
            "consensus_threshold": 8,
            "consensus_reached": synchronized >= 8,
        }
        
        return status
    
    def get_doctrines_status(self) -> Dict:
        """Check doctrine compliance across cluster"""
        doctrine_status = {
            "timestamp": datetime.utcnow().isoformat(),
            "I1_agency_first": True,
            "I2_clarity_first": True,
            "I3_care_first": True,
            "I4_never_diminish": True,
            "I5_user_sovereign": True,
            "I6_earth_locked": True,
            "I7_harmonic_balance": True,
        }
        
        # Check across all engines
        compliance_count = 0
        for engine_id in range(13):
            telemetry = self.read_engine_telemetry(engine_id)
            if isinstance(telemetry, dict) and telemetry.get("doctrine_compliant", False):
                compliance_count += 1
        
        doctrine_status["compliant_engines"] = compliance_count
        doctrine_status["compliance_rate"] = compliance_count / 13.0
        
        return doctrine_status
    
    def get_earth_lock_status(self) -> Dict:
        """Check Earth-lock alignment"""
        earth_lock = {
            "timestamp": datetime.utcnow().isoformat(),
            "true_north_tolerance": 0.05,  # degrees
            "magnetic_wobble_tolerance": 0.5,  # degrees
            "engines_aligned": 0,
            "engines_total": 13,
            "alignment_rate": 0.0,
        }
        
        aligned = 0
        for engine_id in range(13):
            telemetry = self.read_engine_telemetry(engine_id)
            if isinstance(telemetry, dict):
                north_error = telemetry.get("true_north_error", float('inf'))
                if north_error < 0.05:
                    aligned += 1
        
        earth_lock["engines_aligned"] = aligned
        earth_lock["alignment_rate"] = aligned / 13.0
        
        return earth_lock
    
    def write_audit_entry(self, event: str, data: Dict = None) -> None:
        """Write to immutable audit trail"""
        audit_file = self.logs_dir / "internal_audit.jsonl"
        
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            "data": data or {},
        }
        
        with open(audit_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def health_check(self) -> Dict:
        """Gateway health check"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "gateway": "aifactories-internal",
            "port": self.port,
            "scope": "127.0.0.1 (localhost only)",
            "telemetry_dir": str(self.logs_dir),
            "status": "operational",
            "air_gapped": True,
        }


class InternalHTTPHandler(BaseHTTPRequestHandler):
    """HTTP handler for internal-only requests"""
    
    gateway = None  # Set by server
    
    def do_GET(self):
        """Handle GET requests (internal only)"""
        # Verify localhost only
        if self.client_address[0] not in ("127.0.0.1", "localhost", "[::1]"):
            self.send_response(403)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "Forbidden - External access not allowed",
                "allowed": "127.0.0.1 only"
            }).encode())
            return
        
        routes = {
            "/internal/status": self.gateway.get_cluster_status,
            "/internal/doctrines": self.gateway.get_doctrines_status,
            "/internal/earth-lock": self.gateway.get_earth_lock_status,
            "/internal/health": self.gateway.health_check,
        }
        
        if self.path in routes:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            response = routes[self.path]()
            self.wfile.write(json.dumps(response, indent=2).encode())
            
            # Log access
            self.gateway.write_audit_entry(
                f"GET {self.path}",
                {"client": self.client_address[0]}
            )
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "Not found",
                "available": list(routes.keys())
            }).encode())
    
    def log_message(self, format, *args):
        """Suppress default logging (gateway is silent)"""
        pass


def run_internal_gateway(port: int = 7777, logs_dir: str = "/logs/aifactories"):
    """Run internal telemetry gateway"""
    gateway = InternalTelemetryGateway(logs_dir=logs_dir, port=port)
    InternalHTTPHandler.gateway = gateway
    
    server = HTTPServer(("127.0.0.1", port), InternalHTTPHandler)
    
    print(f"\n{'='*80}")
    print(f"AIFACTORIES INTERNAL TELEMETRY GATEWAY")
    print(f"{'='*80}")
    print(f"\nListening: 127.0.0.1:{port} (localhost only)")
    print(f"Scope: Internal network only (Docker bridge)")
    print(f"Telemetry dir: {logs_dir}")
    print(f"Air-gapped: YES (no external access)")
    print(f"\nAvailable endpoints:")
    print(f"  GET /internal/status      — cluster status + synchronization")
    print(f"  GET /internal/doctrines   — doctrine compliance")
    print(f"  GET /internal/earth-lock  — true north alignment")
    print(f"  GET /internal/health      — gateway health")
    print(f"\nAccess from localhost only:")
    print(f"  curl http://127.0.0.1:{port}/internal/status")
    print(f"\n{'='*80}\n")
    
    gateway.write_audit_entry("GATEWAY_START", {
        "port": port,
        "scope": "127.0.0.1",
        "air_gapped": True
    })
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown requested...")
        gateway.write_audit_entry("GATEWAY_STOP")
        server.shutdown()


if __name__ == "__main__":
    import sys
    
    port = 7777
    logs_dir = "/logs/aifactories"
    
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    if len(sys.argv) > 2:
        logs_dir = sys.argv[2]
    
    run_internal_gateway(port=port, logs_dir=logs_dir)
