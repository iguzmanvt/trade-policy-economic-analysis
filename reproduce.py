"""Reproduce the five bounded portfolio projects from their included inputs."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def main() -> None:
    root = Path(__file__).resolve().parent
    projects = [
        "01-observed-duty-intensity",
        "02-trade-concentration",
        "03-nte-barriers",
        "04-mexico-input-output",
        "05-growth-scenarios",
    ]
    for name in projects:
        path = root / "projects" / name
        print(f"Reproducing {name}", flush=True)
        subprocess.run([sys.executable, str(path / "analyze.py")], cwd=path, check=True)
    print("All five projects reproduced successfully.")


if __name__ == "__main__":
    main()
