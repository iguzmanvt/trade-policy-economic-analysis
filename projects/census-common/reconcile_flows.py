"""Show why the two Census statistical layers must not be merged.

Run with Python 3.11+ and the standard library. This creates a descriptive
bridge, not a test that general imports equal imports for consumption.
"""
from pathlib import Path
from collections import defaultdict
import csv


def main():
    here = Path(__file__).resolve().parent
    p01 = here.parent / '01-observed-duty-intensity/data/census_snapshot.csv'
    p02 = here.parent / '02-trade-concentration/product-basket/data/general_imports_monthly.csv'
    consumption = {}
    with p01.open(encoding='utf-8-sig', newline='') as stream:
        for row in csv.DictReader(stream):
            if row['cty_code'] == '2010':
                assert row['basis'] == 'JAN_AUG_MONTHLY_SUM'
                key = (row['time'][:4], row['hts10'])
                assert key not in consumption
                consumption[key] = int(row['con_val_usd'])
    general = defaultdict(int)
    periods = defaultdict(set)
    with p02.open(encoding='utf-8-sig', newline='') as stream:
        for row in csv.DictReader(stream):
            key = (row['period'][:4], row['hts10'])
            if key in consumption:
                assert row['flow'] == 'general_imports'
                assert row['country_code'] == '2010'
                assert row['statistical_basis'] == 'ARCHIVED_MONTHLY'
                assert row['period'] not in periods[key]
                periods[key].add(row['period'])
                general[key] += int(row['general_imports_usd'])
    assert len(consumption) == 6 and set(consumption) == set(general)
    rows = []
    for (year, hts10), value in sorted(consumption.items()):
        assert periods[year, hts10] == {f'{year}-{m:02d}' for m in range(1, 9)}
        rows.append(dict(year=year, period='January-August', origin='Mexico',
                         hts10=hts10, imports_for_consumption_usd=value,
                         general_imports_usd=general[year, hts10],
                         general_minus_consumption_usd=general[year, hts10]-value))
    output = here / 'results/flow_comparison.csv'
    output.parent.mkdir(exist_ok=True)
    with output.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print('Wrote six flow comparisons. Differences are not reconciliation errors.')


if __name__ == '__main__':
    main()
