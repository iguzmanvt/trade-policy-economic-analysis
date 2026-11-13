# Employment growth and labor-force participation in Mexico

**Question.** How can employment increase while labor-force participation declines? This reproducible sample distinguishes changes in headcounts from changes in ratios, using official national labor-force survey tables from Mexico's statistical institute, INEGI.

**Finding.** Employment increased by **599,334 people** between Q2 2025 and Q2 2026, while the population aged 15 and over increased by 1,689,822. Labor-force participation declined by **0.38 percentage points**, and the employment-to-population ratio fell from **57.93% to 57.56%**. Employment and its population share therefore moved in different directions.

A separate September-to-September comparison shows employment falling by **267,333 people**, the labor force falling by 358,839, and the population outside the labor force rising by 1,736,239. The calculated unemployment rate declined from 2.98% to 2.85%. A lower unemployment rate alone does not summarize these simultaneous changes.

**Methods.** The package contains 12 period-by-sex records, representing 60 published counts and 24 published rates. It reconciles demographic and labor-force identities, distinguishes published from calculated rates, and computes a symmetric accounting decomposition of labor-force changes. Python rebuilds three tables, a summary file and two figures in PNG/SVG. All 84 input cells were re-extracted from two official PDFs; source hashes and cell values matched. The validation script also checks exact arithmetic, rejects eight damaged-input cases, and reproduces all eight outputs byte-for-byte under normal and optimized Python execution.

**Scope.** Q2 and September are independent year-on-year comparisons, not a continuous time series. The sample uses published table estimates without additional seasonal adjustment. It does not identify individual transitions, establish causality or test statistical significance. September is not a proxy for the full third quarter. This is a frozen documentary edition dated 26 October 2026, with source PDFs reverified on 13 November 2026.

**Sources.** INEGI, [ENOE bulletin 503/26, 25 August 2026, table 1, p. 3; rates table 4, p. 9](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/enoe/enoe2026_08.pdf); [Employment Indicators bulletin 634/26, 22 October 2026, table 1, p. 4; rates table 5, p. 10](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/iooe/IOE2026_10.pdf). Ratios, differences, code and figures are the author's own work. The package contains aggregate public data and no institutional logos or personal records.

See [README](README.md) for reproduction commands and [the Spanish analytical note](NOTE_ES.md) for definitions and interpretation.
