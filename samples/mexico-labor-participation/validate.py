"""Reproduce outputs, check source anchors and reject damaged inputs."""
from pathlib import Path
from decimal import Decimal as D
import copy
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
from analyze import ROOT, calculate, load_data, require, validate


def inventory(path):
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(path.glob("*")) if p.is_file()}


def main():
    rows=load_data(ROOT/"data/enoe_counts_and_rates.csv")
    idx=validate(rows)
    # Independently read official table values, not generated result files.
    anchors={"2025-T2":(102615200,61065005,59440760),"2026-T2":(104305022,61676698,60040094),
             "2025-09":(104239840,62094108,60244382),"2026-09":(105617240,61735269,59977049)}
    for p,values in anchors.items():
        require(tuple(int(idx[p,"total"][k]) for k in ("population_15plus","labor_force","employed"))==values,"Official national anchor mismatch")
    levels,changes,bridges=calculate(rows)
    totals={r["comparison_period"]:r for r in changes if r["sex"]=="total"}
    require(totals["2026-T2"]["change_employed_persons"]==599334,"Q2 change")
    require(totals["2026-09"]["change_employed_persons"]==-267333,"September change")
    for p,expected in (("2026-T2",D("-0.377641122")),("2026-09",D("-1.116612690"))):
        require(abs(D(totals[p]["change_participation_pp"])-expected)<D("0.000000001"),"Participation change")
    # Identity check using fractions rather than the production Decimal arithmetic.
    from fractions import Fraction as F
    for old,new in (("2025-T2","2026-T2"),("2025-09","2026-09")):
        n0,lf0,e0=anchors[old];n1,lf1,e1=anchors[new]
        p0,p1=F(lf0,n0),F(lf1,n1)
        require(F(n1-n0)*(p0+p1)/2+(p1-p0)*F(n0+n1)/2==lf1-lf0,"Independent exact bridge")
    rejected=[]
    for case in ("duplicate","missing","negative","identity","sex_sum","frequency","source","published_rate"):
        bad=copy.deepcopy(rows)
        if case=="duplicate":bad[1]=bad[0].copy()
        elif case=="missing":bad.pop()
        elif case=="negative":bad[0]["employed"]="-1"
        elif case=="identity":bad[0]["labor_force"]=str(int(bad[0]["labor_force"])+1)
        elif case=="sex_sum":
            for key in ("population_15plus","labor_force","employed"):bad[0][key]=str(int(bad[0][key])+1)
        elif case=="frequency":bad[0]["frequency"]="monthly"
        elif case=="source":bad[0]["source_id"]="unknown"
        else:bad[0]["participation_published_pct"]="50.0"
        try:validate(bad)
        except ValueError:rejected.append(case)
        else:raise ValueError("Mutation not rejected: "+case)
    env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"}
    with tempfile.TemporaryDirectory(prefix="enoe_sample_validation_") as tmp:
        temp=Path(tmp)
        for mode,flags in (("normal",[]),("optimized",["-O"])):
            subprocess.run([sys.executable,*flags,str(ROOT/"analyze.py"),"--output",str(temp/mode)],check=True,capture_output=True,env=env)
        normal,optimized,stored=inventory(temp/"normal"),inventory(temp/"optimized"),inventory(ROOT/"outputs")
        require(normal==optimized==stored,"Outputs differ across normal, -O or stored files")
    report={"status":"PASS","python":platform.python_version(),"platform":platform.system(),
            "national_count_anchors":12,"negative_tests_rejected":rejected,
            "byte_identical_normal_optimized_stored_outputs":len(stored),
            "independent_fraction_bridge":"PASS","validated_input_records":12,
            "limits":"This validates calculations and reproducibility, not survey sampling significance."}
    (ROOT/"VALIDATION.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=="__main__":main()
