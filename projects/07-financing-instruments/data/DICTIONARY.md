# Assumptions and output definitions

## Origin and units

Every numerical input is an original **synthetic scenario assumption**. No borrower, fund, project pipeline or historical climate-loss observation is represented. Amounts are in millions of nominal USD, except fields explicitly marked `lcu`, which use a synthetic local currency. Years are relative to a single full disbursement at time 0. The default 20-year horizon covers all repayments.

The USD 100 million initial funding scale is a normalization. It does not match or propose an FRLD funding-request amount, cap or policy. No observed exchange rate, revenue projection, discount curve or market price is supplied.

## Inputs in assumptions.json

| Field | Definition |
|---|---|
| `grant_usd_m`, `loan_usd_m` | Distinct components of initial funding, summed only once. Each package provides the same total. |
| `interest_rate` | Annual fixed nominal interest on opening loan principal. Interest is paid; there is no capitalization. |
| `maturity_years` | Year of the final principal payment. |
| `principal_holiday_years` | Number of complete annual periods with no principal payment. With a value of 5, first principal is paid at the end of year 6. This explicit timing convention avoids ambiguity about a lender's definition of grace period. |
| `main_discount_rate` | 5% annual analytical discount benchmark in USD. It is not a country-specific opportunity cost. |
| `discount_rates` | Alternative annual benchmarks of 3%, 5% and 7%. |
| `baseline_fx_lcu_per_usd` | One synthetic local-currency unit per USD. A 1.25 multiplier means 25% more local currency is needed per dollar; it is not a 25% decline in the USD price of the local currency. |
| `baseline_envelope_lcu_m` | Assumed annual nominal envelope of 100 million local units. It is not measured public revenue or a debt-service ceiling. |
| `stress_start_year` | First affected annual payment and envelope; set to 6. |
| `post_stress_fx_multiplier` | 1.0 in baseline; 1.25 under currency stress. |
| `post_stress_envelope_multiplier` | 1.0 normally; 0.8 under the combined stress. |
| `timing_experiment` | Separate six-month cash-availability illustration. It does not change annual debt schedules or present values. |
| `opening_cash_buffer_usd_m` | USD 10 million available before monthly receipts/spending. |
| `monthly_spending_usd_m` | End-of-month spending needs of USD 40m, 30m, 20m, 10m, 0m, 0m. |
| `receipt_months` | Three scenarios: full USD 100m received at the beginning of month 1, 3 or 6. |

Loans amortize in equal annual principal amounts after the specified principal holiday. The final payment removes the small residual of floating-point arithmetic. No commitment fees, upfront fees, default losses, refinancing or uncertainty distributions are modeled.

## Output grains

| File | One row represents | Default rows |
|---|---|---:|
| `annual_cashflows.csv` | Funding package × relative year, including year 0 | 84 |
| `fiscal_stress.csv` | Funding package × fiscal scenario × repayment year 1–20 | 240 |
| `package_comparison.csv` | Funding package × fiscal scenario | 12 |
| `discount_sensitivity.csv` | Funding package × discount benchmark | 12 |
| `timing_cashflows.csv` | Monthly receipt scenario × month | 18 |
| `timing_sensitivity.csv` | Monthly receipt scenario | 3 |

## Calculations

- `closing_debt_usd_m = opening_debt_usd_m − principal_usd_m` for repayment years. At time 0, closing debt equals the new loan disbursement.
- `debt_service_usd_m = interest_usd_m + principal_usd_m`.
- `borrower_net_financing_cashflow_usd_m` is positive initial receipt at time 0 and negative repayment thereafter. It excludes program spending, benefits and the borrower's other finances.
- `pv_repayment_usd_m = Σ debt_service_usd_m(t) / (1 + r)^t` over years 1–20.
- `package_pv_support_pct = 100 × (initial funding − PV repayments) / initial funding`. The denominator includes grants and loans. It is an analytical measure, not the share of proceeds legally classified as a grant, a lender's recorded subsidy cost or official eligibility score. A value below zero can occur when the discount benchmark is below the loan interest rate; outputs are not capped.
- `incremental_service_envelope_pct = 100 × new-loan service in LCU / assumed annual envelope in LCU`. It does not include existing debt service, and no country debt-risk threshold is applied.
- `peak_incremental_service_envelope_pct` is the maximum over years 1–20; `first_peak_year` identifies the first year attaining that maximum. For grants all values are zero, so this convention returns year 1 without implying a payment occurs.
- `new_debt_after_year5_usd_m` is the outstanding new-loan principal after the year-5 payment.
- `unfunded_cash_position_usd_m = opening buffer + cumulative receipts − cumulative spending`, allowing a negative position to expose a gap instead of inserting unmodeled borrowing.
- `cash_shortfall_usd_m = max(0, −unfunded_cash_position_usd_m)`; its maximum is the peak temporary funding gap. Monthly gaps are not summed.

Amounts are calculated with Python floating-point arithmetic, checked with an absolute tolerance of 1e-9 million USD for repayment identities and written with ten decimals. Presentation rounds from those values; do not sum rounded percentages to reconstruct unrounded totals.
