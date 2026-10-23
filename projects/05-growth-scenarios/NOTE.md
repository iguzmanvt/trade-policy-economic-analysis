# Growth scenarios: investment, efficiency and the policy horizon

Isaac Guzmán Valdivia Tovar | 22 October 2026

## Main finding

Investment and efficiency changes have different implications for the horizon of economic policy. In the illustrative exercise here, increasing the investment share by 3 percentage points raises output per worker by 3.83% relative to baseline at year 25 and 4.72% at year 50. Raising the growth rate of labor-augmenting efficiency by 0.5 percentage points produces gaps of 11.10% and 25.34%, respectively. Combining the changes gives larger output gaps, alongside an initial consumption sacrifice from higher saving. The investment-only scenario ultimately returns to the baseline growth rate; the efficiency-growth scenario changes that rate by assumption.

These results are exact conditional calculations from a teaching model, not estimated effects of particular policies and not a forecast of Mexico. Their value for country analysis is to make a proposed growth narrative explicit: which variable changes, through what mechanism, at what cost and over what horizon?

## From existing teaching material to a reproducible exercise

The author's public *Crecimiento* course notes already develop the Solow model's balanced growth path (BGP), distinguish its level and slope, and discuss investment and population growth. The inspected version is pinned to commit `3d67d7dc98edaccbac9333be9839d0084bc5da3b`. This sample writes a new implementation of the same mathematical mechanism and adds transition paths and scenario comparisons. It does not copy the course's prose, embedded charts or code. The model's foundational contribution is attributed to Robert Solow; the accompanying [source record](SOURCES.md) distinguishes the historical model from this new implementation.

The baseline uses values present in the course notes: capital elasticity 0.30, depreciation 0.05, labor growth 0.011, investment share 0.249 and efficiency growth 0.0208. They are adopted as **illustrative teaching assumptions**. This project does not verify the historical data behind the original classroom example or treat those values as a contemporary country calibration. Initial efficiency is normalized to one, and all scenarios start with the same capital stock per effective worker, chosen to be the baseline steady state. Output per worker is normalized to 100 initially.

## Mechanism and implementation

Production is $Y=K^\alpha(AL)^{1-\alpha}$, where $K$ is capital, $L$ is labor and $A$ is labor-augmenting efficiency. Capital evolves according to $\dot K=sY-\delta K$; efficiency and labor grow continuously at constant rates $g$ and $n$. For capital per effective worker $k=K/(AL)$:

$$\dot k=s k^\alpha-(\delta+n+g)k.$$

The implementation uses an exact solution. Define $z=k^{1-\alpha}$ and $\lambda=\delta+n+g$. Then $z^*=s/\lambda$ and:

$$z(t)=z^*+[z(0)-z^*]e^{-(1-\alpha)\lambda t}.$$

This gives $k(t)$ directly and output per worker $y(t)=A_0e^{gt}k(t)^\alpha$. Annual rows sample the continuous solution, avoiding discretization error from a chosen numerical step. Consumption per worker is $(1-s)y(t)$. Every gap compares a scenario with the **same-year baseline**, rather than with its own initial value. Growth rates quoted here are continuously compounded annual rates. The efficiency-growth parameter is not total factor productivity growth: with this production function, the latter equals $(1-\alpha)g$.

Four scenarios hold every unlisted assumption fixed. The investment scenario permanently raises $s$ from 0.249 to 0.279. The efficiency scenario permanently raises $g$ from 0.0208 to 0.0258. The combined scenario imposes both changes. The changes start at time zero and carry no modeled implementation lag or separate resource cost beyond the investment scenario's lower consumption share.

## Results

Output and consumption gaps relative to the same-year baseline, percent:

| Scenario | Output, year 10 | Output, year 25 | Output, year 50 | Consumption, initial | Consumption, year 25 | Consumption, year 50 |
|---|---:|---:|---:|---:|---:|---:|
| Baseline | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| Higher investment | 2.22 | 3.83 | 4.72 | −3.99 | −0.32 | 0.54 |
| Faster efficiency growth | 3.94 | 11.10 | 25.34 | 0.00 | 11.10 | 25.34 |
| Both changes | 6.27 | 15.41 | 31.29 | −3.99 | 10.80 | 26.05 |

Source: `results/scenario_summary.csv`; author’s calculations from `data/parameters.json`. Rounded values are for presentation only.

![Illustrative output gaps relative to baseline](results/output_gaps.svg)

The higher investment scenario gradually accumulates additional capital and approaches a higher output level relative to baseline. Its long-run output-per-worker growth remains 2.08% continuously compounded, exactly as in baseline. The extra investment initially reduces consumption by 3.99%, since output cannot jump when the capital stock is fixed. Consumption is still slightly below baseline at year 25 and above it at year 50. This illustrates why higher gross investment alone is an incomplete measure of policy success.

Faster efficiency growth changes both the long-run slope and the transition. Output does not immediately jump: the common initial capital and efficiency levels keep initial output equal. Faster growth in effective labor also lowers capital per effective worker relative to what it would otherwise have been. The reported output gap therefore includes capital adjustment, rather than merely applying an extra growth rate mechanically to baseline output. In the long run, output per worker grows at 2.58% continuously compounded. That change is imposed by the scenario, not explained or estimated by the model.

## Implications for policy analysis

A near-term increase in investment may be consistent with medium-term level gains without establishing a permanently higher growth rate. A policy assessment should therefore state whether it anticipates capital deepening, a productivity-level improvement, or a sustained acceleration in efficiency growth. The last claim requires evidence beyond this framework: investment composition, adoption, skills, competition and innovation mechanisms would have to be examined empirically.

The scenario comparison is useful for disciplined sensitivity analysis. An analyst can state a proposed mechanism, change its parameter transparently and inspect the path of output and consumption. It cannot establish that the more favorable parameter path is feasible, affordable or optimal. There is no reform-to-efficiency equation, fiscal budget or empirical policy effect in this sample. A faster-efficiency scenario has no separately modeled implementation cost, so its larger gains cannot be read as a cost-benefit ranking against investment policy.

For country work, the appropriate next evidence would be the national accounts' investment composition, depreciation and capital-stock information, labor measures and productivity estimates. Those data are outside this bounded project. The completed deliverable is the reproducible mechanism and its conditional results; the link from a specific reform to the parameters remains outside the present scope.

## Reproduction and limitations

`analyze.py` produces 204 path rows, four scenario summaries, a standalone SVG figure and a validation record from one small parameter file. Checks cover key uniqueness, coverage, finite values, shared initial output, baseline stationarity, consumption-plus-investment accounting and agreement between the exact derivative and the capital-accumulation equation. All reproduction is offline with Python's standard library. This is a deterministic teaching simulation; no statistical estimation, probability distribution, confidence interval or forecast uncertainty has been fitted.
