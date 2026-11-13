#!/usr/bin/env python3
"""Reproduce the bounded national FDI sample. No network or external packages."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from decimal import Decimal, ROUND_HALF_UP, localcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMPONENTS = ("Nuevas inversiones", "Reinversión de utilidades", "Cuentas entre compañías")
ROLES = ("TOTAL",) + COMPONENTS
FILES = ("annual_2006_2025.csv", "snapshot_2026s1.csv")
EXPECTED_HASHES = {
    FILES[0]: "9f186a5811e461c80338434097eef92977c23ffd86421528afc7e7fbf57af9a0",
    FILES[1]: "aaac961e34b9a5b50d3d1bf501558c6402e579bb3d1f72e5214f0228fe79ab32",
}
FIELDS = "segmento anio periodo_origen entidad_origen tipo_inversion ied_mdd estado archivo_fuente hoja celda etiqueta_fila formula_fuente".split()


def text(value: Decimal) -> str:
    return format(value, "f")


def ratio(numerator: Decimal, denominator: Decimal) -> str:
    if denominator <= 0:
        raise ValueError("This fixed sample requires a positive published denominator")
    return text((100 * numerator / denominator).quantize(Decimal("0.000000000001"), rounding=ROUND_HALF_UP))


def excel_column(index: int) -> str:
    value = ""
    while index:
        index, rem = divmod(index - 1, 26)
        value = chr(65 + rem) + value
    return value


def validate_rows(rows: list[dict[str, str]], annual: bool) -> None:
    expected_years = range(2006, 2026) if annual else [2026]
    expected_keys = {(str(y), role) for y in expected_years for role in ROLES}
    keys = [(r["anio"], r["tipo_inversion"]) for r in rows]
    if len(keys) != len(set(keys)) or set(keys) != expected_keys:
        raise ValueError("Missing, additional or duplicate year-component keys")
    segment = "anual_actualizada" if annual else "semestre_2026_original"
    source = "tipo_actualizado.xlsx" if annual else "tipo_original.xlsx"
    for row in rows:
        year = int(row["anio"])
        role = row["tipo_inversion"]
        col = excel_column(5 + 4 * (year - 2006)) if annual else "AI"
        expected_cell = col + str(5 + ROLES.index(role))
        checks = {
            "segmento": segment,
            "periodo_origen": f"{year}-4" if annual else "2026-2",
            "entidad_origen": "Total general",
            "estado": "publicado",
            "archivo_fuente": source,
            "hoja": "Por Tipo de Inversión",
            "celda": expected_cell,
            "etiqueta_fila": "Total general" if role == "TOTAL" else role,
            "formula_fuente": "",
        }
        if any(row[k] != v for k, v in checks.items()):
            raise ValueError(f"Inconsistent source metadata for {year}, {role}")
        amount = Decimal(row["ied_mdd"])
        if not amount.is_finite() or amount <= 0:
            raise ValueError("This frozen national sample contains published positive amounts only")


def load_inputs(data_dir: Path = ROOT / "data") -> tuple[list[dict], list[dict]]:
    groups = []
    for index, name in enumerate(FILES):
        content = (data_dir / name).read_bytes()
        if hashlib.sha256(content).hexdigest() != EXPECTED_HASHES[name]:
            raise ValueError(f"Pinned input hash mismatch: {name}")
        with (data_dir / name).open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != FIELDS:
                raise ValueError(f"Unexpected columns: {name}")
            rows = list(reader)
        validate_rows(rows, index == 0)
        groups.append(rows)
    return tuple(groups)


def calculate(annual: list[dict], snapshot: list[dict]) -> dict[str, list[dict]]:
    outputs = {"annual_shares.csv": [], "snapshot_2026s1.csv": [], "annual_changes.csv": [], "reconciliation.csv": []}
    with localcontext() as ctx:
        ctx.prec = 80
        for rows, destination in ((annual, "annual_shares.csv"), (snapshot, "snapshot_2026s1.csv")):
            indexed = {(r["anio"], r["tipo_inversion"]): r for r in rows}
            for year in sorted({r["anio"] for r in rows}):
                total_row = indexed[year, "TOTAL"]
                total = Decimal(total_row["ied_mdd"])
                amounts = [Decimal(indexed[year, c]["ied_mdd"]) for c in COMPONENTS]
                for comp, amount in zip(COMPONENTS, amounts):
                    source = indexed[year, comp]
                    outputs[destination].append({
                        "segment": source["segmento"], "year": year, "source_period": source["periodo_origen"],
                        "component": comp, "amount_usdm": source["ied_mdd"],
                        "published_total_usdm": total_row["ied_mdd"], "share_pct": ratio(amount, total),
                        "source_file": source["archivo_fuente"], "source_sheet": source["hoja"],
                        "component_cell": source["celda"], "total_cell": total_row["celda"],
                    })
                residual = total - sum(amounts)
                outputs["reconciliation.csv"].append({
                    "segment": total_row["segmento"], "year": year, "published_total_usdm": total_row["ied_mdd"],
                    "component_sum_usdm": text(sum(amounts)), "residual_usdm": text(residual),
                    "status": "exact" if residual == 0 else "residual_preserved",
                })
        indexed = {(int(r["anio"]), r["tipo_inversion"]): r for r in annual}
        for year in range(2007, 2026):
            base_total = Decimal(indexed[year - 1, "TOTAL"]["ied_mdd"])
            for role in ROLES:
                base = indexed[year - 1, role]
                current = indexed[year, role]
                change = Decimal(current["ied_mdd"]) - Decimal(base["ied_mdd"])
                outputs["annual_changes.csv"].append({
                    "base_year": year - 1, "current_year": year, "component": role,
                    "base_usdm": base["ied_mdd"], "current_usdm": current["ied_mdd"],
                    "change_usdm": text(change), "component_growth_pct": ratio(change, Decimal(base["ied_mdd"])),
                    "contribution_total_growth_pp": "" if role == "TOTAL" else ratio(change, base_total),
                    "contribution_status": "not_applicable_total" if role == "TOTAL" else "calculated",
                })
    return outputs


def write_outputs(outputs: dict[str, list[dict]], output_dir: Path) -> None:
    output_dir = output_dir.resolve()
    if output_dir == ROOT or ROOT in output_dir.parents:
        raise ValueError("Use a new output directory outside the project to preserve bundled files")
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError("Output directory must be new or empty")
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, rows in outputs.items():
        with (output_dir / filename).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
    receipt = {
        "input_rows": 84, "annual_source_rows": 80, "partial_year_source_rows": 4,
        "output_rows": {name: len(rows) for name, rows in outputs.items()},
        "input_sha256": EXPECTED_HASHES,
        "method": "Decimal precision 80; percentages rounded to 12 decimals HALF_UP; exact amount residuals retained",
        "scope": "Offline arithmetic reproduction of the fixed national extract; no fresh official-source download",
    }
    (output_dir / "calculation_receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="New/empty directory outside this project")
    args = parser.parse_args()
    annual, snapshot = load_inputs()
    write_outputs(calculate(annual, snapshot), args.output)
    print("Reproduced 84 national source amounts in two separate temporal segments.")


if __name__ == "__main__":
    main()
