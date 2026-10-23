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

No unfinished folder, empty proposal or duplicated tariff analysis is counted in the five-project total.
