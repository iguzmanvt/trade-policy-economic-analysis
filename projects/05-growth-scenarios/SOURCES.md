# Sources, prior work and authorship

Information cutoff: 22 October 2026. No later statistical release is used; all simulated dates are relative model years.

| Source | Exact locator | Use in this project | Verification |
|---|---|---|---|
| Isaac Guzmán, *Crecimiento* public teaching repository | [Repository](https://github.com/iguzmanvt/Crecimiento), [pinned commit 3d67d7dc98edaccbac9333be9839d0084bc5da3b](https://github.com/iguzmanvt/Crecimiento/commit/3d67d7dc98edaccbac9333be9839d0084bc5da3b), committed 26 June 2025 | Establishes the pre-existing teaching work and model scope | Full recursive tree, commit metadata and selected source files inspected through GitHub plugin |
| *Crecimiento Economico 2 Nota.Rmd* | [Pinned source](https://github.com/iguzmanvt/Crecimiento/blob/3d67d7dc98edaccbac9333be9839d0084bc5da3b/Clases_Crecimiento_Economico/Solow/Crecimiento%20Economico%202%20Nota.Rmd); section **Estudios de caso usando el modelo de Solow**, U.S. example; Git blob `39267ed7b55d42e0beae2a3e3edb4bafd6b0a3ed` | Balanced-growth mechanism and baseline parameter values 0.30, 0.05, 0.011, 0.249 and 0.0208 | Full UTF-8 content inspected; embedded Plotly charts were not revalidated or copied |
| *Crecimiento Economico 2.Rmd* | [Pinned source](https://github.com/iguzmanvt/Crecimiento/blob/3d67d7dc98edaccbac9333be9839d0084bc5da3b/Clases_Crecimiento_Economico/Solow/Crecimiento%20Economico%202.Rmd); Git blob `511f8bcd73fa0a2c85094d7e67a7453f1ec1b835` | Confirms the same model was developed in the presentation material | Full UTF-8 content inspected; slides not reproduced |
| Robert M. Solow (1956), “A Contribution to the Theory of Economic Growth,” *The Quarterly Journal of Economics* 70(1), 65–94 | [Publisher and DOI](https://doi.org/10.2307/1884513); [reading copy hosted by UNAM](https://www.depfe.unam.mx/doctorado/teorias-crecimiento-desarrollo/solow_1956.pdf), printed pp. 66–69, model and capital/labor dynamics | Foundational model attribution | Publisher bibliographic record and relevant paper pages read; no paper PDF or passage redistributed |

## New contribution and adaptations

`analyze.py`, the English prose, data dictionary and generated chart are newly written for this portfolio. The code independently implements the standard mathematical model and its closed-form transition. The new scenario choices are disclosed in the input file. Model equations and numerical assumptions are distinguished from authored text or code; neither the original course source files nor third-party course images are copied.

The baseline values are reused as teaching inputs. They are not independently verified historical estimates. The original notes include rounded intermediate arithmetic and a historical efficiency normalization; this release consistently uses `g=0.0208` and the explicit normalization `A0=1`, and makes no attempt to reproduce their historical chart levels. This is a documented extension, not a claim that the original source contained the new Python simulation or scenario results.

## Rights and release treatment

No README or license file was present at the root of the inspected recursive source tree, and no license file was found in that tree. Public availability alone is not an open-source license. The existing repository is linked without changing or relicensing it. All course files, third-party figures, external embeds and article copies are excluded from this new package. No blanket license is asserted over external material. Public dissemination of the independently prepared portfolio was authorized by the author on 22 October 2026; the source-material exclusions and attribution conditions remain in effect.
