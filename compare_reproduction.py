"""Compare two reproduction trees without relaxing source or artifact identity.

Usage: python compare_reproduction.py BEFORE AFTER

Only P05 results/paths.csv permits numeric differences, in its seven derived
columns, with absolute tolerance 1e-12 and no relative tolerance. The bound is
above the observed Windows difference (2.842170943040401e-14), below the model's
1e-11 accounting bound, and below the precision communicated in its notes.
This is a bounded reproduction criterion, not validation of model accuracy or
a guarantee for every platform. Never regenerate the reference to hide a drift.

All other file bytes, the file set, P05 CRLF serialization, header, ordered
204 scenario/year keys and parameter cells must match. Only the root .git
entry is excluded; keep environments, caches and logs outside both trees.
"""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal, DecimalException, Inexact, localcontext
import io
import json
import os
from pathlib import Path
import re
import sys

GROWTH_PATH = "projects/05-growth-scenarios/results/paths.csv"
ABS_TOL = Decimal("1e-12")
FIELDS = (
    "scenario", "year", "capital_per_effective_worker",
    "output_per_worker_index", "consumption_per_worker_index",
    "investment_per_worker_index", "instantaneous_output_growth_pct",
    "investment_share", "efficiency_growth", "output_gap_pct",
    "consumption_gap_pct",
)
DERIVED_FIELDS = (
    "capital_per_effective_worker", "output_per_worker_index",
    "consumption_per_worker_index", "investment_per_worker_index",
    "instantaneous_output_growth_pct", "output_gap_pct", "consumption_gap_pct",
)
DERIVED_INDEXES = tuple(FIELDS.index(name) for name in DERIVED_FIELDS)
EXACT_INDEXES = tuple(i for i in range(len(FIELDS)) if i not in DERIVED_INDEXES)
EXPECTED_KEYS = tuple(
    (scenario, str(year))
    for scenario in ("baseline", "investment", "productivity", "combined")
    for year in range(51)
)
NUMBER = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")


class ComparisonError(ValueError):
    """A reproduction changed something outside the accepted equivalence."""


def file_map(root: Path) -> dict[str, Path]:
    if not root.is_dir():
        raise ComparisonError(f"Not a directory: {root}")

    def traversal_error(error: OSError) -> None:
        raise ComparisonError(f"Cannot inspect every file in {root}: {error}") from error

    result = {}
    for current, directories, files in os.walk(root, followlinks=False, onerror=traversal_error):
        current = Path(current)
        if current == root:
            directories[:] = [name for name in directories if name != ".git"]
            files = [name for name in files if name != ".git"]
        for name in directories:
            if (current / name).is_symlink():
                raise ComparisonError(f"Symlinks are not supported: {current / name}")
        for name in files:
            path = current / name
            if path.is_symlink() or not path.is_file():
                raise ComparisonError(f"Not a regular file: {path}")
            result[path.relative_to(root).as_posix()] = path
    return result


def growth_rows(data: bytes, label: str) -> list[list[str]]:
    try:
        text = data.decode("utf-8")
        rows = list(csv.reader(io.StringIO(text, newline=""), strict=True))
    except (UnicodeError, csv.Error) as exc:
        raise ComparisonError(f"{label}: malformed UTF-8 CSV: {exc}") from exc
    if not rows or tuple(rows[0]) != FIELDS:
        raise ComparisonError(f"{label}: P05 header changed")
    body = rows[1:]
    if any(len(row) != len(FIELDS) for row in body):
        raise ComparisonError(f"{label}: P05 row has missing or extra cells")
    if tuple((row[0], row[1]) for row in body) != EXPECTED_KEYS:
        raise ComparisonError(f"{label}: P05 ordered 204 scenario/year keys changed")
    # Require the existing writer's exact CRLF, quoting and final newline.
    # Parsing alone would silently accept LF, extra quoting and blank records.
    canonical = io.StringIO(newline="")
    csv.writer(canonical, lineterminator="\r\n").writerows(rows)
    if canonical.getvalue().encode("utf-8") != data:
        raise ComparisonError(f"{label}: P05 CSV serialization changed (expected canonical CRLF)")
    return body


def derived_number(value: str, label: str) -> Decimal:
    if not NUMBER.fullmatch(value):
        raise ComparisonError(f"{label}: invalid or non-finite numeric value {value!r}")
    try:
        number = Decimal(value)
    except DecimalException as exc:
        raise ComparisonError(f"{label}: invalid numeric value {value!r}") from exc
    if not number.is_finite():
        raise ComparisonError(f"{label}: non-finite numeric value {value!r}")
    return number


def compare_growth(reference: bytes, actual: bytes) -> dict:
    before = growth_rows(reference, "reference")
    after = growth_rows(actual, "actual")
    changed_cells = 0
    max_difference = Decimal(0)
    for row_index, (left, right) in enumerate(zip(before, after), start=2):
        for index in EXACT_INDEXES:
            if left[index] != right[index]:
                raise ComparisonError(
                    f"{GROWTH_PATH}:{row_index}: exact field {FIELDS[index]} changed"
                )
        for index in DERIVED_INDEXES:
            label = f"{GROWTH_PATH}:{row_index}:{FIELDS[index]}"
            a = derived_number(left[index], f"reference {label}")
            b = derived_number(right[index], f"actual {label}")
            try:
                with localcontext() as context:
                    # Align the two decimal coefficients and reserve a carry
                    # digit. A fixed precision could round an above-boundary
                    # difference down to exactly the permitted tolerance.
                    at, bt = a.as_tuple(), b.as_tuple()
                    exponent = min(at.exponent, bt.exponent)
                    context.prec = max(
                        len(at.digits) + at.exponent - exponent,
                        len(bt.digits) + bt.exponent - exponent,
                    ) + 1
                    context.traps[Inexact] = True
                    difference = abs(a - b)
            except DecimalException as exc:
                raise ComparisonError(f"{label}: numeric difference cannot be compared") from exc
            if difference > ABS_TOL:
                raise ComparisonError(
                    f"{label}: absolute difference {difference} exceeds {ABS_TOL}"
                )
            max_difference = max(max_difference, difference)
            changed_cells += left[index] != right[index]
    return {
        "rows": len(before),
        "changed_derived_cells": changed_cells,
        "maximum_absolute_difference": str(max_difference),
        "absolute_tolerance": str(ABS_TOL),
        "relative_tolerance": "0",
    }


def compare_trees(reference: Path, actual: Path) -> dict:
    reference, actual = reference.resolve(), actual.resolve()
    before, after = file_map(reference), file_map(actual)
    missing, extra = sorted(before.keys() - after.keys()), sorted(after.keys() - before.keys())
    if missing or extra:
        raise ComparisonError(f"File set changed: missing={missing}, extra={extra}")
    if GROWTH_PATH not in before:
        raise ComparisonError(f"Required P05 output is missing: {GROWTH_PATH}")
    identical = 0
    growth = None
    for name in sorted(before):
        left, right = before[name].read_bytes(), after[name].read_bytes()
        if name == GROWTH_PATH:
            # Check structure and finiteness even for byte-identical inputs.
            growth = compare_growth(left, right)
        elif left != right:
            raise ComparisonError(f"Bytes changed outside the P05 numeric exception: {name}")
        identical += left == right
    return {
        "status": "passed",
        "file_count": len(before),
        "byte_identical_files": identical,
        "numeric_exception_path": GROWTH_PATH,
        "growth": growth,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path, help="Tree captured before reproduction")
    parser.add_argument("actual", type=Path, help="Tree after reproduction")
    args = parser.parse_args()
    try:
        result = compare_trees(args.reference, args.actual)
    except (ComparisonError, OSError) as exc:
        print(f"Reproduction comparison failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
