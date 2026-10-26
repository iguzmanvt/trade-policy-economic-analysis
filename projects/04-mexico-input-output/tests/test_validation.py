"""Focused, isolated P04 acceptance tests. Standard library only.

Run: python tests/test_validation.py [--source-directory /path/to/six/workbooks]
Both ordinary and optimized Python subprocesses are always exercised.
The optional official sources enable exact extraction and a one-byte mutation test.
No project inputs or outputs are changed; every subprocess runs in a temporary copy.
"""
import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLES = ('origin_and_uses.csv', 'intermediate_destination_groups.csv',
          'final_uses.csv', 'universe_comparison.csv')
RECORDS = []


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_state(directory):
    return {str(p.relative_to(directory)): digest(p) for p in sorted(directory.rglob('*')) if p.is_file()}


def copied_project(path):
    path.mkdir()
    for filename in ('analyze.py', 'extract_cells.py'):
        shutil.copy2(ROOT / filename, path / filename)
    shutil.copytree(ROOT / 'data', path / 'data')
    shutil.copytree(ROOT / 'results', path / 'results')
    return path


def mutate_csv(project, case):
    path = project / 'data/official_cells.csv'
    with path.open(encoding='utf-8', newline='') as stream:
        reader = csv.DictReader(stream)
        fields, rows = reader.fieldnames, list(reader)
    if case == 'inconsistent_intermediate':
        for row in rows:
            if (row['family'], row['origin'], row['kind']) == ('MIP', 'D', 'intermediate') and row['value'] != '0':
                row['value'] = '999999'
                break
    elif case == 'late_cou_failure':
        for row in rows:
            if (row['family'], row['origin'], row['target']) == ('COU', 'T', 'all_published'):
                row['value'] = '251871.392'
                break
    elif case == 'missing_destination':
        rows.pop(0)
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def execute(project, mode, script, arguments=()):
    command = [sys.executable] + (['-O'] if mode == 'optimized' else []) + [str(project / script), *map(str, arguments)]
    process = subprocess.run(command, capture_output=True, text=True, timeout=180)
    return command, process


def record(case, mode, command, process, details):
    RECORDS.append({'case': case, 'mode': mode, 'command': command,
                    'exit_code': process.returncode, 'passed': True,
                    'details': details, 'stdout': process.stdout, 'stderr': process.stderr})


def run(source_directory=None):
    with tempfile.TemporaryDirectory(prefix='p04-tests-') as directory:
        work = Path(directory)
        names = [r['file'] for r in json.loads((ROOT / 'data/workbook_provenance.json').read_text())]
        bad_source = work / 'mismatched_workbooks'
        bad_source.mkdir()
        if source_directory:
            for name in names:
                shutil.copy2(source_directory / name, bad_source / name)
            # Appending one byte leaves the original files untouched and forces a SHA256 mismatch.
            with (bad_source / 'MIP_19.xlsx').open('ab') as stream:
                stream.write(b'!')
            mismatch_description = 'Only MIP_19.xlsx differs from the official input (one appended byte).'
        else:
            for name in names:
                (bad_source / name).write_bytes(b'Invalid test fixture; not an official workbook.\n')
            mismatch_description = 'Six deliberately invalid byte fixtures; no claim of official-source extraction.'
        for mode in ('normal', 'optimized'):
            for case in ('valid_analysis', 'inconsistent_intermediate', 'late_cou_failure', 'missing_destination'):
                project = copied_project(work / f'{case}-{mode}')
                before = file_state(project / 'results')
                if case != 'valid_analysis':
                    mutate_csv(project, case)
                command, process = execute(project, mode, 'analyze.py')
                if case == 'valid_analysis':
                    require(process.returncode == 0, f'{case}/{mode}: {process.stderr}')
                    require('Passed:' in process.stdout, f'{case}/{mode}: missing successful check result')
                    require(all(digest(project / 'results' / name) == before[name] for name in TABLES),
                            f'{case}/{mode}: a published table changed')
                    details = 'Valid snapshot reproduced; all four CSV tables are byte-identical.'
                else:
                    expected = {'inconsistent_intermediate': 'MIP/D destination sum',
                                'late_cou_failure': 'COU/T published use total',
                                'missing_destination': 'Source cell count'}[case]
                    require(process.returncode != 0 and expected in process.stderr,
                            f'{case}/{mode}: wrong rejection: {process.stdout} {process.stderr}')
                    require('Passed:' not in process.stdout, f'{case}/{mode}: premature success')
                    require(file_state(project / 'results') == before, f'{case}/{mode}: existing results changed')
                    details = f'Rejected with {expected!r}; all pre-existing results preserved byte-for-byte.'
                record(case, mode, command, process, details)
            project = copied_project(work / f'workbook_hash_mismatch-{mode}')
            before = file_state(project / 'data')
            command, process = execute(project, mode, 'extract_cells.py', [bad_source, '--output', project / 'data'])
            require(process.returncode != 0 and 'SHA256 mismatch for MIP_19.xlsx' in process.stderr,
                    f'hash mismatch/{mode}: wrong rejection: {process.stdout} {process.stderr}')
            require('Passed:' not in process.stdout, f'hash mismatch/{mode}: premature success')
            require(file_state(project / 'data') == before, f'hash mismatch/{mode}: snapshot/provenance changed')
            record('workbook_hash_mismatch', mode, command, process,
                   mismatch_description + ' Rejected before extraction; all data/provenance files unchanged.')
            if source_directory:
                project = copied_project(work / f'valid_official_extraction-{mode}')
                command, process = execute(project, mode, 'extract_cells.py', [source_directory, '--output', project / 'reextracted'])
                require(process.returncode == 0 and 'Passed:' in process.stdout,
                        f'extraction/{mode}: {process.stdout} {process.stderr}')
                require(all(digest(project / 'reextracted' / name) == digest(ROOT / 'data' / name)
                            for name in ('official_cells.csv', 'workbook_provenance.json')),
                        f'extraction/{mode}: exact snapshot/provenance mismatch')
                record('valid_official_extraction', mode, command, process,
                       'All six pinned official hashes matched; 2,557 cells and historical provenance reproduced byte-for-byte.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-directory', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    run(args.source_directory.resolve() if args.source_directory else None)
    report = {'executed_at_utc': datetime.now(timezone.utc).isoformat(),
              'python_version': sys.version, 'case_count': len(RECORDS),
              'all_passed': True, 'official_sources_supplied': args.source_directory is not None,
              'tests': RECORDS}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'Passed: {len(RECORDS)} isolated subprocess cases, including normal and python -O modes.')
    if not args.source_directory:
        print('Exact official extraction was not run; provide --source-directory to test it.')


if __name__ == '__main__':
    main()
