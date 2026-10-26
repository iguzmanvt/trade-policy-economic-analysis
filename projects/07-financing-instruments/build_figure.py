#!/usr/bin/env python3
"""Optional figure export. Run analyze.py first. Requires matplotlib."""
import csv
from decimal import Decimal, ROUND_HALF_UP
import os
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "p07-matplotlib"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "svg.fonttype": "none", "svg.hashsalt": "p07-financing-instruments-v1"})
with (ROOT / "results/annual_cashflows.csv").open() as f:
    annual = list(csv.DictReader(f))
with (ROOT / "results/package_comparison.csv").open() as f:
    comparison = list(csv.DictReader(f))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.8, 5.8), gridspec_kw={"width_ratios": [1.15, 1]})
colors = {"grant": "#626872", "concessional": "#24587A", "mixed": "#A76B10", "reference": "#885073"}
labels = {"grant": "Grant", "concessional": "Concessional loan", "mixed": "50% grant / 50% loan", "reference": "Reference loan"}
styles = {"grant": (0, (2, 2)), "concessional": "-", "mixed": "--", "reference": "-."}
for package in ("reference", "concessional", "mixed", "grant"):
    rows = [r for r in annual if r["package"] == package and int(r["year"]) > 0]
    ax1.plot([int(r["year"]) for r in rows], [float(r["debt_service_usd_m"]) for r in rows],
             color=colors[package], linestyle=styles[package], linewidth=2.1, label=labels[package])
ax1.set(title="Annual repayment profiles", xlabel="Year after initial disbursement", ylabel="Principal and interest  |  USD million", xlim=(1, 20), ylim=(-0.4, 16))
ax1.set_xticks([1, 5, 6, 10, 15, 20])
ax1.set_yticks([0, 5, 10, 15])
ax1.axvline(6, color="#A5A8AB", linewidth=0.9, linestyle=":")
ax1.legend(frameon=False, loc="upper right", fontsize=9)

packages = ["concessional", "mixed", "reference"]
scenarios = ["baseline", "fx25", "fx25_envelope20"]
scenario_colors = ["#B8C9D6", "#638BA8", "#244E6C"]
scenario_labels = ["Baseline", "FX shock", "FX + lower envelope"]
height = 0.22
for j, scenario in enumerate(scenarios):
    values = [float(next(r for r in comparison if r["package"] == p and r["fiscal_scenario"] == scenario)["peak_incremental_service_envelope_pct"]) for p in packages]
    positions = [i + (j - 1) * height for i in range(len(packages))]
    bars = ax2.barh(positions, values, height=height * 0.90, color=scenario_colors[j], label=scenario_labels[j])
    ax2.bar_label(bars, labels=[f"{Decimal(str(v)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}%" for v in values], padding=4, fontsize=9)
ax2.set_yticks(range(len(packages)), ["Concessional loan", "50% grant / 50% loan", "Reference loan"])
ax2.invert_yaxis()
ax2.set(title="Peak annual service relative to a fiscal envelope", xlabel="Incremental debt service  |  % of assumed annual envelope", xlim=(0, 23))
ax2.set_xticks([0, 5, 10, 15, 20])
ax2.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.45, -0.19), ncols=1, fontsize=9)

for ax in (ax1, ax2):
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#B5B7B9")
    ax.tick_params(length=3, color="#B5B7B9")
    ax.set_axisbelow(True)
ax1.grid(axis="y", color="#E5E7E9", linewidth=0.7)
ax2.grid(axis="x", color="#E5E7E9", linewidth=0.7)
fig.suptitle("Financing packages with the same USD 100 million initial funding", fontsize=15, x=0.065, ha="left", y=0.99)
fig.text(0.065, 0.935, "Synthetic illustration  |  Loans are fully disbursed at t=0; equal annual principal after any principal-payment holiday", fontsize=10, color="#50565C")
fig.text(0.065, 0.10, "FX shock: local-currency price of USD rises 25% from year 6. Combined stress also lowers the nominal envelope 20%.", fontsize=9)
fig.text(0.065, 0.062, "The envelope is synthetic, not government revenue. Grant repayments are zero under every scenario. No debt-sustainability threshold is estimated.", fontsize=9)
fig.text(0.065, 0.025, "Source: original calculations from data/assumptions.json. Illustrative analytical terms, not FRLD policy or an estimate of climate losses.", fontsize=9, color="#50565C")
fig.subplots_adjust(left=0.065, right=0.96, bottom=0.34, top=0.81, wspace=0.45)
dest = ROOT / "figures"
dest.mkdir(exist_ok=True)
fig.savefig(dest / "repayment_and_fiscal_stress.svg", metadata={"Date": None})
fig.savefig(dest / "repayment_and_fiscal_stress.png", dpi=180, metadata={"Software": "matplotlib"})
plt.close(fig)
print("Wrote figures/repayment_and_fiscal_stress.svg and .png")
