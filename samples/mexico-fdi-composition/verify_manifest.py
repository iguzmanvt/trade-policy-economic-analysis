#!/usr/bin/env python3
"""Check the exact standalone sample inventory and recorded file hashes."""
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "MANIFEST_SHA256.csv"


def main():
    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    paths = [r["path"] for r in rows]
    if len(paths) != len(set(paths)):
        raise ValueError("Duplicate manifest paths")
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file() and p != MANIFEST}
    if set(paths) != actual:
        raise ValueError(f"File inventory mismatch; missing={set(paths)-actual}; added={actual-set(paths)}")
    for row in rows:
        target = (ROOT / row["path"]).resolve()
        if ROOT not in target.parents:
            raise ValueError("Manifest path outside sample")
        raw = target.read_bytes()
        if len(raw) != int(row["bytes"]) or hashlib.sha256(raw).hexdigest() != row["sha256"]:
            raise ValueError(f"File hash/size mismatch: {row['path']}")
    print(f"PASS: {len(rows)} files match the sample manifest.")


if __name__ == "__main__":
    main()
