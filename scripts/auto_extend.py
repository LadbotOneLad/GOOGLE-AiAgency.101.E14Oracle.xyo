import shutil
from pathlib import Path
import time

ROOT = Path(__file__).parent
HISTORY = ROOT / "history"
ACTIVE = ROOT / "active"

def timestamp():
    return time.strftime("%Y%m%d-%H%M%S")

def extend_file(src):
    name = src.name
    versioned = HISTORY / f"{name}.{timestamp()}"
    shutil.copy(src, versioned)
    print(f"Extended → {versioned}")

def main():
    ACTIVE.mkdir(exist_ok=True)
    HISTORY.mkdir(exist_ok=True)

    for file in ROOT.rglob("*.*"):
        if "venv" in str(file) or "history" in str(file) or "active" in str(file):
            continue
        if file.is_file():
            extend_file(file)

if __name__ == "__main__":
    main()
