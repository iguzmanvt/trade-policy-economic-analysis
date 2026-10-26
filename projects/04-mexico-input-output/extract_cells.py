"""Extract the exact public snapshot from six unmodified INEGI 2018 workbooks.

The pinned data/workbook_provenance.json is read before any workbook is opened.
A missing or unexpected binary rejects the run without changing the snapshot.
This is exact-snapshot reproduction, not an automatic source-revision tool.
Python's standard library is sufficient, including under python -O.
"""
import argparse
import csv
import hashlib
import json
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from analyze import ValidationError, build_results, equal, read, require

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
ROOT = Path(__file__).resolve().parent
REGISTRY = ROOT / 'data/workbook_provenance.json'
FILES = {
    'MIP_19.xlsx': ('MIP', 'D', 196), 'MIP_38.xlsx': ('MIP', 'M', 196),
    'MIP_10.xlsx': ('MIP', 'T', 196), 'COU_177.xlsx': ('COU', 'D', 48),
    'COU_184.xlsx': ('COU', 'M', 48), 'COU_170.xlsx': ('COU', 'T', 48),
}


def preflight(source):
    """Compare all six files before parsing or creating output files."""
    registry_bytes = REGISTRY.read_bytes()
    records = json.loads(registry_bytes)
    require(isinstance(records, list), 'Pinned provenance must be a list')
    require(all(isinstance(r, dict) and 'file' in r for r in records),
            'Malformed pinned provenance record')
    equal(len(records), len(FILES), 'Pinned workbook count')
    equal({r['file'] for r in records}, set(FILES), 'Pinned workbook names')
    registry = {r['file']: r for r in records}
    problems = []
    hashes = {}
    for name in FILES:
        expected = registry[name].get('sha256', '')
        require(re.fullmatch(r'[0-9a-f]{64}', expected) is not None,
                f'Invalid pinned SHA256 for {name}')
        path = source / name
        if not path.is_file():
            problems.append(f'Missing workbook: {name}')
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        hashes[name] = digest
        if digest != expected:
            problems.append(f'SHA256 mismatch for {name}: expected={expected}, actual={digest}')
    require(not problems,
            'Workbook preflight rejected; existing snapshot and provenance are unchanged. '
            + '; '.join(problems))
    return registry, registry_bytes, hashes


def workbook(path, sheet_number=1):
    with ZipFile(path) as archive:
        strings = []
        if 'xl/sharedStrings.xml' in archive.namelist():
            for string in ET.fromstring(archive.read('xl/sharedStrings.xml')).findall('m:si', NS):
                strings.append(''.join(string.itertext()))
        result = {}
        xml = archive.read(f'xl/worksheets/sheet{sheet_number}.xml')
        for cell in ET.fromstring(xml).findall('.//m:c', NS):
            value = cell.find('m:v', NS)
            if value is not None:
                result[cell.attrib['r']] = strings[int(value.text)] if cell.attrib.get('t') == 's' else value.text
            elif cell.attrib.get('t') == 'inlineStr':
                result[cell.attrib['r']] = ''.join(cell.find('m:is', NS).itertext())
        return result


def extract(source, out):
    registry, registry_bytes, hashes = preflight(source)
    rows = []
    for name, (family, origin, source_row) in FILES.items():
        path = source / name
        cells, metadata = workbook(path), workbook(path, 2)
        record = registry[name]
        equal(metadata.get('C12'), str(record['reference_year']), f'{name} reference year')
        equal(metadata.get('C14'), record['metadata_update'], f'{name} metadata update')
        equal(cells.get('A3'), record['table_title'], f'{name} table title')
        equal(source_row, record['source_row'], f'{name} pinned source row')
        code = '311513' if family == 'MIP' else '3115'
        label = cells.get('A' + str(source_row), '').strip()
        require(re.match(r'^' + code + r'(?:\s|$)', label) is not None,
                f'{name} source row does not identify {code}: {label!r}')
        selected = []
        if family == 'MIP':
            for address in cells:
                if re.fullmatch(r'[A-Z]+196', address):
                    column = address[:-3]
                    header = cells.get(column + '6', '')
                    if re.match(r'^\d{6} - ', header):
                        selected.append((column, 'intermediate', header.split(' - ', 1)[0], header))
            finals = ['AFG', 'AFH', 'AFI', 'AFJ', 'AFK', 'AFL'] + (['AFM'] if origin == 'T' else [])
            selected += [('B', 'control', 'all_published', 'Published total'),
                         ('C', 'control', 'intermediate_published', 'Intermediate total'),
                         ('AFF', 'control', 'final_published', 'Published final total')]
        else:
            finals = ['JH', 'JI', 'JJ', 'JK', 'JL', 'JM']
            selected += [('B', 'control', 'all_published', 'Published total'),
                         ('C', 'control', 'intermediate_published', 'Intermediate total'),
                         ('JG', 'control', 'final_published', 'Published final total')]
        for column in finals:
            header = cells.get(column + '6', '')
            key = {
                'AFG': 'private_consumption', 'AFH': 'government_consumption',
                'AFI': 'fixed_capital', 'AFJ': 'inventories', 'AFK': 'exports',
                'AFL': 'imports_net' if origin == 'T' else 'discrepancy', 'AFM': 'discrepancy',
                'JH': 'private_consumption', 'JI': 'government_consumption', 'JJ': 'fixed_capital',
                'JK': 'inventories', 'JL': 'exports', 'JM': 'discrepancy',
            }[column]
            selected.append((column, 'final', key, header))
        for column, kind, target, original_label in selected:
            address = column + str(source_row)
            require(address in cells, f'Missing cell {name}:{address}')
            rows.append({'family': family, 'product_code': code, 'origin': origin,
                         'kind': kind, 'target': target, 'value': cells[address],
                         'file': name, 'sheet': 'Tabulado', 'cell': address,
                         'label_original': original_label})

    # All structural and accounting checks run before the output directory changes.
    build_results(rows)
    # Protect against a source being replaced while it was parsed.
    for name, digest in hashes.items():
        equal(hashlib.sha256((source / name).read_bytes()).hexdigest(), digest,
              f'{name} changed during extraction')
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.p04-extract-', dir=out.parent) as temporary:
        stage = Path(temporary)
        snapshot = stage / 'official_cells.csv'
        with snapshot.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=rows[0])
            writer.writeheader()
            writer.writerows(rows)
        # Re-read the serialized form; the analyzer's checks must also pass on disk.
        build_results(read(snapshot))
        (stage / 'workbook_provenance.json').write_bytes(registry_bytes)
        out.mkdir(parents=True, exist_ok=True)
        snapshot.replace(out / 'official_cells.csv')
        # Preserve the historical registry byte-for-byte. No new retrieval date is invented.
        (stage / 'workbook_provenance.json').replace(out / 'workbook_provenance.json')
    print(f'Passed: six pinned workbook hashes and metadata; extracted and validated {len(rows)} cells. '
          'Historical provenance preserved unchanged.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_directory', type=Path)
    parser.add_argument('--output', type=Path, default=ROOT / 'data')
    args = parser.parse_args()
    try:
        extract(args.source_directory, args.output)
    except (ValidationError, OSError, ValueError, BadZipFile, ET.ParseError, KeyError, IndexError) as error:
        print(f'Extraction failed: {error}', file=sys.stderr)
        sys.exit(1)
