# Validation and interpretation

The source review was completed on 26 October 2026. The primary 2026 Board report is an advance UNFCCC version published on 19 October and adopted by the Board in decision BM-2026/05. Its reporting period ends on 31 July; later publication does not establish later operational status.

The source register identifies four official sources. The full Governing Instrument, the 2024 background paper and the downloaded 2026 report were read at the relevant locators. Selected official indexed excerpts were used for the B.8 decision compendium because direct download returned HTTP 403. The 2026 report corroborates adoption of the relevant B.8 arrangements and the two review routes. A byte-for-byte archive of the B.8 compendium was not obtained.

The eight policy-status records were checked against their stated locators. The twelve matrix rows are original analyst suggestions organized into three modules. Suggested evidence and follow-up actions are not represented as official application requirements. Each row links to a policy record, and all case states remain `not_assessed`.

`validate.py` checks the structured files, source relationships and non-assessment boundary. It uses explicit exceptions, so the validation remains active when Python runs with `-O`. No network request is required to reproduce these checks. The result in `results/validation.json` confirms document integrity only; it does not certify a country or request, verify every later policy change or replace expert review.

Before using the framework in a real case, retrieve any subsequent decisions, the applicable funding documents and country-specific evidence. Preserve the distinction between financial analysis, legal provisions, fiduciary judgment, results monitoring and the institution's final decision.
