# Diccionario y criterios de cálculo

La inversión extranjera directa (IED) incluida es un **flujo neto nacional notificado**, expresado en millones de dólares estadounidenses corrientes. Los tres componentes son «Nuevas inversiones», «Reinversión de utilidades» y «Cuentas entre compañías». `TOTAL` es un rol asignado al agregado publicado; no es un cuarto componente.

## Entradas

Ambos CSV conservan doce campos y las etiquetas del extracto:

| Campo | Interpretación |
|---|---|
| `segmento` | `anual_actualizada` o `semestre_2026_original`. |
| `anio` | Año; no convierte el registro de 2026 en total anual. |
| `periodo_origen` | `AAAA-4` para cierre anual; `2026-2` para enero–junio. Son acumulados, no trimestres aislados. |
| `entidad_origen` | `Total general`, agregado nacional; «origen» describe la etiqueta procedente del libro, no un país de origen. |
| `tipo_inversion` | Uno de los tres componentes o el rol `TOTAL`. |
| `ied_mdd` | Lexema decimal extraído del valor XML; se mantiene como texto numérico en CSV. |
| `estado` | `publicado` en todas las filas de esta selección. |
| `archivo_fuente` | `tipo_actualizado.xlsx` o `tipo_original.xlsx`, asociados a URL y hash en `sources.json`. |
| `hoja`, `celda` | Hoja literal y dirección Excel exacta. |
| `etiqueta_fila` | Etiqueta literal de la fuente, incluida «Total general». |
| `formula_fuente` | Vacío: las celdas seleccionadas contenían valores, no fórmulas almacenadas. |

Los 80 montos anuales y cuatro semestrales son positivos y publicados en la muestra fijada. El programa rechaza ceros, negativos, reservas y claves ajenas porque cambian ese contrato; esto **no afirma** que tales casos sean imposibles en la estadística general. Ampliar la muestra exige revisar datos, hashes y métodos, no reutilizarla automáticamente. La selección omite los desgloses estatales: no contiene ni permite inferir las reservas territoriales.

## Resultados

| Archivo | Filas | Campos y unidades principales |
|---|---:|---|
| `annual_shares.csv` | 60 | Tres componentes × veinte años; monto, total publicado, participación porcentual y localizadores de numerador y denominador. |
| `snapshot_2026s1.csv` | 3 | Los mismos campos para enero–junio de 2026, separados del archivo anual. |
| `annual_changes.csv` | 76 | Diecinueve pares de años consecutivos × cuatro roles; base, actual, cambio, tasa propia y aporte al crecimiento total. El aporte de `TOTAL` queda vacío. |
| `reconciliation.csv` | 21 | Total publicado, suma de tres componentes y residuo exacto por periodo y segmento. |

`amount_usdm`, `published_total_usdm`, `base_usdm` y `current_usdm` conservan las cadenas originales. Los cambios y residuos se calculan con aritmética decimal de precisión 80. Las participaciones, tasas y aportes se redondean a doce decimales con `ROUND_HALF_UP` como decisión de salida; las etiquetas gráficas usan una decimal y la nota emplea una o dos según la medida.

```
share_pct = 100 × amount_usdm / published_total_usdm
change_usdm = current_usdm − base_usdm
component_growth_pct = 100 × change_usdm / base_usdm
contribution_total_growth_pp = 100 × component_change_usdm / previous_published_total_usdm
residual_usdm = published_total_usdm − sum(three_components)
```

Los aportes son puntos porcentuales del crecimiento nominal de la IED, no del PIB. Los residuos se clasifican como `exact` sólo si son exactamente cero; en otro caso permanecen `residual_preserved`. No se asigna causa a las diferencias ni se usa el redondeo visual como prueba de precisión estadística.

El auditor independiente usa `Fraction`, sin importar el constructor. Exige igualdad exacta para montos, cambios y residuos. Sólo tolera hasta `0.0000000000005` en porcentajes derivados, correspondiente al redondeo a doce decimales. Esa tolerancia de representación no es una cota de error económico.
