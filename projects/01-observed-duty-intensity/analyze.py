"""Reproduce a bounded comparison of calculated U.S. import duty intensity.

Run from any directory with Python 3.11 or later. Standard library only.
The input contains January–August totals reconstructed from archived monthly
observations. It is not a direct download of Census's revised YTD (_YR) fields.
No confidential source paths, tokens, or client identifiers are needed.
"""
from __future__ import annotations
import argparse
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path
import hashlib
import json
from html import escape

PRODUCTS = {
    '8471500150': 'Processing units',
    '8471709000': 'Storage units',
    '8517620020': 'Switching and routing apparatus',
}
COUNTRIES = {'2010':'Mexico','5700':'China','5830':'Taiwan','5520':'Vietnam','5570':'Malaysia'}
PERIODS = ['2025-08','2026-08']
BASIS = 'JAN_AUG_MONTHLY_SUM'
REQUIRED = ['time','basis','cty_code','country','hts10','con_val_usd','calc_dut_usd']

def gap_figure(path: Path, rates):
    """Write an accessible, dependency-free SVG; panels use explicit scales."""
    latest=[r for r in rates if r['period']=='2026-08' and r['country']!='Mexico']
    colors={'Processing units':'#002060','Storage units':'#008285',
            'Switching and routing apparatus':'#A15500'}
    width,height=1200,700
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
      '<title id="title">Observed duty intensity gaps relative to Mexico, January–August 2026</title>',
      '<desc id="desc">Positive gaps indicate a higher supplier duty-to-value ratio than Mexico. China has gaps of about 26 to 28 percentage points. Gaps for Taiwan, Vietnam and Malaysia are between minus 0.102 and plus 1.231 points. Panels deliberately use different scales.</desc>',
      '<rect width="1200" height="700" fill="white"/>',
      '<style>text{font-family:Arial,sans-serif;fill:#182333}.title{font-size:25px;font-weight:bold}.sub{font-size:16px}.lab{font-size:15px}.axis{font-size:14px}.value{font-size:15px;font-weight:bold}</style>',
      '<text x="38" y="43" class="title">Observed duty intensity gaps relative to Mexico</text>',
      '<text x="38" y="71" class="sub">January–August 2026 · supplier ratio minus Mexico ratio · percentage points</text>',
      '<text x="38" y="97" class="sub">Two panels with different scales preserve the smaller positive and negative gaps.</text>']
    def panel(x0,y0,w,rows,lo,hi,ticks,title):
        label_w=142
        plot_x=x0+label_w; plot_w=w-label_w-76
        transform=lambda v: plot_x+(v-lo)/(hi-lo)*plot_w
        h=len(rows)*35
        parts.append(f'<text x="{x0}" y="{y0-27}" class="sub" font-weight="bold">{escape(title)}</text>')
        for tick in ticks:
            x=transform(tick)
            parts.append(f'<line x1="{x:.2f}" y1="{y0-11}" x2="{x:.2f}" y2="{y0+h-6}" stroke="#d9dee5"/>')
            parts.append(f'<text x="{x:.2f}" y="{y0+h+16}" text-anchor="middle" class="axis">{tick:g}</text>')
        zero=transform(0)
        parts.append(f'<line x1="{zero:.2f}" y1="{y0-11}" x2="{zero:.2f}" y2="{y0+h-6}" stroke="#576575" stroke-width="1.8"/>')
        for i,r in enumerate(rows):
            y=y0+i*35+7; val=float(r['gap_vs_mexico_pp']); x=transform(val)
            label=r['country']+' · '+{'Processing units':'P','Storage units':'S','Switching and routing apparatus':'N'}[r['product']]
            parts.append(f'<text x="{plot_x-12}" y="{y+5}" text-anchor="end" class="lab">{label}</text>')
            parts.append(f'<line x1="{zero:.2f}" y1="{y}" x2="{x:.2f}" y2="{y}" stroke="{colors[r["product"]]}" stroke-width="4"/>')
            parts.append(f'<circle cx="{x:.2f}" cy="{y}" r="5" fill="{colors[r["product"]]}"/>')
            # Keep a fixed label column rather than overlapping points near zero.
            parts.append(f'<text x="{plot_x+plot_w+12}" y="{y+5}" class="value">{val:+.3f}</text>')
    panel(38,170,540,[r for r in latest if r['country']=='China'],0,30,[0,10,20,30],'China')
    panel(602,170,560,[r for c in ['Taiwan','Vietnam','Malaysia'] for r in latest if r['country']==c],-.2,1.4,[-.2,0,.4,.8,1.2],'Other selected suppliers')
    parts += [
      '<text x="38" y="552" class="lab">P: Processing units (8471500150)   S: Storage units (8471709000)</text>',
      '<text x="38" y="578" class="lab">N: Switching and routing apparatus (8517620020)</text>',
      '<text x="38" y="619" class="lab">Source: archived U.S. Census import aggregates; author’s calculations.</text>',
      '<text x="38" y="644" class="lab">January–August totals reconstructed from archived monthly observations; 30 input aggregates.</text>',
      '<text x="38" y="669" class="lab">Ratio: 100 × calculated duties / customs value of imports for consumption. No new monthly-source verification.</text>',
      '</svg>']
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text('\n'.join(parts),encoding='utf-8')

def decimal_value(text: str, field: str, row: int) -> Decimal:
    try:
        value=Decimal(text)
    except (InvalidOperation, TypeError):
        raise ValueError(f'Invalid {field} at input row {row}') from None
    if not value.is_finite() or value < 0:
        raise ValueError(f'Nonfinite or negative {field} at input row {row}')
    return value

def load_rows(path: Path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        if reader.fieldnames != REQUIRED:
            raise ValueError(f'Expected exact input fields {REQUIRED}; received {reader.fieldnames}')
        rows=[]; keys=set()
        for i,r in enumerate(reader,start=2):
            if None in r or any(v is None or v=='' for v in r.values()):
                raise ValueError(f'Empty or malformed field at input row {i}')
            if r['basis']!=BASIS:
                raise ValueError(f'Input row {i} is not explicitly a January–August monthly sum')
            if r['cty_code'] not in COUNTRIES or r['country']!=COUNTRIES[r['cty_code']]:
                raise ValueError(f'Country-code mismatch at input row {i}')
            if r['hts10'] not in PRODUCTS or r['time'] not in PERIODS:
                raise ValueError(f'Out-of-scope product or date at input row {i}')
            key=(r['time'],r['cty_code'],r['hts10'])
            if key in keys: raise ValueError(f'Duplicate key {key}')
            keys.add(key)
            r['con_val_usd']=decimal_value(r['con_val_usd'],'con_val_usd',i)
            r['calc_dut_usd']=decimal_value(r['calc_dut_usd'],'calc_dut_usd',i)
            if r['con_val_usd']==0:
                raise ValueError(f'Zero denominator at input row {i}; no rate is imputed')
            rows.append(r)
    expected={(t,c,p) for t in PERIODS for c in COUNTRIES for p in PRODUCTS}
    if keys!=expected:
        raise ValueError(f'Incomplete comparison. Missing keys: {sorted(expected-keys)}')
    return rows

def write_csv(path,fields,rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def analyze(path: Path, output: Path):
    rows=load_rows(path);output.mkdir(parents=True,exist_ok=True)
    lookup={(r['time'],r['cty_code'],r['hts10']):r for r in rows}
    rates=[]
    for t in PERIODS:
        for product in PRODUCTS:
            mexico=lookup[t,'2010',product]
            mx_rate=100*mexico['calc_dut_usd']/mexico['con_val_usd']
            for code,name in COUNTRIES.items():
                r=lookup[t,code,product]
                rate=100*r['calc_dut_usd']/r['con_val_usd']
                rates.append({'period':t,'period_label':f'January–August {t[:4]}','period_basis':BASIS,
                    'hts10':product,'product':PRODUCTS[product],'country':name,
                    'imports_usd':str(r['con_val_usd']),'calculated_duties_usd':str(r['calc_dut_usd']),
                    'duty_intensity_pct':str(rate),'gap_vs_mexico_pp':str(rate-mx_rate)})
    growth=[]
    for product in PRODUCTS:
        old=lookup[PERIODS[0],'2010',product]['con_val_usd']
        new=lookup[PERIODS[1],'2010',product]['con_val_usd']
        growth.append({'hts10':product,'product':PRODUCTS[product],'period_basis':BASIS,
            'imports_2025_usd':str(old),'imports_2026_usd':str(new),
            'change_usd':str(new-old),'change_pct':str(100*(new-old)/old)})
    total_old=sum(Decimal(r['imports_2025_usd']) for r in growth)
    total_new=sum(Decimal(r['imports_2026_usd']) for r in growth)
    country_totals=[]
    for t in PERIODS:
        for code,name in COUNTRIES.items():
            selected=[lookup[t,code,p] for p in PRODUCTS]
            value=sum(r['con_val_usd'] for r in selected)
            duties=sum(r['calc_dut_usd'] for r in selected)
            country_totals.append({'period':t,'period_label':f'January–August {t[:4]}','period_basis':BASIS,
                'country':name,'imports_usd':str(value),
                'calculated_duties_usd':str(duties),'duty_intensity_pct':str(100*duties/value)})
    write_csv(output/'duty_intensity_by_line.csv',list(rates[0]),rates)
    write_csv(output/'mexico_import_growth.csv',list(growth[0]),growth)
    write_csv(output/'weighted_duty_intensity.csv',list(country_totals[0]),country_totals)
    rate_lookup={(r['period'],r['country'],r['hts10']):r for r in rates}
    rate_changes=[]
    for product in PRODUCTS:
        for country in COUNTRIES.values():
            before=rate_lookup['2025-08',country,product]
            after=rate_lookup['2026-08',country,product]
            rate_changes.append({'hts10':product,'product':PRODUCTS[product],
                'country':country,'period_basis':BASIS,
                'duty_intensity_2025_pct':before['duty_intensity_pct'],
                'duty_intensity_2026_pct':after['duty_intensity_pct'],
                'change_pp':str(Decimal(after['duty_intensity_pct'])-Decimal(before['duty_intensity_pct']))})
    write_csv(output/'duty_intensity_changes.csv',list(rate_changes[0]),rate_changes)
    gap_figure(output.parent/'figures'/'gaps_vs_mexico_2026.svg',rates)
    results={
        'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'records':len(rows),'period_basis':'January–August totals reconstructed from archived monthly observations; not revised Census _YR values',
        'products':PRODUCTS,'countries':COUNTRIES,
        'mexico_total_2025_usd':str(total_old),'mexico_total_2026_usd':str(total_new),
        'mexico_change_usd':str(total_new-total_old),
        'mexico_change_pct':str(100*(total_new-total_old)/total_old),
        'rates':rates,'growth':growth,'country_totals':country_totals,'rate_changes':rate_changes,
        'checks':{
            'exact_product_country_period_coverage':True,
            'unique_product_country_period_keys':True,
            'positive_import_value_denominators':True,
            'finite_nonnegative_numeric_inputs':True,
            'all_rows_explicitly_january_august_monthly_sums':True,
            'country_codes_match_country_names':True,
            'aggregate_rates_use_ratio_of_sums':True,
            'monthly_records_revalidated_in_this_run':False,
            'live_census_refresh_performed_in_this_run':False,
        },
        'limits':[
            'Archived monthly vintages can differ from subsequently revised official YTD totals.',
            'Selected product lines, not the universe of electronics or data-center inputs.',
            'Gross nominal imports for consumption, not domestic value added or GDP.',
            'Calculated duty intensity is not a legal tariff schedule or final net revenue.',
            'Contemporaneous comparisons do not identify causal effects of tariffs.',
            'Coverage checks do not independently verify the original statistical source.'
        ]
    }
    (output/'results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf-8')
    print(f'Validated {len(rows)} records; wrote reproducible results to {output}')
    return results

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,default=Path(__file__).parent/'data'/'census_snapshot.csv')
    parser.add_argument('--output',type=Path,default=Path(__file__).parent/'results')
    args=parser.parse_args();analyze(args.input,args.output)
