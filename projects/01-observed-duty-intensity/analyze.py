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

PRODUCTS = {
    '8471500150': 'Processing units',
    '8471709000': 'Storage units',
    '8517620020': 'Switching and routing apparatus',
}
COUNTRIES = {'2010':'Mexico','5700':'China','5830':'Taiwan','5520':'Vietnam','5570':'Malaysia'}
PERIODS = ['2025-08','2026-08']
BASIS = 'JAN_AUG_MONTHLY_SUM'
REQUIRED = ['time','basis','cty_code','country','hts10','con_val_usd','calc_dut_usd']

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
    results={
        'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'records':len(rows),'period_basis':'January–August totals reconstructed from archived monthly observations; not revised Census _YR values',
        'products':PRODUCTS,'countries':COUNTRIES,
        'mexico_total_2025_usd':str(total_old),'mexico_total_2026_usd':str(total_new),
        'mexico_change_usd':str(total_new-total_old),
        'mexico_change_pct':str(100*(total_new-total_old)/total_old),
        'rates':rates,'growth':growth,'country_totals':country_totals,
        'checks':{
            'exact_product_country_period_coverage':True,
            'unique_product_country_period_keys':True,
            'positive_import_value_denominators':True,
            'finite_nonnegative_numeric_inputs':True,
            'all_rows_explicitly_january_august_monthly_sums':True,
            'country_codes_match_country_names':True,
            'aggregate_rates_use_ratio_of_sums':True,
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
