# Method and data boundaries

## Scope and units

The input contains 18 identified records: 13 reported observations and five explicit evidence gaps. Numeric values are either USD million, requests or contributors. The pipeline's reported USD 2.8 billion is converted to 2,800 million for arithmetic, while its original coarse precision is retained. No currency conversion is performed on underlying contributor currencies.

The resource reference date is 31 July 2026. The request counts describe the submission cohort ending 15 June 2026, as subsequently reported. Historical allocation decisions are recorded as decisions described by the reporting-period end, not as cash balances observed on that date. The analysis date and report publication date are separate metadata.

## Field dictionary

| Field | Meaning |
|---|---|
| `metric_id` | Unique stable identifier for one reported measure or evidence gap |
| `metric` | Readable description |
| `value` | Decimal number; blank for missing evidence |
| `unit` | USD million, requests or contributors |
| `reference_date` | Snapshot, reporting-period end or submission-cohort cutoff |
| `date_basis` | Meaning of that date for this record |
| `source_id` | Source-register identifier |
| `pdf_page` / `printed_page` | One-based PDF and printed annex page numbers |
| `paragraph` | Source paragraph or the selected passage searched for an unavailable measure |
| `evidence_status` | Reported, reported with discrepancy, rounded, or not in the selected passages |
| `precision` | Precision stated in the source; never inferred from the CSV's decimal format |
| `note` | Interpretation limit or duplicate-counting warning |

`not_in_selected_passages` means the selected resource paragraphs do not give the amount. It is not a claim that no other publication or page contains the information, and it does not establish a zero balance.

## Calculations

For each of the two received figures, the descriptive ratio is `100 × received / pledges`. The displayed range uses the minimum and maximum of those two calculations, not a statistical confidence interval. The difference in amounts received is `summary − body`.

The intake residual is `received requests − pipeline requests − non-compliant requests`. The allocation residual is `revised funding-request allocation − initial allocation − increment`. Both must equal zero before results are written. The pipeline comparison is `rounded requested amount / funding-request allocation`; oversight is excluded because the numerator contains requested project funding rather than an independently reconciled total including oversight.

All arithmetic uses Python `Decimal`, with displayed results rounded half up to two decimal places. Outputs retain status and input identifiers. The script preserves both contradictory observations and never imputes the missing fields. Data validation uses explicit exceptions and continues to operate with Python optimization enabled.

## Interpretation boundaries

This module does not estimate arrears, immediately spendable cash, available commitment authority, approved financing gaps, disbursements, climate-attributable losses or program effectiveness. It does not decide which of the two receipts values is correct. It does not convert the pipeline into a sovereign financing requirement. A future source update requires new dates, reviewed passages and reconciliation; changing the input date to pretend that the same data are current is rejected.

The original official PDF is not bundled. `--source-pdf` can check a local copy against the pinned SHA-256 before any output is written. This checks identity, not authenticity of all underlying financial transactions. The published outputs are reproducible from the included bounded extract without network access.
