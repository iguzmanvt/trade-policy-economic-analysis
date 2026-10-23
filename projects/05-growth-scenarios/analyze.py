#!/usr/bin/env python3
"""Exact, offline Solow scenarios. Python 3.11+, standard library only.

New implementation for this portfolio; mathematical mechanism developed in
the author's pre-existing public Solow teaching materials. No source code or
figures from those materials are copied. See SOURCES.md.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def chart(rows: list[dict], scenarios: list[dict], path: Path) -> None:
    """Standalone SVG using the reviewed model rows; no external renderer."""
    width, height = 1060, 600
    left, right, top, bottom = 85, 1000, 125, 485
    ymin, ymax, xmax = -5, 35, max(r["year"] for r in rows)
    x = lambda t: left + (right - left) * t / xmax
    y = lambda v: bottom - (bottom - top) * (v - ymin) / (ymax - ymin)
    colors = ["#333333", "#002060", "#a8750d", "#8d4259"]
    dashes = ["6 4", "", "9 3", "3 3"]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
             '<title id="title">Illustrative output per worker gaps relative to baseline</title>',
             '<desc id="desc">Four exact Solow model paths over fifty years; values are percentage gaps relative to the same-year baseline. These are hypothetical scenarios, not forecasts.</desc>',
             '<rect width="1060" height="600" fill="white"/>',
             '<g font-family="Arial, sans-serif" fill="#222222">',
             '<text x="85" y="35" font-size="23" font-weight="bold">Investment and efficiency affect different horizons</text>',
             '<text x="85" y="61" font-size="15">Output per worker: percent gap relative to the same-year baseline</text>']
    for i, s in enumerate(scenarios):
        lx = 85 + [0, 170, 405, 700][i]
        dash = f' stroke-dasharray="{dashes[i]}"' if dashes[i] else ""
        parts += [f'<line x1="{lx}" x2="{lx+30}" y1="90" y2="90" stroke="{colors[i]}" stroke-width="2.7"{dash}/>',
                  f'<text x="{lx+38}" y="95" font-size="14">{escape(s["label"])}</text>']
    for v in range(-5, 36, 5):
        yy = y(v)
        parts += [f'<line x1="{left}" x2="{right}" y1="{yy}" y2="{yy}" stroke="{"#aaa" if v == 0 else "#e9e9e9"}" stroke-width="1"/>',
                  f'<text x="{left-12}" y="{yy+5}" text-anchor="end" font-size="14">{v}%</text>']
    for t in range(0, xmax + 1, 10):
        xx = x(t)
        parts += [f'<line x1="{xx}" x2="{xx}" y1="{bottom}" y2="{bottom+5}" stroke="#444"/>',
                  f'<text x="{xx}" y="{bottom+27}" text-anchor="middle" font-size="14">{t}</text>']
    parts += [f'<path d="M {left} {top} V {bottom} H {right}" stroke="#444" fill="none"/>',
              '<text x="542" y="540" text-anchor="middle" font-size="15">Years after the assumed change</text>']
    for i, s in enumerate(scenarios):
        rr = [r for r in rows if r["scenario"] == s["id"]]
        assert all(ymin <= r["output_gap_pct"] <= ymax for r in rr)
        points = " ".join(f'{x(r["year"]):.3f},{y(r["output_gap_pct"]):.3f}' for r in rr)
        dash = f' stroke-dasharray="{dashes[i]}"' if dashes[i] else ""
        parts.append(f'<polyline points="{points}" fill="none" stroke="{colors[i]}" stroke-width="2.7"{dash}/>')
    parts += ['<text x="85" y="574" font-size="13">Source: author’s exact Solow model calculation. Illustrative parameters; no country forecast or confidence interval.</text>', '</g></svg>']
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    input_path = ROOT / "data" / "parameters.json"
    p = json.loads(input_path.read_text(encoding="utf-8"))
    a, delta, n, A0, T = (p[k] for k in ("alpha", "depreciation", "labor_growth", "initial_efficiency", "horizon_years"))
    assert 0 < a < 1 and delta >= 0 and n >= 0 and A0 > 0
    assert isinstance(T, int) and T >= 50
    scenarios = p["scenarios"]
    assert len({s["id"] for s in scenarios}) == len(scenarios)
    baseline = next(s for s in scenarios if s["id"] == "baseline")
    base_lambda = delta + n + baseline["efficiency_growth"]
    k0 = (baseline["investment_share"] / base_lambda) ** (1 / (1-a))
    y0 = A0 * k0**a
    raw = []
    max_ode_residual = 0.0
    max_accounting_residual = 0.0
    for s in scenarios:
        saving, g = s["investment_share"], s["efficiency_growth"]
        assert 0 < saving < 1 and delta + n + g > 0
        lam = delta + n + g
        z0, zstar = k0 ** (1-a), saving / lam
        for t in range(T + 1):
            decay = math.exp(-(1-a)*lam*t)
            z = zstar + (z0-zstar)*decay
            k = z ** (1/(1-a))
            A = A0 * math.exp(g*t)
            output = A * k**a
            consumption, investment = (1-saving)*output, saving*output
            zdot = -(1-a)*lam*(z0-zstar)*decay
            kdot_exact = z**(a/(1-a))*zdot/(1-a)
            kdot_ode = saving*k**a - lam*k
            max_ode_residual = max(max_ode_residual, abs(kdot_exact-kdot_ode))
            max_accounting_residual = max(max_accounting_residual, abs(consumption+investment-output))
            growth = g + a*kdot_exact/k
            if s["id"] == "baseline":
                assert math.isclose(k, k0, rel_tol=1e-12)
                assert math.isclose(growth, baseline["efficiency_growth"], abs_tol=1e-12)
            raw.append({"scenario":s["id"], "year":t,
                        "capital_per_effective_worker":k,
                        "output_per_worker_index":100*output/y0,
                        "consumption_per_worker_index":100*consumption/((1-baseline["investment_share"])*y0),
                        "investment_per_worker_index":100*investment/(baseline["investment_share"]*y0),
                        "instantaneous_output_growth_pct":100*growth,
                        "investment_share":saving, "efficiency_growth":g})
    base_by_year = {r["year"]:r for r in raw if r["scenario"] == "baseline"}
    for r in raw:
        b = base_by_year[r["year"]]
        r["output_gap_pct"] = 100*(r["output_per_worker_index"]/b["output_per_worker_index"]-1)
        r["consumption_gap_pct"] = 100*(r["consumption_per_worker_index"]/b["consumption_per_worker_index"]-1)
        assert all(math.isfinite(v) for v in r.values() if isinstance(v, (float,int)))
    assert len(raw) == len(scenarios)*(T+1)
    assert len({(r["scenario"],r["year"]) for r in raw}) == len(raw)
    assert max_ode_residual < 1e-11 and max_accounting_residual < 1e-11
    assert all(abs(r["output_gap_pct"]) < 1e-10 for r in raw if r["year"] == 0)
    summary=[]
    for s in scenarios:
        rr={r["year"]:r for r in raw if r["scenario"]==s["id"]}
        summary.append({"scenario":s["id"], "label":s["label"],
                        "output_gap_year_10_pct":rr[10]["output_gap_pct"],
                        "output_gap_year_25_pct":rr[25]["output_gap_pct"],
                        "output_gap_year_50_pct":rr[50]["output_gap_pct"],
                        "initial_consumption_gap_pct":rr[0]["consumption_gap_pct"],
                        "consumption_gap_year_25_pct":rr[25]["consumption_gap_pct"],
                        "consumption_gap_year_50_pct":rr[50]["consumption_gap_pct"],
                        "long_run_output_growth_pct":100*s["efficiency_growth"],
                        "target_capital_per_effective_worker":(s["investment_share"]/(delta+n+s["efficiency_growth"]))**(1/(1-a))})
    out=ROOT/"results"
    out.mkdir(exist_ok=True)
    write_csv(out/"paths.csv",raw)
    write_csv(out/"scenario_summary.csv",summary)
    chart(raw,scenarios,out/"output_gaps.svg")
    record={"input_sha256":hashlib.sha256(input_path.read_bytes()).hexdigest(),
            "rows":len(raw),"scenario_count":len(scenarios),"years_including_initial":T+1,
            "duplicate_keys":0,"finite_values":True,"shared_initial_capital":k0,
            "max_ode_residual":max_ode_residual,"max_accounting_residual":max_accounting_residual,
            "baseline_stationarity_checked":True,"same_initial_output_checked":True,
            "method":"Closed-form continuous-time transition; no discretization step or numerical solver"}
    (out/"validation.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":"passed",**record},indent=2))


if __name__ == "__main__":
    main()
