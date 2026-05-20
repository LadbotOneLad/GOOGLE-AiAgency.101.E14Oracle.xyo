import os
import shutil
from pathlib import Path

ROOT = Path(__file__).parent

RULES = {
    "engine": ["engine", "truth", "market", "xyo", "neo"],
    "runner": ["run_", "runner"],
    "api": ["api", "endpoint"],
    "manifest": ["manifest", ".json"],
    "data": ["data", "packet", "output"],
}

TARGETS = {
    "engine": ROOT / "engines",
    "runner": ROOT / "runners",
    "api": ROOT / "api",
    "manifest": ROOT / "manifests",
    "data": ROOT / "data",
}

def classify(name):
    lower = name.lower()
    for key, patterns in RULES.items():
        if any(p in lower for p in patterns):
            return key
    return None

def main():
    for file in ROOT.rglob("*.*"):
        if file.is_file() and "venv" not in str(file):
            category = classify(file.name)
            if category:
                target = TARGETS[category] / file.name
                if file != target:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(file), str(target))
                    print(f"Moved {file.name} → {target}")

if __name__ == "__main__":
    main()
