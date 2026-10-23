# Data dictionary and units

All inputs are explicitly chosen teaching assumptions. There is no empirical observation file. Each scenario changes its stated parameters permanently at time zero. Years are relative model time, with no calendar-year or country mapping.

## `data/parameters.json`

| Field | Definition and unit |
|---|---|
| `alpha` | Capital elasticity in the Cobb–Douglas production function, dimensionless |
| `depreciation` | Continuous capital depreciation rate per year |
| `labor_growth` | Continuous labor growth rate per year |
| `initial_efficiency` | Common initial labor-augmenting efficiency, normalized to 1 |
| `horizon_years` | Last sampled model year; this release uses 50 |
| `scenarios[].id` | Unique scenario key |
| `scenarios[].label` | English display name |
| `scenarios[].investment_share` | Gross investment and saving divided by output; fraction, not percent |
| `scenarios[].efficiency_growth` | Continuous growth rate of labor-augmenting efficiency per year; not total factor productivity growth |
| `parameter_status`, `time_convention`, `initial_condition` | Explanatory metadata, with no numerical role |

Baseline values match the mathematical teaching example inspected in the existing repository. Scenario changes of +0.030 in investment share and +0.005 in efficiency growth are illustrative choices added for this portfolio. Initial capital per effective worker is calculated as $(s_0/(\delta+n+g_0))^{1/(1-\alpha)}$.

## `results/paths.csv`

Unique key: `scenario,year`. Four scenarios × 51 annual samples = 204 rows. No missing values are expected; zero gaps are valid values.

| Field | Definition and unit |
|---|---|
| `scenario` | Foreign key to `scenarios[].id` |
| `year` | Years elapsed, integer 0–50 |
| `capital_per_effective_worker` | $K/(AL)$ in normalized model units; not a currency value |
| `output_per_worker_index` | $100y_s(t)/y_0(0)$; common initial output = 100 |
| `consumption_per_worker_index` | $100c_s(t)/c_0(0)$; baseline initial consumption = 100; higher-saving scenarios initially below 100 |
| `investment_per_worker_index` | $100i_s(t)/i_0(0)$; baseline initial investment = 100 |
| `instantaneous_output_growth_pct` | $100[g+\alpha\dot k/k]$, percent per year in continuous time |
| `investment_share` | Scenario input copied to each row; fraction of output |
| `efficiency_growth` | Scenario continuous efficiency-growth input per year |
| `output_gap_pct` | $100[y_s(t)/y_0(t)-1]$; denominator is same-year baseline output |
| `consumption_gap_pct` | $100[c_s(t)/c_0(t)-1]$; denominator is same-year baseline consumption |

The three indices have different initial denominators and must not be added. The underlying levels satisfy $c+i=y$; the code checks that identity before normalization.

## `results/scenario_summary.csv`

Unique key: `scenario`. Fields ending in `year_10_pct`, `year_25_pct` and `year_50_pct` select the corresponding gap from `paths.csv`. `initial_consumption_gap_pct` selects year 0. `long_run_output_growth_pct` equals $100g$ (continuously compounded percent per year). `target_capital_per_effective_worker` equals $(s/(\delta+n+g))^{1/(1-\alpha)}$; the year-50 level need not have reached it. `label` is the display label.

## `results/validation.json`

Contains the SHA256 of the exact input bytes, expected coverage and numerical residuals. Residuals use unnormalized model units and double-precision floating point. This record certifies internal arithmetic and model consistency, not empirical validity or policy causality.
