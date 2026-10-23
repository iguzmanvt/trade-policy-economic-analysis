"""Extract a public row snapshot from the unmodified INEGI 2018 workbooks.
Uses only Python's standard library. The six source workbooks remain external.
"""
import argparse, csv, hashlib, json, re
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
ROOT=Path(__file__).resolve().parent
FILES={'MIP_19.xlsx':('MIP','D',196),'MIP_38.xlsx':('MIP','M',196),'MIP_10.xlsx':('MIP','T',196),'COU_177.xlsx':('COU','D',48),'COU_184.xlsx':('COU','M',48),'COU_170.xlsx':('COU','T',48)}
def workbook(path,sheet_number=1):
    with ZipFile(path) as z:
        strings=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',NS):
                strings.append(''.join(si.itertext()))
        out={}
        for c in ET.fromstring(z.read(f'xl/worksheets/sheet{sheet_number}.xml')).findall('.//m:c',NS):
            v=c.find('m:v',NS)
            if v is not None: out[c.attrib['r']]=strings[int(v.text)] if c.attrib.get('t')=='s' else v.text
            elif c.attrib.get('t')=='inlineStr':out[c.attrib['r']]=''.join(c.find('m:is',NS).itertext())
        return out

def extract(source,out):
    rows=[];provenance=[]
    for name,(family,origin,row) in FILES.items():
        p=source/name;cells=workbook(p);meta=workbook(p,2)
        assert meta['C12']=='2018'
        assert meta['C14']=='2023-08-29'
        assert cells['A'+str(row)].strip().startswith('311513' if family=='MIP' else '3115')
        provenance.append({'file':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'table_title':cells['A3'],'source_row':row,'metadata_update':meta['C14'],'reference_year':int(meta['C12'])})
        selected=[]
        if family=='MIP':
            for address,val in cells.items():
                if re.fullmatch('[A-Z]+196',address):
                    col=address[:-3];head=cells.get(col+'6','')
                    if re.match(r'^\d{6} - ',head):selected.append((col,'intermediate',head.split(' - ',1)[0],head))
            finals=['AFG','AFH','AFI','AFJ','AFK','AFL']+(['AFM'] if origin=='T' else [])
            selected += [('B','control','all_published','Published total'),('C','control','intermediate_published','Intermediate total'),('AFF','control','final_published','Published final total')]
        else:
            finals=['JH','JI','JJ','JK','JL','JM']
            selected += [('B','control','all_published','Published total'),('C','control','intermediate_published','Intermediate total'),('JG','control','final_published','Published final total')]
        for col in finals:
            header=cells.get(col+'6','')
            key={'AFG':'private_consumption','AFH':'government_consumption','AFI':'fixed_capital','AFJ':'inventories','AFK':'exports','AFL':'imports_net' if origin=='T' else 'discrepancy','AFM':'discrepancy','JH':'private_consumption','JI':'government_consumption','JJ':'fixed_capital','JK':'inventories','JL':'exports','JM':'discrepancy'}[col]
            selected.append((col,'final',key,header))
        for col,kind,target,label in selected:
            addr=col+str(row)
            if addr not in cells:raise ValueError('Missing cell '+name+':'+addr)
            rows.append({'family':family,'product_code':'311513' if family=='MIP' else '3115','origin':origin,'kind':kind,'target':target,'value':cells[addr],'file':name,'sheet':'Tabulado','cell':addr,'label_original':label})
    out.mkdir(parents=True,exist_ok=True)
    with (out/'official_cells.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    (out/'workbook_provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Extracted',len(rows),'cells from',len(FILES),'workbooks')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source_directory',type=Path);p.add_argument('--output',type=Path,default=ROOT/'data');a=p.parse_args();extract(a.source_directory,a.output)
