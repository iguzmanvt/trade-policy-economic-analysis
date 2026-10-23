#!/usr/bin/env python3
"""Optional upstream verification: download official PDFs and check coded-page anchors."""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from urllib.request import urlopen
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent

def normalized(text):
    return re.sub(r'\s+', ' ', text).casefold()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-dir', required=True, type=Path,
                        help='Directory for official PDFs, kept outside the release package')
    parser.add_argument('--download', action='store_true', help='Download missing official PDFs')
    args = parser.parse_args()
    args.source_dir.mkdir(parents=True, exist_ok=True)
    sources = json.loads((ROOT / 'sources.json').read_text())['sources']
    readers = {}
    source_checks = []
    for s in sources:
        path = args.source_dir / f"NTE{s['edition_year']}.pdf"
        if not path.exists():
            if not args.download:
                raise FileNotFoundError(f'{path.name}: use --download to obtain official source')
            with urlopen(s['url'], timeout=60) as response:
                path.write_bytes(response.read())
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == s['sha256'], f"Changed source bytes: {s['source_id']}"
        reader = PdfReader(path)
        assert len(reader.pages) == s['pdf_pages']
        readers[s['source_id']] = reader
        source_checks.append({'source_id': s['source_id'], 'sha256': digest, 'pdf_pages': len(reader.pages)})
    with (ROOT / 'data' / 'nte_cheese_sample.csv').open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    checked = []
    text_cache = {}
    for r in rows:
        bounds = [int(p) for p in r['pdf_pages'].split('–')]
        pages = list(range(bounds[0], bounds[-1] + 1))
        text = ''
        for p in pages:
            key = (r['source_id'], p)
            if key not in text_cache:
                text_cache[key] = readers[r['source_id']].pages[p-1].extract_text()
            text += '\n' + text_cache[key]
        assert normalized(r['anchor']) in normalized(text), f"Anchor not found: {r['record_id']}"
        assert 'cheese' in normalized(text), f"No cheese context: {r['record_id']}"
        checked.append(r['record_id'])
    result = {'source_hashes_verified': source_checks, 'page_anchors_verified': len(checked),
              'record_ids': checked,
              'scope': 'Hashes and anchor presence supplement manual context review; automated checks do not validate legal claims or coding judgments.'}
    (ROOT / 'results' / 'source_verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
