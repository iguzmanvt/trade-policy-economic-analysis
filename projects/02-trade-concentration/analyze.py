#!/usr/bin/env python3
"""Reproduce partner concentration from the included public-statistics extract."""
from pathlib import Path
from collections import defaultdict
from decimal import Decimal, getcontext
import argparse
import csv
import hashlib
import json

getcontext().prec = 40
D = Decimal
ROOT = Path(__file__).resolve().parent


def write_csv(path, rows):
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def make_chart(rows, path):
    """A self-contained vector chart, no third-party plotting dependency."""
    colors = {'M': '#002060', 'X': '#00857d'}
    s = ['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="490" viewBox="0 0 900 490">',
         '<rect width="900" height="490" fill="white"/>',
         '<g font-family="Arial, sans-serif" fill="#172b4d">',
         '<text x="450" y="28" text-anchor="middle" font-size="20">U.S. goods trade: partner concentration and North American exposure</text>',
         '<text x="450" y="52" text-anchor="middle" font-size="13">January–August sums of archived monthly observations, 2023–2026</text>']
    for j, (field, title, ymin, ymax, ticks) in enumerate([
            ('hhi', 'Partner HHI (0–10,000 scale)', 600, 800, [600,650,700,750,800]),
            ('canada_mexico_share_pct', 'Canada + Mexico share (%)', 24, 36, [24,27,30,33,36])]):
        left = 75 + j * 440
        right = left + 335
        top, bottom = 108, 365
        s += [f'<text x="{(left+right)/2}" y="88" text-anchor="middle" font-size="16">{title}</text>',
              f'<path d="M{left} {top}V{bottom}H{right}" fill="none" stroke="#172b4d"/>']
        for t in ticks:
            y = bottom - (t-ymin)/(ymax-ymin)*(bottom-top)
            s.append(f'<text x="{left-10}" y="{y+4:.2f}" text-anchor="end" font-size="12">{t}</text>')
        for flow in ['M','X']:
            part = [r for r in rows if r['flow']==flow]
            pts = []
            for i, r in enumerate(part):
                x = left + i*(right-left)/3
                y = bottom-(float(r[field])-ymin)/(ymax-ymin)*(bottom-top)
                pts.append(f'{x:.2f},{y:.2f}')
                if i==3:
                    s.append(f'<text x="{x-3}" y="{y-8:.2f}" text-anchor="end" fill="{colors[flow]}" font-size="12">{float(r[field]):.1f}</text>')
            s.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{colors[flow]}" stroke-width="3"/>')
        for i, year in enumerate(range(2023,2027)):
            x = left+i*(right-left)/3
            s.append(f'<text x="{x}" y="388" text-anchor="middle" font-size="12">{year}</text>')
    s += ['<path d="M260 417H292" stroke="#002060" stroke-width="3"/><text x="302" y="421" font-size="13">General imports</text>',
          '<path d="M470 417H502" stroke="#00857d" stroke-width="3"/><text x="512" y="421" font-size="13">Total exports</text>',
          '<text x="450" y="452" text-anchor="middle" font-size="12">Source: archived U.S. Census statistics; author’s calculations. The vertical axes are truncated.</text>',
          '<text x="450" y="474" text-anchor="middle" font-size="12">HHI squares each individual partner share before summing; Canada and Mexico are pooled only in the share panel.</text>', '</g></svg>']
    path.write_text('\n'.join(s)+'\n', encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=Path, default=ROOT/'data/partner_values.csv')
    ap.add_argument('--output', type=Path, default=ROOT/'results')
    args = ap.parse_args()
    with args.input.open(encoding='utf-8-sig') as f:
        raw = list(csv.DictReader(f))
    groups, seen = defaultdict(list), set()
    for r in raw:
        key = (r['flow'],r['period'],r['country_code'])
        assert key not in seen, ('Duplicate key', key)
        seen.add(key)
        assert r['flow'] in ['M','X']
        assert r['period'] in [f'{y}-01_08' for y in range(2023,2027)]
        assert len(r['country_code'])==4 and r['country_code'].isdigit()
        assert 1000 <= int(r['country_code']) <= 7999
        assert r['iso3'] not in ['WLD','WORLD','EU','EUN']
        r['value'] = D(r['value_usd'])
        assert r['value'].is_finite() and r['value']>=0
        assert r['value']==int(r['value'])
        groups[r['flow'],r['period']].append(r)
    assert len(groups)==8
    summary, shares = [], []
    for (flow, period), rows in sorted(groups.items()):
        total = sum(r['value'] for r in rows)
        assert total>0
        part = []
        for r in rows:
            share = r['value']/total
            part.append(dict(flow=flow,period=period,country_code=r['country_code'],
                             country_name=r['country_name'],iso3=r['iso3'],value_usd=r['value'],
                             share_pct=share*100,hhi_component=share*share*10000))
        bycode = {r['country_code']:r for r in part}
        assert '1220' in bycode and '2010' in bycode
        hhi = sum(r['hhi_component'] for r in part)
        assert 0<=hhi<=10000 and abs(sum(r['share_pct'] for r in part)-100)<D('1e-30')
        top5 = sorted(part,key=lambda x:x['value_usd'],reverse=True)[:5]
        summary.append(dict(flow=flow,period=period,total_value_usd=total,hhi=hhi,
                            effective_equal_partners=10000/hhi,
                            positive_partners=sum(r['value']>0 for r in rows),
                            canada_share_pct=bycode['1220']['share_pct'],
                            mexico_share_pct=bycode['2010']['share_pct'],
                            canada_mexico_share_pct=bycode['1220']['share_pct']+bycode['2010']['share_pct'],
                            top_five_share_pct=sum(r['share_pct'] for r in top5)))
        shares.extend(sorted(part,key=lambda x:x['value_usd'],reverse=True))
    contributions = []
    for flow in ['M','X']:
        before={r['country_code']:r for r in shares if r['flow']==flow and r['period']=='2025-01_08'}
        after={r['country_code']:r for r in shares if r['flow']==flow and r['period']=='2026-01_08'}
        total_change=sum(r['value_usd'] for r in after.values())-sum(r['value_usd'] for r in before.values())
        assert total_change!=0
        for c in sorted(before.keys()|after.keys()):
            b=before.get(c,{}).get('value_usd',D(0)); a=after.get(c,{}).get('value_usd',D(0))
            desc=after.get(c,before.get(c))
            contributions.append(dict(flow=flow,country_code=c,country_name=desc['country_name'],
                                      value_2025_usd=b,value_2026_usd=a,change_usd=a-b,
                                      contribution_pct_of_net_change=100*(a-b)/total_change))
        assert abs(sum(r['contribution_pct_of_net_change'] for r in contributions if r['flow']==flow)-100)<D('1e-30')
    args.output.mkdir(parents=True,exist_ok=True)
    write_csv(args.output/'concentration_summary.csv',summary)
    write_csv(args.output/'partner_shares.csv',shares)
    write_csv(args.output/'growth_contributions_2025_2026.csv',contributions)
    make_chart(summary,args.output/'concentration_exposure.svg')
    check=dict(input_sha256=hashlib.sha256(args.input.read_bytes()).hexdigest(),rows=len(raw),
               unique_keys=len(seen),groups=len(groups),nonnegative_values=True,
               shares_sum_to_100=True,hhi_individual_partners=True,
               growth_contributions_sum_to_100=True,basis='JAN_AUG_ARCHIVED_MONTHLY_SUM')
    (args.output/'validation.json').write_text(json.dumps(check,indent=2)+'\n')
    print(f'Validated {len(raw)} partner-flow-period rows; reproduced 8 concentration summaries.')


if __name__=='__main__':
    main()
