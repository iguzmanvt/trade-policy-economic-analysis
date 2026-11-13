"""Download fixed official PDFs to an external cache and audit all 84 input cells.

Requires Poppler's pdftotext. PDF originals and institutional logos are not
redistributed with this sample. A changed SHA stops the audit for manual review.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess
from urllib.request import Request,urlopen
from analyze import ROOT,load_data,require

INDICATORS=("population_15plus","labor_force","employed","unemployed","outside_labor_force")
PATTERNS=(r"^(Total|Mujeres|Hombres)\s",r"^Población económicamente activa",r"^Ocupada",r"^Desocupada",r"^Población no económicamente activa")
INTEGER=re.compile(r"-?\d{1,3}(?: \d{3}){1,2}")
DECIMAL=re.compile(r"-?\d+\.\d+")
SEXES=("total","mujeres","hombres")


def run(cache,download):
    cache=cache.resolve()
    require(not cache.is_relative_to(ROOT),"Official PDF cache must be outside the public sample")
    require(shutil.which("pdftotext") is not None,"Install Poppler to audit source PDFs")
    cache.mkdir(parents=True,exist_ok=True)
    meta=json.loads((ROOT/"data/sources.json").read_text(encoding="utf-8"))
    rows=load_data(ROOT/"data/enoe_counts_and_rates.csv")
    idx={(r["period"],r["sex"]):r for r in rows}
    checks=0;files=[]
    for src in meta["sources"]:
        target=cache/(src["id"]+".pdf")
        if not target.is_file():
            require(download,"Missing cached PDF; add --download")
            b=urlopen(Request(src["url"],headers={"User-Agent":"public-economic-data-audit/1.0"}),timeout=40).read()
            require(b.startswith(b"%PDF"),"Response is not a PDF")
            require(hashlib.sha256(b).hexdigest()==src["sha256"],"Source PDF changed: review a new vintage")
            target.write_bytes(b)
        require(hashlib.sha256(target.read_bytes()).hexdigest()==src["sha256"],"Cached PDF hash mismatch")
        text=subprocess.run(["pdftotext","-layout",str(target),"-"],check=True,capture_output=True).stdout.decode("utf-8")
        pages=text.split("\f");monthly=src["id"]=="enoe_202609"
        suffix="-09" if monthly else "-T2"
        page=pages[3 if monthly else 2].split("Cuadro 1",1)[1]
        sex=None;count=0
        for line in (s.strip() for s in page.splitlines()):
            for i,pattern in enumerate(PATTERNS):
                if re.match(pattern,line):
                    if i==0:sex={"Total":"total","Mujeres":"mujeres","Hombres":"hombres"}[line.split()[0]]
                    require(sex is not None,"Missing sex in source table")
                    values=INTEGER.findall(line)
                    require(len(values)>=2,"Missing source levels")
                    for year,value in zip(("2025","2026"),values[:2]):
                        require(idx[year+suffix,sex][INDICATORS[i]]==value.replace(" ",""),"Source count mismatch")
                        checks+=1
                    count+=1;break
        require(count==15,"Expected 15 source count rows")
        rate_page=pages[9 if monthly else 8]
        for field,pattern in (("participation_published_pct",r"Tasa de participación"),("unemployment_published_pct",r"Tasa de desocupación")):
            lines=rate_page.splitlines();positions=[i for i,line in enumerate(lines) if re.match(pattern,line.strip())]
            require(len(positions)==1,"Ambiguous published rate")
            pos=positions[0]
            if monthly:
                for offset,sex in enumerate(SEXES):
                    values=DECIMAL.findall(lines[pos+offset]);require(len(values)==11,"Monthly rate structure changed")
                    for year,value in zip(("2025","2026"),values[4:6]):
                        require(idx[year+suffix,sex][field]==value,"Published rate mismatch");checks+=1
            else:
                values=DECIMAL.findall(lines[pos]);require(len(values)==6,"Quarterly rate structure changed")
                for iy,year in enumerate(("2025","2026")):
                    for ix,sex in enumerate(SEXES):
                        require(idx[year+suffix,sex][field]==values[iy*3+ix],"Published rate mismatch");checks+=1
        files.append({"source_id":src["id"],"sha256":src["sha256"],"match":"PASS"})
    require(checks==84,"Expected 60 counts and 24 rates")
    report={"status":"PASS","pdfs":files,"source_numeric_cells_verified":checks,
            "counts":60,"published_rates":24,"extraction":"pdftotext -layout; exact string/integer comparisons"}
    (ROOT/"SOURCE_AUDIT.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--cache",type=Path,required=True);p.add_argument("--download",action="store_true")
    a=p.parse_args();run(a.cache,a.download)
