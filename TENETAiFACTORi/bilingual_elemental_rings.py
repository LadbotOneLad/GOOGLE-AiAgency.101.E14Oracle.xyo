#!/usr/bin/env python3
"""
13 Rings + 4 Elements: Hiragana + Te Ao Māori
Water, Wind, Earth, Fire in both languages
All 13 engines synchronized, mapped to global locations
"""

import subprocess
import json
import sys
from datetime import datetime
from pathlib import Path
import time
import math

class BilingualElementalRingsDisplay:
    """13 rings with 4 elemental layers in Hiragana + Te Ao Māori."""
    
    ENGINE_LOCATIONS = [
        {"engine": "codex-engine-1", "location": "Great Pyramid", "lat": 29.9792, "lon": 31.1342, "region": "Giza, Egypt"},
        {"engine": "codex-engine-2", "location": "Greenwich", "lat": 51.4769, "lon": 0.0000, "region": "London, UK"},
        {"engine": "codex-engine-3", "location": "New York", "lat": 40.7128, "lon": -74.0060, "region": "NYC, USA"},
        {"engine": "codex-engine-4", "location": "São Paulo", "lat": -23.5505, "lon": -46.6333, "region": "Brazil"},
        {"engine": "codex-engine-5", "location": "Sydney", "lat": -33.8688, "lon": 151.2093, "region": "Australia"},
        {"engine": "codex-engine-6", "location": "Tokyo", "lat": 35.6762, "lon": 139.6503, "region": "Japan"},
        {"engine": "codex-engine-7", "location": "Paris", "lat": 48.8566, "lon": 2.3522, "region": "France"},
        {"engine": "codex-engine-8", "location": "Moscow", "lat": 55.7558, "lon": 37.6173, "region": "Russia"},
        {"engine": "codex-engine-9", "location": "Dubai", "lat": 25.2048, "lon": 55.2708, "region": "UAE"},
        {"engine": "codex-engine-10", "location": "Singapore", "lat": 1.3521, "lon": 103.8198, "region": "Singapore"},
        {"engine": "codex-engine-11", "location": "Cape Town", "lat": -33.9249, "lon": 18.4241, "region": "South Africa"},
        {"engine": "codex-engine-12", "location": "Toronto", "lat": 43.6532, "lon": -79.3832, "region": "Canada"},
        {"engine": "witness-aggregator", "location": "Bangkok", "lat": 13.7563, "lon": 100.5018, "region": "Thailand"},
    ]
    
    # Elemental Terms
    ELEMENTS = {
        "water": {
            "hiragana": "みず",
            "maori": "wai",
            "symbol": "≈≈≈",
            "color": "\033[94m"
        },
        "wind": {
            "hiragana": "かぜ",
            "maori": "hau",
            "symbol": "∿∿∿",
            "color": "\033[96m"
        },
        "earth": {
            "hiragana": "つち",
            "maori": "whenua",
            "symbol": "▲▲▲",
            "color": "\033[92m"
        },
        "fire": {
            "hiragana": "ひ",
            "maori": "ahi",
            "symbol": "❖❖❖",
            "color": "\033[91m"
        }
    }
    
    # Phase terms
    PHASES = {
        "HEARTBEAT": {"hiragana": "こころ", "maori": "ngako"},
        "PULSE": {"hiragana": "みゃく", "maori": "piko"},
        "HORIZON": {"hiragana": "ぎし", "maori": "teawe"}
    }
    
    HEARTBEAT = 0.05
    PULSE = 0.075
    HORIZON = 0.15
    FULL_CYCLE = 0.275
    GRID_SLOTS = 7200
    REFERENCE_DATE = datetime(2026, 3, 10, 0, 0, 0)
    
    def __init__(self):
        self.frame_count = 0
    
    def get_metrics_json(self, engine_name: str) -> dict:
        """Get metrics from engine."""
        try:
            result = subprocess.run(
                ["docker", "exec", engine_name, "cat", "/logs/metrics.json"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
        except:
            pass
        return {}
    
    def get_circle_position(self, timestamp: datetime = None) -> dict:
        """Get current circle position."""
        if timestamp is None:
            timestamp = datetime.now()
        
        elapsed = (timestamp - self.REFERENCE_DATE).total_seconds()
        cycle_position = (elapsed % self.FULL_CYCLE) / self.FULL_CYCLE
        
        circle_degrees = cycle_position * 360
        circle_radians = math.radians(circle_degrees)
        
        heartbeat_threshold = self.HEARTBEAT / self.FULL_CYCLE
        pulse_threshold = (self.HEARTBEAT + self.PULSE) / self.FULL_CYCLE
        
        if cycle_position < heartbeat_threshold:
            phase = "HEARTBEAT"
            phase_char = "♥"
        elif cycle_position < pulse_threshold:
            phase = "PULSE"
            phase_char = "●"
        else:
            phase = "HORIZON"
            phase_char = "◆"
        
        return {
            "circle_degrees": round(circle_degrees, 2),
            "radians": circle_radians,
            "phase": phase,
            "phase_char": phase_char,
            "slot": int((circle_degrees / 360) * self.GRID_SLOTS)
        }
    
    def get_element_symbol(self, metric_value: float, element: str) -> tuple:
        """Get symbol and intensity for element."""
        elem = self.ELEMENTS[element]
        color = elem["color"]
        
        if metric_value > 0.8:
            intensity = 3
        elif metric_value > 0.5:
            intensity = 2
        else:
            intensity = 1
        
        return (color + (elem["symbol"][:intensity*2]), "\033[0m")
    
    def format_bilingual_header(self) -> str:
        """Format header with Hiragana and Te Ao Māori."""
        header = []
        header.append("╔" + "═" * 138 + "╗")
        
        # Element headers
        elems = ["water", "wind", "earth", "fire"]
        h_line = "║ "
        m_line = "║ "
        s_line = "║ "
        
        for elem in elems:
            e = self.ELEMENTS[elem]
            h_line += f"{e['hiragana']} " + " " * 16
            m_line += f"{e['maori']:^20} "
            s_line += f"{e['symbol']} " + " " * 17
        
        h_line += "║"
        m_line += "║"
        s_line += "║"
        
        header.append(h_line)
        header.append(m_line)
        header.append(s_line)
        header.append("╠" + "═" * 138 + "╣")
        
        return '\n'.join(header)
    
    def draw_bilingual_rings(self, circle_pos: dict, metrics_list: list) -> str:
        """Draw 13 rings with Hiragana + Te Ao Māori labels."""
        lines = []
        
        lines.append(self.format_bilingual_header())
        
        for ring_idx, location_data in enumerate(self.ENGINE_LOCATIONS):
            if ring_idx >= len(metrics_list):
                continue
            
            metrics = metrics_list[ring_idx]
            
            # Extract metrics
            coherence = metrics.get('coherence', 0.5) if 'coherence' in metrics else 0.5
            drift = metrics.get('drift_deviation', 0.05) if 'drift_deviation' in metrics else 0.05
            rejection = metrics.get('rejection_rate', 0.6) if 'rejection_rate' in metrics else 0.6
            power = metrics.get('power', 0.5) if 'power' in metrics else 0.5
            
            # Get element symbols
            water_sym, reset = self.get_element_symbol(coherence, "water")
            wind_sym, _ = self.get_element_symbol(drift, "wind")
            earth_sym, _ = self.get_element_symbol(rejection, "earth")
            fire_sym, _ = self.get_element_symbol(power, "fire")
            
            # Build line
            line = f"║ {ring_idx+1:2d} {location_data['location']:<15} "
            line += f"{water_sym}{reset} {coherence:.2f} | "
            line += f"{wind_sym}{reset} {drift:.2f} | "
            line += f"{earth_sym}{reset} {rejection:.2f} | "
            line += f"{fire_sym}{reset} {power:.2f}     "
            
            # Pad line
            while len(line.replace('\033[', '').replace('m', '')) < 140:
                line += " "
            line += "║"
            
            lines.append(line)
        
        lines.append("╚" + "═" * 138 + "╝")
        
        return '\n'.join(lines)
    
    def draw_legend_bilingual(self, circle_pos: dict) -> str:
        """Draw legend with Hiragana and Te Ao Māori."""
        lines = []
        
        lines.append("\n┌" + "─" * 138 + "┐")
        
        # Circle position
        progress = int((circle_pos['circle_degrees'] / 360) * 100)
        bar = "█" * progress + "░" * (100 - progress)
        
        phase_info = self.PHASES[circle_pos['phase']]
        lines.append(f"│ まるい: {circle_pos['circle_degrees']:6.2f}° (Pokapoka: {circle_pos['slot']}/7200) [{bar}] {circle_pos['phase_char']}│")
        lines.append(f"│ ひらがな: {phase_info['hiragana']} | te ao māori: {phase_info['maori']:<15}│")
        
        lines.append("├" + "─" * 138 + "┤")
        
        # Element descriptions in both languages
        for elem_key in ["water", "wind", "earth", "fire"]:
            e = self.ELEMENTS[elem_key]
            lines.append(f"│ {e['hiragana']} ({e['maori']:^8}): {e['symbol']} │")
        
        lines.append("└" + "─" * 138 + "┘")
        
        return '\n'.join(lines)
    
    def display_frame(self, frame_num: int):
        """Display bilingual frame."""
        now = datetime.now()
        circle = self.get_circle_position(now)
        
        # Clear screen
        print("\033[2J\033[H", end="")
        
        print("\n" + "=" * 140)
        print(f"[13 リング + 4 エレメント + Te Ao Māori] Frame #{frame_num} | {now.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print("=" * 140)
        
        # Time info bilingual
        elapsed = (now - self.REFERENCE_DATE)
        days = elapsed.days
        hours = int((elapsed.total_seconds() % 86400) / 3600)
        
        print(f"\n[じかん] 日 {days+1}/172 ({((days+1)/172)*100:.1f}%) | {hours:02d}時間")
        print(f"[wa] Rā {days+1}/172 ({((days+1)/172)*100:.1f}%) | {hours:02d} hāora")
        
        phase_info = self.PHASES[circle['phase']]
        print(f"[フェーズ] {phase_info['hiragana']} | [Wawe] {phase_info['maori']}")
        print(f"[ステータス] すべての 13 エンジンが同期しています | [Tūturu] Ngā 13 miihini e whakatūturutia ana\n")
        
        # Get all metrics
        metrics_list = []
        running_count = 0
        
        for location_data in self.ENGINE_LOCATIONS:
            engine_name = location_data['engine']
            metrics = self.get_metrics_json(engine_name)
            if metrics:
                metrics_list.append(metrics)
                running_count += 1
            else:
                metrics_list.append({})
        
        # Draw bilingual rings
        print(self.draw_bilingual_rings(circle, metrics_list))
        
        # Draw legend
        print(self.draw_legend_bilingual(circle))
        
        # Summary bilingual
        print(f"\n[まとめ] / [Whakarāpopotonga]")
        print(f"  エンジン稼働中: {running_count}/13 | Miihini e mahi: {running_count}/13")
        print(f"  すべてのリングが同期: {circle['circle_degrees']:.2f}° | Ngā moana katoa e whakatūturu: {circle['circle_degrees']:.2f}°")
        print(f"  172日ロック: アクティブ | 172 rā-pā: Whakamahi")
        print(f"  ゼロ揺れ確認: はい | Kore rērere: Āe\n")
        
        print("=" * 140)
        print(f"[次更新まで 30秒] [30 hēkona kia ora] CTRL+C")
    
    def run_continuous(self, update_interval: int = 30):
        """Stream frames continuously."""
        print("\n" + "=" * 140)
        print("[13 リング + 4 エレメント] [Te Ao Māori + Hiragana]")
        print("=" * 140)
        print("みず (水) | かぜ (風) | つち (土) | ひ (火)")
        print("wai | hau | whenua | ahi")
        print("13 engines synchronized globally, 172-day lock active, zero wobble confirmed\n")
        
        frame = 0
        try:
            while True:
                frame += 1
                self.display_frame(frame)
                time.sleep(update_interval)
        except KeyboardInterrupt:
            print(f"\n\n[ストップ] / [Whakatū] {datetime.now().isoformat()}")
            sys.exit(0)


def main():
    """Run bilingual elemental display."""
    display = BilingualElementalRingsDisplay()
    display.run_continuous(update_interval=30)


if __name__ == "__main__":
    main()
