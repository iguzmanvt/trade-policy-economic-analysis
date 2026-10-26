# Executed validation

**Current review: 26 October 2026, America/Mexico_City. Data reference year: 2018.**

The current review continues the public project at commit `de51038af1394c48d6d1b7ad684bc3b335c462ca` of `iguzmanvt/trade-policy-economic-analysis`. The live `main` read at the start matched that commit. The 14 supplied project files were checked against their recorded Git blob identities. The four analytical CSV tables, `data/official_cells.csv` and `data/workbook_provenance.json` retain their exact published bytes.

## 1. Fresh official source recovery

All six original workbooks were downloaded anew from the INEGI catalog on **26 October 2026 at 16:23, Mexico City time**. Each SHA256 matched the pinned historical binary. A coordinate-by-coordinate comparison covered **2,557 selected values with zero differences**; workbook titles, row category labels, reference year and metadata date also agreed.

| Workbook | Selected cells compared | SHA256 vs pinned file | Selected-value differences |
|---|---:|---|---:|
| MIP_19.xlsx | 843 | Exact | 0 |
| MIP_38.xlsx | 843 | Exact | 0 |
| MIP_10.xlsx | 844 | Exact | 0 |
| COU_177.xlsx | 9 | Exact | 0 |
| COU_184.xlsx | 9 | Exact | 0 |
| COU_170.xlsx | 9 | Exact | 0 |
| **Total** | **2,557** | **6 of 6 exact** | **0** |

Effective URLs, actual retrieval times, HTTP metadata, titles, edition identifiers, source locators and scope are in `data/source_recovery_20261026.json`. Source history remains in `sources.json`; the historical provenance was not overwritten or relabelled as a new vintage. SCIAN 2018 definitions were checked at printed pages 150-151 / PDF pages 169-170. No source revision was detected.

Full-file hash identity covers all six binaries. Economic and cell-level checks cover the selected rows and their metadata, not every account in the full matrices. The downloaded workbooks remain external to the public project.

## 2. Accounting reproduction and independent arithmetic

`python analyze.py` ran successfully on the final project. Explicit validations replace all substantive `assert` statements. They check schema, unique keys and locators, finite values, exact source coordinates, product universes, origins, and all **834 destinations per MIP origin**, including zeros.

All following identities passed before writing new results:

- Domestic plus imported equals combined for every MIP destination and final component.
- Each origin's destination sum equals its published intermediate total; the six analytical groups exhaust the same total.
- Final components sum to published final totals with the combined MIP imports-netting entry handled separately.
- Intermediate plus published final equals published total for each MIP and COU origin.
- COU origin totals and final components reconcile within the distinct 3115 universe.
- Gross MIP final uses equal `84,412.694 - (-21,761.015) = 106,173.709`.
- Gross MIP total uses equal `18,072.048 + 106,173.709 = 124,245.757` and domestic total plus imported total.
- The combined MIP negative imports entry equals the negative of all imported-origin uses; it is not counted as another demand flow.
- Signed inventory changes remain intact: **-162.465** in MIP 311513, and separately **-160.904** in COU 3115.

A separate Decimal-based recalculation, importing no project analysis code, passed **65 checks**, including all numeric fields of the four result CSVs. It confirmed the five requested ratios: **41.5400014431%, 17.5144934728%, 34.4980645434%, 14.5454045566% and 17.5536614879%**. It also confirmed 89 positive and 745 zero combined MIP destinations, the 74.3073225569% top-three share and the 13.4250617542% imported share of final uses. This is independent arithmetic, not an independent external audit opinion.

The unchanged input SHA256 is:

```text
28fbf1b5591ac22062606b0c5707d18b8193575d131a0e0187e56bcf86de5d02
```

## 3. Isolated normal and optimized-Python tests

Executed with Python **3.12.14**, using temporary copies and the six exact recovered official files:

```bash
python tests/test_validation.py --source-directory SOURCE_DIRECTORY --report test_results.json
```

The harness ran each case normally and with **`python -O`**, for **12 executed subprocess cases**:

| Case | Normal | Optimized | Evidence checked |
|---|---|---|---|
| Valid analysis | Exit 0 | Exit 0 | All four analytical CSVs byte-identical to the published baseline |
| Inconsistent intermediate value | Correct rejection, exit 1 | Correct rejection, exit 1 | Clear destination-sum error; existing results unchanged |
| Inconsistent COU total, after MIP checks | Correct rejection, exit 1 | Correct rejection, exit 1 | Clear COU total error; existing results unchanged |
| Missing destination row | Correct rejection, exit 1 | Correct rejection, exit 1 | Explicit source-count error; existing results unchanged |
| One byte appended to MIP_19.xlsx | Correct rejection, exit 1 | Correct rejection, exit 1 | Explicit expected/actual SHA256 mismatch before parsing; snapshot/provenance unchanged |
| Exact official re-extraction | Exit 0 | Exit 0 | All six pinned hashes passed; extract and historical provenance byte-identical |

The invalid-input cases emitted no premature success message. The extractor preflights all six hashes and stages output only after metadata and accounting checks pass. These tests validate the specified rejection behavior; they are not claims about untested operating-system failures or every possible malformed input.

## 4. Note, figure and complete publication reproduction

`python analyze.py --publication` successfully generated the final Markdown note, PDF and figure from the result CSVs. Optional dependencies used: **Matplotlib 3.10.8** and **ReportLab 4.4.9**. The core calculation still requires only Python's standard library.

Two further isolated executions, normal and optimized, were invoked from a different working directory. Both returned zero and reproduced **ten outputs byte-for-byte**: the four CSV tables, validation JSON, Markdown and PDF note, PNG and SVG figure, and publication manifest. Thus there were **12 focused code-control cases plus two complete publication reproduction runs**, not 14 different adversarial cases.

`NOTE.pdf` contains **three pages**. Every final page was rendered to PNG and visually inspected. Font substitution found in an initial draft was corrected by embedding the same font family used in the figure. The final pages have readable tables, intact labels and citations, consistent units, no clipping or overlap, and sequential page numbers. The figure uses a zero-based value axis, distinct domestic/imported segments, all six destination labels and both-origin total labels generated from the CSV. Only one figure is included because it already shows magnitude and origin composition.

An economic review of the note confirmed denominator and matrix distinctions. One phrase was corrected to specify that negative inventories remain in **final-use and gross-use totals**, rather than in every denominator. The note and Markdown share the same generated prose and tables; the PDF uses compact clickable source labels where Markdown prints the full URLs.

`results/publication_manifest.json` records the current publication hashes. Visual checks are documented here, not inferred from that manifest.

## 5. Historical record and current limits

The received 22 October 2026 record reports an earlier reconstruction from archived official books and an uncompleted fresh binary download. That history remains in `sources.json` and the unchanged provenance register. The current six-file recovery resolves that specific download limitation; it does not rewrite the earlier date or imply a newer statistical observation.

Current limits are the defined scope of the exercise: 2018 product-use accounts, no country of origin within imports, no named cheeses, no firm or retail-channel identification, no destination industry's full input-cost structure, and no substitution, compliance-cost, pass-through, causal, multiplier or welfare estimate. No Leontief or general-equilibrium model was run. The public row decomposition is complete within this scope.
