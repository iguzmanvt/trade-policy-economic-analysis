# Financing packages, repayment timing and fiscal exposure

**Isaac Guzmán Valdivia Tovar · Independent analytical sample · 26 October 2026**

This reproducible exercise compares grants and illustrative loans with the same initial funding. It separates three questions that a financing review should answer: how much cash arrives when it is needed, what future repayment obligations are created, and how those obligations respond to exchange-rate and budget pressures.

**All numerical inputs are synthetic.** This is a prospective analytical exercise, not a past client assignment, an FRLD operation, an empirical estimate of climate losses or a country debt sustainability analysis. The USD 100 million scale is a normalization; it is not an FRLD request amount or funding limit. The loan terms are illustrative and do not represent approved FRLD instruments.

## Main result

At the stated 5% annual discount benchmark, the illustrative concessional loan produces USD 63.37 million of present-value repayments for USD 100 million received initially. Its annual service jumps from USD 1.00 million to USD 7.67 million when principal repayment starts in year 6. Under a simultaneous 25% rise in the local-currency price of the dollar and 20% reduction in the assumed budget envelope, peak incremental service rises from 7.67% to 11.98% of that envelope. These are conditional cash-flow results, not risk ratings.

The separate monthly timing experiment shows why concessionality and liquidity must be reviewed separately: receiving the same USD 100 million in month 3 instead of month 1 leaves a peak USD 60 million temporary funding gap under the specified spending path and USD 10 million opening buffer. No bridge borrowing is assumed or priced.

[Read the analytical note](NOTE.md) · [Inputs and definitions](data/DICTIONARY.md) · [Comparison table](results/package_comparison.csv) · [Validation](VALIDATION.md)

![Illustrative repayment profiles and fiscal-envelope sensitivity](figures/repayment_and_fiscal_stress.svg)

## Policy context

The FRLD Governing Instrument includes grants and highly concessional loans, subject to Board policy and debt sustainability considerations. The 2026 Board report describes the Barbados Implementation Modalities (BIM) as a first set of grant interventions for 2025–2026. These have different policy status: this exercise explores possible financing trade-offs and does not imply that its loan packages are available under BIM. See the dated primary-source register in [sources.json](sources.json).

## Reproduce

Python 3.11 or later; calculations and tests use only the standard library, local synthetic inputs and no network access. Commands work from any current directory when the script path is supplied.

```bash
python projects/07-financing-instruments/analyze.py
python projects/07-financing-instruments/tests/test_model.py
```

To regenerate the optional static figure:

```bash
python -m pip install -r projects/07-financing-instruments/requirements-figure.txt
python projects/07-financing-instruments/build_figure.py
```

If working in this directory directly, omit `projects/07-financing-instruments/` from each command. Core execution does not regenerate the figure and requires no plotting package.

## Scope and reuse

The package contains four funding options, three fiscal scenarios, three discount benchmarks and a separate three-case disbursement-timing experiment. It produces 84 annual cash-flow rows, 240 fiscal-sensitivity rows, 12 comparison rows, 12 discount-sensitivity rows and 18 monthly cash-flow rows plus three timing summaries.

The framework can be populated with verified term sheets and a country macro-fiscal framework after appropriate review. Such use would additionally require debt stocks, existing service, revenue projections, contingent liabilities, disbursement conditions, legal authority, fiduciary capacity and implementation evidence. A low modeled repayment cost does not establish country affordability, eligibility, value for money or the suitability of borrowing to respond to loss and damage.
