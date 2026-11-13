"""Two separate year-on-year labor-market comparisons; Python 3.10+.

Run `python analyze.py` to rebuild tables and figures offline. Statistical
estimates come from INEGI's published tables; all derived ratios are explicit.
"""
from pathlib import Path
from decimal import Decimal as D
import argparse
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parent
PERIODS = ("2025-T2", "2026-T2", "2025-09", "2026-09")
SEXES = ("total", "mujeres", "hombres")
COUNTS = ("population_15plus", "labor_force", "employed", "unemployed", "outside_labor_force")
PAIRS = (("2025-T2", "2026-T2"), ("2025-09", "2026-09"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_data(path):
    with Path(path).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def validate(rows):
    require(len(rows) == 12, "Expected 12 period-sex records")
    idx = {}
    for r in rows:
        key = (r["period"], r["sex"])
        require(key not in idx, "Duplicate period-sex record")
        require(key[0] in PERIODS and key[1] in SEXES, "Unexpected period or sex")
        quarterly = key[0].endswith("T2")
        require(r["frequency"] == ("quarterly" if quarterly else "monthly"), "Frequency mismatch")
        require(r["source_id"] == ("enoe_2026t2" if quarterly else "enoe_202609"), "Source mismatch")
        for c in COUNTS:
            require(r[c].isdigit(), f"Count must be a nonnegative integer: {c}")
        n, lf, e, u, inactive = [int(r[c]) for c in COUNTS]
        require(n > 0 and lf > 0, "Zero denominator")
        require(n == lf + inactive, "Population != labor force + outside labor force")
        require(lf == e + u, "Labor force != employed + unemployed")
        for published, numerator, denominator in (
            ("participation_published_pct", lf, n),
            ("unemployment_published_pct", u, lf),
        ):
            p = D(r[published])
            require(0 <= p <= 100, "Published rate outside 0-100")
            require(abs(D(numerator)/D(denominator)*100-p) <= D("0.051"), "Published rate inconsistent with counts")
        idx[key] = r
    require(set(idx) == {(p,s) for p in PERIODS for s in SEXES}, "Incomplete coverage")
    for p in PERIODS:
        for c in COUNTS:
            require(int(idx[p,"total"][c]) == int(idx[p,"mujeres"][c]) + int(idx[p,"hombres"][c]), "Sex totals do not reconcile")
    return idx


def rounded(value):
    result = D(value).quantize(D("0.000000001"))
    return f"{abs(result) if result == 0 else result:.9f}"


def calculate(rows):
    idx = validate(rows)
    levels = []
    changes = []
    bridges = []
    for r in rows:
        n, lf, e, u = [D(r[c]) for c in COUNTS[:4]]
        levels.append({"period":r["period"], "frequency":r["frequency"], "sex":r["sex"],
                       "participation_pct":rounded(lf/n*100),
                       "employment_population_pct":rounded(e/n*100),
                       "unemployment_pct":rounded(u/lf*100)})
    for old, new in PAIRS:
        for s in SEXES:
            a,b = idx[old,s],idx[new,s]
            n0,n1 = D(a["population_15plus"]),D(b["population_15plus"])
            p0,p1 = D(a["labor_force"])/n0,D(b["labor_force"])/n1
            changes.append({"base_period":old,"comparison_period":new,"frequency":b["frequency"],"sex":s,
                **{f"change_{c}_persons":int(b[c])-int(a[c]) for c in COUNTS},
                "change_participation_pp":rounded((p1-p0)*100),
                "change_employment_population_pp":rounded((D(b["employed"])/n1-D(a["employed"])/n0)*100),
                "change_unemployment_pp":rounded((D(b["unemployed"])/D(b["labor_force"])-D(a["unemployed"])/D(a["labor_force"]))*100)})
            population = (n1-n0)*(p0+p1)/2
            participation = (p1-p0)*(n0+n1)/2
            delta = D(b["labor_force"])-D(a["labor_force"])
            residual = population+participation-delta
            require(abs(residual)<D("0.000000001"), "Labor-force bridge does not close")
            bridges.append({"base_period":old,"comparison_period":new,"sex":s,
                 "change_labor_force_persons":int(delta),"population_component_persons":rounded(population),
                 "participation_component_persons":rounded(participation),"identity_residual_persons":rounded(residual)})
    return levels,changes,bridges


def write_csv(path, rows):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
        w.writeheader();w.writerows(rows)


def charts(levels, changes, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":11,
                         "svg.hashsalt":"mexico-labor-participation-v1", "axes.spines.top":False,
                         "axes.spines.right":False})
    blue,orange,ink,grid = "#215b7b","#bd602d","#263747","#e5e9ed"
    labels={"total":"Total","mujeres":"Mujeres","hombres":"Hombres"}
    fig,axes=plt.subplots(1,2,figsize=(11.5,6),sharex=True)
    fig.subplots_adjust(left=.11,right=.98,top=.74,bottom=.23,wspace=.32)
    for ax,(old,new) in zip(axes,PAIRS):
        values=[next(x for x in changes if x["comparison_period"]==new and x["sex"]==s)["change_employed_persons"]/1000 for s in SEXES]
        ax.barh(range(3),values,height=.48,color=[blue if x>=0 else orange for x in values])
        ax.set_yticks(range(3),[labels[s] for s in SEXES]);ax.invert_yaxis()
        ax.set_xlim(-1400,1200);ax.set_xticks([-1000,-500,0,500,1000])
        ax.axvline(0,color=ink,lw=.9);ax.grid(axis="x",color=grid,lw=.7);ax.set_axisbelow(True)
        ax.set_title("Segundo trimestre" if "T2" in new else "Septiembre",loc="left",fontsize=13,pad=14)
        ax.set_xlabel("Cambio anual, miles de personas",labelpad=12)
        for y,v in enumerate(values):
            ax.text(v+(30 if v>=0 else -30),y,f"{v:+,.1f}",ha="left" if v>=0 else "right",va="center",color=ink,fontweight="bold")
    fig.text(.04,.93,"Población ocupada: cambios por sexo",fontsize=21,fontweight="bold",color=ink)
    fig.text(.04,.865,"México, población de 15 años y más · cada panel compara 2026 con el mismo periodo de 2025",fontsize=11,color=ink)
    fig.text(.04,.11,"Fuente: INEGI, ENOE, boletines 503/26 y 634/26, cuadro 1. Cálculos propios.",fontsize=10,color=ink)
    fig.text(.04,.065,"Son diferencias entre estimaciones agregadas, no transiciones individuales. Septiembre no representa todo el 3T.",fontsize=9,color=ink)
    for ext in ("svg","png"):
        fig.savefig(output/f"employment_by_sex.{ext}",dpi=170,metadata={"Date":None} if ext=="svg" else {"Software":"matplotlib"})
    plt.close(fig)
    fig,ax=plt.subplots(figsize=(11.5,6.7));fig.subplots_adjust(left=.29,right=.96,top=.75,bottom=.24)
    ys=[0,1,2.7,3.7];names=[]
    for k,(old,new) in enumerate(PAIRS):
        a=next(x for x in levels if x["period"]==old and x["sex"]=="total")
        b=next(x for x in levels if x["period"]==new and x["sex"]=="total")
        for j,(key,label) in enumerate((("participation_pct","Participación"),("employment_population_pct","Ocupación / población"))):
            y=ys[2*k+j];v0,v1=float(a[key]),float(b[key]);names.append(label+(" · 2T" if k==0 else " · septiembre"))
            ax.plot([v0,v1],[y,y],color=blue,lw=2)
            ax.scatter([v0],[y],facecolors="white",edgecolors=blue,s=70,zorder=3,label="2025" if k==j==0 else None)
            ax.scatter([v1],[y],facecolors=blue,edgecolors=blue,s=70,zorder=3,label="2026" if k==j==0 else None)
            ax.text(v0+.06,y-.18,f"{v0:.2f}%",fontsize=10,ha="left",color=ink)
            ax.text(v1-.06,y+.24,f"{v1:.2f}%",fontsize=10,ha="right",color=ink)
    ax.set_yticks(ys,names);ax.set_ylim(4.4,-.6);ax.set_xlim(55,61);ax.set_xticks(range(55,62))
    ax.set_xlabel("Porcentaje de población de 15 años y más · escala de 55% a 61%",labelpad=12)
    ax.grid(axis="x",color=grid);ax.set_axisbelow(True)
    ax.legend(loc="upper right",bbox_to_anchor=(1,1.18),ncol=2,frameon=False)
    fig.text(.04,.94,"Participación y ocupación respecto a la población",fontsize=20,fontweight="bold",color=ink)
    fig.text(.04,.885,"México, total nacional · comparaciones interanuales independientes, 2025–2026",fontsize=11,color=ink)
    fig.text(.04,.12,"Fuente: INEGI, ENOE, cuadro 1 de los boletines 503/26 y 634/26. Razones calculadas con los conteos.",fontsize=10,color=ink)
    fig.text(.04,.075,"Participación = PEA / población 15+; ocupación / población = ocupados / población 15+.",fontsize=9,color=ink)
    fig.text(.04,.038,"PEA: población económicamente activa. La figura no presenta la tasa de ocupación sobre la PEA.",fontsize=9,color=ink)
    for ext in ("svg","png"):
        fig.savefig(output/f"participation_and_employment_population.{ext}",dpi=170,metadata={"Date":None} if ext=="svg" else {"Software":"matplotlib"})
    plt.close(fig)


def run(data, output, make_charts=True):
    rows=load_data(data)
    levels,changes,bridges=calculate(rows)
    output.mkdir(parents=True,exist_ok=True)
    write_csv(output/"rates_calculated.csv",levels)
    write_csv(output/"year_on_year_changes.csv",changes)
    write_csv(output/"labor_force_bridge.csv",bridges)
    summary={"scope":"Two independent national year-on-year comparisons, Q2 and September 2025–2026",
             "national_changes":[r for r in changes if r["sex"]=="total"],
             "national_labor_force_bridge":[r for r in bridges if r["sex"]=="total"],
             "input_sha256":hashlib.sha256(Path(data).read_bytes()).hexdigest(),
             "input_records":len(rows),"raw_count_cells":60,"published_rate_cells":24,
             "limits":["No statistical significance test","No causal or individual-transition interpretation","September is not the third quarter"]}
    (output/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if make_charts:charts(levels,changes,output)
    return summary


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data",type=Path,default=ROOT/"data/enoe_counts_and_rates.csv")
    parser.add_argument("--output",type=Path,default=ROOT/"outputs")
    parser.add_argument("--no-charts",action="store_true",help="Rebuild tables using only the standard library")
    args=parser.parse_args()
    result=run(args.data,args.output,not args.no_charts)
    print(json.dumps({"status":"PASS","records":result["input_records"],"output":str(args.output)},ensure_ascii=False))
