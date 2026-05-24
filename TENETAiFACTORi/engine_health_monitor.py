#!/usr/bin/env python3
"""
Engine Health Monitor: Real-time status across all containers
Tracks heartbeat, pulse, horizon phases + resource utilization + operational events
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class EngineHealthMonitor:
    """Monitor all running engines and their health."""
    
    # Known engines from docker-compose
    ENGINES = [
        "codex-engine-1", "codex-engine-2", "codex-engine-3", "codex-engine-4",
        "codex-engine-5", "codex-engine-6", "codex-engine-7", "codex-engine-8",
        "codex-engine-9", "codex-engine-10", "codex-engine-11", "codex-engine-12",
        "witness-aggregator", "engine-stress-test", "engine"
    ]
    
    # Three Rhythms phases
    HEARTBEAT = 0.05
    PULSE = 0.075
    HORIZON = 0.15
    
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.engines_status = {}
    
    def get_docker_stats(self) -> Dict[str, Any]:
        """Get live docker stats for all engines."""
        try:
            result = subprocess.run(
                ["docker", "stats", "--no-stream", "--format", "json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                stats_output = result.stdout
                # Parse JSON output
                try:
                    # Docker stats outputs newline-delimited JSON
                    stats_list = []
                    for line in stats_output.strip().split('\n'):
                        if line:
                            stats_list.append(json.loads(line))
                    return {container['Container']: container for container in stats_list}
                except json.JSONDecodeError:
                    return {}
        except Exception as e:
            print(f"[ERROR] Docker stats failed: {e}")
        
        return {}
    
    def get_docker_ps(self) -> Dict[str, Any]:
        """Get container status from docker ps."""
        try:
            result = subprocess.run(
                ["docker", "ps", "-a", "--format", "json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                containers = {}
                for line in result.stdout.strip().split('\n'):
                    if line:
                        container = json.loads(line)
                        name = container.get('Names', '')
                        containers[name] = {
                            'id': container.get('ID', '')[:12],
                            'image': container.get('Image', ''),
                            'status': container.get('Status', ''),
                            'state': container.get('State', ''),
                            'created': container.get('CreatedAt', '')
                        }
                return containers
        except Exception as e:
            print(f"[ERROR] Docker ps failed: {e}")
        
        return {}
    
    def get_container_logs(self, container_name: str, lines: int = 5) -> List[str]:
        """Get recent logs from container."""
        try:
            result = subprocess.run(
                ["docker", "logs", "--tail", str(lines), container_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return result.stdout.strip().split('\n')
        except Exception:
            pass
        
        return []
    
    def determine_three_rhythm_phase(self) -> str:
        """Determine which rhythm phase we're in."""
        now = datetime.now()
        millis_in_day = (now.hour * 3600 + now.minute * 60 + now.second) * 1000 + now.microsecond // 1000
        
        heartbeat_ms = self.HEARTBEAT * 1000  # 50ms
        pulse_ms = self.PULSE * 1000           # 75ms
        horizon_ms = self.HORIZON * 1000       # 150ms
        
        total_cycle = heartbeat_ms + pulse_ms + horizon_ms  # 275ms
        position = millis_in_day % total_cycle
        
        if position < heartbeat_ms:
            return f"HEARTBEAT (t={self.HEARTBEAT})"
        elif position < (heartbeat_ms + pulse_ms):
            return f"PULSE (t={self.PULSE})"
        else:
            return f"HORIZON (t={self.HORIZON})"
    
    def assess_engine_health(self, container_name: str, ps_data: Dict, stats_data: Dict) -> Dict[str, Any]:
        """Assess health of single engine."""
        ps_info = ps_data.get(container_name, {})
        stats_info = stats_data.get(container_name, {})
        
        state = ps_info.get('state', 'unknown').upper()
        status = ps_info.get('status', 'unknown')
        
        # Parse CPU and memory from status string if available
        cpu_percent = "N/A"
        memory_mb = "N/A"
        
        if stats_info:
            try:
                cpu_str = stats_info.get('CPUPerc', '0%').replace('%', '')
                cpu_percent = float(cpu_str) if cpu_str else 0.0
            except:
                cpu_percent = "N/A"
            
            try:
                mem_str = stats_info.get('MemUsage', '0MiB').split('/')[0].replace('MiB', '').strip()
                memory_mb = float(mem_str) if mem_str else 0.0
            except:
                memory_mb = "N/A"
        
        # Determine health status
        if state == "RUNNING":
            if isinstance(cpu_percent, float) and isinstance(memory_mb, float):
                if cpu_percent > 90 or memory_mb > 400:
                    health = "CRITICAL"
                elif cpu_percent > 70 or memory_mb > 300:
                    health = "WARNING"
                else:
                    health = "HEALTHY"
            else:
                health = "RUNNING"
        elif state == "EXITED":
            health = "STOPPED"
        else:
            health = "UNKNOWN"
        
        # Get recent logs
        recent_logs = self.get_container_logs(container_name, 3)
        
        return {
            "name": container_name,
            "container_id": ps_info.get('id', 'N/A'),
            "state": state,
            "status_string": status,
            "health": health,
            "cpu_percent": cpu_percent,
            "memory_mb": memory_mb,
            "recent_logs": recent_logs
        }
    
    def monitor_all_engines(self):
        """Monitor all engines and display health dashboard."""
        print("\n" + "=" * 130)
        print(f"[ENGINE HEALTH MONITOR] {self.timestamp}")
        print(f"[CURRENT PHASE] {self.determine_three_rhythm_phase()}")
        print("=" * 130)
        
        # Get data from Docker
        ps_data = self.get_docker_ps()
        stats_data = self.get_docker_stats()
        
        print(f"\n[CONTAINER STATUS OVERVIEW]")
        print("-" * 130)
        print(f"{'Container Name':<30} {'State':<12} {'Health':<12} {'CPU %':<10} {'Memory MB':<12} {'Status':<30}")
        print("-" * 130)
        
        health_summary = {
            "HEALTHY": 0,
            "WARNING": 0,
            "CRITICAL": 0,
            "RUNNING": 0,
            "STOPPED": 0,
            "UNKNOWN": 0
        }
        
        running_count = 0
        total_cpu = 0.0
        total_memory = 0.0
        
        # Check each engine
        for engine_name in self.ENGINES:
            health = self.assess_engine_health(engine_name, ps_data, stats_data)
            
            cpu_display = f"{health['cpu_percent']:.1f}%" if isinstance(health['cpu_percent'], float) else health['cpu_percent']
            mem_display = f"{health['memory_mb']:.1f}" if isinstance(health['memory_mb'], float) else health['memory_mb']
            
            print(f"{health['name']:<30} {health['state']:<12} {health['health']:<12} {cpu_display:<10} {mem_display:<12} {health['status_string']:<30}")
            
            # Track summary
            health_summary[health['health']] += 1
            if health['state'] == 'RUNNING':
                running_count += 1
                if isinstance(health['cpu_percent'], float):
                    total_cpu += health['cpu_percent']
                if isinstance(health['memory_mb'], float):
                    total_memory += health['memory_mb']
        
        print("-" * 130)
        print(f"\n[SUMMARY]")
        print(f"Containers Running: {running_count}")
        print(f"Healthy: {health_summary['HEALTHY']} | Warning: {health_summary['WARNING']} | Critical: {health_summary['CRITICAL']} | Stopped: {health_summary['STOPPED']}")
        print(f"Total CPU: {total_cpu:.1f}% | Total Memory: {total_memory:.1f} MB")
        
        # Detailed view for running engines
        print(f"\n[DETAILED LOGS - RUNNING ENGINES]")
        print("-" * 130)
        
        for engine_name in self.ENGINES:
            health = self.assess_engine_health(engine_name, ps_data, stats_data)
            if health['state'] == 'RUNNING':
                print(f"\n[{engine_name}] {health['health']}")
                if health['recent_logs']:
                    for log_line in health['recent_logs']:
                        if log_line.strip():
                            print(f"  {log_line[:120]}")
                else:
                    print(f"  (No recent logs)")
        
        print("=" * 130)
    
    def save_health_report(self, output_file: str = "engine_health_report.json"):
        """Save health report to file."""
        ps_data = self.get_docker_ps()
        stats_data = self.get_docker_stats()
        
        report = {
            "timestamp": self.timestamp,
            "phase": self.determine_three_rhythm_phase(),
            "engines": {}
        }
        
        for engine_name in self.ENGINES:
            health = self.assess_engine_health(engine_name, ps_data, stats_data)
            report["engines"][engine_name] = health
        
        log_path = Path("./logs") / output_file
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n[SAVED] Health report: {log_path}")


def main():
    """Execute engine health monitoring."""
    monitor = EngineHealthMonitor()
    monitor.monitor_all_engines()
    monitor.save_health_report()


if __name__ == "__main__":
    main()
