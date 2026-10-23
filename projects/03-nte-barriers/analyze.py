#!/usr/bin/env python3
"""Reproduce descriptive tables from an independently coded NTE public sample."""
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def write_csv(name, rows, fields):
    with (ROOT / 'results' / name).open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def main():
    path = ROOT / 'data' / 'nte_cheese_sample.csv'
    with path.open(encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f))
    with (ROOT / 'data' / 'taxonomy.csv').open(encoding='utf-8', newline='') as f:
        topics = {r['topic'] for r in csv.DictReader(f)}
    sources = json.loads((ROOT / 'sources.json').read_text())
    source_map = {s['source_id']: s for s in sources['sources']}
    assert len(rows) == 18
    assert len({r['record_id'] for r in rows}) == len(rows), 'Duplicate record'
    keys = [(r['edition_year'], r['issue_id']) for r in rows]
    assert len(set(keys)) == len(keys), 'Duplicate edition–issue key'
    for r in rows:
        assert all(r.values())
        assert r['topic'] in topics
        assert 2024 <= int(r['edition_year']) <= 2026
        s = source_map[r['source_id']]
        assert int(r['edition_year']) == s['edition_year']
        assert r['source_url'] == s['url']
        for p in r['pdf_pages'].split('–'):
            assert 1 <= int(p) <= s['pdf_pages']
        assert r['verification'].startswith('Official PDF')
    (ROOT / 'results').mkdir(exist_ok=True)
    by_topic = []
    for topic in sorted(topics):
        selected = [r for r in rows if r['topic'] == topic]
        by_topic.append({'topic': topic, 'coded_records': len(selected),
                         'distinct_issues': len({r['issue_id'] for r in selected})})
    write_csv('topic_summary.csv', by_topic, ['topic', 'coded_records', 'distinct_issues'])
    annual = []
    for year in range(2024, 2027):
        selected = [r for r in rows if int(r['edition_year']) == year]
        annual.append({'edition_year': year, 'coded_records': len(selected),
                       'selected_chapters': len({r['report_chapter'] for r in selected})})
    write_csv('selected_coverage.csv', annual, ['edition_year', 'coded_records', 'selected_chapters'])
    issues = defaultdict(list)
    for r in rows:
        issues[r['issue_id']].append(int(r['edition_year']))
    continuity = [{'issue_id': k, 'observed_editions': ';'.join(map(str, sorted(v))),
                   'coded_edition_count': len(v)} for k, v in sorted(issues.items())]
    write_csv('issue_continuity.csv', continuity, ['issue_id', 'observed_editions', 'coded_edition_count'])
    timeline = [r for r in rows if r['issue_id'] in ('EU-GI-NAMES', 'CHL-PRIOR-USERS')]
    fields = ['issue_id', 'edition_year', 'source_instrument', 'reported_status', 'printed_pages', 'pdf_pages', 'source_url']
    write_csv('temporal_cases.csv', [{k: r[k] for k in fields} for r in timeline], fields)
    stats = {'records': len(rows), 'distinct_issues': len(issues), 'editions': [2024, 2025, 2026],
             'chapters': sorted({r['report_chapter'] for r in rows}),
             'jurisdictions': sorted({r['jurisdiction'] for r in rows}),
             'topics': len(topics), 'reported_status_counts': dict(sorted(Counter(r['reported_status'] for r in rows).items())),
             'input_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
             'interpretation': 'Purposive coded sample counts, not barrier prevalence, severity, economic cost or legal findings.',
             'validation': 'Passed uniqueness, populated fields, taxonomy, edition and page bounds checks.'}
    (ROOT / 'results' / 'summary.json').write_text(json.dumps(stats, indent=2) + '\n')
    print(json.dumps(stats, indent=2))

if __name__ == '__main__':
    main()
