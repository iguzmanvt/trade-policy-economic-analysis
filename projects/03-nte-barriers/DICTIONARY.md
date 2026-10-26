# Data dictionary

All CSV files are UTF-8, comma-delimited, with a header. Blank `record_id` in a reviewed non-mention is intentional; it is not a numeric zero. Printed and physical page ranges use an en dash; physical PDF pages are one-based.

## `data/nte_cheese_sample.csv`

One row per positively observed edition–issue. The original 18 record identifiers are preserved; Chile 2024 is the only added positive record.

| Field | Definition |
|---|---|
| `record_id` | Stable unique identifier of the edition–issue observation. |
| `edition_year` | NTE edition label, not adoption or enforcement year. |
| `report_chapter` | Country or regional chapter in the report. |
| `jurisdiction` | Jurisdiction of the selected measure. Qatar is distinct from the Gulf Cooperation Council chapter. |
| `issue_id` | Stable policy-problem identifier; does not imply the same legal instrument over time. |
| `topic` | Primary analytical mechanism, defined in `taxonomy.csv`. Not an adjudicated legal category. |
| `product` | Product or input scope identified by the passage. |
| `printed_pages` | Numbers printed on the report pages. |
| `pdf_pages` | Physical PDF pages, one-based, in the exact source variant. |
| `source_id` | Foreign key to a core official file in `sources.json`. |
| `source_url` | Exact official URL for the source file. |
| `anchor` | Legacy short locator for continuity. More specific page-level checks are in `locator_checks.csv`. |
| `reported_status` | Author's classification of the source statement, defined in `reported_status_dictionary.csv`. |
| `source_instrument` | Instrument expressly identified in the selected passage; not an independent legal-status opinion. |
| `summary` | Concise original summary attributed to USTR. |
| `verification` | Human source-review description; automated results are separate. |
| `report_subsection` | Heading verified from the public source, with no inherited extraction label. |
| `verification_date` | Date of this review in America/Mexico_City. |
| `source_description` | What measure, proposal or arrangement the source describes. |
| `ustr_position` | Concern, request or assurance expressed in the U.S. account. |
| `analyst_interpretation` | The author's inference and limits, distinct from the source assertion. |
| `measure_stage` | Descriptive stage as reported, such as proposed modification or recalled approval. |

## Other input tables

| File | Grain and fields |
|---|---|
| `selected_issues.csv` | Eight issue rows: chapter, jurisdiction, topic, label, selection reason, follow-up evidence and continuity rule. |
| `coverage_review.csv` | 24 issue–edition cells: coverage status, source, printed/PDF review ranges, positive record ID when applicable, scope, review note and date. |
| `locator_checks.csv` | Short check per record/source/page: `check_id`, `record_id`, `source_id`, `pdf_page`, `printed_page`, `anchor`, `anchor_type`. Multiple anchors can check the same page. |
| `search_terms.csv` | Candidate term, direct/context role, matching method and manual inclusion rule. Context hits alone are insufficient. |
| `taxonomy.csv` | Mechanism codes and analytical inclusion rules inherited from the public sample, with author-coded classification. |
| `reported_status_dictionary.csv` | Five allowed source-status codes and definitions. |
| `chile_event_chronology.csv` | Four corroborated dates, event, supporting source ID, locator and interpretation; not extra NTE rows. |

Coverage states are documented in [METHOD.md](METHOD.md). A chapter-reviewed non-mention differs from a search with no match and from an unreviewed document. No unreviewed or unresolved cells remain inside the fixed 24-cell grid.

## Sources and outputs

`sources.json` distinguishes four core NTE PDFs from three supporting official sources. Core source fields include a unique local cache filename, edition, publisher, URL, SHA-256, physical page count, retrieval date and review scope. The old retrieval metadata is retained separately from the 26 October re-verification. Supplementary official materials have human-readable locators and reading method; no local-file hash is claimed when no file was downloaded.

`results/topic_summary.csv` and `selected_coverage.csv` describe the selected coding only. `issue_continuity.csv` links positive observations. `coverage_matrix.csv` exposes all cells and their states. `comparison_table.csv` provides one row per issue and a source/status/page mapping for every edition. `temporal_cases.csv` shows the instrument and statement status for EU and Chile records. JSON receipts describe actual table checks and optional official-source checks. None of these outputs is a barrier index or an estimate of effect size.
