#!/usr/bin/env python3
"""Independently audit generated CSV arithmetic using exact rational numbers."""
import argparse
import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMPONENTS = ("Nuevas inversiones", "Reinversión de utilidades", "Cuentas entre compañías")
ROLES = ("TOTAL",) + COMPONENTS
TOLERANCE = Fraction(1, 2 * 10**12)  # only for the 12-decimal percentage output


def read(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def audit(results):
    metadata = json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))
    for filename, digest in metadata["input_sha256"].items():
        require(hashlib.sha256((ROOT / "data" / filename).read_bytes()).hexdigest() == digest, "Input hash mismatch")
    annual = read(ROOT / "data/annual_2006_2025.csv")
    partial = read(ROOT / "data/snapshot_2026s1.csv")
    lookup = {(r["segmento"], r["anio"], r["tipo_inversion"]): r for r in annual + partial}
    checked = 0
    for filename, segment, years in (("annual_shares.csv", "anual_actualizada", range(2006, 2026)), ("snapshot_2026s1.csv", "semestre_2026_original", [2026])):
        rows = read(results / filename)
        expected = {(str(y), c) for y in years for c in COMPONENTS}
        keys = [(r["year"], r["component"]) for r in rows]
        require(len(keys) == len(set(keys)) and set(keys) == expected, "Wrong share coverage")
        for row in rows:
            src = lookup[segment, row["year"], row["component"]]
            total = lookup[segment, row["year"], "TOTAL"]
            require(row["segment"] == segment and row["source_period"] == src["periodo_origen"], "Temporal segment changed")
            require(row["amount_usdm"] == src["ied_mdd"] and row["published_total_usdm"] == total["ied_mdd"], "Source amount changed")
            for a, b in (("source_file", "archivo_fuente"), ("source_sheet", "hoja"), ("component_cell", "celda")):
                require(row[a] == src[b], "Source locator changed")
            require(row["total_cell"] == total["celda"], "Denominator locator changed")
            exact = 100 * Fraction(src["ied_mdd"]) / Fraction(total["ied_mdd"])
            require(abs(Fraction(row["share_pct"]) - exact) <= TOLERANCE, "Incorrect share")
            checked += 1
    rows = read(results / "annual_changes.csv")
    keys = [(int(r["current_year"]), r["component"]) for r in rows]
    require(len(keys) == len(set(keys)) and set(keys) == {(y, c) for y in range(2007, 2026) for c in ROLES}, "Wrong annual-change coverage")
    for row in rows:
        y = int(row["current_year"])
        c = row["component"]
        require(int(row["base_year"]) == y - 1, "Nonconsecutive annual comparison")
        base = lookup["anual_actualizada", str(y - 1), c]["ied_mdd"]
        actual = lookup["anual_actualizada", str(y), c]["ied_mdd"]
        change = Fraction(actual) - Fraction(base)
        require(row["base_usdm"] == base and row["current_usdm"] == actual, "Amount in annual change changed")
        require(Fraction(row["change_usdm"]) == change, "Incorrect change")
        require(abs(Fraction(row["component_growth_pct"]) - 100 * change / Fraction(base)) <= TOLERANCE, "Incorrect growth rate")
        if c == "TOTAL":
            require(row["contribution_total_growth_pp"] == "" and row["contribution_status"] == "not_applicable_total", "Total double counted")
        else:
            total_base = Fraction(lookup["anual_actualizada", str(y - 1), "TOTAL"]["ied_mdd"])
            require(abs(Fraction(row["contribution_total_growth_pp"]) - 100 * change / total_base) <= TOLERANCE, "Incorrect growth contribution")
            require(row["contribution_status"] == "calculated", "Wrong contribution status")
        checked += 1
    rows = read(results / "reconciliation.csv")
    keys = [(r["segment"], r["year"]) for r in rows]
    expected = {("anual_actualizada", str(y)) for y in range(2006, 2026)} | {("semestre_2026_original", "2026")}
    require(len(keys) == len(set(keys)) and set(keys) == expected, "Wrong reconciliation coverage")
    max_residual = Fraction(0)
    for row in rows:
        s, y = row["segment"], row["year"]
        total = Fraction(lookup[s, y, "TOTAL"]["ied_mdd"])
        component_sum = sum(Fraction(lookup[s, y, c]["ied_mdd"]) for c in COMPONENTS)
        residual = total - component_sum
        require(Fraction(row["published_total_usdm"]) == total and Fraction(row["component_sum_usdm"]) == component_sum, "Incorrect reconciliation terms")
        require(Fraction(row["residual_usdm"]) == residual, "Residual altered or allocated")
        require(row["status"] == ("exact" if residual == 0 else "residual_preserved"), "Wrong exact-identity status")
        max_residual = max(max_residual, abs(residual))
        checked += 1
    return {"status": "PASS", "independently_checked_output_rows": checked, "method": "Fraction, independent of analyze.py", "percentage_tolerance": "0.0000000000005 (12-decimal display only)", "exact_amount_checks": True, "max_abs_residual_fraction_usdm": str(max_residual), "no_new_source_retrieval": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(audit(args.results), indent=2))


if __name__ == "__main__":
    main()
