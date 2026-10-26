# Execution and validation

Prepared 22 October 2026 (Mexico City). **Ready within the reviewed, bounded scope.** Statistical vintage and inference limits remain part of the results.

## Initial execution and review — 22 October 2026

Executed successfully with Python 3.12:

```bash
python reproduce.py
```

All five projects exited successfully using included inputs, the Python standard library and no network connection or credentials. Project-specific execution records distinguish offline reproduction from upstream verification.

| Project | Executed result | Independent checks |
|---|---|---|
| Duty intensity | 30 product–partner–period observations; ratios, gaps, country aggregates and growth tables | All 30 rates and gaps recomputed with exact fractions; Mexico totals and input hash checked. Completed sample input and code preserved. |
| Trade concentration | 1,846 partner–flow–period rows; eight HHI/exposure summaries and partner growth contributions | All eight HHI values, Canada/Mexico shares, period totals and every 2025–2026 partner contribution recomputed independently. |
| NTE barriers | 18 coded records, eight longitudinal issues, seven chapters, five topics | All 18 page anchors and three official source PDF hashes matched. Human summaries and legal interpretation remain distinct from anchor checks. |
| Mexico input–output | 2,557 source cells; 834 detailed intermediate destinations per origin; four output tables | Origin/intermediate totals recomputed with exact fractions. A sample of 69 source cells matched the six original workbooks; no claim of a full independent matrix audit. |
| Growth scenarios | Four scenarios, 204 annual model rows, summary table and SVG | Exact transitions compared with independent Runge–Kutta numerical integration: maximum capital difference below 4.2 × 10⁻¹⁴. Accounting and shared initial conditions checked. |

## Integrated execution — 23 October 2026

Executed `python reproduce.py` with Python 3.12.14 in a clean copy of the integrated repository. All **seven components of five projects** passed without network access or external packages: enhanced P01; P02 partners; P02 selected products; Census flow bridge; P03; P04; P05. Execution changed no bundled output bytes and created no undeclared files. This is an integration/reproduction check, not a new Census download or upstream source audit.

- P01 retains the same 30-row snapshot, SHA256 `b68c40d953e13a6a15c9babc17b76ab3a39129dcbd56a819a259b7387ac147ca`, and its three prior CSV tables. The enhanced script adds 15 temporal changes and a figure. Inherited provenance, mappings and both historical source hashes remain in `sources.json`, with their not-rehashed caveat. None of the 240 original monthly consumption records is bundled or newly revalidated.
- P02's partner code, data, results, analytical note and source register remain byte-identical to the prior release. The separate product view includes 4,794 monthly records: 93,601,850,780 dollars in 2025 and 153,704,865,960 dollars in 2026. Its product HHI rises from 2,853.090839 to 4,289.037367, while three lines contribute 99.636688% of the net increase. Independent rational-arithmetic checks matched these controls.
- The shared flow bridge reproduces all six general-minus-consumption differences from the supplied inputs. Paths and the common dictionary distinguish P01 consumption, P02 partners and P02 products, including their different absence conventions. The bridge does not authenticate P01's missing monthly records.
- The P01 and product-contribution SVGs were rendered and visually inspected after integration. Their underlying values and geometry remain those of the reviewed input. Local links and public-file privacy patterns were checked.
- P03's historical research window and P04's unidentified import-origin wording were clarified. Their data, code and results did not change; this round did not repeat their original source-page or workbook audit. P05 is unchanged.

The supplied integration review is distinct from a formal external audit verdict. Optional product-coverage sensitivities are not included in this release. The original selection, archived statistical vintages and inference limits remain unchanged.

## P03 integration — 26 October 2026

Executed `python projects/03-nte-barriers/analyze.py` from the repository root with Python 3.12.14. Exit status was zero; all bundled outputs reproduced without byte differences or undeclared new files. The existing general runner still invokes this canonical entry point. Other project scripts were not rerun for this update.

The current P03 result is **19 positive records, eight selected issues, seven chapters, five mechanisms, three editions (2024–2026) and four distinct official source PDFs**. Its **24 reviewed cells equal 19 positive cells plus five chapter-reviewed non-mentions**. All 18 earlier record IDs remain, and the only added ID is `CHL-PRIOR-USERS-2024`. These are sample and coverage counts, not numbers of independent barriers.

Original metadata of the three prior core sources is preserved. The additional `NTE-2024-ALT394` retains its own URL, hash, page count and locators. The original and alternate 2024 PDFs are not treated as the same file or as a dated official replacement. `NOTE.pdf` is copied unchanged from the reviewed input; its three-page visual review was already completed before integration.

Input manifests, affected relative links, code entry, coverage states, private/public separation and file identities were checked. The underlying source verification and manual review recorded in P03 are retained evidence; the four official PDF files were not downloaded again and their page-level verification was not repeated in this integration. This update is not a reconstruction of the website as of 22 October 2026.

## P04 integration — 26 October 2026

Executed from the repository root with Python 3.12.14:

```bash
python projects/04-mexico-input-output/analyze.py
python -O projects/04-mexico-input-output/analyze.py
```

Both commands exited successfully and reproduced all bundled outputs without byte differences. Ten isolated acceptance cases also passed, exercising valid data, inconsistent totals, missing destinations and invalid workbook-byte rejection in normal and optimized modes. Accounting and structural checks use explicit exceptions and remain active with `python -O`; rejected inputs leave existing outputs intact.

An additional `analyze.py --publication` execution in an isolated copy, with matplotlib 3.10.8 and reportlab 4.4.9, reproduced the three-page note PDF, editable note, PNG/SVG figure and publication manifest without byte differences. All 22 public P04 files remained identical to the reviewed return. The supplied three-page visual review is retained; no layout change was introduced.

The reviewed CHAT04 return records six fresh official INEGI downloads on 26 October 2026, six exact pinned-hash matches and all 2,557 selected cell values without differences. That source recovery is distinct from these integration tests: no new workbook download or official re-extraction was performed here. CHAT04’s 12 source-enabled test cases and 65 independent accounting checks remain attributed to its review; this integration ran the ten cases available without the source workbooks.

The public extract, historical workbook provenance and all four numerical CSV tables remain byte-identical to the preceding public commit. Imported-origin shares remain 41.5% of intermediate uses and 17.5% of all gross uses; the within-imported intermediate share is 34.5%, the overall intermediate share is 14.5%, and 17.6% belongs to the separate broader COU category. Three destination groups retain 74.3% of intermediate uses. Data year remains 2018, with source metadata dated 29 August 2023.

Only P04 and necessary root references were updated. The existing general runner’s P04 entry is unchanged and was checked without running other projects. Integration-map identities, source-history preservation, publication hashes, affected relative links and the repository manifest were checked. Original execution and recovery dates remain in the historical record; this is a 26 October 2026 integration, not a 22 October source recovery or a new audit of the other projects.

## Public-release content checks

The release folder contains project notes, independently prepared code, bounded public inputs, generated results, source registers and execution records. Application documents, contact details, student data, original client reports/scripts, private paths, credentials, full source PDFs and original teaching files are excluded. File inventory and SHA256 manifest identify the exact release contents.

Project questions and denominators are different. Top-level claims were reconciled to the generated tables. Relative document links and referenced project files were checked. Generated figures were rendered and inspected. No live statistical update is implied by arithmetic reproduction.

## Boundaries closed for this release

These exclusions are not additional completed projects:

- A public reconstruction of every worldwide cheese mention across NTE editions 2007–2026 is not delivered. The completed documentary project is the declared 2024–2026 sample. Economic-cost estimates and legal adjudication lack the necessary evidence here.
- Gross bilateral trade does not identify transshipment, foreign content or a causal tariff effect. Neither trade project estimates those objects.
- The input–output snapshot does not provide a full structural model, bilateral import origins or named-cheese detail. Leontief multipliers, price transmission and policy counterfactuals are not estimated.
- The growth exercise does not estimate reform effects or forecast Mexico. Parameters are disclosed teaching assumptions.
- Archived Census inputs and recovered INEGI workbook vintages are reproducible here; a successful fresh binary/statistical download is not claimed where it was not completed.

No unfinished folder, empty proposal or duplicated tariff analysis is counted in the original five-project total.

## Climate finance additions — 26 October 2026

The new `reproduce_climate_finance.py` entry point ran successfully with Python 3.12 in the integrated repository. It checks P06's document integrity and reproduces P07–P08 calculations with bundled inputs and the standard library. The original seven-component runner and P01–P05 project files remain unchanged; this review did not repeat their analytical audits.

| New sample | Completed checks | Scope and material limits |
|---|---|---|
| P06 operational review | Eight policy records, twelve analyst-designed checks and four source records; identifier, source linkage, status and non-assessment checks passed in normal and optimized execution. | The official annual report was read in full at the relevant pages; B.8 decision details use official indexed excerpts, with direct-PDF retrieval limitations disclosed. File validation does not establish policy completeness, eligibility or fiduciary approval. |
| P07 financing instruments | Eleven tests passed in normal and optimized execution; an independent Decimal-based recomputation compared 2,046 numeric result fields, with zero differences greater than 1e-8. The two-panel figure was visually reviewed. | All quantitative inputs are synthetic. Cash-flow identities and scenario results do not establish country affordability, debt sustainability or official instrument availability. Core reproduction excludes optional figure regeneration. |
| P08 resource reconciliation | Eighteen metric records, including five preserved missing values. Ten named tests exercise twenty normal/optimized cases. Count and allocation identities and the reported ratios were independently recomputed with exact fraction arithmetic. Both conflicting receipt figures were visually inspected in the official source. | The source discrepancy remains unresolved. Data represent dated report passages, not a current cash balance or transaction audit. Missing amounts are not zero. |

The official annual-report PDF was downloaded and matched the source hash recorded in P06 and P08. P08's optional `--source-pdf` verification was also exercised; the public source PDF itself is not bundled. Its default output truthfully records that optional verification as not run during offline reproduction. The dated source-review evidence is retained separately in the source register and execution record.

The integrated copy passed P07's eleven tests and P08's ten tests (twenty subprocess cases). Public narrative was checked against the results and source scope. New relative links, privacy-sensitive patterns and manifest entries were checked before publication. The portfolio now has eight projects, with the original shared Census component still classified as support.
