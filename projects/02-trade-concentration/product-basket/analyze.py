"""Reproduce P02 from the bundled archived monthly general-imports panel.

Python 3.9+; standard library only. No network requests or silent data updates.
"""
from collections import Counter, defaultdict
from decimal import Decimal, getcontext
from pathlib import Path
from html import escape
import csv
import hashlib
import json

getcontext().prec = 36
ROOT = Path(__file__).resolve().parent
YEARS = ('2025', '2026')
LEADERS = ('8471500150', '8471709000', '8517620020')
LABELS = {'8471500150': 'Processing units', '8471709000': 'Storage units',
          '8517620020': 'Switching and routing', 'REST': 'All other selected lines'}

def read_csv(path):
    with path.open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))

def write_csv(name, rows):
    with (ROOT / 'results' / name).open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)

def percentage(value, denominator):
    return Decimal(value) / Decimal(denominator) * 100 if denominator else None

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    (ROOT / 'results').mkdir(exist_ok=True)
    (ROOT / 'figures').mkdir(exist_ok=True)
    checks = []
    def check(name, passed, detail):
        checks.append({'check': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise ValueError(f'{name}: {detail}')
    rows = read_csv(ROOT / 'data/general_imports_monthly.csv')
    basket = read_csv(ROOT / 'data/basket_hts10.csv')
    source = json.loads((ROOT / 'sources.json').read_text())
    basket_lookup = {row['hts10']: row for row in basket}
    check('input_hash', sha(ROOT / source['public_panel_file']) == source['public_panel_sha256'], source['public_panel_sha256'])
    check('basket_hash', sha(ROOT / source['public_basket_file']) == source['public_basket_sha256'], source['public_basket_sha256'])
    check('basket_unique', len(basket_lookup) == len(basket) == 374, '374 unique historical HTS10 codes')
    check('monthly_unique', len({(r['period'], r['hts10'], r['partner_iso3']) for r in rows}) == len(rows), len(rows))
    periods = {f'{year}-{month:02d}' for year in YEARS for month in range(1, 9)}
    check('periods', {r['period'] for r in rows} == periods, '16 distinct month periods; unequal sparse row counts retained')
    check('scope', all(r['flow'] == 'general_imports' and r['partner_iso3'] == 'MEX' and r['country_code'] == '2010' and r['statistical_basis'] == 'ARCHIVED_MONTHLY' for r in rows), 'United States reporter; Mexico partner; general imports')
    check('membership', all(r['hts10'] in basket_lookup and r['hs6'] == r['hts10'][:6] == basket_lookup[r['hts10']]['hs6'] for r in rows), 'Exact published basket membership')
    check('values', all(r['general_imports_usd'] != '' and int(r['general_imports_usd']) >= 0 for r in rows), 'Integer nominal dollars; no null amount in reported rows')
    values = defaultdict(int)
    hs6_values = defaultdict(int)
    month_values = defaultdict(int)
    counts = Counter()
    for row in rows:
        year, code, hs6 = row['period'][:4], row['hts10'], row['hs6']
        value = int(row['general_imports_usd'])
        values[year, code] += value
        hs6_values[year, hs6] += value
        month_values[row['period']] += value
        counts[year, code] += 1
    totals = {year: sum(value for (y, _), value in values.items() if y == year) for year in YEARS}
    codes = sorted({code for _, code in values})
    families = sorted({row['hs6'] for row in basket})
    check('hs6_coverage', all({code for (y, code) in hs6_values if y == year} == set(families) for year in YEARS), 'All 88 selected HS6 observed in each January-August window')
    summary = {'reporter': 'United States', 'partner': 'Mexico', 'flow': 'general_imports',
               'period': 'January-August of 2025 and 2026', 'basis': 'ARCHIVED_MONTHLY_SUM',
               'monthly_rows': len(rows), 'basket_historical_hts10': len(basket), 'basket_hs6': len(families),
               'observed_hts10_union': len(codes), 'totals_usd': totals,
               'change_usd': totals['2026'] - totals['2025'],
               'growth_percent': str(percentage(totals['2026'] - totals['2025'], totals['2025']))}
    hhi_rows = []
    for year in YEARS:
        total = totals[year]
        selected_hs6 = [hs6_values[year, code] for code in families]
        hhi = sum((Decimal(value) / total * 100) ** 2 for value in selected_hs6)
        hhi_rows.append({'year': year, 'dimension': 'selected_HTS10_aggregated_to_HS6', 'observed_groups': len(families),
                         'denominator_usd': total, 'hhi_0_10000': str(hhi),
                         'effective_equal_sized_groups': str(Decimal(10000) / hhi)})
    contributions = []
    for code in (*LEADERS, 'REST'):
        period_values = {year: values[year, code] if code != 'REST' else totals[year] - sum(values[year, leader] for leader in LEADERS) for year in YEARS}
        change = period_values['2026'] - period_values['2025']
        contributions.append({'hts10_or_group': code, 'label': LABELS[code],
                              'value_2025_usd': period_values['2025'], 'value_2026_usd': period_values['2026'],
                              'change_usd': change, 'share_2025_percent': str(percentage(period_values['2025'], totals['2025'])),
                              'share_2026_percent': str(percentage(period_values['2026'], totals['2026'])),
                              'contribution_to_net_change_percent': str(percentage(change, summary['change_usd'])),
                              'contribution_to_growth_percentage_points': str(percentage(change, totals['2025']))})
    check('contributions_add', sum(r['change_usd'] for r in contributions) == summary['change_usd'], summary['change_usd'])
    check('composition_add', all(sum(r[f'value_{year}_usd'] for r in contributions) == totals[year] for year in YEARS), 'Exact dollar reconciliation in both periods')
    check('hhi_bounds', all(Decimal(10000) / len(families) <= Decimal(r['hhi_0_10000']) <= 10000 for r in hhi_rows), 'HHI scale 0-10,000; 88 selected HS6')
    hts_rows = []
    for code in codes:
        # Missing period records remain blank. Their absence is not a measured zero.
        before = values.get(('2025', code))
        after = values.get(('2026', code))
        change = sum(int(r['general_imports_usd']) for r in rows if r['hts10'] == code and r['period'].startswith('2026')) - sum(int(r['general_imports_usd']) for r in rows if r['hts10'] == code and r['period'].startswith('2025'))
        hts_rows.append({'hts10': code, 'hs6': code[:6],
                         'value_2025_usd': '' if before is None else before,
                         'value_2026_usd': '' if after is None else after,
                         'reported_months_2025': counts['2025', code], 'reported_months_2026': counts['2026', code],
                         'reported_sum_change_usd': change,
                         'availability': 'BOTH_PERIODS' if before is not None and after is not None else 'ONE_PERIOD_ONLY_NO_ZERO_IMPUTATION'})
    hs6_rows = []
    for code in families:
        a, b = hs6_values['2025', code], hs6_values['2026', code]
        hs6_rows.append({'hs6': code, 'value_2025_usd': a, 'value_2026_usd': b, 'change_usd': b-a,
                         'share_2025_percent': str(percentage(a, totals['2025'])),
                         'share_2026_percent': str(percentage(b, totals['2026'])),
                         'contribution_to_net_change_percent': str(percentage(b-a, summary['change_usd']))})
    for year in YEARS:
        check('hts_hs6_reconcile_'+year, sum(r[f'value_{year}_usd'] for r in hs6_rows) == totals[year], totals[year])
    summary['hhi_hs6'] = {r['year']: r['hhi_0_10000'] for r in hhi_rows}
    summary['three_leading_lines_contribution_percent'] = str(sum(Decimal(r['contribution_to_net_change_percent']) for r in contributions[:3]))
    summary['observed_hts10_by_year'] = {year: len({code for y, code in values if y == year}) for year in YEARS}
    write_csv('contributions.csv', contributions)
    write_csv('composition_hs6.csv', hs6_rows)
    write_csv('reported_hts10_sums.csv', hts_rows)
    write_csv('concentration.csv', hhi_rows)
    write_csv('monthly_totals.csv', [{'period': p, 'general_imports_usd': month_values[p]} for p in sorted(periods)])
    (ROOT / 'results/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    (ROOT / 'results/checks.json').write_text(json.dumps(checks, indent=2) + '\n')
    draw_contributions(contributions, summary)
    print(json.dumps(summary, indent=2))

def draw_contributions(rows, summary):
    # A deterministic self-contained SVG; all values come from the actual results.
    width, height = 1120, 600
    xzero, xend = 300, 1000
    largest = max(abs(r['change_usd']) for r in rows) / 1e9
    scale = (xend - xzero) / (largest * 1.12)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
           '<rect width="1120" height="600" fill="white"/>',
           '<g font-family="Arial, sans-serif" fill="#172b4d">',
           f'<text x="40" y="45" font-size="25" font-weight="bold">Three lines account for {float(summary["three_leading_lines_contribution_percent"]):.1f}% of the increase</text>',
           '<text x="40" y="77" font-size="17">U.S. general imports from Mexico in a fixed HTS10 basket, grouped into 88 HS6 categories</text>',
           '<text x="40" y="104" font-size="16">Change: January-August 2026 minus January-August 2025; billions of nominal U.S. dollars</text>']
    for i, row in enumerate(rows):
        y = 165 + i * 79
        value = row['change_usd'] / 1e9
        bar = abs(value) * scale
        color = '#002060' if row['hts10_or_group'] != 'REST' else '#608aa7'
        x = xzero if value >= 0 else xzero - bar
        label = f"{row['label']}"
        svg += [f'<text x="40" y="{y+19}" font-size="18">{escape(label)}</text>',
                f'<rect x="{x:.2f}" y="{y}" width="{bar:.2f}" height="30" fill="{color}"/>',
                f'<text x="{x+bar+9:.2f}" y="{y+21}" font-size="18" font-weight="bold">{value:+.3f}</text>',
                f'<text x="40" y="{y+41}" font-size="12" fill="#526277">{escape(row["hts10_or_group"])}</text>']
    svg += [f'<line x1="{xzero}" y1="145" x2="{xzero}" y2="465" stroke="#6a7a8f"/>',
            f'<text x="40" y="512" font-size="18" font-weight="bold">Total increase: +{summary["change_usd"]/1e9:.3f} billion dollars ({float(summary["growth_percent"]):.1f}%)</text>',
            '<text x="40" y="547" font-size="14">Source: U.S. Census Bureau archived monthly records; author calculations. Recovered archive; no fresh API verification.</text>',
            '<text x="40" y="570" font-size="14">The basket is selected and retrospective. Gross values do not identify final use, domestic value added or causality.</text>', '</g></svg>']
    (ROOT / 'figures/contributions.svg').write_text('\n'.join(svg) + '\n')

if __name__ == '__main__':
    main()
