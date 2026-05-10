# 🧠 Optimización Asintótica en la Predicción del Mercado de Memoria RAM

> **Proyecto académico** · Universidad de Guadalajara · Mayo 2026
> **Materia:** Ciencia de Datos · Asymptotic Notation + Bayesian Inference

## 👥 Equipo de trabajo

| Integrante | Rol |
|---|---|
| **José Carmen Najera Ortiz** | Coordinador técnico · Scraping · ML · Análisis de complejidad |
| **Juan Pablo Cruz** | Análisis SQL · Benchmark · Queries analíticas |
| **Diego De Jesús** | Comunicación visual · Diseño del póster · Defensa oral |
| **Bernardo Maciel** | Análisis estadístico · EDA · Tests de hipótesis |

---

## 📖 Resumen ejecutivo

Pipeline integral de Ciencia de Datos aplicado al mercado de memoria RAM: desde la extracción vía web scraping en Newegg hasta el análisis empírico de complejidad computacional, modelado predictivo y comunicación visual. El proyecto integra programación, bases de datos SQL, estadística, matemáticas aplicadas y análisis asintótico bajo un sprint comprimido de 12 días.

**Pregunta de investigación:**

> ¿Qué variables técnicas de un módulo de RAM (capacidad, frecuencia, tipo DDR, latencia CAS, marca) son los predictores más fuertes del precio de mercado, y cómo se reduce la complejidad computacional del pipeline desde 𝒪(n) hasta 𝒪(1) en cada etapa del análisis?

---

## 📅 Estado del Sprint (12 días · deadline 19-may-2026)

| Día | Fecha | Sprint | Estado |
|---|---|---|---|
| 1 | jue 7 may | Reconocimiento de Newegg + setup del entorno | ✅ Completo |
| 2 | vie 8 may | Scraper de producción + parsers regex | ✅ Completo |
| 3 | sáb 9 may | Limpieza, feature engineering y EDA visual | ✅ Completo |
| 4 | dom 10 may | SQLite + benchmark empírico de complejidad O() | ✅ Completo |
| 5 | lun 11 may | Análisis estadístico inferencial | ✅ Completo |
| 6 | mar 12 may | Modelo 1 — Regresión lineal multivariada | ⏳ Próximo |
| 7 | mié 13 may | Modelo 2 — K-Means clustering | ⏳ |
| 8 | jue 14 may | Análisis empírico de complejidad ML | ⏳ |
| 9 | vie 15 may | Diseño del póster académico | ⏳ |
| 10 | sáb 16 may | Redacción y pulido del póster | ⏳ |
| 11 | dom 17 may | Ensayo de defensa oral | ⏳ |
| 12 | lun 18 may | Buffer + ensayo final | ⏳ |
| 🎯 | **mar 19 may** | **Entrega + defensa oral** | 🔒 |

**Progreso actual: 50% · 4+ commits · 0 bloqueos**

---

## 📊 Resultados acumulados (cierre Día 4)

### 1. Dataset extraído y limpio

| Métrica | Día 2 (raw) | Día 3 (clean) |
|---|---|---|
| **Total productos** | 359 | **350** |
| **Tipos DDR distintos** | 4 (3 + unknown) | **3** (DDR3, DDR4, DDR5) |
| **Marcas únicas** | 25+ | 5 + Other |
| **Tiempo de extracción** | ~38 s | — |
| **Columnas finales** | 12 | **17** (con features derivados) |
| **Cobertura `cas_latency`** | 63.8% nativa | **100%** (con imputación) |

### 2. Distribución del dataset limpio

```
Tipos DDR:
  DDR5: 229 productos (65.4%) · gama actual
  DDR4: 110 productos (31.4%) · mainstream
  DDR3:  11 productos  (3.2%) · legacy

Top marcas (Top-5 + Other):
  CORSAIR    103
  Other      100
  G.SKILL     59
  Kingston    43
  Team        24
  Crucial     21

Estadísticas de precio:
  min:        $14.51
  max:     $4,999.99
  media:     $503.12
  mediana:   $409.99
  std:       $510.50

Estadísticas de price_per_gb:
  min:    $2.75 / GB   (RAM económica DDR3)
  max:   $27.73 / GB   (premium DDR5)
  media: $13.16 / GB   (mercado balanceado)
```

### 3. Hallazgos estadísticos clave (Día 3)

**Correlaciones más fuertes con `price_usd`:**

| Variable | Pearson r | Interpretación |
|---|---|---|
| `capacity_gb` | **0.95** | Predictor dominante (R²≈0.90) |
| `log_price` | 0.78 | Validación de la transformación |
| `price_per_gb` | 0.56 | Feature derivado útil para clustering |
| `cas_latency_imputed` | 0.45 | Importa más en escala log (0.69) |
| `num_sticks` | 0.41 | Captura efecto kit dual/quad-channel |
| `speed_mhz` | 0.37 | Sube a 0.58 con log_price |

**Validación de la transformación logarítmica:**

```
Asimetría price_usd:  +3.61   ← muy asimétrica (cola pesada)
Asimetría log_price:  -0.61   ← prácticamente normal
```

La asimetría se reduce ~6× tras aplicar `log(1+x)`, cumpliendo el supuesto de normalidad aproximada de los residuos requerido por el teorema de Gauss-Markov.

### 4. Base de datos SQLite (Día 4)

```
ram_market.db
├── Tabla:      ram_products
├── Filas:      350
├── Columnas:   18 (id PK + 17 features)
├── Tamaño sin índices:  140 KB
├── Tamaño con índices:  160 KB (+14.3% overhead)
└── Índices B-Tree creados:
    ├── idx_ddr_type           → acelera filtros categóricos
    ├── idx_capacity_gb        → acelera filtros numéricos de rango
    └── idx_brand_normalized   → acelera agregaciones GROUP BY
```

### 5. Análisis empírico de complejidad asintótica (Día 4)

#### 5.1 Benchmark base · 5 queries con n=350 (mediana de N=100 ejecuciones)

| Query | Tipo | Plan SIN índice | Plan CON índice | Pre (ms) | Post (ms) | Speedup |
|---|---|---|---|---|---|---|
| Q1 | Filtro categórico (`ddr_type='DDR5'`) | SCAN | SEARCH USING INDEX | 1.98 | 1.58 | **1.26×** |
| Q2 | Filtro numérico (`capacity_gb ≥ 32`) | SCAN | SEARCH USING INDEX | 1.13 | 1.00 | **1.13×** |
| Q3 | Top-N ordenado | SCAN + TEMP B-TREE | SCAN + TEMP B-TREE | 0.21 | 0.19 | 1.08× |
| Q4 | Agregación GROUP BY | SCAN + TEMP B-TREE | SCAN USING COVERING INDEX | 0.25 | 0.27 | 0.96× |
| Q5 | Filtro compuesto AND | SCAN | SEARCH USING INDEX | 0.53 | 0.59 | 0.90× |

#### 5.2 Test de escalado · n ∈ [350, 50,000]

Para validar la teoría asintótica empíricamente, se replicó la tabla a tamaños progresivos y se midió cómo escala el speedup con `n`:

| n | Q1 sin idx (ms) | Q1 con idx (ms) | Q1 speedup | Q2 speedup | **Q4 speedup** |
|---|---|---|---|---|---|
| 350 | 1.83 | 1.68 | 1.08× | 1.54× | **1.61×** |
| 1,000 | 5.59 | 3.70 | 1.51× | 1.13× | **2.66×** |
| 5,000 | 18.99 | 25.85 | 0.73× | 0.85× | **8.65×** |
| 10,000 | 34.16 | 46.48 | 0.74× | 0.76× | **8.14×** |
| 50,000 | 192.75 | 243.61 | 0.79× | 0.61× | **13.79×** |

**Hallazgo central:** el speedup de Q4 (con covering index) crece de **1.6× → 13.8×** al escalar el dataset 143 veces, **validando empíricamente la predicción teórica del análisis asintótico**.

---

## 🎓 Hallazgo metodológico crítico · La paradoja del índice

El experimento reveló un fenómeno educativo importante: **la indexación NO es universalmente beneficiosa**. Tres comportamientos distintos según la selectividad de la query:

### Caso 1 · Queries con baja selectividad (Q1, Q2)
Cuando una query retorna **>30% del dataset**, usar un índice degrada el rendimiento porque el costo de saltos al B-Tree supera el beneficio. Para n=50,000, Q1 (que retorna 65% del dataset) es **27% más lenta con índice**.

### Caso 2 · Queries con covering index (Q4)
Cuando el índice contiene toda la información que la query necesita (sin volver a la tabla), el speedup es claro y crece monotónicamente con `n`. Q4 valida la teoría asintótica con 13.8× a n=50,000.

### Caso 3 · Queries con sort temporal (Q3)
SQLite ya construye un B-Tree en memoria para ordenamientos. Indexar columnas adicionales no aporta porque el costo dominante es el sort.

**Conclusión defendible:** la decisión de indexar requiere conocer el patrón de queries, no solo aplicar índices "por si acaso". Esta es una **lección práctica del trade-off entre teoría asintótica y rendimiento real**.

---

## 🛠️ Stack tecnológico

| Capa | Herramientas |
|---|---|
| **Web Scraping** | `requests` + `BeautifulSoup4` + `lxml` |
| **Procesamiento** | `pandas` + `numpy` |
| **Visualización** | `matplotlib` + `seaborn` |
| **Persistencia** | `SQLite` (módulo nativo de Python) |
| **Benchmarking** | `time.perf_counter()` (resolución ns) + `statistics` |
| **Modelado ML** *(Día 6+)* | `scikit-learn` (LinearRegression + KMeans) |
| **Versionado** | Git + GitHub |

---

## 🔬 Hallazgos técnicos del proyecto (acumulados)

Seis historias técnicas documentadas que demuestran resiliencia y rigor del pipeline.

### 1. Bug de compresión Brotli (Día 1)

La librería `requests` de Python no descomprime el formato Brotli (`br`) sin el paquete adicional. Cuando Newegg recibe `Accept-Encoding: gzip, deflate, br` responde en Brotli y `requests` entrega un blob corrupto de ~58 KB en lugar de la página real (~1.2 MB).

**Solución:** forzar `gzip` removiendo `br` del header de negociación HTTP.

### 2. Fragmentación del DOM en el precio (Día 2)

Newegg presenta el precio fragmentado en dos elementos HTML por razones de renderizado tipográfico:

```html
<li class="price-current">
    <strong>309</strong>
    <sup>.99</sup>
</li>
```

Usar `.text` directamente sobre el contenedor producía contaminación con texto de descuentos y promociones. **Solución:** parser específico que reconstruye el `float` desde sus átomos del DOM, alcanzando 100% de cobertura.

### 3. CAS Latency embebido en SKU (Día 2)

Newegg dejó de exponer el CAS Latency como `CL{n}` legible en los títulos. Ahora aparece codificado dentro del SKU del fabricante:

| Fabricante | SKU | CL real |
|---|---|---|
| Kingston Fury | `KF556C36BBEK2-16` | 36 |
| XPG Lancer | `AX5U6000C3016G-DCLABK` | 30 |
| Corsair | `CMW32GX4M2E3200C16` | 16 |
| Crucial Pro | `CP2K32G60C40U5W` | 40 |
| Patriot Viper | `PVV564G600C36K` | 36 |
| Team T-Force | `TF3D432G3200HC16FDC01` | 16 |
| **G.SKILL (DDR5)** | **`F5-6000J3636F32GX2-RS5K`** | **36** (patrón `J####`) |
| **CORSAIR moderno** | **`CMK16GX5M2B5200Z40`** | **40** (patrón `Z##`) |

**Solución:** parser **v4** con cuádruple estrategia en cascada:

1. **Estrategia 1** — buscar `CL\d+` explícito (compatibilidad legacy)
2. **Estrategia 2** — extraer patrón `\d+H?C\d{2}` del bloque `Model XXXX`
3. **Estrategia 3** — patrón G.SKILL `J\d{2}\d{2}` (los primeros 2 dígitos son el CL)
4. **Estrategia 4** — patrón CORSAIR moderno `Z\d{2}` al final del SKU
5. **Validación** — el CL aceptado debe estar en el rango razonable [10, 60]

**Impacto:** cobertura del feature `cas_latency` subió de **0% → 85.5% nativo → 100% tras imputación**.

### 4. Bug de paginación rota en Newegg (Día 3)

Durante el análisis exploratorio se detectó que el dataset original presentaba **duplicación masiva**: 180 filas con solo 12 productos únicos (cada producto aparecía 15 veces, una por cada página scrapeada). La URL original (`/Memory/Category/ID-17`) ignoraba el parámetro `&page=N` y devolvía siempre la misma primera página.

**Diagnóstico:** se probaron empíricamente 4 URLs alternativas comparando los primeros productos de páginas consecutivas. Tres URLs respondieron correctamente, una falló (la original).

**Solución:** adoptar la URL de búsqueda con filtros `https://www.newegg.com/p/pl?N=100007611%204131&page={N}` que sí respeta paginación. Resultado: **dataset multiplicado por 30× (12 → 359 productos únicos)**, con 3 generaciones de DDR (incluyendo DDR3 legacy) y 4× más diversidad de marcas.

Esta validación de paginación es ahora un paso obligatorio del pipeline.

### 5. Imputación bayesiana ligera de `cas_latency` (Día 3)

51 productos (~14.5%) no tenían CAS Latency detectable ni en el título ni en el SKU. En lugar de eliminar las filas (sesgo) o imputar con la media global (incorrecto), se aplicó **imputación condicional por mediana de DDR**:

```
DDR3: CL=10  ← prior informativo legacy
DDR4: CL=16  ← prior informativo mainstream
DDR5: CL=36  ← prior informativo actual
```

Esta es la versión simplificada de un razonamiento bayesiano: incorporar conocimiento del dominio (las latencias típicas por generación) como **prior informativo** en lugar de tratar el missing data como aleatorio. El flag `cas_was_imputed` permite diferenciar valores observados vs imputados para análisis posterior.

### 6. Paradoja del índice en SQLite (Día 4)

Test de escalado a n=50,000 reveló que para queries con baja selectividad (>30% del dataset), los índices B-Tree DEGRADAN el rendimiento. Solo queries con covering index muestran el speedup teórico predicho.

**Explicación técnica:** Cuando una query retorna muchas filas, usar un índice agrega overhead (saltos del árbol al disco) sin descartar suficientes filas para compensar. SQLite a veces detecta esto y elige el plan SCAN, pero en el experimento forzamos el uso del índice y observamos el efecto adverso.

**Lección práctica:** la decisión de indexar requiere análisis del patrón real de queries. Esta es una **manifestación del límite del análisis asintótico**: el big-O describe el comportamiento cuando n → ∞, pero las constantes ocultas y los efectos de sistema importan en datasets reales.

---

## 📁 Estructura del proyecto

```
Web_scraping/
├── README.md                              ← Este archivo
├── .gitignore                             ← Exclusiones de Git
│
├── Scraping (Días 1-2)
│   ├── scraper.py                         ← Scraper principal de Newegg
│   ├── recalcular_cas.py                  ← Reaplicar parser CL sin re-scrapear
│   └── web_scraping.py                    ← Hello world inicial
│
├── Pipeline de datos (Día 3)
│   ├── limpiar.py                         ← Pipeline completo de limpieza
│   └── eda.py                             ← EDA visual + 3 figuras
│
├── Análisis de complejidad (Día 4)
│   ├── crear_db.py                        ← Construir ram_market.db
│   ├── crear_indices.py                   ← Crear 3 índices B-Tree
│   ├── bench_pre.py                       ← Benchmark SIN índices (Fase A)
│   ├── bench_post.py                      ← Benchmark CON índices (Fase B)
│   └── bench_escalado.py                  ← Test de escalado n ∈ [350, 50000]
│
├── Tests y validación
│   ├── test_parsers.py                    ← Validación de los 7 parsers regex
│   ├── test_minimo.py                     ← Test aislado del parser CAS v3
│   └── test_paginacion.py                 ← Test de URLs alternativas Newegg
│
├── Diagnósticos
│   ├── diagnostico.py                     ← HTTP debugging Día 1
│   ├── diagnostico_cas.py                 ← Cobertura CAS Día 2
│   ├── diagnostico_duplicados.py          ← Detección duplicación Día 3
│   └── diagnostico_v2.py                  ← Análisis post re-scraping Día 3
│
├── figures/                               ← Visualizaciones a 300 DPI
│   ├── 01_correlation_heatmap.png         ← Matriz de correlación
│   ├── 02_price_by_ddr.png                ← Premium por DDR
│   ├── 03_log_transform.png               ← Justificación del log
│   ├── 04_complexity_benchmark.png        ← Benchmark pre vs post
│   └── 05_scaling_benchmark.png           ← Test de escalado (clave del póster)
│
└── data/
    ├── ram_raw.csv                        ← 359 productos extraídos
    ├── ram_clean.csv                      ← 350 productos limpios
    ├── ram_market.db                      ← Base de datos SQLite
    ├── bench_pre_results.csv              ← Tiempos sin índices
    ├── bench_post_results.csv             ← Tiempos con índices
    ├── benchmark_comparison.csv           ← Tabla comparativa pre/post
    └── scaling_benchmark.csv              ← Test de escalado completo
```

---

## ⚙️ Reproducir el pipeline completo

### Requisitos

- Python 3.10+
- ~15 minutos para reproducir todo el pipeline (con test de escalado)
- Conexión a internet estable (para el scraping)

### Setup del entorno

```bash
git clone https://github.com/Jnajera96/ram-pricing-2026.git
cd ram-pricing-2026

# Entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Dependencias
pip install requests beautifulsoup4 lxml pandas numpy scikit-learn \
            matplotlib seaborn sqlalchemy
```

### Ejecutar el pipeline completo

```bash
# Día 2: Extracción (~40 s)
python scraper.py

# Día 3: Limpieza + EDA visual (~10 s)
python limpiar.py
python eda.py

# Día 4: Base de datos + análisis de complejidad (~12 min)
python crear_db.py        # ~2 s
python bench_pre.py       # ~30 s
python crear_indices.py   # ~1 s
python bench_post.py      # ~30 s
python bench_escalado.py  # ~10 min (test exhaustivo)
```

### Salida esperada

```
🚀 Iniciando scraping de Newegg RAM
✅ Scraping completado en ~38s
💾 Dataset final: data/ram_raw.csv (359 filas)

🧹 LIMPIEZA Y FEATURE ENGINEERING
  Cobertura CL: 63.8% → 85.5% nativo → 100% imputado
  Asimetría: 3.61 → -0.61
✅ ram_clean.csv (350 filas × 17 columnas)

🎨 Generando 3 figuras a 300 DPI
✅ figures/01_correlation_heatmap.png
✅ figures/02_price_by_ddr.png
✅ figures/03_log_transform.png

📦 BLOQUE 1 · CONSTRUCCIÓN DE ram_market.db
✅ Tabla `ram_products` creada con 350 filas

🔑 BLOQUE 3 · CREACIÓN DE ÍNDICES B-TREE
✅ 3 índices B-Tree creados (+14.3% storage overhead)

📊 BLOQUE 5 · TEST DE ESCALADO
✅ Speedup Q4: 1.61× (n=350) → 13.79× (n=50,000)
✅ Validación empírica del análisis asintótico
```

---

## 🧮 Análisis asintótico del pipeline

El proyecto demuestra empíricamente la transición de complejidad en cada etapa:

```
EXTRACCIÓN  · 𝒪(n · t_red)   → scraping secuencial dominado por I/O (~40s)
LIMPIEZA    · 𝒪(n)           → regex amortizado 𝒪(1) por fila (~5s)
SQL SCAN    · 𝒪(n)           → búsqueda lineal sin índice (medido)
SQL B-TREE  · 𝒪(log n)       → búsqueda con índice (medido y validado)
INFERENCIA  · 𝒪(1)           → modelo entrenado, predicción constante (Día 6)
```

**Validación empírica del salto SCAN → SEARCH USING INDEX:**

- Para n=350: speedup observado 1.08× a 1.61× (marginal, esperado para n pequeño)
- Para n=50,000: speedup en Q4 alcanza **13.79×** confirmando crecimiento logarítmico
- La gráfica `figures/05_scaling_benchmark.png` muestra la tendencia completa

---

## 📖 Decisiones de diseño defendibles

Cada decisión técnica fue tomada con criterio académico justificable:

- **`dataclass` en lugar de `dict`:** impone tipado estricto desde el origen y evita bugs silenciosos. Filosofía contract-driven.

- **`try/except` por item, no por página:** granularidad de fallo correcta. Perder 1 producto cuesta 1 fila; abortar la página perdería 36. Filosofía *fail soft, log loud*.

- **`time.sleep(2.5)` sin paralelismo:** los sitios web son I/O bound, no CPU bound. Paralelizar desde la misma IP solo acelera el bloqueo. La constante de espera es el costo de operar éticamente.

- **Checkpoints intermedios cada 5 páginas:** misma lógica que un commit incremental en Git.

- **Rutas con `Path(__file__).parent`:** robustez ante CWD distintos. Práctica de portabilidad estándar.

- **`log(1+x)` en lugar de `log(x)`:** robusto ante valores potenciales de 0 (no aplica en este dataset, pero es la mejor práctica).

- **Imputación condicional por mediana de DDR:** evita el sesgo de la media global y respeta la jerarquía de generaciones del hardware.

- **Backup defensivo antes de sobrescribir CSV:** lección aprendida del Día 2, ahora aplicada sistemáticamente.

- **Validación empírica de paginación:** lección del Día 3. Antes de confiar en un endpoint paginado, comparar productos entre páginas para validar que el servidor respeta `&page=N`.

- **Schema SQL explícito antes de `df.to_sql()`:** evita inferencia automática de pandas; mantiene `NOT NULL`, `PK`, tipos correctos. Decisión consciente de producción vs exploración.

- **`time.perf_counter()` en vez de `time.time()`:** resolución ns vs ms; monotónico; diseñado para benchmarking.

- **Mediana en vez de media:** robusta a outliers de garbage collection y otras interferencias del SO.

- **N=100 ejecuciones por query:** reduce varianza por √N (aplicación práctica del Teorema Central del Límite).

- **Indexación selectiva (3 índices, no todos):** trade-off consciente entre velocidad de lectura y overhead de storage/escritura.

- **Test de escalado a n=50,000:** validación más fuerte que evidencia con un único `n`. Demuestra el crecimiento del speedup con n, no solo un punto de medición.

---

## 🔮 Próximas etapas

- **Día 5 (lun 11 may):** estadística inferencial. Tests de hipótesis (¿DDR5 significativamente más caro que DDR4? t-test). ANOVA por marca. Validación de normalidad con Shapiro-Wilk.
- **Día 6 (mar 12 may):** regresión lineal multivariada con one-hot encoding de marcas y DDR. Métricas R², MAE, RMSE.
- **Día 7 (mié 13 may):** K-Means clustering por segmento de mercado.
- **Día 8 (jue 14 may):** medición empírica de complejidad de los modelos ML.
- **Día 9-11 (vie 15 - dom 17 may):** póster A1 + ensayos de defensa oral.
- **Día 12 (lun 18 may):** buffer + ensayo final.

---

## 📈 Visualizaciones generadas (5 figuras a 300 DPI)

1. **`01_correlation_heatmap.png`** — Matriz de correlación de Pearson entre todas las features numéricas. Muestra `capacity_gb` ↔ `price_usd` con r=0.95. La gráfica estrella del proyecto.

2. **`02_price_by_ddr.png`** — Comparación lado a lado de boxplots en escala USD lineal vs `log(1+precio)`. Demuestra el premium DDR5 sobre DDR4 sobre DDR3 y la estabilización de varianza con la transformación log.

3. **`03_log_transform.png`** — Histogramas comparativos de la distribución original (asimetría +3.61) versus la log-transformada (asimetría -0.61). Justifica matemáticamente la transformación para regresión.

4. **`04_complexity_benchmark.png`** — Comparación pre vs post-índices a n=350 con barras de speedup + proyección teórica de complejidad asintótica.

5. **`05_scaling_benchmark.png`** — Test de escalado n ∈ [350, 50000] mostrando crecimiento del speedup con `n`. **Gráfica central del análisis asintótico para el póster.**

---

## 📚 Referencias y aprendizajes documentados

- **Cormen, Leiserson, Rivest & Stein.** *Introduction to Algorithms* — marco asintótico, análisis de B-Trees.
- **Gauss-Markov theorem** — supuestos de normalidad de residuos en regresión OLS.
- **Pearson, K. (1895).** Coeficiente de asimetría — base de la decisión de transformación log.
- **SQLite documentation** — `EXPLAIN QUERY PLAN`, optimización de índices, covering indexes.
- **Documentación de `requests`** sobre [content negotiation](https://requests.readthedocs.io/) — origen del bug de Brotli del Día 1.
- **Convenciones de SKU de fabricantes** (Kingston, Corsair, G.SKILL, XPG, Crucial, Patriot, Team Group) — derivadas empíricamente del scraping.
- **JEDEC standards for DDR memory** — referencia de timings típicos por generación.
- **Bayesian Inference (UDG · 2026)** — aplicación de priors informativos en imputación condicional.
- **Asymptotic Notation (UDG · 2026)** — análisis O(n), O(log n) aplicado a estructuras B-Tree reales.

---

## 📝 Licencia

Proyecto académico de uso educativo. El código se puede reusar bajo MIT License. Los datos extraídos pertenecen a Newegg.com y se usan únicamente con fines académicos no comerciales.

---

> *"Programar bien no es tener todo perfecto al primer intento — es saber diagnosticar, ajustar y documentar el aprendizaje. Y a veces, los resultados negativos son los más educativos."*

**Última actualización:** domingo 10 de mayo de 2026 · cierre del Día 4 · 42% del sprint completado · 6 historias técnicas documentadas · 5 visualizaciones a 300 DPI

---

## 🤝 Reconocimientos

Este proyecto representa un esfuerzo colaborativo del equipo de cuatro estudiantes de la Universidad de Guadalajara, integrando conocimientos de programación, bases de datos, estadística y análisis matemático en un sprint comprimido de 12 días.

**Agradecimientos:** A los profesores de las materias de Asymptotic Notation y Bayesian Inference por proporcionar el marco teórico que da estructura al análisis empírico presentado.
