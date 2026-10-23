# Shared Census data contract and flow bridge

This directory supports P01 and the two perspectives of P02. It is shared documentation and reconciliation code, **not an additional portfolio project**.

| Layer | Question / dimension | Statistical flow and partner coverage | Product universe | Period and included input |
|---|---|---|---|---|
| [P01 — observed duty intensity](../01-observed-duty-intensity/README.md) | How do calculated-duty ratios differ across suppliers within the same product? | U.S. imports for consumption; Mexico, China, Taiwan, Vietnam and Malaysia | Three exact ten-digit Harmonized Tariff Schedule (HTS10) lines | January–August 2025 and 2026; 30 archived aggregates |
| [P02A — partner concentration](../02-trade-concentration/README.md) | How concentrated are U.S. suppliers and destinations, and how much trade involves Canada and Mexico? | U.S. general imports and total exports, analyzed separately; individual foreign partners | All reported merchandise products retained in the archived partner extract | January–August 2023–2026; 1,846 partner–flow–period totals |
| [P02B — product-basket concentration](../02-trade-concentration/product-basket/README.md) | Which products account for concentration and change within a fixed research basket? | U.S. general imports from Mexico | Frozen selection of 374 historical HTS10 lines grouped into 88 Harmonized System six-digit (HS6) categories | January–August 2025 and 2026; 4,794 reported monthly rows |

Partner and product Herfindahl–Hirschman Index (HHI) measures use different dimensions and denominators. Do not combine them into one time series, add their trade values or interpret their changes as inconsistent revisions. All layers preserve their own archived statistical vintages; none is a newly certified live Census release.

See [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for fields, denominators and absence conventions and [SOURCES.md](SOURCES.md) for public definitions and provenance. The core computations use included inputs and the Python standard library; no network, account or package installation is required.

## Flow bridge

From the portfolio root:

```bash
python projects/census-common/reconcile_flows.py
```

Or run `python reconcile_flows.py` from this directory. Paths resolve relative to the script. It reads the canonical P01 consumption aggregate and the P02B general-import monthly panel and writes [six product–period comparisons](results/flow_comparison.csv) for Mexico. The general-minus-consumption difference is a comparison of flows, not additional trade or an estimated warehouse balance. Values are neither summed across flows nor forced to equality. The bridge does not use or alter P02A's partner extract.

## Version and validation boundaries

The P01 snapshot remains byte-identical to its earlier input. Its 240 upstream monthly consumption observations were documented previously, but are not included or revalidated by this support code. P02B's general-import rows are a separate recovered input; their presence does not authenticate P01's missing monthly rows. The bridge checks eight months only for the three matched P02B general-import series.

P02A inherits coverage checks for its own partner extract. Its absent-partner convention for a signed change decomposition does not establish completeness of P02B's sparse code-month panel. A new hash and an explicit change record are required before replacing any input. Never append monthly and year-to-date totals as additional observations of trade.

No layer estimates legal tariff entitlement, domestic value added, final use, production relocation, transshipment or a causal tariff effect.
