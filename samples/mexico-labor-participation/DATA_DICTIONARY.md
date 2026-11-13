# Diccionario y procedencia

La clave de `data/enoe_counts_and_rates.csv` es `period` + `sex`. Los doce registros cubren cuatro periodos y tres categorías de sexo publicadas por INEGI; el total es una categoría de control y no debe sumarse a mujeres y hombres.

| Campo | Definición / unidad |
|---|---|
| `period` | `2025-T2`, `2026-T2`, `2025-09` o `2026-09` |
| `frequency` | `quarterly` o `monthly`; nunca se mezclan en una comparación |
| `sex` | `total`, `mujeres`, `hombres` |
| `population_15plus` | Población de 15 años y más, personas |
| `labor_force` | Población económicamente activa (PEA), personas |
| `employed` | Población ocupada, personas |
| `unemployed` | Población desocupada, personas |
| `outside_labor_force` | Población no económicamente activa, personas |
| `participation_published_pct` | Tasa publicada a una decimal: PEA / población de 15 años y más, % |
| `unemployment_published_pct` | Tasa publicada a una decimal: desocupada / PEA, % |
| `source_id` | Identificador de `data/sources.json` |

Los conteos proceden del cuadro 1 de cada fuente; las tasas, del cuadro 4 (trimestral) y del cuadro 5 (mensual). Se preserva la precisión de las publicaciones. No hay microdatos, estimaciones sintéticas ni imputaciones. Los datos son nacionales y no incorporan un ajuste estacional adicional por parte del autor.

`outputs/rates_calculated.csv` contiene razones recalculadas en porcentaje con nueve decimales de salida; esa precisión sirve para verificar las operaciones, no aumenta la precisión estadística de la encuesta. `outputs/year_on_year_changes.csv` conserva diferencias en personas y puntos porcentuales. `outputs/labor_force_bridge.csv` conserva los dos componentes contables simétricos en personas equivalentes y su residuo. Sus definiciones y fórmulas figuran en [NOTE_ES.md](NOTE_ES.md).

`data/sources.json` identifica títulos, URL, fechas de publicación, localizadores, universo y SHA-256 de los PDF. La reproducción ordinaria sólo usa el CSV. El cotejo opcional vuelve a extraer las celdas de los PDF fijados; si una fuente cambia, no se reemplaza silenciosamente la edición.
