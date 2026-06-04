# Codex 6.65: XYO Witness Layer + BOM Weather Integration
# © 2026 Rebecca

import os
import json
import time
import requests
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict


@dataclass
class XYOWitness:
    """XYO geolocation witness record"""
    timestamp: float
    latitude: float
    longitude: float
    accuracy_meters: float
    witness_id: str
    signature: str


@dataclass
class BOMWeatherRecord:
    """Bureau of Meteorology (Australia) radar record"""
    timestamp: float
    location: str  # E.g., "Sydney", "Melbourne"
    latitude: float
    longitude: float
    temperature_c: float
    wind_speed_kmh: float
    wind_direction: str
    radar_reflectivity_dbz: float  # Radar dBZ value
    rainfall_mm: float


@dataclass
class GeoWitness:
    """Combined geo-cryptographic witness"""
    phase: float
    coherence: float
    power: float
    xyo_witness: Optional[XYOWitness]
    bom_weather: Optional[BOMWeatherRecord]
    consensus_score: float
    aligned: bool


class XYOWitnessAdapter:
    """XYO Network geolocation witness integration"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("XYO_API_KEY", "demo")
        self.base_url = "https://api.xyo.network/v1"
        self.witness_cache: List[XYOWitness] = []

    def fetch_witness(self, lat: float, lon: float) -> Optional[XYOWitness]:
        """Fetch XYO witness for given coordinates"""
        try:
            # Mock implementation (replace with real XYO API call)
            timestamp = time.time()
            witness = XYOWitness(
                timestamp=timestamp,
                latitude=lat + (hash(str(timestamp)) % 100) / 1000.0,
                longitude=lon + (hash(str(timestamp)) % 100) / 1000.0,
                accuracy_meters=5.0 + (hash(str(timestamp)) % 50),
                witness_id=f"xyo-{int(timestamp)}",
                signature=f"sig-{hash((lat, lon, timestamp))}",
            )
            self.witness_cache.append(witness)
            return witness
        except Exception as e:
            print(f"XYO witness fetch failed: {e}")
            return None

    def get_cached_witnesses(self, limit: int = 10) -> List[XYOWitness]:
        """Return most recent cached witnesses"""
        return self.witness_cache[-limit:]


class BOMWeatherAdapter:
    """Bureau of Meteorology radar + weather integration"""

    def __init__(self, location: str = "Sydney"):
        self.location = location
        self.base_url = "https://api.bom.gov.au/v1"
        self.weather_cache: List[BOMWeatherRecord] = []

    def fetch_weather(self) -> Optional[BOMWeatherRecord]:
        """Fetch BOM weather + radar data"""
        try:
            # Mock implementation (replace with real BOM API)
            timestamp = time.time()
            record = BOMWeatherRecord(
                timestamp=timestamp,
                location=self.location,
                latitude=-33.8688 if self.location == "Sydney" else -37.8136,
                longitude=151.2093 if self.location == "Sydney" else 144.9631,
                temperature_c=20.0 + (hash(str(timestamp)) % 15),
                wind_speed_kmh=10.0 + (hash(str(timestamp)) % 30),
                wind_direction=["N", "NE", "E", "SE", "S", "SW", "W", "NW"][
                    hash(str(timestamp)) % 8
                ],
                radar_reflectivity_dbz=15.0 + (hash(str(timestamp)) % 40),
                rainfall_mm=(hash(str(timestamp)) % 50) / 10.0,
            )
            self.weather_cache.append(record)
            return record
        except Exception as e:
            print(f"BOM weather fetch failed: {e}")
            return None

    def get_cached_weather(self, limit: int = 10) -> List[BOMWeatherRecord]:
        """Return most recent cached weather records"""
        return self.weather_cache[-limit:]


class GeocryphicalWitnessAggregator:
    """Geocryptical: combines three-ring consensus with XYO witness + BOM weather"""

    def __init__(self):
        self.xyo = XYOWitnessAdapter()
        self.bom = BOMWeatherAdapter()
        self.witnesses: List[GeoWitness] = []

    def evaluate_with_witness(
        self,
        phase: float,
        coherence: float,
        power: float,
        latitude: float,
        longitude: float,
        location: str = "Sydney",
    ) -> GeoWitness:
        """Evaluate state with XYO + BOM witness data"""

        # Fetch witness data
        xyo_witness = self.xyo.fetch_witness(latitude, longitude)
        bom_weather = self.bom.fetch_weather()

        # Compute consensus score (0.0-1.0)
        score = coherence * 0.5  # Base coherence weight
        if xyo_witness:
            score += 0.3 * (1.0 - min(xyo_witness.accuracy_meters / 100.0, 1.0))
        if bom_weather:
            # Weather reflectivity as witness confidence (30-70 dBZ is typical rain)
            weather_confidence = 1.0 - abs(bom_weather.radar_reflectivity_dbz - 50.0) / 50.0
            score += 0.2 * max(0, weather_confidence)

        aligned = score > 0.6 and coherence > 0.3

        witness = GeoWitness(
            phase=phase,
            coherence=coherence,
            power=power,
            xyo_witness=xyo_witness,
            bom_weather=bom_weather,
            consensus_score=score,
            aligned=aligned,
        )

        self.witnesses.append(witness)
        return witness

    def export_witness_log(self, filepath: str = "/logs/geocryphical_witnesses.jsonl"):
        """Export all witnesses to JSONL"""
        with open(filepath, "w") as f:
            for witness in self.witnesses:
                record = {
                    "timestamp": time.time(),
                    "phase": witness.phase,
                    "coherence": witness.coherence,
                    "power": witness.power,
                    "consensus_score": witness.consensus_score,
                    "aligned": witness.aligned,
                }
                if witness.xyo_witness:
                    record["xyo"] = asdict(witness.xyo_witness)
                if witness.bom_weather:
                    record["bom"] = asdict(witness.bom_weather)
                f.write(json.dumps(record) + "\n")

    def get_witness_summary(self) -> Dict[str, Any]:
        """Summary statistics"""
        if not self.witnesses:
            return {}

        aligned_count = sum(1 for w in self.witnesses if w.aligned)
        avg_score = sum(w.consensus_score for w in self.witnesses) / len(self.witnesses)

        return {
            "total_witnesses": len(self.witnesses),
            "aligned_count": aligned_count,
            "alignment_rate": aligned_count / len(self.witnesses),
            "avg_consensus_score": avg_score,
            "xyo_witnesses": len([w for w in self.witnesses if w.xyo_witness]),
            "bom_records": len([w for w in self.witnesses if w.bom_weather]),
        }
