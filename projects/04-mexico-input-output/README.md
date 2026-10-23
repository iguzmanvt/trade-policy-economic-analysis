# Mexico's dairy linkages: intermediate demand, final uses and import exposure

Isaac Guzmán Valdivia Tovar · 22 October 2026

**Question.** How much of Mexico's use of dairy derivatives is intermediate demand, and how does the imported-origin share differ between intermediate and final uses?

**Result.** In the 2018 input–output table, imported products supply **17.5% of all gross uses** of product category 311513 but **41.5% of its intermediate uses**. The category's intermediate-use share is **14.5%**. A broader dairy supply-and-use category has a different **17.6%** share; the two are separate statistical universes.

[Analytical note](NOTE.md) · [Source register](sources.json) · [Data dictionary](data/DICTIONARY.md) · [Execution record](VALIDATION.md)

## Reproduce offline

Python 3.11+; standard library only. No credentials or network access are required.

```bash
python analyze.py
```

The script reads the included 2,557-cell official-data snapshot and regenerates four tables plus `results/validation.json`. It accepts invocation from any working directory. All ratios use unrounded Decimal arithmetic.

To independently recreate the snapshot from the same six official workbook vintages, obtain the listed tables from the National Institute of Statistics and Geography (INEGI) [input–output](https://www.inegi.org.mx/programas/mip/2018/) and [supply-and-use](https://www.inegi.org.mx/programas/cou/2018/) pages, place them in a directory, and run:

```bash
python extract_cells.py SOURCE_DIRECTORY
python analyze.py
```

`data/workbook_provenance.json` records the exact workbook SHA256 hashes and table titles. The original workbook bytes were inspected from the recovered archive; a fresh download of those binary files was not completed in this preparation. The public source pages and classification definition were checked. No automated fresh-download claim is made.

## Scope

The input–output matrix (MIP, its Spanish acronym) is symmetric and product by product. The row is North American Industry Classification System, Mexico 2018 (SCIAN) category **311513**, translated here as *dairy derivatives and ferments*. Columns represent homogeneous product groups. The supply-and-use tables (COU) comparison uses the broader **3115** dairy category with buyer-industry columns. Reference year: **2018**; published metadata update: **29 August 2023**. Units: **millions of pesos, 2018 basic prices**. Domestic and imported origin are separately preserved.

This is an accounting decomposition of public statistics, not a forecast or causal policy estimate. It does not identify particular cheese names, national origins within imports, retail channels or establishment-level purchasing. The included snapshot is a row extract, so no Leontief multiplier is calculated.

## Contents

| File | Purpose |
|---|---|
| `NOTE.md` | Policy-oriented interpretation and denominator discipline |
| `analyze.py` | Accounting identities, aggregation and result reproduction |
| `extract_cells.py` | Independent source-cell extractor, six external workbooks |
| `data/official_cells.csv` | All 834 MIP destinations for three origins, final components and controls; separate COU controls |
| `data/workbook_provenance.json` | Original titles, vintages and hashes |
| `data/DICTIONARY.md` | Field definitions, zero treatment and grouping rules |
| `results/origin_and_uses.csv` | Origin–use decomposition |
| `results/intermediate_destination_groups.csv` | Six exhaustive destination groups |
| `results/final_uses.csv` | Final-account components, preserving inventory drawdown |
| `results/universe_comparison.csv` | MIP 311513 versus COU 3115, kept separate |
| `results/validation.json` | Executed checks and snapshot hash |
| `sources.json` | Public sources, cell locators and reuse terms |
| `VALIDATION.md` | What was executed and what was not established |

Source: INEGI, *Matriz de Insumo Producto 2018* and *Cuadros de Oferta y Utilización 2018*, metadata update 29 August 2023. Extraction, aggregation, translation and analysis are the author's own; they are not an official INEGI product or endorsement. See the [INEGI information reuse terms](https://www.inegi.org.mx/inegi/terminos.html).
