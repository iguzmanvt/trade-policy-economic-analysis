"""Accounting decomposition of Mexico's dairy product uses. Standard library only.

All validations are explicit exceptions, including when Python runs with -O.
The four CSV tables are written only after every accounting check has passed.
"""
import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from decimal import Decimal as D, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data/official_cells.csv'
OUT = ROOT / 'results'
FIELDS = ['family', 'product_code', 'origin', 'kind', 'target', 'value',
          'file', 'sheet', 'cell', 'label_original']
ORIGINS = ('D', 'M', 'T')
PARTS = ('private_consumption', 'government_consumption', 'fixed_capital',
         'inventories', 'exports', 'discrepancy')
CONTROLS = ('all_published', 'intermediate_published', 'final_published')
SOURCE_FILES = {
    ('MIP', 'D'): 'MIP_19.xlsx', ('MIP', 'M'): 'MIP_38.xlsx',
    ('MIP', 'T'): 'MIP_10.xlsx', ('COU', 'D'): 'COU_177.xlsx',
    ('COU', 'M'): 'COU_184.xlsx', ('COU', 'T'): 'COU_170.xlsx',
}


class ValidationError(ValueError):
    """An input or accounting condition failed; no new results are written."""


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def equal(actual, expected, message):
    require(actual == expected,
            f'{message}: actual={actual}, expected={expected}')


def column_number(letters):
    number = 0
    for letter in letters:
        number = number * 26 + ord(letter) - ord('A') + 1
    return number


def read(path=DATA):
    with path.open(encoding='utf-8', newline='') as stream:
        reader = csv.DictReader(stream)
        require(reader.fieldnames == FIELDS,
                f'Unexpected source schema: {reader.fieldnames!r}')
        rows = list(reader)
    return rows


def validate_rows(raw_rows):
    equal(len(raw_rows), 2557, 'Source cell count')
    rows = []
    keys = set()
    locators = set()
    for number, raw in enumerate(raw_rows, start=2):
        require(set(raw) == set(FIELDS) and all(raw[k] is not None for k in FIELDS),
                f'Malformed CSV row {number}')
        row = dict(raw)
        family, origin, kind, target = (row[k] for k in ('family', 'origin', 'kind', 'target'))
        require((family, origin) in SOURCE_FILES,
                f'Invalid family/origin at row {number}: {family}/{origin}')
        equal(row['product_code'], '311513' if family == 'MIP' else '3115',
              f'Product universe at row {number}')
        equal(row['file'], SOURCE_FILES[family, origin], f'Source file at row {number}')
        equal(row['sheet'], 'Tabulado', f'Source sheet at row {number}')
        require(kind in ('intermediate', 'final', 'control'),
                f'Unknown cell kind at row {number}: {kind!r}')
        key = (family, origin, kind, target)
        require(key not in keys, f'Duplicate source cell key: {key}')
        keys.add(key)
        locator = (row['file'], row['sheet'], row['cell'])
        require(locator not in locators, f'Duplicate source locator: {locator}')
        locators.add(locator)
        match = re.fullmatch(r'([A-Z]+)(\d+)', row['cell'])
        require(match is not None, f'Invalid source cell: {locator}')
        col, source_row = match.group(1), int(match.group(2))
        equal(source_row, 196 if family == 'MIP' else 48, f'Source row at {locator}')
        if kind == 'intermediate':
            require(family == 'MIP', f'Unexpected COU destination cell at {locator}')
            require(re.fullmatch(r'\d{6}', target) is not None,
                    f'Invalid destination code at {locator}: {target!r}')
            require(4 <= column_number(col) <= 837,
                    f'Destination outside D:AFE at {locator}')
            require(row['label_original'].startswith(target + ' - '),
                    f'Destination code/header mismatch at {locator}')
        else:
            if kind == 'control':
                mapping = dict(zip(CONTROLS, ('B', 'C', 'AFF' if family == 'MIP' else 'JG')))
            elif family == 'MIP':
                mapping = dict(zip(PARTS, ('AFG', 'AFH', 'AFI', 'AFJ', 'AFK',
                                          'AFM' if origin == 'T' else 'AFL')))
                if origin == 'T':
                    mapping['imports_net'] = 'AFL'
            else:
                mapping = dict(zip(PARTS, ('JH', 'JI', 'JJ', 'JK', 'JL', 'JM')))
            require(target in mapping, f'Unexpected {kind} target at {locator}: {target!r}')
            equal(col, mapping[target], f'Target/coordinate mismatch at {locator}')
        try:
            row['value'] = D(row['value'])
        except (InvalidOperation, ValueError, TypeError) as error:
            raise ValidationError(f'Invalid numeric value at {locator}: {raw["value"]!r}') from error
        require(row['value'].is_finite(), f'Non-finite value at {locator}')
        rows.append(row)

    for family in ('MIP', 'COU'):
        for origin in ORIGINS:
            expected = {(family, origin, 'control', x) for x in CONTROLS}
            expected |= {(family, origin, 'final', x) for x in PARTS}
            if (family, origin) == ('MIP', 'T'):
                expected.add((family, origin, 'final', 'imports_net'))
            actual = {k for k in keys if k[0:2] == (family, origin) and k[2] != 'intermediate'}
            equal(actual, expected, f'Final/control coverage for {family}/{origin}')

    inter = [r for r in rows if r['kind'] == 'intermediate']
    equal(len(inter), 3 * 834, 'Intermediate cell count')
    destination_sets = {}
    for origin in ORIGINS:
        selected = [r for r in inter if r['origin'] == origin]
        destination_sets[origin] = {r['target'] for r in selected}
        equal(len(destination_sets[origin]), 834, f'Destination coverage for MIP/{origin}')
        equal({column_number(re.match(r'[A-Z]+', r['cell']).group()) for r in selected},
              set(range(4, 838)), f'Destination column coverage for MIP/{origin}')
    equal(destination_sets['M'], destination_sets['D'], 'Imported/domestic destination sets')
    equal(destination_sets['T'], destination_sets['D'], 'Total/domestic destination sets')
    return rows


def group(code):
    if code.startswith('3115'):
        return 'Dairy products'
    if code.startswith(('311', '3121')):
        return 'Other food and beverages'
    if code.startswith(('31', '32', '33')):
        return 'Other manufactures'
    if code.startswith('722'):
        return 'Food and beverage services'
    if code.startswith(('61', '62', '93')):
        return 'Education, health and government services'
    return 'Other products and services'


def build_results(raw_rows):
    """Validate the complete snapshot, then compute tables without writing files."""
    rows = validate_rows(raw_rows)
    cells = {(r['family'], r['origin'], r['target']): r['value']
             for r in rows if r['kind'] != 'intermediate'}
    inter = [r for r in rows if r['kind'] == 'intermediate']
    intermediate = {r['target']: {} for r in inter if r['origin'] == 'D'}
    for row in inter:
        intermediate[row['target']][row['origin']] = row['value']
    for origin in ORIGINS:
        equal(sum(r['value'] for r in inter if r['origin'] == origin),
              cells['MIP', origin, 'intermediate_published'],
              f'MIP/{origin} destination sum')
    for code, values in intermediate.items():
        equal(values['D'] + values['M'], values['T'], f'MIP destination {code}: D+M=T')
    equal(cells['MIP', 'D', 'intermediate_published'] + cells['MIP', 'M', 'intermediate_published'],
          cells['MIP', 'T', 'intermediate_published'], 'MIP intermediate total: D+M=T')

    for family in ('MIP', 'COU'):
        for component in PARTS:
            equal(cells[family, 'D', component] + cells[family, 'M', component],
                  cells[family, 'T', component], f'{family} {component}: D+M=T')
        for origin in ORIGINS:
            component_total = sum(cells[family, origin, component] for component in PARTS)
            if (family, origin) == ('MIP', 'T'):
                component_total += cells['MIP', 'T', 'imports_net']
            equal(component_total, cells[family, origin, 'final_published'],
                  f'{family}/{origin} final component sum')
            equal(cells[family, origin, 'intermediate_published'] + cells[family, origin, 'final_published'],
                  cells[family, origin, 'all_published'], f'{family}/{origin} published use total')
    for target in CONTROLS:
        equal(cells['COU', 'D', target] + cells['COU', 'M', target], cells['COU', 'T', target],
              f'COU {target}: D+M=T')

    final = sum(cells['MIP', origin, 'final_published'] for origin in ('D', 'M'))
    alluses = final + cells['MIP', 'T', 'intermediate_published']
    equal(final, cells['MIP', 'T', 'final_published'] - cells['MIP', 'T', 'imports_net'],
          'MIP gross-final import-netting bridge')
    equal(alluses, cells['MIP', 'T', 'all_published'] - cells['MIP', 'T', 'imports_net'],
          'MIP gross-total import-netting bridge')
    equal(cells['MIP', 'T', 'imports_net'], -cells['MIP', 'M', 'all_published'],
          'MIP negative import entry equals imported-origin total')
    equal(alluses, cells['MIP', 'D', 'all_published'] + cells['MIP', 'M', 'all_published'],
          'MIP gross uses equal D+M (without adding T again)')
    # Signed values are retained; there is no clipping, absolute value or zero fill.
    require(cells['MIP', 'D', 'inventories'] < 0 and cells['MIP', 'T', 'inventories'] < 0,
            'Expected signed negative MIP inventory changes are missing in this snapshot')
    require(cells['COU', 'D', 'inventories'] < 0 and cells['COU', 'T', 'inventories'] < 0,
            'Expected signed negative COU inventory changes are missing in this snapshot')
    for family, origin, target in [(f, o, t) for f in ('MIP', 'COU') for o in ORIGINS
                                   for t in ('intermediate_published', 'all_published')]:
        require(cells[family, origin, target] > 0, f'Nonpositive denominator {family}/{origin}/{target}')
    require(final > 0 and alluses > 0, 'Nonpositive gross-use denominator')

    origin_rows = []
    for origin in ('D', 'M'):
        i = cells['MIP', origin, 'intermediate_published']
        f = cells['MIP', origin, 'final_published']
        a = i + f
        origin_rows.append(dict(origin=origin, intermediate=i, final=f, all_uses=a,
                                intermediate_share_of_origin_pct=100*i/a,
                                origin_share_of_all_uses_pct=100*a/alluses,
                                origin_share_of_intermediate_pct=100*i/cells['MIP', 'T', 'intermediate_published']))
    groups = defaultdict(lambda: defaultdict(D))
    for code, values in intermediate.items():
        for origin, value in values.items():
            groups[group(code)][origin] += value
    for name, values in groups.items():
        require(values['T'] > 0, f'Nonpositive destination-group denominator: {name}')
        equal(values['D'] + values['M'], values['T'], f'Grouped destination {name}: D+M=T')
    for origin in ORIGINS:
        equal(sum(values[origin] for values in groups.values()),
              cells['MIP', origin, 'intermediate_published'], f'Grouped destination sum {origin}')
    grouped = [dict(destination_group=name, domestic=values['D'], imported=values['M'], total=values['T'],
                    share_of_intermediate_pct=100*values['T']/cells['MIP', 'T', 'intermediate_published'],
                    imported_share_within_group_pct=100*values['M']/values['T'])
               for name, values in sorted(groups.items(), key=lambda x: x[1]['T'], reverse=True)]
    outputs = {
        'origin_and_uses.csv': origin_rows,
        'intermediate_destination_groups.csv': grouped,
        'final_uses.csv': [dict(component=c, domestic=cells['MIP', 'D', c], imported=cells['MIP', 'M', c],
                                total=cells['MIP', 'D', c]+cells['MIP', 'M', c],
                                share_of_final_pct=100*(cells['MIP', 'D', c]+cells['MIP', 'M', c])/final)
                           for c in PARTS],
        'universe_comparison.csv': [
            dict(table='MIP', code='311513', axis='homogeneous product groups',
                 intermediate=cells['MIP', 'T', 'intermediate_published'], gross_all_uses=alluses,
                 intermediate_share_pct=100*cells['MIP', 'T', 'intermediate_published']/alluses),
            dict(table='COU', code='3115', axis='buyer industries',
                 intermediate=cells['COU', 'T', 'intermediate_published'], gross_all_uses=cells['COU', 'T', 'all_published'],
                 intermediate_share_pct=100*cells['COU', 'T', 'intermediate_published']/cells['COU', 'T', 'all_published'])
        ],
    }
    summary = {
        'input_rows': len(rows),
        'MIP_product_destinations': 834,
        'MIP_positive_destinations': sum(v['T'] > 0 for v in intermediate.values()),
        'all_uses_million_MXN': alluses,
        'intermediate_million_MXN': cells['MIP', 'T', 'intermediate_published'],
        'final_million_MXN': final,
        'imported_share_intermediate_pct': 100*cells['MIP', 'M', 'intermediate_published']/cells['MIP', 'T', 'intermediate_published'],
        'MIP_inventories_million_MXN': cells['MIP', 'T', 'inventories'],
        'MIP_imports_net_million_MXN': cells['MIP', 'T', 'imports_net'],
        'checks': ('Passed: schema and provenance locators; unique keys; finite values; 834 destinations '
                   'per origin including zeros; MIP destination and grouped sums; D+M=T destination '
                   'and final-component identities; MIP and COU final components and use totals; '
                   'COU origin totals; signed negative inventories; import-netting bridge without double counting'),
        'validation_method': 'Explicit exceptions; active with python -O. No output written before all checks pass.',
    }
    return outputs, summary


def write_outputs(outputs, summary, out=OUT):
    """Stage all files after validation; replace only this script's own outputs."""
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.p04-results-', dir=out.parent) as temporary:
        stage = Path(temporary)
        for name, rows in outputs.items():
            with (stage / name).open('w', encoding='utf-8', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=rows[0])
                writer.writeheader()
                writer.writerows(rows)
        (stage / 'validation.json').write_text(json.dumps(summary, indent=2, default=str) + '\n', encoding='utf-8')
        out.mkdir(parents=True, exist_ok=True)
        for name in [*outputs, 'validation.json']:
            (stage / name).replace(out / name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publication', action='store_true',
                        help='Also rebuild the figure and note; requires the optional publication dependencies.')
    args = parser.parse_args()
    outputs, summary = build_results(read())
    summary = {'input_rows': summary.pop('input_rows'),
               'input_sha256': hashlib.sha256(DATA.read_bytes()).hexdigest(), **summary}
    write_outputs(outputs, summary)
    if args.publication:
        subprocess.run([sys.executable, str(ROOT / 'build_publication.py')], check=True)
    print(json.dumps(summary, default=str, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValidationError, OSError, subprocess.CalledProcessError) as error:
        print(f'Validation failed: {error}', file=sys.stderr)
        sys.exit(1)
