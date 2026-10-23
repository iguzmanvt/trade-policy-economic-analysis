# Trade policy and economic analysis

**Isaac Guzmán Valdivia Tovar** · Economist · Information cutoff: 22 October 2026

Five reproducible examples connect trade measurement, external exposure, institutional evidence, production accounts and growth mechanisms. Each addresses a different question and states what its evidence can establish. The notes and results are in English. This is independent analytical work; no institutional endorsement is implied.

## Project index

| Project and question | Verifiable result | Evidence and method | Read / reproduce |
|---|---|---|---|
| **1. Observed duty intensity.** How do duty-to-import-value ratios differ across suppliers of selected computer and network equipment? | U.S. imports for consumption from Mexico in the selected lines rose 109.8% in January–August 2026; duty differences are large against China and much smaller against the other selected suppliers. These are descriptive comparisons. | 30 archived U.S. Census observations: three exact tariff lines, five suppliers, two January–August periods. Ratios of sums, within-product comparisons. | [Project](projects/01-observed-duty-intensity/README.md) · [Note](projects/01-observed-duty-intensity/NOTE.md) · [Code](projects/01-observed-duty-intensity/analyze.py) |
| **2. North American trade concentration.** How concentrated are U.S. merchandise suppliers and destinations, and how has North American exposure changed? | Partner concentration fell from 2023 to 2026. Canada and Mexico together accounted for 28.53% of covered U.S. general imports and 30.35% of covered total exports in January–August 2026. | All goods and individual partners, 2023–2026. Herfindahl–Hirschman Index (HHI), partner shares and growth contributions; imports and exports kept separate. | [Project](projects/02-trade-concentration/README.md) · [Note](projects/02-trade-concentration/NOTE.md) · [Code](projects/02-trade-concentration/analyze.py) |
| **3. Documented non-tariff barriers.** What mechanisms affect cheese market access in a verified sample of U.S. National Trade Estimate (NTE) reports? | An auditable sample links 18 edition–issue records to eight longitudinal issues, seven country/regional chapters and five mechanism categories. | Official U.S. Trade Representative reports, 2024–2026; original factual coding, page locators, taxonomy and European Union/Chile temporal cases. A purposive sample, with no claim of full twenty-edition coverage. | [Project](projects/03-nte-barriers/README.md) · [Note](projects/03-nte-barriers/NOTE.md) · [Code](projects/03-nte-barriers/analyze.py) |
| **4. Mexico input–output linkages.** Where are dairy-product uses recorded, and how does origin change their intermediate/final composition? | The 2018 product row 311513 records intermediate uses of 18,072.048 million pesos; imported products account for 41.54% of these intermediate uses. | Official Mexican input–output cells at basic prices. Origin and use decompositions; the detailed product row and the broader 3115 supply-use category are kept distinct. | [Project](projects/04-mexico-input-output/README.md) · [Note](projects/04-mexico-input-output/NOTE.md) · [Code](projects/04-mexico-input-output/analyze.py) |
| **5. Growth and policy horizons.** How do investment and efficiency-growth scenarios differ in transition costs and long-run mechanisms? | In an illustrative Solow exercise, the year-25 output gap is 3.83% for higher investment and 11.10% for faster efficiency growth. The investment scenario initially reduces consumption. | New exact transition implementation of a model developed in existing public teaching materials; four scenarios, 204 annual model rows. No empirical policy estimate or Mexico forecast. | [Project](projects/05-growth-scenarios/README.md) · [Note](projects/05-growth-scenarios/NOTE.md) · [Code](projects/05-growth-scenarios/analyze.py) |

## Reproduce everything

Python 3.11 or later. Core reproduction uses only the standard library, included small inputs and no credentials or network access:

```bash
python reproduce.py
```

The command regenerates every project's tables and any included figures. Individual project READMEs document the input grain, definitions, denominators, execution checks and upstream source-reconstruction limits. Optional source downloads/extractions may require extra tools and are distinguished from offline reproduction. No dependency file is needed for core reproduction.

## Read the evidence correctly

Projects 1 and 2 retain archived January–August monthly vintages, which can differ from subsequently revised official year-to-date totals. Project 2 measures partner concentration for all goods, rather than repeating the selected product comparison in Project 1. Gross trade does not identify domestic value added, transshipment or final use.

NTE records express the reporting perspective of the United States; they do not by themselves establish a World Trade Organization violation or the economic cost of a barrier. Input–output uses are accounting relationships, not retail channels or causal multipliers. Growth paths are conditional simulations with illustrative parameters. Each note develops these limits beside the relevant result.

## Sources and prior work

The statistical sources are the U.S. Census Bureau and Mexico's National Institute of Statistics and Geography (INEGI); documentary sources are official U.S. Trade Representative reports. Project 5 links to the existing [Crecimiento course repository](https://github.com/iguzmanvt/Crecimiento) at a pinned commit and adds a new implementation without altering that repository's history.

See [source guide](SOURCES.md), [rights and attribution](RIGHTS_AND_SOURCES.md), [execution and validation](VALIDATION.md), [preparation record](CHANGELOG.md) and [two-line project descriptions](PROJECT_SUMMARIES.md). Only public inputs and independently prepared portfolio code/text are included.
