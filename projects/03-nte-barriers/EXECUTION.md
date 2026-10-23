# Execution and source-review record

Prepared 22 October 2026, America/Mexico_City. Information cutoff: 22 October 2026; source editions: 2024–2026.

## Completed

- Recovered and read the effective prior research's consolidated source index and scope. It identifies a 2007–2026 window. Used it to establish continuity and scope, not as public numerical/textual input.
- Downloaded the three official USTR PDFs from the URLs in `sources.json`; all returned HTTP 200. The public package includes hashes and locators, not the PDFs or the prior corpus.
- Independently read the selected official pages in full and wrote the 18 new English summaries and status codes. Both printed and physical PDF page numbers were recorded. Taxonomy and issue identifiers were newly prepared for this sample.
- Executed `python analyze.py` successfully with Python 3.11-compatible standard-library code. Passed populated-field, unique record/key, topic, source/edition and page-bounds checks. Outputs: 18 records, eight issue identifiers, five topics, seven chapters.
- Executed `python verify_sources.py --source-dir <official-pdf-directory>` successfully with pypdf 6.10.0. All three source SHA256 digests/page counts and all 18 page anchors passed. The machine-readable result is `results/source_verification.json`.
- Kept the underlying internal research packages, original client code/text, private actor data, source PDFs, extracted full text and local paths outside the release folder.

## Reproduction boundary

`analyze.py` reproduces descriptive summaries from the released coding. It does not reproduce human judgment or claim an automatic extraction of every NTE mention. `verify_sources.py` supplements the manual review with file identity and anchor checks; an anchor match does not validate a legal conclusion. Core arithmetic requires no network, accounts or additional packages. Optional source downloads may fail or change; hash mismatch fails explicitly.

## Closed for this release

A full public reconstruction of the 20-edition worldwide corpus is outside this bounded release. Economic-cost estimates, legal eligibility decisions and violation adjudication lack the necessary evidence here and are not delivered. These exclusions do not count as additional completed projects.
