# 🧠 Optimización Asintótica en la Predicción del Mercado de Memoria RAM

> **Proyecto académico** · Universidad de Guadalajara · Mayo 2026
> **Materia:** Ciencia de Datos · Asymptotic Notation + Bayesian Inference

## 👥 Equipo de trabajo

| Integrante | Rol |
|---|---|
| **José Carmen Najera Ortiz** | Coordinador técnico · Scraping · Limpieza · SQL · Análisis inferencial · K-Means · Ridge |
| **Juan Pablo Cruz** | Análisis SQL · Benchmark · Queries analíticas |
| **Diego De Jesús** | Comunicación visual · Diseño del póster · Defensa oral |
| **Bernardo Maciel** | Regresión lineal OLS · Validación Gauss-Markov · Análisis inferencial |

---

## 📖 Resumen ejecutivo

Pipeline integral de Ciencia de Datos aplicado al mercado de memoria RAM: desde la extracción vía web scraping en Newegg hasta el análisis empírico de complejidad computacional, modelado predictivo (5 modelos comparativos) y comunicación visual. El proyecto integra programación, bases de datos SQL, estadística inferencial, regresión lineal multivariada, clustering no-supervisado, regularización L2, matemáticas aplicadas y análisis asintótico bajo un sprint comprimido de 12 días.

**Pregunta de investigación:**

> ¿Qué variables técnicas de un módulo de RAM (capacidad, frecuencia, tipo DDR, latencia CAS, marca) son los predictores más fuertes del precio de mercado, y cómo se reduce la complejidad computacional del pipeline desde 𝒪(n) hasta 𝒪(1) en cada etapa del análisis?

**Respuesta cuantificada (triangulación de 3 paradigmas al Día 7):**
- **Estadística inferencial (ANOVA):** la generación DDR explica el **60.8%** de la varianza (η²_DDR), la marca añade un **22.4%** adicional (η²_marca).
- **Regresión paramétrica (OLS):** modelo final con **R²=0.878**, todas las features técnicas significativas (p<0.001).
- **Aprendizaje no-supervisado (K-Means):** segmenta el mercado en 2 clusters principales (Premium 100% DDR5 vs Económico 93.8% DDR4) con silhouette=0.420.
- **Regularización L2 (Ridge):** confirma que el modelo OLS estaba bien especificado (empate técnico R²=0.869 vs 0.876).

**Hallazgo central:** los 3 paradigmas convergen en la misma conclusión — **la generación DDR es el factor dominante de precios**, no la marca. CORSAIR comanda un premium de marca del 10-35% solo dentro de su gama tecnológica.

---

## 📅 Estado del Sprint (12 días · deadline 19-may-2026)

| Día | Fecha | Sprint | Estado |
|---|---|---|---|
| 1 | jue 7 may | Reconocimiento de Newegg + setup del entorno | ✅ Completo |
| 2 | vie 8 may | Scraper de producción + parsers regex | ✅ Completo |
| 3 | sáb 9 may | Limpieza, feature engineering y EDA visual | ✅ Completo |
| 4 | dom 10 may | SQLite + benchmark empírico de complejidad O() | ✅ Completo |
| 5 | lun 11 may | Análisis estadístico inferencial | ✅ Completo |
| 6 | mar 12 may | **Modelo 1** — Regresión lineal multivariada (OLS) | ✅ Completo |
| 7 | mié 13 may | **Modelo 2** — K-Means + **Modelo 3** — Ridge Regression | ✅ Completo |
| 8 | jue 14 may | **Modelo 4** — Random Forest + **Modelo 5** — Gradient Boosting + tabla comparativa | ⏳ Próximo |
| 9 | vie 15 may | Análisis empírico de complejidad ML + decisión modelo final | ⏳ |
| 10 | sáb 16 may | Diseño del póster académico A1 | ⏳ |
| 11 | dom 17 may | Redacción del póster + ensayo defensa oral | ⏳ |
| 12 | lun 18 may | Buffer + ensayo final | ⏳ |
| 🎯 | **mar 19 may** | **Entrega + defensa oral** | 🔒 |

**Progreso actual: 58% · 10+ commits · 0 bloqueos · 3 modelos completos de 5**

---

## 📊 Resultados acumulados (cierre Día 7)

### 1. Dataset extraído y limpio

| Métrica | Valor |
|---|---|
| **Total productos limpios** | 350 (300 válidos tras filtros de modelos) |
| **Tipos DDR distintos** | 3 (DDR3, DDR4, DDR5) |
| **Marcas únicas** | 5 + Other |
| **Columnas finales** | 17 (con features derivados) |
| **Cobertura `cas_latency`** | 100% (con imputación) |

### 2. Análisis empírico de complejidad asintótica (Día 4)

#### 2.1 Test de escalado · n ∈ [350, 50,000]

| n | Q1 speedup | Q2 speedup | **Q4 speedup** |
|---|---|---|---|
| 350 | 1.08× | 1.54× | **1.61×** |
| 1,000 | 1.51× | 1.13× | **2.66×** |
| 5,000 | 0.73× | 0.85× | **8.65×** |
| 10,000 | 0.74× | 0.76× | **8.14×** |
| 50,000 | 0.79× | 0.61× | **13.79×** |

**Hallazgo central:** el speedup de Q4 (covering index) crece de **1.6× → 13.8×** al escalar el dataset 143 veces, **validando empíricamente la predicción teórica del análisis asintótico**.

### 3. Análisis estadístico inferencial (Día 5)

#### 3.1 Test t · DDR4 vs DDR5

| Test | Estadístico | p-value | Resultado |
|---|---|---|---|
| **Welch's t-test** | t=17.83 | <0.000001 | ✅ Significativo |
| **Mann-Whitney U** | U=23,657 | <0.000001 | ✅ Significativo |
| **Cohen's d** | d=2.20 | — | "muy grande" |

#### 3.2 ANOVA por DDR

| Métrica | Valor |
|---|---|
| F-statistic | 269.24 |
| η² (eta-squared) | **0.608** (grande) |

#### 3.3 ANOVA por marca

| Métrica | Valor |
|---|---|
| F-statistic | 19.84 |
| η² (eta-squared) | **0.224** (grande) |

### 4. Modelos predictivos (Días 6-7) · Comparativa parcial

| Modelo | Tipo | R² test | RMSE | MAE | MAPE | Interpretable |
|---|---|---|---|---|---|---|
| **1. Regresión Lineal OLS** | Lineal | **0.876** | $203 | $107 | 17.4% | ✅ Sí |
| **2. K-Means (k=2)** | Clustering | N/A | N/A | N/A | N/A | ✅ Sí (centroides) |
| **3. Ridge (α=7.91)** | Lineal regularizado | 0.869 | $198 | $106 | 17.5% | ✅ Sí |
| **4. Random Forest** | Ensemble bagging | ⏳ Día 8 | — | — | — | ⚠️ Parcial |
| **5. Gradient Boosting** | Ensemble boosting | ⏳ Día 8 | — | — | — | ❌ Black-box |

### 5. Modelo 1 · Regresión Lineal Multivariada (Día 6)

#### 5.1 Especificación del modelo

```
log(precio_usd) ~ capacity_gb + speed_mhz + cas_latency + num_sticks
                  + has_rgb + DDR5 (vs DDR_legacy) + brand (5 dummies)
```

#### 5.2 Validación de supuestos Gauss-Markov

| Supuesto | Test | Resultado |
|---|---|---|
| **Multicolinealidad** | VIF | Todos VIF<5 ✅ |
| **Normalidad de residuos** | QQ-plot | r=0.94 ✅ |
| **Sin autocorrelación** | Durbin-Watson | DW=2.02 ✅ |
| **Homocedasticidad** | Scale-location plot | Aproximadamente plana ✅ |
| **Linealidad** | Residuos vs ajustados | Leve curvatura cuadrática ⚠️ |

#### 5.3 Hallazgo notable · Premium de marca

Todas las marcas tienen coeficientes NEGATIVOS respecto a CORSAIR (categoría base), confirmando que **CORSAIR comanda un premium de marca real** de 10-35% controlando por features técnicos.

### 6. Modelo 2 · K-Means Clustering (Día 7)

#### 6.1 Estrategia híbrida

| Estrategia | Silhouette | Uso |
|---|---|---|
| **k=2 (principal)** | 0.420 | Segmentación de mercado por parsimonia |
| **k=8 (exploratorio)** | 0.493 | Detección de nichos finos |

#### 6.2 Modelo principal · k=2

| Cluster | n | % | Precio mediano | DDR dominante |
|---|---|---|---|---|
| **0 · Premium** | 219 | 73.0% | $490 | 100% DDR5 |
| **1 · Económico** | 81 | 27.0% | $166 | 93.8% DDR4 |

#### 6.3 Hallazgo crítico · El mercado se segmenta por DDR, NO por marca

**Cross-tabulación de marca por cluster:**
- Cluster Premium: CORSAIR 39%, G.SKILL 17%, Other 20%, Kingston 12%
- Cluster Económico: CORSAIR 20%, G.SKILL 21%, Other 32%, Kingston 14%

**Las marcas están MEZCLADAS en ambos clusters.** Esto **valida cuantitativamente** el hallazgo del ANOVA del Día 5: la generación tecnológica explica más varianza que la marca específica.

#### 6.4 PCA · Visualización 2D

PCA captura el **69.3% de la varianza** en 2 componentes (PC1: 49.8%, PC2: 19.5%), permitiendo visualizar la separación de clusters en un espacio bidimensional sin perder información esencial.

### 7. Modelo 3 · Ridge Regression (Día 7)

#### 7.1 Búsqueda de α óptimo

| Métrica | Valor |
|---|---|
| Rango probado | [10⁻⁴, 10⁴] (50 valores) |
| **α óptimo** | **7.91** |
| Método | GridSearchCV con 5-fold CV |
| CV-5 R² óptimo | 0.8851 |

#### 7.2 Comparación Ridge vs OLS

| Métrica | OLS | Ridge | Δ |
|---|---|---|---|
| R² train | 0.9066 | 0.9055 | -0.0011 |
| R² test | 0.8758 | 0.8686 | -0.0072 |
| RMSE USD | $203.14 | $198.46 | **-$4.69** |
| MAE USD | $107.11 | $106.14 | **-$0.97** |
| MAPE % | 17.36% | 17.45% | +0.09% |

#### 7.3 Hallazgo · Empate técnico defendible

**La curva de R² es plana en el rango α ∈ [10⁻⁴, 10]** — recién en α≈100 empieza a caer. Esto significa que el modelo es **estable frente a regularización moderada**, confirmando que:
1. El OLS del Día 6 estaba bien especificado
2. Los VIF<5 ya habían descartado multicolinealidad
3. Ridge actúa como **detector implícito de relevancia**: encoge más las marcas (-31% a -73%) que las features técnicas (-4% a -11%)

#### 7.4 Aparente contradicción · R² peor pero RMSE mejor

Ridge tiene R² menor (en escala log) pero **errores absolutos en USD menores**. Esto se explica porque Ridge es más conservador con outliers extremos: sub-predice los precios muy altos en lugar de "dispararse" como OLS. La elección entre modelos depende del criterio de error preferido (porcentaje vs valor absoluto).

---

## 🎓 Hallazgos metodológicos críticos

### 1. Paradoja del índice (Día 4)

Test de escalado a n=50,000 reveló que para queries con baja selectividad (>30% del dataset), los índices B-Tree DEGRADAN el rendimiento. Solo queries con covering index muestran el speedup teórico predicho.

### 2. Triangulación metodológica (Días 5-7)

Tres paradigmas independientes convergen en la misma estructura del mercado:

| Paradigma | Método | Conclusión |
|---|---|---|
| **Inferencial frecuentista** | ANOVA + Tukey | η²_DDR (60.8%) >> η²_marca (22.4%) |
| **Paramétrico predictivo** | OLS + Ridge | DDR5 y capacity son coef. dominantes |
| **No-supervisado** | K-Means k=2 | Segmentación primaria por DDR |

**Esta convergencia desde paradigmas distintos es validación cruzada robusta de nivel publicación académica.**

### 3. Ridge como detector implícito de relevancia (Día 7)

El shrinkage diferencial revela que las marcas tienen **señal estadística más débil** que las features técnicas:

```
Capacity:    -4%   (señal fuerte, coef estable)
Speed:       -11%  (señal fuerte)
Brand_Kingston: -73%  (señal débil)
Brand_G.SKILL:  -31%  (señal débil)
```

---

## 🛠️ Stack tecnológico

| Capa | Herramientas |
|---|---|
| **Web Scraping** | `requests` + `BeautifulSoup4` + `lxml` |
| **Procesamiento** | `pandas` + `numpy` |
| **Visualización** | `matplotlib` + `seaborn` |
| **Persistencia** | `SQLite` (módulo nativo de Python) |
| **Benchmarking** | `time.perf_counter()` (resolución ns) + `statistics` |
| **Estadística inferencial** | `scipy.stats` (Shapiro-Wilk, Levene, t-test, ANOVA, Tukey, Mann-Whitney, Kruskal-Wallis) |
| **Regresión lineal** | OLS manual (`np.linalg.pinv`) + `sklearn` |
| **Clustering** | `sklearn.cluster.KMeans` + `StandardScaler` + `PCA` |
| **Regularización** | `sklearn.linear_model.Ridge` + `GridSearchCV` |
| **Modelado ML** *(Día 8+)* | `RandomForestRegressor` + `GradientBoostingRegressor` |
| **Versionado** | Git + GitHub |

---

## 🔬 Hallazgos técnicos del proyecto (acumulados)

Ocho historias técnicas documentadas que demuestran resiliencia y rigor del pipeline.

### 1. Bug de compresión Brotli (Día 1)

La librería `requests` no descomprime Brotli sin paquete adicional. Newegg respondía con blob corrupto de 58 KB.
**Solución:** forzar `gzip` removiendo `br` del header `Accept-Encoding`.

### 2. Fragmentación del DOM en el precio (Día 2)

Newegg fragmenta el precio en `<strong>` y `<sup>` por razones tipográficas.
**Solución:** parser específico que reconstruye el `float` desde sus átomos del DOM.

### 3. CAS Latency embebido en SKU (Día 2)

Parser v4 con cuádruple estrategia en cascada (CL explícito, patrón estándar, patrón G.SKILL `J####`, patrón CORSAIR `Z##`) y validación de rango [10, 60].
**Impacto:** cobertura 0% → 85.5% nativo → 100% tras imputación.

### 4. Bug de paginación rota en Newegg (Día 3)

URL original ignoraba `&page=N`. Detectado durante EDA por duplicación masiva.
**Solución:** adoptar `https://www.newegg.com/p/pl?N=100007611%204131&page={N}` que sí pagina.
**Impacto:** dataset 30× más grande (12 → 359 productos únicos).

### 5. Imputación bayesiana ligera (Día 3)

51 productos sin CAS Latency detectable. Imputación condicional por **mediana de DDR** como prior informativo.

### 6. Paradoja del índice en SQLite (Día 4)

Test de escalado a n=50,000 reveló que para queries con baja selectividad, los índices B-Tree DEGRADAN el rendimiento.

### 7. Premium de marca controlando por features (Día 6)

Análisis de regresión reveló que TODAS las marcas tienen coeficientes negativos respecto a CORSAIR, indicando **premium de marca real** de 10-35%.

### 8. Convergencia metodológica de 3 paradigmas (Día 7)

K-Means (no-supervisado) descubrió la misma segmentación que ANOVA (paramétrico) y regresión OLS (predictivo): la generación DDR es el factor primario del mercado. **Validación cruzada robusta desde paradigmas independientes.**

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
│   ├── bench_pre.py                       ← Benchmark SIN índices
│   ├── bench_post.py                      ← Benchmark CON índices
│   └── bench_escalado.py                  ← Test de escalado n ∈ [350, 50000]
│
├── Análisis inferencial (Día 5)
│   ├── inferencia.py                      ← Validación de supuestos
│   ├── inferencia_bloque2.py              ← Test t DDR4 vs DDR5
│   ├── inferencia_bloque3.py              ← ANOVA + Tukey por DDR
│   ├── inferencia_bloque4.py              ← ANOVA + Tukey por marca
│   └── inferencia_dashboard.py            ← Dashboard consolidado
│
├── Modelos predictivos (Días 6-7)
│   ├── regresion.py                       ← Modelo 1: OLS multivariado (Día 6)
│   ├── kmeans.py                          ← Modelo 2: K-Means k=2 + k=8 (Día 7)
│   └── ridge.py                           ← Modelo 3: Ridge Regression (Día 7)
│
├── Tests y validación
│   ├── test_parsers.py                    ← Validación de los 7 parsers regex
│   ├── test_minimo.py                     ← Test aislado del parser CAS v3
│   └── test_paginacion.py                 ← Test de URLs alternativas
│
├── Diagnósticos
│   ├── diagnostico.py                     ← HTTP debugging Día 1
│   ├── diagnostico_cas.py                 ← Cobertura CAS Día 2
│   ├── diagnostico_duplicados.py          ← Detección duplicación Día 3
│   └── diagnostico_v2.py                  ← Análisis post re-scraping Día 3
│
├── figures/                               ← Visualizaciones a 300 DPI (22 figuras)
│   ├── 01_correlation_heatmap.png         ← Matriz de correlación (Día 3)
│   ├── 02_price_by_ddr.png                ← Premium por DDR (Día 3)
│   ├── 03_log_transform.png               ← Justificación del log (Día 3)
│   ├── 04_complexity_benchmark.png        ← Benchmark pre vs post (Día 4)
│   ├── 05_scaling_benchmark.png           ← Test de escalado (Día 4)
│   ├── 06_normality_check.png             ← QQ-plots por DDR (Día 5)
│   ├── 07_ttest_ddr4_vs_ddr5.png          ← Test t (Día 5)
│   ├── 08_anova_ddr.png                   ← ANOVA por DDR (Día 5)
│   ├── 09_anova_marca.png                 ← ANOVA por marca (Día 5)
│   ├── 10_inferential_dashboard.png       ← Dashboard inferencial (Día 5)
│   ├── 11-20_regresion_*.png              ← 10 figuras de regresión OLS (Día 6)
│   ├── 21_kmeans_clustering.png           ← K-Means k=2 + k=8 + PCA (Día 7)
│   └── 22_ridge_vs_ols.png                ← Ridge vs OLS comparativa (Día 7)
│
└── data/
    ├── ram_raw.csv                        ← 359 productos extraídos
    ├── ram_clean.csv                      ← 350 productos limpios
    ├── ram_market.db                      ← Base de datos SQLite
    ├── bench_*.csv                        ← Resultados de benchmark (Día 4)
    ├── scaling_benchmark.csv              ← Test de escalado (Día 4)
    ├── inferential_results.csv            ← Tests inferenciales (Día 5)
    ├── kmeans_results.csv                 ← Inertia y silhouette por k (Día 7)
    ├── kmeans_assignments.csv             ← Cluster asignado por producto (Día 7)
    └── ridge_vs_ols.csv                   ← Comparativa Ridge vs OLS (Día 7)
```

---

## ⚙️ Reproducir el pipeline completo

### Requisitos

- Python 3.10+
- ~20 minutos para reproducir todo el pipeline
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
            matplotlib seaborn sqlalchemy scipy
```

### Ejecutar el pipeline completo

```bash
# Día 2: Extracción (~40 s)
python scraper.py

# Día 3: Limpieza + EDA visual (~10 s)
python limpiar.py
python eda.py

# Día 4: Base de datos + análisis de complejidad (~12 min)
python crear_db.py
python bench_pre.py
python crear_indices.py
python bench_post.py
python bench_escalado.py

# Día 5: Estadística inferencial (~30 s)
python inferencia.py
python inferencia_bloque2.py
python inferencia_bloque3.py
python inferencia_bloque4.py
python inferencia_dashboard.py

# Día 6: Regresión lineal multivariada (~10 s)
python regresion.py

# Día 7: K-Means + Ridge (~30 s)
python kmeans.py
python ridge.py
```

---

## 🧮 Análisis asintótico del pipeline

El proyecto demuestra empíricamente la transición de complejidad en cada etapa:

```
EXTRACCIÓN  · 𝒪(n · t_red)   → scraping secuencial dominado por I/O (~40s)
LIMPIEZA    · 𝒪(n)           → regex amortizado 𝒪(1) por fila (~5s)
SQL SCAN    · 𝒪(n)           → búsqueda lineal sin índice (medido)
SQL B-TREE  · 𝒪(log n)       → búsqueda con índice (medido y validado)
K-MEANS     · 𝒪(n·k·i·d)     → clustering, próximo Día 8 medición empírica
RIDGE       · 𝒪(p³)          → solución cerrada vía SVD
INFERENCIA  · 𝒪(1)           → modelo entrenado, predicción constante
```

**Validación empírica:** speedup en Q4 (covering index) crece de **1.6× (n=350) → 13.8× (n=50,000)**, confirmando el crecimiento logarítmico predicho.

---

## 📖 Decisiones de diseño defendibles

### Pipeline de datos
- **`dataclass` en lugar de `dict`:** tipado estricto desde el origen.
- **`try/except` por item:** granularidad de fallo correcta.
- **`log(1+x)` en lugar de `log(x)`:** robusto ante valores potenciales de 0.
- **Imputación condicional por mediana de DDR:** prior informativo bayesiano.

### Análisis de complejidad
- **`time.perf_counter()` en vez de `time.time()`:** resolución ns vs ms; monotónico.
- **Mediana en vez de media:** robusta a outliers de garbage collection.
- **N=100 ejecuciones por query:** reduce varianza por √N (TCL bayesiano).
- **Test de escalado a n=50,000:** validación más fuerte que evidencia con un único n.

### Análisis inferencial
- **Triangulación de tests:** Welch's t + Mann-Whitney + Cohen's d.
- **Test unilateral con dirección esperada:** mayor potencia estadística.
- **Tukey HSD post-hoc:** controla FWER tras ANOVA.

### Regresión lineal (Día 6)
- **OLS matricial manual:** demuestra entendimiento profundo del álgebra.
- **VIF para multicolinealidad:** todos los VIF < 5.
- **Train/test split 80/20 con random_state=42:** reproducible y comparable con otros modelos.
- **DDR3+DDR4 agrupados como DDR_legacy:** n=11 en DDR3 penaliza potencia.

### K-Means (Día 7)
- **StandardScaler obligatorio:** evita que features con escalas grandes dominen.
- **Estrategia híbrida k=2 + k=8:** parsimonia + exploración de nichos.
- **n_init=20:** mayor estabilidad ante inicializaciones aleatorias.
- **PCA para visualización:** captura 69.3% de la varianza en 2D.
- **Reordenamiento de clusters por mediana:** cluster 0 = Premium siempre.

### Ridge (Día 7)
- **GridSearchCV con 50 valores de α en escala log:** búsqueda exhaustiva [10⁻⁴, 10⁴].
- **Mismo split que OLS:** comparabilidad directa.
- **Reportar tanto R² como RMSE/MAE:** revelar la aparente contradicción entre escalas.

---

## 🔮 Próximas etapas

- **Día 8 (jue 14 may):** Random Forest + Gradient Boosting + Tabla comparativa final de 5 modelos.
- **Día 9 (vie 15 may):** medición empírica de complejidad de los 5 modelos ML + decisión del modelo final.
- **Día 10-11 (sáb 16 - dom 17 may):** póster A1 + ensayos de defensa oral.
- **Día 12 (lun 18 may):** buffer + ensayo final.

---

## 📈 Visualizaciones generadas (22 figuras a 300 DPI)

### EDA y feature engineering (Día 3)
1. **`01_correlation_heatmap.png`** — Matriz de correlación de Pearson.
2. **`02_price_by_ddr.png`** — Premium DDR5 sobre DDR4 sobre DDR3.
3. **`03_log_transform.png`** — Justificación de la transformación log.

### Análisis de complejidad (Día 4)
4. **`04_complexity_benchmark.png`** — Pre vs post-índices a n=350.
5. **`05_scaling_benchmark.png`** — Test de escalado. **Gráfica central del análisis asintótico.**

### Análisis inferencial (Día 5)
6. **`06_normality_check.png`** — QQ-plots por DDR.
7. **`07_ttest_ddr4_vs_ddr5.png`** — Test t triangulado.
8. **`08_anova_ddr.png`** — ANOVA + Tukey post-hoc por DDR.
9. **`09_anova_marca.png`** — ANOVA + Tukey post-hoc por marca.
10. **`10_inferential_dashboard.png`** — Dashboard consolidado.

### Regresión lineal (Día 6)
11. **`11_regresion_distribucion_precio.png`** — Distribución de la variable dependiente.
12. **`12_regresion_precio_por_ddr.png`** — Precios medianos por generación DDR.
13. **`13_regresion_scatter_numericas.png`** — Scatter plots features numéricas.
14. **`14_regresion_precio_por_marca.png`** — Boxplot por marca.
15. **`15_regresion_correlacion.png`** — Matriz de correlación enfocada al modelo.
16. **`16_regresion_vif.png`** — Análisis VIF (todos <5).
17. **`17_regresion_supuestos_gauss_markov.png`** — 6 paneles validando supuestos OLS.
18. **`18_regresion_coeficientes.png`** — Coeficientes β con IC 95%.
19. **`19_regresion_real_vs_predicho.png`** — Evaluación R²=0.878.
20. **`20_regresion_pairplot.png`** — Pairplot variables del modelo.

### K-Means y Ridge (Día 7)
21. **`21_kmeans_clustering.png`** — 6 paneles: elbow, silhouette, k=2 PCA, k=8 PCA, 2 boxplots. **Validación cruzada con Día 5.**
22. **`22_ridge_vs_ols.png`** — 4 paneles: curva α, coeficientes shrinkage, predicción comparada, tabla.

---

## 📚 Referencias y aprendizajes documentados

- **Cormen, Leiserson, Rivest & Stein.** *Introduction to Algorithms* — marco asintótico, análisis de B-Trees.
- **Gauss-Markov theorem** — supuestos de normalidad de residuos en regresión OLS.
- **Cohen, J. (1988).** *Statistical Power Analysis for the Behavioral Sciences* — interpretación de Cohen's d y eta-squared.
- **Tukey, J.W. (1949).** *Comparing Individual Means in the Analysis of Variance* — origen del Tukey HSD.
- **Tikhonov, A.N. (1943).** Origen de la regularización L2 (Ridge Regression).
- **MacQueen, J. (1967).** *Some Methods for Classification and Analysis of Multivariate Observations* — algoritmo K-Means original.
- **Rousseeuw, P.J. (1987).** *Silhouettes: a graphical aid to the interpretation and validation of cluster analysis* — origen del silhouette score.
- **Pearson, K. (1895).** Coeficiente de asimetría — base de la decisión de transformación log.
- **Pearson, K. (1901).** *On Lines and Planes of Closest Fit to Systems of Points in Space* — origen del PCA.
- **SQLite documentation** — `EXPLAIN QUERY PLAN`, optimización de índices, covering indexes.
- **Bayesian Inference (UDG · 2026)** — aplicación de priors informativos en imputación condicional.
- **Asymptotic Notation (UDG · 2026)** — análisis O(n), O(log n) aplicado a estructuras B-Tree reales.

---

## 📝 Licencia

Proyecto académico de uso educativo. El código se puede reusar bajo MIT License. Los datos extraídos pertenecen a Newegg.com y se usan únicamente con fines académicos no comerciales.

---

> *"Programar bien no es tener todo perfecto al primer intento — es saber diagnosticar, ajustar y documentar el aprendizaje. Y a veces, los resultados negativos son los más educativos."*

**Última actualización:** miércoles 13 de mayo de 2026 · cierre del Día 7 · 58% del sprint completado · 8 historias técnicas documentadas · 22 visualizaciones a 300 DPI · 3 modelos predictivos completos de 5 · Triangulación metodológica de 3 paradigmas validada

---

## 🤝 Reconocimientos

Este proyecto representa un esfuerzo colaborativo del equipo de cuatro estudiantes de la Universidad de Guadalajara.

**Contribuciones específicas:**
- **José Najera:** infraestructura del proyecto (scraping, limpieza, base de datos, índices B-Tree, análisis inferencial completo, K-Means clustering, Ridge regression, integración del equipo, gestión de Git).
- **Bernardo Maciel:** regresión lineal multivariada con OLS matricial, validación de supuestos Gauss-Markov, análisis de residuos, generación de 10 figuras del Día 6.
- **Juan Pablo Cruz:** análisis SQL, queries analíticas, benchmark.
- **Diego De Jesús:** comunicación visual, diseño del póster académico, preparación de la defensa oral.

**Agradecimientos:** A los profesores de las materias de Asymptotic Notation y Bayesian Inference por proporcionar el marco teórico que da estructura al análisis empírico presentado.
