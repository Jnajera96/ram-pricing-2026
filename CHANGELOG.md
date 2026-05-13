# 📝 Historial de Cambios
 
Todos los cambios notables de este proyecto están documentados en este archivo.
 
El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
y este proyecto sigue [Versionado Semántico](https://semver.org/lang/es/).
 
---
 
## [1.0.0] · 2026-05-15 · Versión Académica 🎓
 
### Resumen
Primera versión académica completa con 5 modelos predictivos, inferencia
estadística y análisis empírico de complejidad. Proyecto listo para
defensa universitaria.
 
### Estadísticas del Proyecto
- 📊 350 productos de memoria RAM analizados
- 🤖 5 modelos predictivos entrenados y comparados
- 🏆 Mejor modelo: Gradient Boosting (MAPE 8.32%, R²=0.962)
- ⚡ α=1.03 valida 𝒪(n) empíricamente
- 📈 26 figuras generadas a 300 DPI
- 🔬 6 paradigmas triangulados
---
 
## [0.10.0] · 2026-05-15 · Día 10 · Reestructura del Repositorio
 
### Añadido
- Estructura profesional de carpetas (`src/`, `tests/`, `docs/`, `archive/`)
- Script de migración (`migrate.py`) con modos dry-run, real y revert
- `requirements.txt` con dependencias fijadas
- `LICENSE` (MIT)
- `ROADMAP.md` con visión del proyecto
- `CHANGELOG.md` (este archivo)
- `.gitignore` mejorado
- 5 archivos de documentación en `docs/`
- `__init__.py` en cada paquete Python
### Modificado
- Movidos 29 archivos Python de la raíz a la estructura modular
- Renombrados archivos a convenciones en inglés (`limpiar.py` → `clean.py`, etc.)
- Reorganizadas las figuras de `figures/` por fase de análisis
### Decisiones de diseño
- Backup físico completo antes de mover archivos
- Branch separado (`restructure-professional`) para experimentar con seguridad
- Migración con seguridad triple: dry-run, log JSON reversible, branch separado
- Estructura inspirada en proyectos top de GitHub (clean code, modular)
---
 
## [0.9.0] · 2026-05-15 · Día 9 · Análisis Empírico de Complejidad ML
 
### Añadido
- `complejidad_ml.py` · Benchmarks empíricos de complejidad ML
- `dashboard_final.py` · Visualización maestra sintetizando todos los resultados
- `figures/25_complejidad_ml.png` · Análisis de complejidad (n hasta 100K)
- `figures/26_dashboard_final.png` · Visualización maestra del proyecto
- `data/complejidad_ml.csv` · Mediciones de escalado temporal
- `data/pendientes_complejidad.csv` · Exponentes empíricos
### Hallazgos
- **Gradient Boosting α=1.03 valida 𝒪(n) teórico empíricamente** ✅
- Random Forest α=0.72 (el paralelismo oculta la complejidad real)
- Modelos lineales α≈0.4 (optimización BLAS/LAPACK)
- 75 mediciones totales (5 modelos × 5 tamaños × 3 repeticiones)
### Insight metodológico crítico
> Los exponentes asintóticos solo emergen cuando n es suficientemente
> grande respecto al overhead del runtime. Gradient Boosting, al ser
> inherentemente secuencial, ofrece la validación más limpia de la
> teoría asintótica.
 
---
 
## [0.8.0] · 2026-05-14 · Día 8 · Modelos Ensemble
 
### Añadido
- `random_forest.py` · Modelo 4 (Ensemble Bagging)
- `gradient_boosting.py` · Modelo 5 (Ensemble Boosting) 🏆
- `figures/23_random_forest.png` · Comparativa de Random Forest
- `figures/24_gradient_boosting.png` · Comparativa de Gradient Boosting
- Optimización con GridSearchCV para ambos modelos
- Tabla comparativa final de los 5 modelos
### Resultados
- Random Forest: R²=0.902, MAPE=10.42%
- **Gradient Boosting: R²=0.9616, MAPE=8.32%** (mejor modelo)
- Gap train-test de solo 0.030 para GB (excelente generalización)
- Convergencia: capacity_gb alcanza 85.6% de importance en GB
### Decisión académica
- Reportar **dos modelos complementarios** en lugar de uno solo:
  - OLS para **INFERENCIA** (interpretabilidad)
  - Gradient Boosting para **PREDICCIÓN** (menor error)
---
 
## [0.7.0] · 2026-05-13 · Día 7 · K-Means y Ridge
 
### Añadido
- `kmeans.py` · Modelo 2 (Clustering no-supervisado)
- `ridge.py` · Modelo 3 (Regresión regularizada L2)
- `figures/21_kmeans_clustering.png` · Visualización de 6 paneles
- `figures/22_ridge_vs_ols.png` · Comparativa con Ridge
- Visualización PCA para clusters
### Hallazgos
- K-Means k=2 revela segmentación **Premium (DDR5) vs Económico (DDR4)**
- Silhouette=0.420 (estructura razonable)
- Ridge α=7.91 (GridSearchCV) — prácticamente idéntico a OLS
- **Tres paradigmas independientes convergen** en la misma estructura del mercado
### Insight crítico
> Las marcas están **MEZCLADAS** en ambos clusters. Esto valida
> cuantitativamente el hallazgo del ANOVA del Día 5: la generación
> tecnológica explica más varianza que la marca específica.
 
---
 
## [0.6.0] · 2026-05-12 · Día 6 · Regresión Lineal (Bernardo)
 
### Añadido
- `regresion.py` · Modelo 1 (OLS multivariado) por Bernardo Maciel
- 10 figuras (11-20) cubriendo distribuciones, scatter plots, VIF, coeficientes
- Implementación OLS manual con `np.linalg.pinv`
- Validación completa de supuestos Gauss-Markov
### Resultados
- R²=0.876, RMSE=$203, MAPE=17.36%
- Todos los VIF<5 (sin multicolinealidad)
- Durbin-Watson=2.02 (sin autocorrelación)
- **Premium de marca CORSAIR de 10-35%** controlando por features técnicos
### Frase de defensa oral memorable
> "CORSAIR comanda un premium real de marca, no es percepción.
> Todas las demás marcas tienen coeficientes negativos respecto a CORSAIR,
> con p<0.001 en todos los casos."
 
---
 
## [0.5.0] · 2026-05-11 · Día 5 · Inferencia Estadística
 
### Añadido
- `inferencia.py` · Tests de normalidad (Shapiro-Wilk, Levene)
- `inferencia_bloque2.py` · Test t de Welch (DDR4 vs DDR5)
- `inferencia_bloque3.py` · ANOVA + Tukey HSD por DDR
- `inferencia_bloque4.py` · ANOVA + Tukey HSD por marca
- `inferencia_dashboard.py` · Dashboard inferencial consolidado
- 5 figuras (06-10) cubriendo todos los tests estadísticos
### Hallazgos
- **DDR4 vs DDR5: t=17.83, p<0.000001, Cohen's d=2.20** (efecto muy grande)
- ANOVA DDR: F=269.24, η²=0.608 (efecto grande)
- ANOVA marca: F=19.84, η²=0.224 (efecto grande pero menor)
- DDR explica **2.7× más varianza** que la marca
### Triangulación metodológica
- Welch's t-test (paramétrico)
- Mann-Whitney U (no-paramétrico)
- Cohen's d (effect size)
- → Los 3 convergen en la misma conclusión
---
 
## [0.4.0] · 2026-05-10 · Día 4 · Análisis de Complejidad SQL
 
### Añadido
- `crear_db.py` · Construcción de la base de datos SQLite
- `crear_indices.py` · Creación de índices B-Tree
- `bench_pre.py` · Benchmarks pre-índices
- `bench_post.py` · Benchmarks post-índices
- `bench_escalado.py` · Test de escalado (n: 350 → 50,000)
- 2 figuras (04-05) mostrando benchmarks de complejidad
### Hallazgos
- **Speedup Q4 (covering index) crece de 1.6× a 13.8×** con escalado
- "Paradoja del índice": índices DEGRADAN para queries de baja selectividad
- Validación empírica de 𝒪(log n) con mediciones reales
### Insight inesperado
> Para queries con baja selectividad (>30% del dataset), los índices
> B-Tree empeoran el rendimiento. Esto contradice la teoría ingenua
> pero es un fenómeno documentado en bases de datos reales.
 
---
 
## [0.3.0] · 2026-05-09 · Día 3 · Limpieza de Datos y EDA
 
### Añadido
- `limpiar.py` · Pipeline completo de limpieza de datos
- `eda.py` · Análisis exploratorio con 3 figuras
- Imputación bayesiana ligera para CAS Latency (mediana por DDR)
### Corregido
- **Bug de paginación en Newegg** · Adoptado parámetro URL alternativo
- Dataset creció de 12 → 359 productos únicos (**30× más grande**)
### Resultados
- 350 productos limpios
- 100% cobertura de CAS Latency (post-imputación)
- 17 columnas finales incluyendo features derivados
### Decisión técnica defendible
> La imputación bayesiana ligera (mediana por DDR) actúa como prior
> informativo. Es defendible porque la CAS Latency está fuertemente
> correlacionada con la generación DDR (validado con ANOVA).
 
---
 
## [0.2.0] · 2026-05-08 · Día 2 · Scraper de Producción
 
### Añadido
- `scraper.py` · Scraper principal de Newegg con parsers regex multi-estrategia
- `recalcular_cas.py` · Utilidad de reprocesamiento de CAS Latency
- 4 scripts de test para validación de parsers
### Resuelto
- **Bug de compresión Brotli** · Forzado encoding gzip
- **Fragmentación del DOM en precio** · Parser que reconstruye desde átomos
- **CAS Latency embebido en SKU** · Parser de cascada en 4 estrategias
### Decisiones de arquitectura
- `dataclass` para representación type-safe de productos
- `try/except` por item (no por batch) para granularidad de error
- HTTP con `requests` puro (sin headless browser) para mayor velocidad
---
 
## [0.1.0] · 2026-05-07 · Día 1 · Fundación del Proyecto
 
### Añadido
- Estructura inicial del proyecto
- `.gitignore`
- `web_scraping.py` · Primer script de exploración
- `diagnostico.py` · Utilidad de debugging HTTP
### Descubierto
- Medidas anti-scraping de Newegg (encoding Brotli)
- Necesidad de estrategias robustas de parsing con regex
### Primer aprendizaje del proyecto
> El scraping no es solo `requests.get()`. Los sitios modernos tienen
> defensas (Brotli, DOM fragmentado, datos embebidos en SKU). La calidad
> del parser determina la calidad del dataset.
 
---
 
## 📋 Estrategia de Versionado
 
Este proyecto usa **Versionado Semántico**:
- **MAJOR.MINOR.PATCH**
- MAJOR (1.x) = Hitos del proyecto (versión académica, web app, etc.)
- MINOR (x.X) = Completar sprint diario durante desarrollo académico
- PATCH (x.x.X) = Correcciones de bugs y mejoras menores
Las versiones pre-1.0 representan los días del sprint académico
(Día 1 → 0.1.0, Día 9 → 0.9.0). La versión 1.0.0 marca la versión
académica final para la defensa universitaria.
 
---
 
## 👥 Contribuidores por Sprint
 
| Día(s) | Contribuidor | Contribuciones Principales |
|--------|--------------|---------------------------|
| 1-10 | José Najera | Arquitectura, scraping, SQL, inferencia, K-Means, Ridge, RF, GB, complejidad, reestructura |
| 6 | Bernardo Maciel | Regresión OLS, validación Gauss-Markov, 10 figuras |
| Varios | Juan Pablo Cruz | Análisis SQL, optimización de queries |
| Varios | Diego De Jesús | Comunicación visual, diseño del póster |
 
---
 
## 🎯 Métricas del Sprint
 
### Velocidad de trabajo
- **9 días continuos** sin un solo bloqueo serio
- **75% del sprint completado** en tiempo
- **0 días perdidos** por bugs o problemas técnicos
### Calidad del código
- **26 figuras** generadas a 300 DPI
- **75 mediciones** empíricas de complejidad
- **6 paradigmas** triangulados
- **5 modelos** entrenados con GridSearchCV
- **2,769 inserciones** en el commit final de reestructura
### Hallazgos científicos
- **capacity_gb domina** en 6 paradigmas convergentes
- **CORSAIR premium** del 10-35% validado estadísticamente
- **Gradient Boosting α=1.03** valida 𝒪(n) empíricamente
- **DDR explica 2.7×** más varianza que marca
---
 
## 🛣️ Hacia el Futuro
 
Consulta [ROADMAP.md](ROADMAP.md) para conocer las fases planeadas:
 
- **Fase 2 · Web Application** (Q3 2026): Dashboard React + FastAPI
- **Fase 3 · Data Expansion** (Q4 2026): Multi-source scraping, time series
- **Fase 4 · Production Features** (Futuro): Cuentas, alertas, recomendaciones
---
 
## 📝 Convenciones del Changelog
 
### Tipos de cambios
- **Añadido** · Para funcionalidades nuevas
- **Modificado** · Para cambios en funcionalidades existentes
- **Obsoleto** · Para funcionalidades que serán removidas pronto
- **Removido** · Para funcionalidades removidas
- **Corregido** · Para arreglo de bugs
- **Seguridad** · Para temas de seguridad
### Formato de fechas
- Formato: YYYY-MM-DD (ISO 8601)
- Zona horaria: America/Mexico_City
### Frase de mentor que define el proyecto
> *"Programar bien no es tener todo perfecto al primer intento — es saber
> diagnosticar, ajustar y documentar el aprendizaje. La verdadera
> contribución académica es el método de evaluación: cinco modelos sobre
> el mismo split, mismas features, métricas comparables, decisión justificada."*
 
---
 
