#!/usr/bin/env python3
"""Reproduce a bounded FRLD reporting reconciliation; Python standard library only."""
from __future__ import annotations

import argparse
import csv
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIELDS = ['metric_id', 'metric', 'value', 'unit', 'reference_date', 'date_basis',
          'source_id', 'pdf_page', 'printed_page', 'paragraph', 'evidence_status',
          'precision', 'note']
IDS = {'pledges', 'received_body', 'received_summary', 'signed_contributors',
       'signed_amount', 'requests_received', 'pipeline_requests',
       'noncompliant_requests', 'pipeline_amount', 'bim_initial', 'bim_increase',
       'bim_revised', 'oversight_total', 'oversight_increase', 'cash_composition',
       'commitment_authority', 'commitments', 'transfers'}
MISSING = {'signed_amount', 'cash_composition', 'commitment_authority', 'commitments', 'transfers'}
REQUESTS = {'requests_received', 'pipeline_requests', 'noncompliant_requests'}
REQUIRED_EVIDENCE = {
    'signed_amount': 'Agreement-level amounts and payment schedules at a common valuation date',
    'cash_composition': 'Trustee reconciliation of cash and any promissory notes or other instruments',
    'commitment_authority': 'Trustee statement of resources available for future commitments under the applicable basis',
    'commitments': 'Commitment register with approvals and legal financial liabilities',
    'transfers': 'Transfer register matched to commitments and recipient or access entity',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_metrics(path):
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        require(reader.fieldnames == FIELDS, 'Unexpected input schema')
        rows = list(reader)
    ids = [r['metric_id'] for r in rows]
    require(len(ids) == len(set(ids)), 'Duplicate metric IDs')
    require(set(ids) == IDS, 'Missing or unexpected metric IDs')
    records = {}
    for row in rows:
        k = row['metric_id']
        require(None not in row and all(v is not None for v in row.values()), 'Malformed CSV row')
        reference_date = date.fromisoformat(row['reference_date'])
        expected_date = date(2026, 6, 15) if k in REQUESTS else date(2026, 7, 31)
        require(reference_date == expected_date, f'Unexpected date for {k}')
        require(row['source_id'] == 'R1', f'Unexpected source for {k}')
        require(int(row['pdf_page']) - int(row['printed_page']) == 2, f'Page locator mismatch for {k}')
        require(bool(row['paragraph']) and bool(row['date_basis']) and bool(row['note']), f'Missing context for {k}')
        expected_unit = 'requests' if k in REQUESTS else ('contributors' if k == 'signed_contributors' else 'USD million')
        require(row['unit'] == expected_unit, f'Incorrect unit for {k}')
        if k in MISSING:
            require(row['value'] == '', f'Missing evidence must not be coded as zero for {k}')
            require(row['evidence_status'] == 'not_in_selected_passages', f'Incorrect missing status for {k}')
            value = None
        else:
            try:
                value = Decimal(row['value'])
            except InvalidOperation as exc:
                raise ValueError(f'Invalid number for {k}') from exc
            require(value.is_finite() and value >= 0, f'Invalid value for {k}')
            expected_status = ('reported_discrepancy' if k.startswith('received_') else
                               'reported_rounded' if k == 'pipeline_amount' else 'reported')
            require(row['evidence_status'] == expected_status, f'Incorrect evidence status for {k}')
            if k in REQUESTS or k == 'signed_contributors':
                require(value == value.to_integral_value(), f'Noninteger count for {k}')
        records[k] = dict(row, number=value)
    v = lambda k: records[k]['number']
    require(v('pledges') > 0 and v('requests_received') > 0 and v('bim_revised') > 0, 'Zero denominator')
    require(v('requests_received') == v('pipeline_requests') + v('noncompliant_requests'), 'Request counts do not reconcile')
    require(v('bim_initial') + v('bim_increase') == v('bim_revised'), 'BIM allocation does not reconcile')
    require(v('oversight_increase') <= v('oversight_total'), 'Oversight increment exceeds reported total')
    for k in ('received_body', 'received_summary'):
        require(v(k) <= v('pledges'), 'Received amount exceeds pledges')
    require(records['pipeline_amount']['precision'] == '0.1 billion', 'Lost reported pipeline precision')
    return records


def formatted(value, places='0.01'):
    return str(value.quantize(Decimal(places), rounding=ROUND_HALF_UP))


def reconcile(records):
    v = lambda k: records[k]['number']
    rows = []
    def add(metric, value, unit, status, input_ids, interpretation):
        rows.append(dict(metric=metric, value=formatted(value), unit=unit,
                         status=status, input_ids=';'.join(input_ids), interpretation=interpretation))
    delta = v('received_summary') - v('received_body')
    add('received_summary_minus_body', delta, 'USD million', 'unresolved_source_discrepancy' if delta else 'reconciled',
        ['received_summary','received_body'], 'Preserve both observations; no corrected value is inferred')
    ratios = []
    for label in ('body', 'summary'):
        key = 'received_' + label
        ratio = v(key) / v('pledges') * 100
        ratios.append(ratio)
        add('received_to_pledges_' + label, ratio, 'percent', 'descriptive_ratio', [key,'pledges'],
            'Reported received divided by pledges; not a cash or commitment-authority ratio')
        add('pledges_minus_received_' + label, v('pledges') - v(key), 'USD million', 'arithmetic_difference',
            ['pledges',key], 'Not arrears or necessarily amounts presently due under signed agreements')
    add('received_to_pledges_min', min(ratios), 'percent', 'range_from_source_discrepancy',
        ['received_body','received_summary','pledges'], 'Minimum of the two reported-figure calculations')
    add('received_to_pledges_max', max(ratios), 'percent', 'range_from_source_discrepancy',
        ['received_body','received_summary','pledges'], 'Maximum of the two reported-figure calculations')
    add('request_count_residual', v('requests_received') - v('pipeline_requests') - v('noncompliant_requests'),
        'requests', 'reconciled', ['requests_received','pipeline_requests','noncompliant_requests'], 'Intake-cohort identity')
    add('pipeline_entry_share', v('pipeline_requests') / v('requests_received') * 100, 'percent', 'descriptive_ratio',
        ['pipeline_requests','requests_received'], 'Entry into pipeline is not funding approval')
    add('bim_allocation_residual', v('bim_revised') - v('bim_initial') - v('bim_increase'), 'USD million', 'reconciled',
        ['bim_revised','bim_initial','bim_increase'], 'Revised funding-request allocation minus original and increment')
    add('pipeline_to_funding_request_allocation', v('pipeline_amount') / v('bim_revised'), 'times',
        'approximate_descriptive_ratio', ['pipeline_amount','bim_revised'],
        'Rounded requested amount relative to funding-request allocation; not an approved financing gap')
    missing = [dict(metric_id=k, status='not_in_selected_passages', value='',
                    why_needed=REQUIRED_EVIDENCE[k]) for k in sorted(MISSING)]
    return rows, missing


def csv_text(rows):
    out = io.StringIO(newline='')
    writer = csv.DictWriter(out, fieldnames=list(rows[0]), lineterminator='\n')
    writer.writeheader(); writer.writerows(rows)
    return out.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=ROOT/'data'/'reported_metrics.csv')
    parser.add_argument('--output', type=Path, default=ROOT/'results')
    parser.add_argument('--source-pdf', type=Path, help='Optional official PDF for SHA-256 verification; not distributed')
    args = parser.parse_args()
    records = read_metrics(args.data)
    source_check = 'not_run_local_pdf_not_requested'
    if args.source_pdf:
        sources = json.loads((ROOT/'sources.json').read_text())
        actual = hashlib.sha256(args.source_pdf.read_bytes()).hexdigest()
        require(actual == sources['sources'][0]['sha256'], 'Source PDF SHA-256 mismatch')
        source_check = 'pass'
    reconciliations, missing = reconcile(records)
    metrics = {r['metric']: {'value': r['value'], 'unit': r['unit'], 'status': r['status']} for r in reconciliations}
    validation = {'status': 'PASS', 'records': len(records), 'missing_values_preserved': len(missing),
                  'input_sha256': hashlib.sha256(args.data.read_bytes()).hexdigest(),
                  'source_pdf_hash_check': source_check, 'request_count_identity': 'PASS',
                  'bim_allocation_identity': 'PASS', 'reference_dates': ['2026-06-15','2026-07-31'],
                  'source_discrepancies': [{'metric':'amount_received', 'status':'UNRESOLVED',
                                          'summary_minus_body_usd_million': metrics['received_summary_minus_body']['value']}],
                  'limitation':'PASS validates this bounded extract and calculations; it does not resolve the source discrepancy or certify current available financing.'}
    # Finish all validation and serialization before touching any existing output.
    outputs = {'reconciliation.csv':csv_text(reconciliations), 'missing_evidence.csv':csv_text(missing),
               'metrics.json':json.dumps(metrics,indent=2)+'\n', 'validation.json':json.dumps(validation,indent=2)+'\n'}
    args.output.mkdir(parents=True, exist_ok=True)
    for name, content in outputs.items():
        (args.output/name).write_text(content, encoding='utf-8')
    print(json.dumps({'status':'PASS','records':len(records),'missing':len(missing),
                      'received_ratio_range_percent':[metrics['received_to_pledges_min']['value'],metrics['received_to_pledges_max']['value']]}))


if __name__ == '__main__':
    main()
