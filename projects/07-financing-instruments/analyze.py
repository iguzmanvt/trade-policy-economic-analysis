#!/usr/bin/env python3
"""Illustrative funding-package cash flows. Standard library; no network access."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOL = 1e-9


def require(condition, message):
    if not condition:
        raise ValueError(message)


def finite_number(value, name, minimum=0):
    require(isinstance(value, (int, float)) and not isinstance(value, bool), f"{name}: numeric value required")
    require(math.isfinite(value) and value >= minimum, f"{name}: finite value >= {minimum} required")


def integer(value, name, minimum=0):
    require(type(value) is int and value >= minimum, f"{name}: integer >= {minimum} required")


def validate_inputs(a):
    require("synthetic" in a["input_status"].lower(), "Synthetic input status must be explicit")
    integer(a["horizon_years"], "horizon_years", 1)
    require(a["packages"] and a["fiscal_scenarios"] and a["discount_rates"], "Inputs cannot be empty")
    for label, group in [("package", a["packages"]), ("fiscal scenario", a["fiscal_scenarios"])]:
        ids = [r["id"] for r in group]
        require(len(set(ids)) == len(ids) and all(ids), f"{label}: duplicate or empty IDs")
    totals = []
    for p in a["packages"]:
        for key in ("grant_usd_m", "loan_usd_m", "interest_rate"):
            finite_number(p[key], f"{p['id']}.{key}")
        for key in ("maturity_years", "principal_holiday_years"):
            integer(p[key], f"{p['id']}.{key}")
        total = p["grant_usd_m"] + p["loan_usd_m"]
        require(total > 0, "A package must provide positive funding")
        totals.append(total)
        if p["loan_usd_m"]:
            require(p["principal_holiday_years"] < p["maturity_years"] <= a["horizon_years"], "Principal holiday must end before maturity; horizon must cover full repayment")
        else:
            require(p["interest_rate"] == p["maturity_years"] == p["principal_holiday_years"] == 0, "Grant-only package cannot have debt terms")
    require(all(math.isclose(t, totals[0], abs_tol=TOL) for t in totals), "Comparisons require equal total initial funding")
    for s in a["fiscal_scenarios"]:
        for key in ("baseline_fx_lcu_per_usd", "baseline_envelope_lcu_m", "post_stress_fx_multiplier", "post_stress_envelope_multiplier"):
            finite_number(s[key], f"{s['id']}.{key}")
            require(s[key] > 0, f"{key} must be strictly positive")
        integer(s["stress_start_year"], "stress_start_year", 1)
        require(s["stress_start_year"] <= a["horizon_years"], "Stress must be within horizon")
    for r in a["discount_rates"]:
        finite_number(r, "discount rate")
    finite_number(a["main_discount_rate"], "main discount rate")
    require(len(set(a["discount_rates"])) == len(a["discount_rates"]), "Duplicate discount rates")
    require(a["main_discount_rate"] in a["discount_rates"], "Main rate must be in sensitivity grid")
    t = a["timing_experiment"]
    finite_number(t["opening_cash_buffer_usd_m"], "opening cash buffer")
    finite_number(t["funding_usd_m"], "timing funding")
    require(t["monthly_spending_usd_m"] and t["receipt_months"], "Monthly experiment cannot be empty")
    for x in t["monthly_spending_usd_m"]:
        finite_number(x, "monthly spending")
    for m in t["receipt_months"]:
        integer(m, "receipt month", 1)
        require(m <= len(t["monthly_spending_usd_m"]), "Receipt must occur within monthly horizon")
    require(len(set(t["receipt_months"])) == len(t["receipt_months"]), "Duplicate receipt months")


def loan_schedule(p, horizon):
    """t=0 disbursement; annual interest in arrears; equal principal after holiday."""
    principal = p["loan_usd_m"]
    balance = principal
    total = p["grant_usd_m"] + principal
    rows = [{"package": p["id"], "year": 0, "initial_receipt_usd_m": total,
             "opening_debt_usd_m": 0.0, "interest_usd_m": 0.0, "principal_usd_m": 0.0,
             "debt_service_usd_m": 0.0, "closing_debt_usd_m": principal,
             "borrower_net_financing_cashflow_usd_m": total}]
    annual_principal = principal / (p["maturity_years"] - p["principal_holiday_years"]) if principal else 0
    for year in range(1, horizon + 1):
        opening = balance
        interest = opening * p["interest_rate"] if year <= p["maturity_years"] else 0.0
        repayment = min(balance, annual_principal) if p["principal_holiday_years"] < year <= p["maturity_years"] else 0.0
        if year == p["maturity_years"]:
            repayment = balance  # eliminate floating-point residual in final payment
        balance -= repayment
        service = interest + repayment
        rows.append({"package": p["id"], "year": year, "initial_receipt_usd_m": 0.0,
                     "opening_debt_usd_m": opening, "interest_usd_m": interest,
                     "principal_usd_m": repayment, "debt_service_usd_m": service,
                     "closing_debt_usd_m": balance,
                     "borrower_net_financing_cashflow_usd_m": -service})
    require(abs(sum(r["principal_usd_m"] for r in rows) - principal) < TOL, "Principal does not reconcile")
    require(abs(balance) < TOL, "Debt remains after horizon")
    for r in rows[1:]:
        require(abs(r["opening_debt_usd_m"] - r["principal_usd_m"] - r["closing_debt_usd_m"]) < TOL, "Debt identity fails")
        require(r["closing_debt_usd_m"] >= -TOL, "Negative debt balance")
    return rows


def present_value(rows, rate):
    return sum(r["debt_service_usd_m"] / (1 + rate) ** r["year"] for r in rows if r["year"] > 0)


def timing_results(t):
    detail, summary = [], []
    for receipt_month in t["receipt_months"]:
        spent = received = 0.0
        gaps = []
        for month, expenditure in enumerate(t["monthly_spending_usd_m"], 1):
            receipt = t["funding_usd_m"] if month == receipt_month else 0.0
            received += receipt
            spent += expenditure
            position = t["opening_cash_buffer_usd_m"] + received - spent
            gap = max(0.0, -position)
            gaps.append(gap)
            detail.append({"receipt_month": receipt_month, "month": month, "receipt_usd_m": receipt,
                           "spending_usd_m": expenditure, "cumulative_receipts_usd_m": received,
                           "cumulative_spending_usd_m": spent,
                           "unfunded_cash_position_usd_m": position, "cash_shortfall_usd_m": gap})
        summary.append({"receipt_month": receipt_month, "funding_usd_m": t["funding_usd_m"],
                        "opening_buffer_usd_m": t["opening_cash_buffer_usd_m"],
                        "peak_cash_shortfall_usd_m": max(gaps), "months_with_shortfall": sum(g > TOL for g in gaps)})
    return detail, summary


def compute(a):
    validate_inputs(a)
    annual, fiscal, summaries, sensitivity = [], [], [], []
    for p in a["packages"]:
        rows = loan_schedule(p, a["horizon_years"])
        annual.extend(rows)
        funding = p["grant_usd_m"] + p["loan_usd_m"]
        for r in a["discount_rates"]:
            pv = present_value(rows, r)
            sensitivity.append({"package": p["id"], "discount_rate_pct": r * 100,
                                "pv_repayment_usd_m": pv,
                                "initial_funding_minus_pv_usd_m": funding - pv,
                                "package_pv_support_pct": (funding - pv) / funding * 100})
        for s in a["fiscal_scenarios"]:
            scenario_rows = []
            for row in rows[1:]:
                after = row["year"] >= s["stress_start_year"]
                fx = s["baseline_fx_lcu_per_usd"] * (s["post_stress_fx_multiplier"] if after else 1)
                envelope = s["baseline_envelope_lcu_m"] * (s["post_stress_envelope_multiplier"] if after else 1)
                local_service = row["debt_service_usd_m"] * fx
                new = {"package": p["id"], "fiscal_scenario": s["id"], "year": row["year"],
                       "fx_lcu_per_usd": fx, "annual_envelope_lcu_m": envelope,
                       "debt_service_usd_m": row["debt_service_usd_m"], "debt_service_lcu_m": local_service,
                       "incremental_service_envelope_pct": 100 * local_service / envelope}
                scenario_rows.append(new)
                fiscal.append(new)
            peak = max(scenario_rows, key=lambda z: z["incremental_service_envelope_pct"])
            pv = present_value(rows, a["main_discount_rate"])
            summaries.append({"package": p["id"], "fiscal_scenario": s["id"],
                              "initial_funding_usd_m": funding, "new_debt_usd_m": p["loan_usd_m"],
                              "nominal_interest_usd_m": sum(r["interest_usd_m"] for r in rows),
                              "pv_repayment_usd_m": pv, "package_pv_support_pct": (funding - pv) / funding * 100,
                              "peak_annual_service_usd_m": max(r["debt_service_usd_m"] for r in rows),
                              "peak_incremental_service_envelope_pct": peak["incremental_service_envelope_pct"],
                              "first_peak_year": peak["year"],
                              "new_debt_after_year5_usd_m": rows[5]["closing_debt_usd_m"] if len(rows) > 5 else ""})
    timing_detail, timing_summary = timing_results(a["timing_experiment"])
    return {"annual_cashflows.csv": annual, "fiscal_stress.csv": fiscal,
            "package_comparison.csv": summaries, "discount_sensitivity.csv": sensitivity,
            "timing_cashflows.csv": timing_detail, "timing_sensitivity.csv": timing_summary}


def csv_text(rows):
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({k: f"{v:.10f}" if isinstance(v, float) else v for k, v in row.items()})
    return out.getvalue()


def run(input_path=ROOT / "data/assumptions.json", output_dir=ROOT / "results"):
    data_bytes = Path(input_path).read_bytes()
    assumptions = json.loads(data_bytes)
    computed = compute(assumptions)  # validate and complete calculations before any writes
    texts = {name: csv_text(rows) for name, rows in computed.items()}
    verification = {"status": "PASS", "scope": "Synthetic-input validation and cash-flow accounting; not a country DSA or official concessionality certification",
                    "input_sha256": hashlib.sha256(data_bytes).hexdigest(),
                    "row_counts": {name: len(rows) for name, rows in computed.items()},
                    "discount_benchmark_pct": assumptions["main_discount_rate"] * 100,
                    "input_status": assumptions["input_status"]}
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, body in texts.items():
        (output_dir / name).write_text(body, encoding="utf-8")
    (output_dir / "validation.json").write_text(json.dumps(verification, indent=2) + "\n", encoding="utf-8")
    return verification


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "data/assumptions.json")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results")
    args = parser.parse_args()
    print(json.dumps(run(args.input, args.output_dir), indent=2))
