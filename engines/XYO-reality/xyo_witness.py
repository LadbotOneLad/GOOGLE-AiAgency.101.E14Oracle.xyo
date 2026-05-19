# -*- coding: utf-8 -*-
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
import uuid

XYO_NODE3 = "466e84dfcbfbae8d50ad4276e8f2b5d37e8834a8"

def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    if not path.exists():
        return None
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def xyo_witness(engine: str, source_path: Path, metrics: dict, tags=None):
    tags = tags or []
    packet = {
        "xyo_node": XYO_NODE3,
        "engine": engine,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "source": {
            "type": "media_metadata",
            "path": str(source_path),
            "hash_sha256": file_sha256(source_path)
        },
        "metrics": metrics,
        "context": {
            "pipeline_run_id": str(uuid.uuid4()),
            "tags": tags
        }
    }

    out_dir = Path("output") / "witness"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"witness_{packet['context']['pipeline_run_id']}.json"
    out_file.write_text(json.dumps(packet, indent=2))
    return packet
