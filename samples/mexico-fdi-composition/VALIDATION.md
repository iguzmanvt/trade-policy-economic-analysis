# Validación de la muestra nacional de IED

**Preparación y ejecución: 13 de noviembre de 2026.** Entorno de esta revisión: Linux, Python 3.12.14 y matplotlib 3.10.8. Se reutilizaron dependencias disponibles; no se instaló software. Esta revisión no se ejecutó en Windows.

## Identidad y alcance de las entradas

El extracto nacional archivado de 84 filas coincidió con su SHA-256 registrado: `b77ae3bae4f9b93469ee18af11cf43cfef9bb8bee85bd767283a0e71e98b6696`. La separación en 80 filas anuales y cuatro del semestre preservó **todos los campos de las 84 filas**. Los hashes de los nuevos archivos están en [data/sources.json](data/sources.json) y fijados además en `analyze.py`.

Se comprobaron la cobertura completa de años/componentes, claves únicas, agregado nacional, estados publicados, periodos acumulados, archivo actualizado/original, hoja, celdas y etiquetas. Todos los montos de esta selección son positivos. La muestra no incorpora desgloses territoriales ni cifras confidenciales.

La revisión anterior identificó y descargó los libros oficiales el 5-nov-2026. Sus URLs, tamaños y hashes se conservan como procedencia histórica. **En esta preparación no se descargaron otra vez los libros ni se reextrajeron sus celdas desde XLSX.** La identidad del extracto y su reconstrucción actual son controles distintos de una auditoría nueva de fuente o de precisión económica.

## Reproducción y auditoría independiente

| Control ejecutado | Resultado |
|---|---|
| Constructor con Decimal, precisión 80 | Cuatro CSV y recibo de cálculo reproducidos sin red. |
| Auditor con Fraction, sin importar el constructor | **160 filas** comprobadas: 60 participaciones anuales, tres del semestre, 76 cambios y 21 conciliaciones. |
| Modo normal y `python -O` | Los cinco archivos de salida coincidieron por bytes entre ambas ejecuciones y con los entregados. |
| Montos, cambios y residuos | Igualdad racional exacta. Mayor residuo absoluto conservado: `0.0000000000081` millones de USD. No se distribuye ni se interpreta su causa. |
| Porcentajes derivados | Tolerancia de `0.0000000000005`, limitada al redondeo a doce decimales. No representa error estadístico. |
| Revisión independiente adicional | Reprodujo ambos modos y rechazó alteraciones de participación, periodo, residuo sustituido por cero y aporte. |

## Pruebas adversas

**Trece pruebas distintas aprobaron**, tanto en modo normal como optimizado. La repetición de entorno de ejecución no duplica el número de pruebas. Los casos comprueban:

1. Rechazo de un rótulo anual aplicado al semestre.
2. Rechazo de mezcla entre libro actualizado y originalmente publicado.
3. Rechazo de clave duplicada.
4. Rechazo de componente ausente.
5. Rechazo de reserva confundida con monto publicado.
6. Rechazo de denominador cero en el contrato de esta muestra.
7. Rechazo de monto no finito.
8. Rechazo de localizador fuente incorrecto.
9. Rechazo de modificación del insumo fijado por hash.
10. Conservación de una salida existente al rechazar un destino ocupado.
11. Igualdad de reproducción y auditoría en modo normal y optimizado.
12. Rechazo independiente de una participación y un residuo alterados.
13. Rechazo de datos alterados antes de escribir figuras.

Los casos artificiales se ejecutan en directorios temporales. No agregan observaciones al conjunto económico. Véase [tests/test_validation.py](tests/test_validation.py).

## Figuras, contenido y distribución

Se generaron y abrieron las dos figuras PNG completas. La figura anual conserva 60 puntos, las fechas de inicio y cierre, escala 0–100%, estilos de línea diferenciados y etiquetas directas. Se separaron las etiquetas finales de nuevas inversiones y cuentas entre compañías tras la primera inspección; se revisó el PNG regenerado. La figura del semestre conserva tres barras, total, participaciones, cantidades, fuente y cobertura visibles. La revisión independiente confirmó la corrección de etiquetas. Los SVG se entregan como versiones vectoriales de las mismas figuras.

El generador llama al auditor de datos antes de crear la salida. La inspección visual no acredita por sí sola los números: éstos se cotejan en los CSV mediante el auditor. No se exige identidad binaria de imágenes entre versiones o entornos de renderizado. No se realizó una prueba de impresión o una interfaz móvil.

README, nota y síntesis inglesa se revisaron contra resultados y límites. La inspección del conjunto público y un barrido dirigido no encontraron nombres del repositorio de preparación, rutas del equipo, credenciales ni datos de clientes. Se revisaron los enlaces locales. Estas comprobaciones son específicas de la muestra, no una garantía universal de seguridad. Los enlaces oficiales se conservan como procedencia; no se afirma una nueva descarga exitosa de cada URL.

El [manifiesto](MANIFEST_SHA256.csv) identifica todos los archivos públicos por ruta, tamaño y SHA-256, excluido el propio manifiesto. `python -B verify_manifest.py` comprueba inventario y bytes. No se incluyen los originales XLSX, información territorial reservada, marcas institucionales ni materiales internos.
