#!/usr/bin/env python3
"""Export two static FDI figures from reproduced results. Requires matplotlib."""
import argparse
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from verify import audit

COLORS = {"Nuevas inversiones": "#286294", "Reinversión de utilidades": "#BA7818", "Cuentas entre compañías": "#687547"}
STYLES = ["-", "--", "-."]
ROOT = Path(__file__).resolve().parent


def read(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def finish(fig, ax, out, stem):
    ax.set_axisbelow(True)
    ax.grid(axis="y", color="#DDE3E9", linewidth=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#87919B")
    ax.tick_params(colors="#34424F", length=3)
    for ext in ("svg", "png"):
        kwargs = {"metadata": {"Date": None}} if ext == "svg" else {"metadata": {"Software": "matplotlib"}}
        fig.savefig(out / f"{stem}.{ext}", dpi=180, facecolor="white", **kwargs)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    out = args.output.resolve()
    if out == ROOT or ROOT in out.parents or (out.exists() and any(out.iterdir())):
        raise ValueError("Choose a new/empty output directory outside the project")
    audit(args.results)
    annual = read(args.results / "annual_shares.csv")
    snapshot = read(args.results / "snapshot_2026s1.csv")
    if len(annual) != 60 or len(snapshot) != 3:
        raise ValueError("Unexpected results coverage")
    if {r["year"] for r in annual} != {str(y) for y in range(2006, 2026)}:
        raise ValueError("Annual chart must cover full years 2006–2025 only")
    out.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "svg.fonttype": "none", "svg.hashsalt": "national-fdi-2t2026-v1", "axes.labelcolor": "#34424F", "text.color": "#1C2C3A"})
    fig, ax = plt.subplots(figsize=(11.6, 6.8))
    fig.subplots_adjust(left=.085, right=.72, bottom=.21, top=.79)
    fig.text(.085, .925, "IED nacional por tipo de financiamiento", fontsize=19, weight="bold")
    fig.text(.085, .873, "Participación en el total publicado · cierres anuales 2006–2025", fontsize=12)
    for (component, color), style in zip(COLORS.items(), STYLES):
        rows = sorted((r for r in annual if r["component"] == component), key=lambda r: int(r["year"]))
        years = [int(r["year"]) for r in rows]
        shares = [float(r["share_pct"]) for r in rows]
        ax.plot(years, shares, color=color, linestyle=style, linewidth=2.3)
        ax.scatter(years[-1], shares[-1], color=color, s=32, zorder=4)
        # These two end values are close; offset their labels while retaining guide lines.
        target = 26 if component == "Nuevas inversiones" else 10 if component == "Cuentas entre compañías" else shares[-1]
        label = component.replace("Cuentas entre compañías", "Cuentas entre\ncompañías").replace("Reinversión de utilidades", "Reinversión de\nutilidades")
        ax.annotate(f"{label}\n{shares[-1]:.1f}%", (years[-1], shares[-1]), xytext=(2025.9, target),
                    ha="left", va="center", color=color, fontsize=11, annotation_clip=False,
                    arrowprops={"arrowstyle": "-", "color": color, "linewidth": .8})
    ax.set_xlim(2006, 2025)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.yaxis.set_major_formatter(PercentFormatter(100, decimals=0))
    ax.set_xticks([2006, 2010, 2015, 2020, 2025])
    fig.text(.085, .105, "Fuente: Secretaría de Economía / RNIE, publicación 2T2026; libro de cifras actualizadas (AC).", fontsize=9.4)
    fig.text(.085, .073, "Información al 30-jun-2026, captura 5-nov-2026. Cálculos propios; no se fuerza el cierre a 100%.", fontsize=9.4)
    fig.text(.085, .041, "Flujos netos nominales. Nuevas inversiones no equivale a proyectos greenfield. El semestre de 2026 se presenta aparte.", fontsize=9.0)
    finish(fig, ax, out, "annual_composition_2006_2025")

    fig, ax = plt.subplots(figsize=(11.6, 6.8))
    fig.subplots_adjust(left=.29, right=.91, bottom=.24, top=.73)
    fig.text(.075, .925, "IED nacional: enero–junio de 2026", fontsize=19, weight="bold")
    total = float(snapshot[0]["published_total_usdm"])
    fig.text(.075, .871, f"Total publicado: {total:,.1f} millones de USD corrientes", fontsize=12)
    rows = sorted(snapshot, key=lambda r: float(r["share_pct"]), reverse=True)
    for index, row in enumerate(rows):
        pct = float(row["share_pct"])
        ax.barh(index, pct, height=.48, color=COLORS[row["component"]])
        label = f"{pct:.1f}% · {float(row['amount_usdm']):,.1f} mdd"
        if pct > 55:
            ax.text(pct - 2, index, label, ha="right", va="center", color="white", fontsize=11, weight="bold")
        else:
            ax.text(pct + 1.5, index, label, ha="left", va="center", fontsize=11, color="#263747")
    ax.set_yticks(range(3), [r["component"].replace("Reinversión de utilidades", "Reinversión de\nutilidades").replace("Cuentas entre compañías", "Cuentas entre\ncompañías") for r in rows])
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.xaxis.set_major_formatter(PercentFormatter(100, decimals=0))
    ax.set_xlabel("Participación en el total nacional publicado", labelpad=10)
    fig.text(.075, .133, "Fuente: Secretaría de Economía / RNIE, publicación 2T2026; libro de cifras originales (OR), celdas AI5:AI8.", fontsize=9.4)
    fig.text(.075, .100, "Captura 5-nov-2026. Montos publicados; participaciones y figura de elaboración propia. Cifras revisables.", fontsize=9.4)
    fig.text(.075, .067, "Acumulado de seis meses: no es un total anual ni se compara como crecimiento con el cierre completo de 2025.", fontsize=9.4)
    finish(fig, ax, out, "snapshot_2026s1")
    receipt = {"figures": 2, "formats": ["SVG", "PNG"], "matplotlib": matplotlib.__version__, "annual_points": 60, "snapshot_bars": 3, "percentage_denominator": "published national total within each segment and period"}
    (out / "figure_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
