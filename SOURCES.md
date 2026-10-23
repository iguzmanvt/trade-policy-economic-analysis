# Source guide

Cutoff: 22 October 2026. Statistical reference periods differ by project and are not presented as a common-date panel.

| Project | Controlling evidence | Detailed register |
|---|---|---|
| 1. Duty intensity | U.S. Census Bureau imports for consumption; archived January–August 2025 and 2026 monthly sums | [Sources, exact codes and input hash](projects/01-observed-duty-intensity/sources.json) · [Methodology](projects/01-observed-duty-intensity/METHODOLOGY.md) |
| 2. Concentration — partners | U.S. Census Bureau all-goods general imports and total exports; archived January–August 2023–2026 partner sums | [Partner sources](projects/02-trade-concentration/sources.json) · [Partner dictionary](projects/02-trade-concentration/DICTIONARY.md) |
| 2. Concentration — products | U.S. Census Bureau general imports from Mexico in a fixed retrospective selection; 4,794 monthly observations, January–August 2025–2026 | [Product sources](projects/02-trade-concentration/product-basket/sources.json) · [Product note](projects/02-trade-concentration/product-basket/NOTE.md) |
| 3. NTE barriers | Office of the U.S. Trade Representative, official 2024, 2025 and 2026 reports; purposive factual sample | [Sources and report hashes](projects/03-nte-barriers/sources.json) · [Record-level data](projects/03-nte-barriers/data/nte_cheese_sample.csv) |
| 4. Input–output | INEGI 2018 input–output and supply-use workbooks, basic prices; classification and origins separately identified | [Cell provenance](projects/04-mexico-input-output/data/official_cells.csv) · [Workbook provenance](projects/04-mexico-input-output/data/workbook_provenance.json) |
| 5. Growth | Existing public course model pinned to commit 3d67d7dc98edaccbac9333be9839d0084bc5da3b; Solow model attribution; disclosed illustrative assumptions | [Sources](projects/05-growth-scenarios/SOURCES.md) · [Parameters](projects/05-growth-scenarios/data/parameters.json) |

Reproduction from included inputs is distinct from a live refresh. Project source records state which upstream files, pages, cells or metadata were actually checked. No live update is claimed when only an archived numerical input was reproduced.

[Census common sources](projects/census-common/SOURCES.md) and the [shared dictionary](projects/census-common/DATA_DICTIONARY.md) describe the three separate Census datasets and the six-row general/consumption flow bridge. The two concentration rows are views of P02; this guide does not add a sixth project.
