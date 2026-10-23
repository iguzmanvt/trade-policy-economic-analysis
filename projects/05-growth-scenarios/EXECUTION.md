# Execution record

Prepared for the 22 October 2026 information cutoff.

## Executed

```bash
python projects/05-growth-scenarios/analyze.py
```

Environment: Python 3.12.14. The script also supports Python 3.11+ and imports only the standard library. The actual run exited with code 0 and returned `status: passed`.

Generated files: `results/paths.csv`, `results/scenario_summary.csv`, `results/output_gaps.svg` and `results/validation.json`.

| Check | Executed result |
|---|---|
| Scenario × year coverage | 4 × 51 = 204 rows |
| Duplicate scenario/year keys | 0 |
| Finite numerical values | Passed |
| Shared initial capital and output | Passed |
| Baseline stationary capital per effective worker | Passed for every sampled year |
| Exact derivative versus capital-accumulation equation | Maximum absolute residual $1.32\times10^{-16}$ |
| Consumption plus investment equals output | Maximum absolute residual $4.44\times10^{-16}$ |
| Parameter-file SHA256 | `377e5cab03428bf04f9a86ff3a373b27bfffc39b1441bc4aeb731ffff2a992d4` |
| SVG geometry and readability | Exported to a temporary PNG with Inkscape and visually inspected; four lines, visible axes, complete legend and no clipping |

The temporary PNG is an internal preview and is excluded from the repository. The delivered SVG is generated directly from the same path rows as the CSV.

## Not claimed

The entire historical teaching repository was not run or audited. External Plotly embeds and the original classroom estimates were not refreshed. No model estimation, country forecast, policy-effect identification or optimal-policy calculation was performed. The existing repository was read only and remains unchanged.
