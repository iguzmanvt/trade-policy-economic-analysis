# FRLD resources and pipeline reporting

**Independent analytical work sample · 26 October 2026**

This note asks what the Fund's published resource and pipeline figures establish, and which additional evidence a financial reviewer would need. It keeps pledges, amounts reported as received, allocations, pipeline requests, commitments and transfers separate.

The [operational note](NOTE.md) uses the Board's advance annual report dated 19 October 2026. Resource figures refer to **31 July 2026**; request counts describe the cohort received by **15 June 2026**. This is a historical reporting reconciliation, not a live treasury statement.

## Main findings

- The two published receipt figures imply a received-to-pledges ratio of **59.05%–59.07%**. A USD 0.20 million source discrepancy remains visible and unresolved.
- The intake counts reconcile: **198 = 176 + 22**. Pipeline entry does not establish funding approval.
- The funding-request allocation reconciles: **USD 250 million + USD 92 million = USD 342 million**. The reported USD 28 million oversight provision is separate; its USD 8 million increment is already included in that total.
- The selected resource passages do not supply an agreement-value total, receipt composition, commitment authority, commitments or transfers. The dataset records these as missing, never zero.

Source locators are in [the data](data/reported_metrics.csv) and [sources.json](sources.json). Definitions and bounds are in [METHOD.md](METHOD.md).

## Reproduce

Python 3.10 or later; standard library only. From the repository root:

```bash
python projects/08-frld-resource-reconciliation/analyze.py
python -O projects/08-frld-resource-reconciliation/analyze.py
python -m unittest discover -s projects/08-frld-resource-reconciliation/tests -v
```

Optional verification of a separately downloaded official report:

```bash
python projects/08-frld-resource-reconciliation/analyze.py --source-pdf /path/to/cp2026_07_cma2016_12_adv.pdf
```

The optional check verifies the published SHA-256. A different version requires a fresh source review rather than treating a hash mismatch as proof that the new report is wrong. No network access is required for the included analysis. To run from another directory, supply the full script path. Core execution records that the optional source-PDF check was not run; the source review retained in this project is a separate check.

## Outputs

- [Calculated reconciliations](results/reconciliation.csv)
- [Machine-readable metrics](results/metrics.json)
- [Additional evidence required](results/missing_evidence.csv)
- [Validation record](results/validation.json)

This original public-source sample is unaffiliated with the Fund or World Bank and is not an official financial assessment. It uses no employer or client material.
