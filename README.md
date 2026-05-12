# 🧠 Optimización Asintótica en la Predicción del Mercado de Memoria RAM
 
> **Proyecto académico** · Universidad de Guadalajara · Mayo 2026
> **Materia:** Ciencia de Datos · Asymptotic Notation + Bayesian Inference
 
## 👥 Equipo de trabajo
 
| Integrante | Rol |
|---|---|
| **José Carmen Najera Ortiz** | Coordinador técnico · Scraping · Limpieza · SQL · Inferencia · K-Means · Ridge · RF · GB |
| **Juan Pablo Cruz** | Análisis SQL · Benchmark · Queries analíticas |
| **Diego De Jesús** | Comunicación visual · Diseño del póster · Defensa oral |
| **Bernardo Maciel** | Regresión lineal OLS · Validación Gauss-Markov · Análisis inferencial |
 
---
 
## 📖 Resumen ejecutivo
 
Pipeline integral de Ciencia de Datos aplicado al mercado de memoria RAM: desde la extracción vía web scraping en Newegg hasta el análisis empírico de complejidad computacional, modelado predictivo comparativo de 5 modelos y comunicación visual. El proyecto integra programación, bases de datos SQL, estadística inferencial, regresión lineal multivariada, clustering no-supervisado, regularización L2, ensembles de árboles (bagging y boosting), matemáticas aplicadas y análisis asintótico bajo un sprint comprimido de 12 días.
 
**Pregunta de investigación:**
 
> ¿Qué variables técnicas de un módulo de RAM (capacidad, frecuencia, tipo DDR, latencia CAS, marca) son los predictores más fuertes del precio de mercado, y cómo se reduce la complejidad computacional del pipeline desde 𝒪(n) hasta 𝒪(1) en cada etapa del análisis?
 
**Respuesta cuantificada (5 paradigmas convergentes al Día 8):**
 
| Paradigma | Método | Conclusión clave |
|---|---|---|
| Inferencial frecuentista | ANOVA + Tukey | η²_DDR=60.8% >> η²_marca=22.4% |
| Paramétrico predictivo | OLS | R²=0.876, β capacity_gb dominante |
| Paramétrico regularizado | Ridge L2 | Empate técnico con OLS (R²=0.869) |
| No-supervisado | K-Means k=2 | Segmentación primaria por DDR (silhouette=0.420) |
| Ensemble bagging | Random Forest | R²=0.902, MAPE=10.4%, importance capacity_gb=46.8% |
| Ensemble boosting | Gradient Boosting | **R²=0.962, MAPE=8.3%, importance capacity_gb=85.6%** |
 
**Hallazgo central:** los 6 métodos convergen — `capacity_gb` es el predictor #1, la generación DDR es el segundo factor, las marcas individuales son secundarias. **CORSAIR comanda un premium de marca del 10-35% controlando por features técnicos.**
 
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
| 8 | jue 14 may | **Modelo 4** — Random Forest + **Modelo 5** — Gradient Boosting | ✅ Completo |
| 9 | vie 15 may | Análisis empírico de complejidad ML + gráfica comparativa final | ⏳ Próximo |
| 10 | sáb 16 may | Diseño del póster académico A1 | ⏳ |
| 11 | dom 17 may | Redacción del póster + ensayo defensa oral | ⏳ |
| 12 | lun 18 may | Buffer + ensayo final | ⏳ |
| 🎯 | **mar 19 may** | **Entrega + defensa oral** | 🔒 |
 
**Progreso actual: 67% · 12+ commits · 0 bloqueos · LOS 5 MODELOS COMPLETOS**
 
---
 
## 🏆 Comparativa final de los 5 modelos predictivos (cierre Día 8)
 
Todos los modelos entrenados sobre el **mismo split 80/20** con `random_state=42` y las **mismas features**, garantizando comparabilidad estricta.
 
| Modelo | Tipo | R² test | CV-5 R² | RMSE | MAE | MAPE | Tiempo | Interpretable |
|---|---|---|---|---|---|---|---|---|
| **1. OLS (Día 6)** | Lineal | 0.8758 | — | $203 | $107 | 17.36% | 0.01s | ✅ Alta |
| **2. K-Means k=2 (Día 7)** | Clustering | N/A | N/A | N/A | N/A | N/A | 0.05s | ✅ Alta (centroides) |
| **3. Ridge α=7.91 (Día 7)** | Lineal regularizado | 0.8686 | 0.8851 | $198 | $106 | 17.45% | 0.02s | ✅ Alta |
| **4. Random Forest (Día 8)** | Ensemble bagging | 0.9020 | 0.9392 | $159 | $71 | 10.42% | 0.13s | ⚠️ Parcial |
| **5. Gradient Boosting (Día 8)** | Ensemble boosting | **0.9616** | **0.9601** | **$125** | **$52** | **8.32%** | 0.11s | ⚠️ Parcial |
 
### 🏅 Ranking por MAPE (menor = mejor)
 
```
🥇 1. Gradient Boosting     MAPE=8.32%   R²=0.9616
🥈 2. Random Forest         MAPE=10.42%  R²=0.9020
🥉 3. OLS                   MAPE=17.36%  R²=0.8758
   4. Ridge                 MAPE=17.45%  R²=0.8686
```
 
### 🎯 Decisión académica · Modelos complementarios
 
| Objetivo | Modelo recomendado | Razón |
|---|---|---|
| **Predicción** (mínimo error) | **Gradient Boosting** 🏆 | MAPE 8.3%, MAE $52 |
| **Inferencia causal** | **OLS** 🏆 | Coeficientes con p-values e IC |
| **Segmentación de mercado** | **K-Means** 🏆 | Cluster Premium vs Económico |
 
El proyecto reporta **OLS para EXPLICAR** (qué variables, con qué magnitud, con qué significancia) y **Gradient Boosting para PREDECIR** (cuánto costará una RAM con estas especificaciones).
 
---
 
## 📊 Resultados acumulados detallados
 
### 1. Dataset extraído y limpio
 
| Métrica | Valor |
|---|---|
| **Total productos limpios** | 350 (300 válidos tras filtros de modelos) |
| **Tipos DDR distintos** | 3 (DDR3, DDR4, DDR5) |
| **Marcas únicas** | 5 + Other |
| **Columnas finales** | 17 (con features derivados) |
| **Cobertura `cas_latency`** | 100% (con imputación) |
 
### 2. Análisis empírico de complejidad asintótica (Día 4)
 
#### Test de escalado · n ∈ [350, 50,000]
 
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
| Tukey HSD pares sig. | 3/3 (todos) |
 
#### 3.3 ANOVA por marca
 
| Métrica | Valor |
|---|---|
| F-statistic | 19.84 |
| η² (eta-squared) | **0.224** (grande) |
| Tukey HSD pares sig. | 6/15 (40%) |
 
### 4. Modelo 1 · Regresión Lineal Multivariada (Día 6)
 
#### Especificación
```
log(precio_usd) ~ capacity_gb + speed_mhz + cas_latency + num_sticks
                  + has_rgb + DDR5 (vs DDR_legacy) + brand (5 dummies)
```
 
#### Validación de supuestos Gauss-Markov
 
| Supuesto | Test | Resultado |
|---|---|---|
| **Multicolinealidad** | VIF | Todos VIF<5 ✅ |
| **Normalidad de residuos** | QQ-plot | r=0.94 ✅ |
| **Sin autocorrelación** | Durbin-Watson | DW=2.02 ✅ |
| **Homocedasticidad** | Scale-location plot | Aproximadamente plana ✅ |
| **Linealidad** | Residuos vs ajustados | Leve curvatura cuadrática ⚠️ |
 
**Hallazgo:** Todas las marcas tienen coeficientes NEGATIVOS respecto a CORSAIR (categoría base), confirmando **premium de marca real** del 10-35%.
 
### 5. Modelo 2 · K-Means Clustering (Día 7)
 
#### Estrategia híbrida
 
| Estrategia | Silhouette | Uso |
|---|---|---|
| **k=2 (principal)** | 0.420 | Segmentación de mercado por parsimonia |
| **k=8 (exploratorio)** | 0.493 | Detección de nichos finos |
 
#### Modelo principal · k=2
 
| Cluster | n | % | Precio mediano | DDR dominante |
|---|---|---|---|---|
| **0 · Premium** | 219 | 73.0% | $490 | 100% DDR5 |
| **1 · Económico** | 81 | 27.0% | $166 | 93.8% DDR4 |
 
**Hallazgo crítico:** El K-Means descubrió que **el mercado se segmenta primariamente por GENERACIÓN DDR, NO por marca**. Las marcas están MEZCLADAS en ambos clusters (CORSAIR aparece en ambos). Esto valida cuantitativamente el ANOVA del Día 5 (η²_DDR >> η²_marca).
 
#### PCA · Visualización 2D
PCA captura el **69.3% de la varianza** en 2 componentes (PC1: 49.8%, PC2: 19.5%).
 
### 6. Modelo 3 · Ridge Regression (Día 7)
 
#### Búsqueda de α óptimo
 
| Métrica | Valor |
|---|---|
| Rango probado | [10⁻⁴, 10⁴] (50 valores) |
| **α óptimo** | **7.91** |
| Método | GridSearchCV con 5-fold CV |
| CV-5 R² óptimo | 0.8851 |
 
#### Comparación Ridge vs OLS
 
| Métrica | OLS | Ridge | Δ |
|---|---|---|---|
| R² train | 0.9066 | 0.9055 | -0.0011 |
| R² test | 0.8758 | 0.8686 | -0.0072 |
| RMSE USD | $203.14 | $198.46 | **-$4.69** |
| MAE USD | $107.11 | $106.14 | **-$0.97** |
| MAPE % | 17.36% | 17.45% | +0.09% |
 
**Hallazgo:** La curva de R² es plana en α ∈ [10⁻⁴, 10] — confirma que el modelo OLS estaba bien especificado. Ridge actúa como **detector implícito de relevancia**: encoge más las marcas (-31% a -73%) que las features técnicas (-4% a -11%).
 
### 7. Modelo 4 · Random Forest Regressor (Día 8)
 
#### Hiperparámetros óptimos (GridSearchCV)
 
| Hiperparámetro | Valor óptimo |
|---|---|
| `n_estimators` | 300 |
| `max_depth` | 20 |
| `min_samples_split` | 2 |
| `max_features` | 'sqrt' |
 
#### Métricas finales
 
| Métrica | Train | Test |
|---|---|---|
| R² | 0.9922 | **0.9020** |
| Gap train-test | — | +0.0902 (overfitting moderado) |
| CV-5 R² | — | 0.9392 ± 0.0185 |
 
#### Feature importances (top 5)
 
| Feature | Importance | % Acumulado |
|---|---|---|
| **capacity_gb** | **0.4677** | 46.8% |
| speed_mhz | 0.1628 | 63.1% |
| cas_latency | 0.1181 | 74.9% |
| ddr_group_DDR_legacy | 0.1129 | 86.2% |
| num_sticks | 0.0726 | 93.4% |
 
**Hallazgo:** RF ganó **+2.62 puntos porcentuales de R²** sobre OLS, pero el verdadero impacto fue en **MAPE: -6.94 puntos** (de 17.4% a 10.4%). El error práctico se redujo dramáticamente.
 
### 8. Modelo 5 · Gradient Boosting Regressor (Día 8)
 
#### Hiperparámetros óptimos (GridSearchCV)
 
| Hiperparámetro | Valor óptimo |
|---|---|
| `n_estimators` | 200 |
| `learning_rate` | 0.05 |
| `max_depth` | 3 |
| `subsample` | 1.0 |
 
#### Métricas finales · El mejor modelo del proyecto
 
| Métrica | Train | Test |
|---|---|---|
| R² | 0.9918 | **0.9616** 🏆 |
| Gap train-test | — | +0.0302 (excelente generalización) |
| CV-5 R² | — | 0.9601 ± 0.0182 |
| RMSE USD | — | **$125** |
| MAE USD | — | **$52** |
| MAPE | — | **8.32%** 🏆 |
 
#### Feature importances (top 5)
 
| Feature | Importance | % Acumulado |
|---|---|---|
| **capacity_gb** | **0.856** | 85.6% |
| speed_mhz | 0.071 | 92.7% |
| ddr_group_DDR_legacy | 0.035 | 96.2% |
| cas_latency | 0.016 | 97.8% |
| brand_normalized_Other | 0.009 | 98.7% |
 
**Hallazgos clave:**
1. **GB es el ganador absoluto**: mejor R², mejor MAPE, mejor MAE, mejor RMSE, mejor CV-5.
2. **Gap train-test de solo 0.030** — tres veces menor que RF (0.090). Excelente generalización **sin overfitting**.
3. **Importance EXTREMA en capacity_gb** (85.6%): GB explota la señal dominante de manera más concentrada que RF.
4. **MAPE de 8.32%** — calidad de modelo profesional, no académica.
---
 
## 🎓 Hallazgos metodológicos críticos
 
### 1. Paradoja del índice (Día 4)
 
Test de escalado a n=50,000 reveló que para queries con baja selectividad (>30% del dataset), los índices B-Tree DEGRADAN el rendimiento. Solo queries con covering index muestran el speedup teórico predicho.
 
### 2. Triangulación metodológica de 6 paradigmas (Días 5-8)
 
Seis métodos independientes convergen en la misma estructura del mercado:
 
| Paradigma | Método | Conclusión |
|---|---|---|
| **Inferencial** | ANOVA | η²_DDR >> η²_marca |
| **Paramétrico** | OLS | β capacity dominante (+0.49) |
| **Regularizado** | Ridge | β capacity estable (+0.47) |
| **No-supervisado** | K-Means | Segmentación por DDR |
| **Bagging** | Random Forest | importance capacity=46.8% |
| **Boosting** | Gradient Boosting | importance capacity=85.6% |
 
**Esta convergencia desde 6 paradigmas independientes es validación cruzada robusta de nivel publicación académica.**
 
### 3. Ridge como detector implícito de relevancia (Día 7)
 
El shrinkage diferencial revela que las marcas tienen **señal estadística más débil** que las features técnicas:
 
```
Capacity:           -4%   (señal fuerte, coef estable)
Speed:              -11%  (señal fuerte)
Brand_Kingston:     -73%  (señal débil)
Brand_G.SKILL:      -31%  (señal débil)
```
 
### 4. La progresión OLS → Ridge → RF → GB tiene rendimientos NO decrecientes (Día 8)
 
Cada modelo añade valor sustancial:
- **OLS → Ridge:** prácticamente igual (validación de buena especificación)
- **Ridge → RF:** +3.3 pp R², -7 pp MAPE (captura no-linealidades)
- **RF → GB:** +6.0 pp R², -2.1 pp MAPE (boosting secuencial corrige residuos)
Esto justifica el uso de los modelos más sofisticados a pesar del costo de interpretabilidad.
 
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
| **Regresión lineal** | OLS manual (`np.linalg.pinv`) + `sklearn.LinearRegression` |
| **Regularización** | `sklearn.linear_model.Ridge` + `GridSearchCV` |
| **Clustering** | `sklearn.cluster.KMeans` + `StandardScaler` + `PCA` |
| **Ensemble bagging** | `sklearn.ensemble.RandomForestRegressor` + `GridSearchCV` |
| **Ensemble boosting** | `sklearn.ensemble.GradientBoostingRegressor` + `GridSearchCV` |
| **Versionado** | Git + GitHub |
 
---
 
## 🔬 Hallazgos técnicos del proyecto (acumulados)
 
Nueve historias técnicas documentadas que demuestran resiliencia y rigor del pipeline.
 
### 1. Bug de compresión Brotli (Día 1)
La librería `requests` no descomprime Brotli. **Solución:** forzar `gzip` removiendo `br` del header.
 
### 2. Fragmentación del DOM en el precio (Día 2)
Newegg fragmenta el precio en `<strong>` y `<sup>`. **Solución:** parser que reconstruye el `float` desde sus átomos.
 
### 3. CAS Latency embebido en SKU (Día 2)
Parser v4 con cuádruple estrategia en cascada. **Impacto:** cobertura 0% → 85.5% nativo → 100% tras imputación.
 
### 4. Bug de paginación rota en Newegg (Día 3)
URL original ignoraba `&page=N`. **Solución:** URL alternativa. **Impacto:** dataset 30× más grande (12 → 359 productos únicos).
 
### 5. Imputación bayesiana ligera (Día 3)
51 productos sin CAS Latency. Imputación condicional por **mediana de DDR** como prior informativo.
 
### 6. Paradoja del índice en SQLite (Día 4)
Para queries con baja selectividad, los índices B-Tree DEGRADAN el rendimiento.
 
### 7. Premium de marca controlando por features (Día 6)
Análisis de regresión reveló que todas las marcas tienen coeficientes negativos respecto a CORSAIR, indicando **premium de marca real** de 10-35%.
 
### 8. Convergencia metodológica de 6 paradigmas (Días 7-8)
ANOVA + OLS + Ridge + K-Means + Random Forest + Gradient Boosting coinciden: `capacity_gb` y generación DDR son los factores dominantes.
 
### 9. Gradient Boosting · El mejor modelo del proyecto (Día 8)
GB con learning_rate=0.05 y max_depth=3 alcanzó MAPE=8.32%, **reduciendo el error a la mitad** respecto a OLS. Gap train-test de solo 0.030 indica **generalización superior incluso a RF**. Demuestra que los árboles superficiales con learning rate conservador son más estables que árboles profundos en bagging.
 
---
 
## 📁 Estructura del proyecto
 
```
Web_scraping/
├── README.md                              ← Este archivo
├── .gitignore                             ← Exclusiones de Git
│
├── Scraping (Días 1-2)
│   ├── scraper.py                         ← Scraper principal de Newegg
│   ├── recalcular_cas.py                  ← Reaplicar parser CL
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
├── Modelos predictivos (Días 6-8) · LOS 5 MODELOS
│   ├── regresion.py                       ← Modelo 1: OLS multivariado (Día 6)
│   ├── kmeans.py                          ← Modelo 2: K-Means k=2 + k=8 (Día 7)
│   ├── ridge.py                           ← Modelo 3: Ridge Regression (Día 7)
│   ├── random_forest.py                   ← Modelo 4: Random Forest (Día 8)
│   └── gradient_boosting.py               ← Modelo 5: Gradient Boosting (Día 8)
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
├── figures/                               ← 24 visualizaciones a 300 DPI
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
│   ├── 22_ridge_vs_ols.png                ← Ridge vs OLS comparativa (Día 7)
│   ├── 23_random_forest.png               ← Random Forest + comparativa (Día 8)
│   └── 24_gradient_boosting.png           ← Gradient Boosting + ranking final (Día 8)
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
    ├── ridge_vs_ols.csv                   ← Comparativa Ridge vs OLS (Día 7)
    ├── rf_comparison.csv                  ← Random Forest vs lineales (Día 8)
    ├── rf_feature_importances.csv         ← Importances RF (Día 8)
    ├── gb_feature_importances.csv         ← Importances GB (Día 8)
    └── comparativa_5_modelos.csv          ← Tabla final de los 5 modelos (Día 8)
```
 
---
 
## ⚙️ Reproducir el pipeline completo
 
### Requisitos
- Python 3.10+
- ~25 minutos para reproducir todo el pipeline (incluyendo GridSearchCV de los ensembles)
- Conexión a internet estable (para el scraping)
### Setup del entorno
 
```bash
git clone https://github.com/Jnajera96/ram-pricing-2026.git
cd ram-pricing-2026
 
# Entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
 
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
 
# Día 8: Random Forest + Gradient Boosting (~1 min)
python random_forest.py
python gradient_boosting.py
```
 
---
 
## 🧮 Análisis asintótico del pipeline
 
```
EXTRACCIÓN     · 𝒪(n · t_red)        → scraping secuencial dominado por I/O (~40s)
LIMPIEZA       · 𝒪(n)                 → regex amortizado 𝒪(1) por fila (~5s)
SQL SCAN       · 𝒪(n)                 → búsqueda lineal sin índice
SQL B-TREE     · 𝒪(log n)             → búsqueda con índice (validado)
OLS            · 𝒪(p³)                → solución cerrada vía SVD
RIDGE          · 𝒪(p³)                → solución cerrada con penalización
K-MEANS        · 𝒪(n·k·i·d)           → próxima medición Día 9
RANDOM FOREST  · 𝒪(n·log n · m)       → m=trees, próxima medición Día 9
GRADIENT BOOST · 𝒪(n·m·d)             → d=depth, próxima medición Día 9
INFERENCIA     · 𝒪(1)                 → modelo entrenado, predicción constante
```
 
**Validación empírica:** speedup en Q4 (covering index) crece de **1.6× (n=350) → 13.8× (n=50,000)**, confirmando crecimiento logarítmico predicho.
 
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
- **Train/test split 80/20 con random_state=42:** reproducible y comparable.
### K-Means (Día 7)
- **StandardScaler obligatorio:** evita que features con escalas grandes dominen.
- **Estrategia híbrida k=2 + k=8:** parsimonia + exploración de nichos.
- **n_init=20:** mayor estabilidad ante inicializaciones aleatorias.
- **PCA para visualización:** captura 69.3% de la varianza en 2D.
### Ridge (Día 7)
- **GridSearchCV con 50 valores de α en escala log:** búsqueda exhaustiva.
- **Mismo split que OLS:** comparabilidad directa.
### Random Forest (Día 8)
- **GridSearchCV con 36 combinaciones × 5 folds:** búsqueda robusta.
- **`max_features='sqrt'`:** descorrelaciona árboles individuales.
- **NO requiere estandarización:** los árboles son insensibles a la escala de features.
### Gradient Boosting (Día 8)
- **GridSearchCV con 54 combinaciones × 5 folds:** búsqueda más profunda que RF.
- **`learning_rate=0.05` (bajo) + `max_depth=3` (superficial):** regularización implícita que reduce overfitting.
- **`subsample=1.0`:** prioriza estabilidad sobre velocidad para dataset pequeño.
---
 
## 🔮 Próximas etapas
 
- **Día 9 (vie 15 may):** medición empírica de complejidad de los 5 modelos ML + gráfica comparativa final consolidada (figura 25) para el póster.
- **Día 10-11 (sáb 16 - dom 17 may):** póster A1 + ensayos de defensa oral.
- **Día 12 (lun 18 may):** buffer + ensayo final.
---
 
## 📈 Visualizaciones generadas (24 figuras a 300 DPI)
 
### EDA y feature engineering (Día 3)
1. **`01_correlation_heatmap.png`** — Matriz de correlación de Pearson.
2. **`02_price_by_ddr.png`** — Premium DDR5 sobre DDR4 sobre DDR3.
3. **`03_log_transform.png`** — Justificación de la transformación log.
### Análisis de complejidad (Día 4)
4. **`04_complexity_benchmark.png`** — Pre vs post-índices a n=350.
5. **`05_scaling_benchmark.png`** — Test de escalado. **Gráfica central del análisis asintótico.**
### Análisis inferencial (Día 5)
6-10. **`06_normality_check.png`**, **`07_ttest_ddr4_vs_ddr5.png`**, **`08_anova_ddr.png`**, **`09_anova_marca.png`**, **`10_inferential_dashboard.png`**
 
### Regresión lineal (Día 6)
11-20. Diez figuras de regresión OLS (distribución, scatter, correlación, VIF, supuestos Gauss-Markov, coeficientes, real vs predicho, pairplot).
 
### K-Means y Ridge (Día 7)
21. **`21_kmeans_clustering.png`** — 6 paneles: elbow, silhouette, k=2 PCA, k=8 PCA, 2 boxplots.
22. **`22_ridge_vs_ols.png`** — 4 paneles: curva α, coeficientes shrinkage, predicción comparada, tabla.
### Random Forest y Gradient Boosting (Día 8)
23. **`23_random_forest.png`** — 4 paneles: feature importances, real vs predicho, comparación R² entre 3 modelos, tabla.
24. **`24_gradient_boosting.png`** — 4 paneles: feature importances, real vs predicho, comparación R² entre 4 modelos, comparación MAPE.
---
 
## 📚 Referencias y aprendizajes documentados
 
- **Cormen, Leiserson, Rivest & Stein.** *Introduction to Algorithms* — marco asintótico, análisis de B-Trees.
- **Gauss-Markov theorem** — supuestos de normalidad de residuos en regresión OLS.
- **Cohen, J. (1988).** *Statistical Power Analysis for the Behavioral Sciences* — interpretación de Cohen's d y eta-squared.
- **Tukey, J.W. (1949).** *Comparing Individual Means in the Analysis of Variance* — origen del Tukey HSD.
- **Tikhonov, A.N. (1943).** Origen de la regularización L2 (Ridge Regression).
- **MacQueen, J. (1967).** *Some Methods for Classification and Analysis of Multivariate Observations* — algoritmo K-Means original.
- **Rousseeuw, P.J. (1987).** *Silhouettes: a graphical aid to the interpretation and validation of cluster analysis* — origen del silhouette score.
- **Breiman, L. (2001).** *Random Forests* — algoritmo Random Forest original.
- **Friedman, J.H. (2001).** *Greedy Function Approximation: A Gradient Boosting Machine* — algoritmo Gradient Boosting original.
- **Pearson, K. (1895).** Coeficiente de asimetría — base de la decisión de transformación log.
- **Pearson, K. (1901).** *On Lines and Planes of Closest Fit to Systems of Points in Space* — origen del PCA.
- **SQLite documentation** — `EXPLAIN QUERY PLAN`, optimización de índices, covering indexes.
- **Bayesian Inference (UDG · 2026)** — aplicación de priors informativos en imputación condicional.
- **Asymptotic Notation (UDG · 2026)** — análisis O(n), O(log n) aplicado a estructuras B-Tree reales.
---
 
## 📝 Licencia
 
Proyecto académico de uso educativo. El código se puede reusar bajo MIT License. Los datos extraídos pertenecen a Newegg.com y se usan únicamente con fines académicos no comerciales.
 
---
 
> *"Programar bien no es tener todo perfecto al primer intento — es saber diagnosticar, ajustar y documentar el aprendizaje. La verdadera contribución académica es el método de evaluación: cinco modelos sobre el mismo split, mismas features, métricas comparables, decisión justificada."*
 
**Última actualización:** jueves 14 de mayo de 2026 · cierre del Día 8 · 67% del sprint completado · 9 historias técnicas documentadas · 24 visualizaciones a 300 DPI · **LOS 5 MODELOS PREDICTIVOS COMPLETOS** · Mejor modelo: Gradient Boosting con MAPE=8.32% · Triangulación metodológica de 6 paradigmas validada
 
---
 
## 🤝 Reconocimientos
 
Este proyecto representa un esfuerzo colaborativo del equipo de cuatro estudiantes de la Universidad de Guadalajara.
 
**Contribuciones específicas:**
- **José Najera:** infraestructura del proyecto (scraping, limpieza, base de datos, índices B-Tree, análisis inferencial completo, K-Means clustering, Ridge regression, Random Forest, Gradient Boosting, integración del equipo, gestión de Git).
- **Bernardo Maciel:** regresión lineal multivariada con OLS matricial, validación de supuestos Gauss-Markov, análisis de residuos, generación de 10 figuras del Día 6.
- **Juan Pablo Cruz:** análisis SQL, queries analíticas, benchmark.
- **Diego De Jesús:** comunicación visual, diseño del póster académico, preparación de la defensa oral.
**Agradecimientos:** A los profesores de las materias de Asymptotic Notation y Bayesian Inference por proporcionar el marco teórico que da estructura al análisis empírico presentado.
