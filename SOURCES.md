# Source guide

Original portfolio reference: 22 October 2026. P03 documentation was updated on 26 October 2026, retaining report editions 2024–2026. P04’s six official workbook binaries were recovered and their pinned hashes matched on 26 October 2026; its data remain 2018, with workbook metadata dated 29 August 2023. All projects retain their existing statistical vintages. Reference periods differ and are not a common-date panel.

| Project | Controlling evidence | Detailed register |
|---|---|---|
| 1. Duty intensity | U.S. Census Bureau imports for consumption; archived January–August 2025 and 2026 monthly sums | [Sources, exact codes and input hash](projects/01-observed-duty-intensity/sources.json) · [Methodology](projects/01-observed-duty-intensity/METHODOLOGY.md) |
| 2. Concentration — partners | U.S. Census Bureau all-goods general imports and total exports; archived January–August 2023–2026 partner sums | [Partner sources](projects/02-trade-concentration/sources.json) · [Partner dictionary](projects/02-trade-concentration/DICTIONARY.md) |
| 2. Concentration — products | U.S. Census Bureau general imports from Mexico in a fixed retrospective selection; 4,794 monthly observations, January–August 2025–2026 | [Product sources](projects/02-trade-concentration/product-basket/sources.json) · [Product note](projects/02-trade-concentration/product-basket/NOTE.md) |
| 3. NTE barriers | Office of the U.S. Trade Representative, three editions (2024–2026) and four distinct core PDF files; 19 positive records plus five chapter-reviewed non-mentions in eight selected issues. P03 updated 26 October 2026. | [Separate source identities and hashes](projects/03-nte-barriers/sources.json) · [Record-level data](projects/03-nte-barriers/data/nte_cheese_sample.csv) · [Coverage matrix](projects/03-nte-barriers/results/coverage_matrix.csv) · [Note PDF](projects/03-nte-barriers/NOTE.pdf) |
| 4. Input–output | INEGI 2018 input–output and supply-use workbooks, basic prices; six exact official binaries recovered on 26 October 2026, six matching hashes and 2,557 selected values without differences. Statistical universes and origins remain separate. | [Source history](projects/04-mexico-input-output/sources.json) · [Dated recovery record](projects/04-mexico-input-output/data/source_recovery_20261026.json) · [Cell provenance](projects/04-mexico-input-output/data/official_cells.csv) · [Unchanged workbook provenance](projects/04-mexico-input-output/data/workbook_provenance.json) |
| 5. Growth | Existing public course model pinned to commit 3d67d7dc98edaccbac9333be9839d0084bc5da3b; Solow model attribution; disclosed illustrative assumptions | [Sources](projects/05-growth-scenarios/SOURCES.md) · [Parameters](projects/05-growth-scenarios/data/parameters.json) |

Reproduction from included inputs is distinct from a live refresh. Project source records state which upstream files, pages, cells or metadata were actually checked. No live update is claimed when only an archived numerical input was reproduced.

[Census common sources](projects/census-common/SOURCES.md) and the [shared dictionary](projects/census-common/DATA_DICTIONARY.md) describe the three separate Census datasets and the six-row general/consumption flow bridge. The two concentration rows are views of P02; this guide does not add a sixth project.

## Climate finance additions — 26 October 2026

| Project | Controlling evidence | Detailed register |
|---|---|---|
| 6. Operational review | FRLD Governing Instrument, B.8 decision excerpts, the 2026 Board report and an explicitly informational 2024 instruments paper. Policy status and analyst proposals are recorded separately. | [Source register](projects/06-frld-operational-review/sources.json) · [Policy register](projects/06-frld-operational-review/data/policy_register.csv) |
| 7. Financing instruments | Original synthetic assumptions, with primary FRLD, UNFCCC, IDA and World Bank documents for conceptual context. No observed country or climate-loss dataset. | [Source register](projects/07-financing-instruments/sources.json) · [Assumptions](projects/07-financing-instruments/data/assumptions.json) |
| 8. Resource reconciliation | Bounded numerical extract from the official 2026 FRLD Board report; report published 19 October, reporting period ending 31 July. Two reported received-contribution values remain separate. | [Source register](projects/08-frld-resource-reconciliation/sources.json) · [Method and outputs](projects/08-frld-resource-reconciliation/README.md) |

The July reporting cutoff is not extended to October by the publication or retrieval date. The official report's source hash and PDF/printed-page locators permit inspection of the retained evidence. Source documents are linked, not republished in full.
