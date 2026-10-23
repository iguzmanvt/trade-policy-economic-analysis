"""Accounting decomposition of Mexico's dairy product uses. Standard library only."""
import csv, hashlib, json
from collections import defaultdict
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data/official_cells.csv'
OUT=ROOT/'results'
def read():
    with DATA.open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
    keys=[(r['family'],r['origin'],r['kind'],r['target']) for r in rows]
    assert len(keys)==len(set(keys)),'Duplicate source cell key'
    for r in rows:r['value']=D(r['value']);assert r['value'].is_finite()
    return rows

def group(code):
    if code.startswith('3115'):return 'Dairy products'
    if code.startswith(('311','3121')):return 'Other food and beverages'
    if code.startswith(('31','32','33')):return 'Other manufactures'
    if code.startswith('722'):return 'Food and beverage services'
    if code.startswith(('61','62','93')):return 'Education, health and government services'
    return 'Other products and services'

def write(name,rows):
    with (OUT/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)

def main():
    rows=read();OUT.mkdir(exist_ok=True)
    cells={(r['family'],r['origin'],r['target']):r['value'] for r in rows if r['kind']!='intermediate'}
    inter=[r for r in rows if r['kind']=='intermediate'];assert len(inter)==3*834
    for o in ['D','M','T']:
        assert sum(r['value'] for r in inter if r['origin']==o)==cells['MIP',o,'intermediate_published']
    intermediate={r['target']:{} for r in inter if r['origin']=='D'}
    for r in inter:intermediate[r['target']][r['origin']]=r['value']
    assert all(v['D']+v['M']==v['T'] for v in intermediate.values())
    parts=['private_consumption','government_consumption','fixed_capital','inventories','exports','discrepancy']
    for o in ['D','M']:
        assert sum(cells['MIP',o,c] for c in parts)==cells['MIP',o,'final_published']
        assert cells['MIP',o,'all_published']==cells['MIP',o,'intermediate_published']+cells['MIP',o,'final_published']
    final=sum(cells['MIP',o,'final_published'] for o in ['D','M']);alluses=final+cells['MIP','T','intermediate_published']
    assert final==cells['MIP','T','final_published']-cells['MIP','T','imports_net']
    assert alluses==cells['MIP','T','all_published']-cells['MIP','T','imports_net']
    origin=[]
    for o in ['D','M']:
        i=cells['MIP',o,'intermediate_published'];f=cells['MIP',o,'final_published'];a=i+f
        origin.append(dict(origin=o,intermediate=i,final=f,all_uses=a,intermediate_share_of_origin_pct=100*i/a,origin_share_of_all_uses_pct=100*a/alluses,origin_share_of_intermediate_pct=100*i/cells['MIP','T','intermediate_published']))
    write('origin_and_uses.csv',origin)
    groups=defaultdict(lambda:defaultdict(D))
    for code,vals in intermediate.items():
        for o,v in vals.items():groups[group(code)][o]+=v
    grouped=[dict(destination_group=g,domestic=v['D'],imported=v['M'],total=v['T'],share_of_intermediate_pct=100*v['T']/cells['MIP','T','intermediate_published'],imported_share_within_group_pct=100*v['M']/v['T']) for g,v in sorted(groups.items(),key=lambda x:x[1]['T'],reverse=True)]
    write('intermediate_destination_groups.csv',grouped)
    write('final_uses.csv',[dict(component=c,domestic=cells['MIP','D',c],imported=cells['MIP','M',c],total=cells['MIP','D',c]+cells['MIP','M',c],share_of_final_pct=100*(cells['MIP','D',c]+cells['MIP','M',c])/final) for c in parts])
    write('universe_comparison.csv',[dict(table='MIP',code='311513',axis='homogeneous product groups',intermediate=cells['MIP','T','intermediate_published'],gross_all_uses=alluses,intermediate_share_pct=100*cells['MIP','T','intermediate_published']/alluses),dict(table='COU',code='3115',axis='buyer industries',intermediate=cells['COU','T','intermediate_published'],gross_all_uses=cells['COU','T','all_published'],intermediate_share_pct=100*cells['COU','T','intermediate_published']/cells['COU','T','all_published'])])
    for target in ['all_published','intermediate_published','final_published']:
        assert cells['COU','D',target]+cells['COU','M',target]==cells['COU','T',target]
    summary={'input_rows':len(rows),'input_sha256':hashlib.sha256(DATA.read_bytes()).hexdigest(),'MIP_product_destinations':834,'MIP_positive_destinations':sum(v['T']>0 for v in intermediate.values()),'all_uses_million_MXN':alluses,'intermediate_million_MXN':cells['MIP','T','intermediate_published'],'final_million_MXN':final,'imported_share_intermediate_pct':100*cells['MIP','M','intermediate_published']/cells['MIP','T','intermediate_published'],'checks':'Passed: unique keys, full destination coverage, D+M=T cell identities, use totals, final components, import-netting bridge, COU origin identities'}
    (OUT/'validation.json').write_text(json.dumps(summary,indent=2,default=str)+'\n');print(json.dumps(summary,default=str,indent=2))
if __name__=='__main__':main()
