"""Reproduce five projects, including both P02 views and the Census support."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def main() -> None:
    root = Path(__file__).resolve().parent
    components = [
        ("P01 observed duties", "01-observed-duty-intensity", "analyze.py"),
        ("P02 partner concentration", "02-trade-concentration", "analyze.py"),
        ("P02 selected product basket", "02-trade-concentration/product-basket", "analyze.py"),
        ("Census flow bridge (support)", "census-common", "reconcile_flows.py"),
        ("P03 documented non-tariff measures", "03-nte-barriers", "analyze.py"),
        ("P04 Mexico input-output", "04-mexico-input-output", "analyze.py"),
        ("P05 growth scenarios", "05-growth-scenarios", "analyze.py"),
    ]
    for label, directory, script in components:
        path = root / "projects" / directory
        print(f"Reproducing {label}", flush=True)
        subprocess.run([sys.executable, str(path / script)], cwd=path, check=True)
    print("Seven components of five projects reproduced successfully; Census common is support.")


if __name__ == "__main__":
    main()
