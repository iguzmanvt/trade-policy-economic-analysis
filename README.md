# Trade policy and economic analysis

**Isaac Guzmán Valdivia Tovar** · Economist · Original portfolio reference: 22 October 2026 · P03 updated: 26 October 2026

This portfolio presents applied trade-policy analysis and reproducible policy research. Five examples connect trade measurement, external exposure, institutional evidence, production accounts and growth mechanisms. Each addresses a different question and states what its evidence can establish. The notes and results are in English. This is independent analytical work; no institutional endorsement is implied.

## Project index

| Project and question | Verifiable result | Evidence and method | Read / reproduce |
|---|---|---|---|
| **1. Observed duty intensity.** How do duty-to-import-value ratios differ across suppliers of selected computer and network equipment? | U.S. imports for consumption from Mexico in the selected lines rose 109.8% in January–August 2026; duty differences are large against China and much smaller against the other selected suppliers. These are descriptive comparisons. | 30 archived U.S. Census observations: three exact tariff lines, five suppliers, two January–August periods. Ratios of sums, within-product comparisons. | [Project](projects/01-observed-duty-intensity/README.md) · [Note](projects/01-observed-duty-intensity/NOTE.md) · [Code](projects/01-observed-duty-intensity/analyze.py) |
| **2. Trade concentration and exposure.** How concentrated are trade partners, and how concentrated are products within a selected import basket from Mexico? | The 2026 partner Herfindahl–Hirschman Index (HHI) is 703.8 for covered general imports and 628.8 for total exports. In the separate product selection, HHI rises from 2,853.1 in 2025 to 4,289.0 in 2026; three lines contribute 99.64% of its net increase. | Two views with separate denominators: all-goods U.S. partners, January–August 2023–2026; fixed selection of 374 historical tariff lines grouped into 88 six-digit products, general imports from Mexico, January–August 2025–2026. These are not one HHI series. | [Two-view project](projects/02-trade-concentration/README.md) · [Partner note](projects/02-trade-concentration/NOTE.md) · [Product note](projects/02-trade-concentration/product-basket/NOTE.md) |
| **3. Documented non-tariff barriers.** How do selected cheese market-access issues and safeguards change across U.S. National Trade Estimate (NTE) editions? | Compares eight selected issues across 2024–2026, distinguishing reported concerns, access safeguards and changes in reporting. The 24-cell panel contains 19 positive evidence records and five chapter-reviewed non-mentions, across seven chapters and five mechanisms. These are not counts of independent barriers. | Three report editions and four separately identified official source PDF files, including two distinct 2024 variants; original coding, page locators and Chile/EU/Qatar temporal comparisons. Updated 26 October 2026; purposive sample, not worldwide prevalence. | [Project](projects/03-nte-barriers/README.md) · [Three-page note](projects/03-nte-barriers/NOTE.pdf) · [Editable note](projects/03-nte-barriers/NOTE.md) · [Code](projects/03-nte-barriers/analyze.py) |
| **4. Mexico input–output linkages.** Where are dairy-product uses recorded, and how does origin change their intermediate/final composition? | The 2018 product row 311513 records intermediate uses of 18,072.048 million pesos; imported products account for 41.54% of these intermediate uses. | Official Mexican input–output cells at basic prices. Origin and use decompositions; the detailed product row and the broader 3115 supply-use category are kept distinct. | [Project](projects/04-mexico-input-output/README.md) · [Note](projects/04-mexico-input-output/NOTE.md) · [Code](projects/04-mexico-input-output/analyze.py) |
| **5. Growth and policy horizons.** How do investment and efficiency-growth scenarios differ in transition costs and long-run mechanisms? | In an illustrative Solow exercise, the year-25 output gap is 3.83% for higher investment and 11.10% for faster efficiency growth. The investment scenario initially reduces consumption. | New exact transition implementation of a model developed in existing public teaching materials; four scenarios, 204 annual model rows. No empirical policy estimate or Mexico forecast. | [Project](projects/05-growth-scenarios/README.md) · [Note](projects/05-growth-scenarios/NOTE.md) · [Code](projects/05-growth-scenarios/analyze.py) |

## Reproduce everything

Python 3.11 or later. Core reproduction uses only the standard library, included small inputs and no credentials or network access:

```bash
python reproduce.py
```

The command runs seven components of five projects: P01, the partner and product views of P02, the shared Census flow bridge, and P03–P05. It regenerates the included tables and figures. [Census common](projects/census-common/README.md) supplies a [shared dictionary](projects/census-common/DATA_DICTIONARY.md) and a bridge between general imports and imports for consumption; it is support, not an additional project. Individual project READMEs document grain, definitions, denominators, execution checks and upstream source-reconstruction limits. Optional source downloads/extractions may require extra tools and are distinguished from offline reproduction. No dependency file is needed for core reproduction.

## Read the evidence correctly

Projects 1 and 2 retain archived January–August monthly vintages, which can differ from subsequently revised official year-to-date totals. P01 includes 30 consumption-import aggregates; its 240 upstream monthly records are not bundled or newly revalidated. P02 keeps partner concentration for all goods separate from concentration within a retrospective product selection. The product view includes its own 4,794 monthly general-import records. The shared bridge compares the two import definitions without adding them or forcing differences to zero. Gross trade does not identify domestic value added, transshipment or final use.

NTE records express the reporting perspective of the United States; they do not by themselves establish a World Trade Organization violation or the economic cost of a barrier. Input–output uses are accounting relationships, not retail channels or causal multipliers. Growth paths are conditional simulations with illustrative parameters. Each note develops these limits beside the relevant result.

## Sources and prior work

The statistical sources are the U.S. Census Bureau and Mexico's National Institute of Statistics and Geography (INEGI); documentary sources are official U.S. Trade Representative reports. Project 5 links to the existing [Crecimiento course repository](https://github.com/iguzmanvt/Crecimiento) at a pinned commit and adds a new implementation without altering that repository's history.

See [source guide](SOURCES.md), [rights and attribution](RIGHTS_AND_SOURCES.md), [execution and validation](VALIDATION.md), [preparation record](CHANGELOG.md) and [two-line project descriptions](PROJECT_SUMMARIES.md). Only public inputs and independently prepared portfolio code/text are included.
