# Cheese-related trade measures and access safeguards in NTE reports

**Isaac Guzmán Valdivia Tovar | Public research sample | Updated 26 October 2026**

**Question.** How do National Trade Estimate (NTE) reports describe cheese-related trade frictions and access safeguards across selected economies, and what changes between the 2024–2026 editions?

**Finding.** The selected evidence describes five distinct mechanisms and several access safeguards. The clearest documented transition is Chile: a prospective concern in the 2024 report is followed by a reported access and prior-user arrangement in 2025, recalled in 2026. Other changes require more cautious interpretation: the European Union discussion cites a different regulation, Qatar's account adds detail, and several selected issues are not mentioned in later chapters. Those observations do not by themselves establish a new restriction, greater severity or repeal.

This release preserves the **18 previously public record IDs** and adds one verified Chile 2024 record. Its fixed panel contains **eight selected issues × three editions = 24 cells**: **19 positive evidence records** and **five chapter-reviewed non-mentions**. It covers seven country/regional chapters and five mechanism categories. These are sample-design counts, not barrier prevalence, costs or proven violations.

[Read the three-page note](NOTE.pdf) · [Editable note](NOTE.md) · [Comparative table](results/comparison_table.csv) · [Evidence](data/nte_cheese_sample.csv) · [Coverage](results/coverage_matrix.csv)

## Coverage and contribution

The selected chapters are Canada, Chile, Dominican Republic, European Union, Gulf Cooperation Council (GCC), Mexico and Vietnam. Qatar is the jurisdiction of the selected GCC issue; the regional chapter is not a proxy for all GCC members. Canada's selected issue concerns milk-protein inputs used in cheese production, not a measured loss of finished-cheese exports.

The contribution is an original, inspectable coding of mechanisms, source positions, access safeguards and temporal interpretation, backed by source-specific page checks. Selection follows the eight issues in the earlier public sample and completes their 2024–2026 observation grid. It is **not exhaustive within these chapters**, across all countries, across cheese measures, or across twenty editions. Tariffs, tariff-rate quotas and other dairy issues are outside this fixed issue selection.

Four official NTE PDF files from the Office of the United States Trade Representative (USTR) are used. Two have the same 2024 edition label but different content: the 392-page baseline file does not contain a Chile chapter; the separate 394-page official file does. The latter supplies Chile 2024 under its own source ID, `NTE-2024-ALT394`. Original source hashes and URLs remain in the index. No revision date or supersession is inferred from the `_1` filename. Three supporting official sources corroborate Chile's chronology and are excluded from NTE observation counts.

Five full chapters were read to resolve the initially uncoded cells: Dominican Republic 2026, Mexico 2025 and 2026, and Vietnam 2024 and 2025. `SECTION_REVIEWED_NO_MENTION` means no mention of the **selected issue** in the documented review scope. It is neither zero barriers nor a finding that the measure ended. The data dictionary also distinguishes a search with no match from an unreviewed document; neither is silently promoted to a reviewed non-mention.

## Reproduce the tables

Python 3.11 or later; standard library only:

```bash
python analyze.py
```

The script reads the manual evidence, issue catalog, coverage grid and locator checks. It validates identifiers, source links, ranges, categories and coverage consistency, then regenerates the tables and JSON receipts in `results/`. Paths resolve relative to the script; the existing portfolio entry point `analyze.py` is retained. Reproduction rebuilds the outputs from disclosed coding. It does not automatically reproduce the human judgment behind a summary or category.

## Verify the official documents

```bash
python -m pip install -r requirements-source-verification.txt
python verify_sources.py --source-dir /path/to/nte-pdfs --download
```

The optional command downloads only missing core NTE PDFs using their unique filenames in `sources.json`. It verifies SHA-256 hashes, page counts, printed/physical page mappings and short source anchors. Existing files with unexpected hashes fail explicitly and are not silently replaced. Omit `--download` for an existing cache. Full PDFs are not distributed in this project.

See [execution and validation](EXECUTION.md), [method and exclusions](METHOD.md), [field dictionary](DICTIONARY.md), [official document index](sources.json) and [rights and source terms](TERMS.md).

## Interpretation

NTE reports convey the U.S. government's perspective. A reported concern is not a World Trade Organization ruling, an independently verified legal violation or a quantified trade loss. Safeguards may depend on terms, origin, prior use and product presentation. Report edition, signature, approval, entry into force and actual enforcement are different dates or events. The sample supports focused follow-up inquiries; it does not estimate tariff equivalents, welfare effects or causal impacts.
