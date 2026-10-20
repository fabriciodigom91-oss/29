# Informe de ganancias de clipping en Looker Studio

Fuente de datos: `proyeccion_clipping.csv` (exportado de la pestaña
"Proyección 12 meses" de `ganancias_clipping.xlsx`, 12 filas, una por mes).
La columna `fecha` usa enero de 2027 como mes 1; cámbiala si empiezas en otro mes.

## 1. Conectar los datos

1. Abre <https://lookerstudio.google.com> → **Crear → Informe**.
2. Conector **Subir archivos** (o primero sube el CSV a Google Sheets y usa el conector **Hojas de cálculo de Google**, así puedes actualizarlo).
3. Revisa los tipos de campo:
   - `fecha` → Fecha (AAAAMMDD)
   - `*_mxn` → Moneda (MXN) · `*_usd` → Moneda (USD)
   - `mes`, `clientes_fijos` → Número; agregación **Ninguna** para `mes`
4. Campo calculado opcional — `% ingreso de clientes`:
   `SUM(ingreso_clientes_mxn) / SUM(ingreso_bruto_mxn)` (tipo Porcentaje).

## 2. Diseño de la página (tamaño 1200 × 900)

| Fila | Componente | Configuración |
|---|---|---|
| Título | Texto | "Proyección de ganancias de clipping — 12 meses" + nota "Estimaciones, no garantías" |
| KPIs | 4 cuadros de resultados | `ganancia_neta_mxn` (SUM) · `ganancia_neta_mxn` (AVG, "Promedio mensual") · `vistas_totales` (SUM, formato compacto) · `% ingreso de clientes` |
| Gráfico 1 | Series temporales | Dimensión `fecha` (mes) · Métricas `ingreso_bruto_mxn` y `ganancia_neta_mxn` |
| Gráfico 2 | Barras apiladas | Dimensión `fecha` · Métricas `ingreso_dolares_mxn` + `ingreso_clientes_mxn` (de dónde viene el dinero) |
| Gráfico 3 | Barras apiladas | Dimensión `fecha` · Métricas `comisiones_mxn`, `impuestos_mxn`, `gastos_mxn` (costos) |
| Gráfico 4 | Combinado | `vistas_totales` (barras) + `clientes_fijos` (línea, eje derecho) |
| Tabla | Tabla con barras | Todas las columnas, ordenada por `mes`, fila de totales activada |
| Control | Control de período | Sobre `fecha`, para filtrar meses |

## 3. Hacerlo con Claude en Chrome

Con la extensión Claude in Chrome abierta en la pestaña de Looker Studio, puedes pegarle esta instrucción:

> Crea un informe nuevo en Looker Studio subiendo el archivo `proyeccion_clipping.csv`.
> Ajusta los tipos de campo según la sección 1 de esta guía y arma la página
> según la tabla de la sección 2. Antes de compartir o publicar nada, pregúntame.
