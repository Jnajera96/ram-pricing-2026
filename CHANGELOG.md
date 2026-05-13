# 📝 Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [1.0.0] · 2026-05-15 · Academic Release 🎓

### Overview
First complete academic version with 5 predictive models, statistical inference,
and empirical complexity analysis. Project ready for university defense.

### Summary Statistics
- 📊 350 RAM products analyzed
- 🤖 5 predictive models trained and compared
- 🏆 Best model: Gradient Boosting (MAPE 8.32%, R²=0.962)
- ⚡ α=1.03 validates O(n) empirically
- 📈 26 figures generated at 300 DPI
- 🔬 6 paradigms triangulated

---

## [0.10.0] · 2026-05-15 · Day 10 · Repository Restructure

### Added
- Professional folder structure (`src/`, `tests/`, `docs/`, `archive/`)
- Migration script (`migrate.py`) with dry-run, real, and revert modes
- `requirements.txt` with pinned dependencies
- `LICENSE` (MIT)
- `ROADMAP.md` with project vision
- `CHANGELOG.md` (this file)
- Enhanced `.gitignore`
- 5 documentation files in `docs/`
- `__init__.py` in each Python package

### Changed
- Moved 29 Python files from root into modular structure
- Renamed files to English conventions (`limpiar.py` → `clean.py`, etc.)
- Reorganized `figures/` by analysis phase

---

## [0.9.0] · 2026-05-15 · Day 9 · ML Complexity Analysis

### Added
- `complejidad_ml.py` · Empirical ML complexity benchmarks
- `dashboard_final.py` · Master visualization synthesizing all results
- `figures/25_complejidad_ml.png` · Complexity analysis (n up to 100K)
- `figures/26_dashboard_final.png` · Project master visualization
- `data/complejidad_ml.csv` · Time scaling measurements
- `data/pendientes_complejidad.csv` · Empirical exponents

### Findings
- **Gradient Boosting α=1.03 validates O(n) theory empirically**
- Random Forest α=0.72 (parallelism hides true complexity)
- Linear models α≈0.4 (BLAS/LAPACK optimization)
- 75 measurements total (5 models × 5 sizes × 3 repetitions)

---

## [0.8.0] · 2026-05-14 · Day 8 · Ensemble Models

### Added
- `random_forest.py` · Model 4 (Bagging ensemble)
- `gradient_boosting.py` · Model 5 (Boosting ensemble) 🏆
- `figures/23_random_forest.png` · RF comparison
- `figures/24_gradient_boosting.png` · GB comparison
- GridSearchCV optimization for both models
- Final 5-model comparison table

### Results
- Random Forest: R²=0.902, MAPE=10.42%
- **Gradient Boosting: R²=0.9616, MAPE=8.32%** (best model)
- Gap train-test of only 0.030 for GB (excellent generalization)
- Convergence: capacity_gb importance reaches 85.6% in GB

---

## [0.7.0] · 2026-05-13 · Day 7 · K-Means and Ridge

### Added
- `kmeans.py` · Model 2 (Unsupervised clustering)
- `ridge.py` · Model 3 (L2 regularized regression)
- `figures/21_kmeans_clustering.png` · 6-panel visualization
- `figures/22_ridge_vs_ols.png` · Ridge comparison
- PCA visualization for clusters

### Findings
- K-Means k=2 reveals **Premium (DDR5) vs Economic (DDR4)** segmentation
- Silhouette=0.420 (reasonable structure)
- Ridge α=7.91 (GridSearchCV) — virtually identical to OLS
- **Three independent paradigms converge** on same market structure

---

## [0.6.0] · 2026-05-12 · Day 6 · Linear Regression (Bernardo)

### Added
- `regresion.py` · Model 1 (Multivariate OLS) by Bernardo Maciel
- 10 figures (11-20) covering distributions, scatter plots, VIF, coefficients
- Manual OLS implementation with `np.linalg.pinv`
- Full Gauss-Markov assumption validation

### Results
- R²=0.876, RMSE=$203, MAPE=17.36%
- All VIF<5 (no multicollinearity)
- Durbin-Watson=2.02 (no autocorrelation)
- **CORSAIR brand premium of 10-35%** controlling for technical features

---

## [0.5.0] · 2026-05-11 · Day 5 · Statistical Inference

### Added
- `inferencia.py` · Normality tests (Shapiro-Wilk, Levene)
- `inferencia_bloque2.py` · Welch's t-test (DDR4 vs DDR5)
- `inferencia_bloque3.py` · ANOVA + Tukey HSD by DDR
- `inferencia_bloque4.py` · ANOVA + Tukey HSD by brand
- `inferencia_dashboard.py` · Consolidated inferential dashboard
- 5 figures (06-10) covering all statistical tests

### Findings
- **DDR4 vs DDR5: t=17.83, p<0.000001, Cohen's d=2.20**
- ANOVA DDR: F=269.24, η²=0.608 (large effect)
- ANOVA brand: F=19.84, η²=0.224 (large but smaller)
- DDR explains 2.7× more variance than brand

---

## [0.4.0] · 2026-05-10 · Day 4 · SQL Complexity Analysis

### Added
- `crear_db.py` · SQLite database construction
- `crear_indices.py` · B-Tree index creation
- `bench_pre.py` · Pre-index query benchmarks
- `bench_post.py` · Post-index query benchmarks
- `bench_escalado.py` · Scaling test (n: 350 → 50,000)
- 2 figures (04-05) showing complexity benchmarks

### Findings
- **Q4 (covering index) speedup grows from 1.6× to 13.8×** with scaling
- "Index paradox": indices DEGRADE performance for low-selectivity queries
- Validates theoretical O(log n) with empirical measurements

---

## [0.3.0] · 2026-05-09 · Day 3 · Data Cleaning and EDA

### Added
- `limpiar.py` · Complete data cleaning pipeline
- `eda.py` · Exploratory data analysis with 3 figures
- Bayesian-light imputation for CAS Latency (median by DDR)

### Fixed
- **Pagination bug in Newegg** · Adopted alternative URL parameter
- Dataset grew from 12 → 359 unique products (30× larger)

### Results
- 350 cleaned products
- 100% CAS Latency coverage (with imputation)
- 17 final columns including derived features

---

## [0.2.0] · 2026-05-08 · Day 2 · Production Scraper

### Added
- `scraper.py` · Main Newegg scraper with multi-strategy regex parsers
- `recalcular_cas.py` · CAS Latency reprocessing utility
- 4 test scripts for parser validation

### Solved
- **Brotli compression bug** · Forced gzip encoding
- **DOM fragmentation in price** · Reconstructive parser
- **CAS Latency embedded in SKU** · 4-strategy cascade parser

---

## [0.1.0] · 2026-05-07 · Day 1 · Project Foundation

### Added
- Initial project structure
- `.gitignore`
- `web_scraping.py` · First exploration script
- `diagnostico.py` · HTTP debugging utility

### Discovered
- Newegg's anti-scraping measures (Brotli encoding)
- Need for robust regex parsing strategies

---

## Versioning Strategy

This project uses **Semantic Versioning**:
- **MAJOR.MINOR.PATCH**
- MAJOR (1.x) = Project milestones (academic release, web app, etc.)
- MINOR (x.X) = Daily sprint completion during academic development
- PATCH (x.x.X) = Bug fixes and minor improvements

Pre-1.0 versions represent the academic sprint days (Day 1 → 0.1.0,
Day 9 → 0.9.0). Version 1.0.0 marks the academic release for university defense.

---

## Contributors

| Day(s) | Contributor | Major Contributions |
|--------|-------------|---------------------|
| 1-10 | Jose Najera | Architecture, scraping, SQL, inference, K-Means, Ridge, RF, GB, complexity, restructure |
| 6 | Bernardo Maciel | OLS regression, Gauss-Markov validation, 10 figures |
| Various | Juan Pablo Cruz | SQL analysis, query optimization |
| Various | Diego De Jesus | Visual communication, poster design |

---

*Last updated: 2026-05-15 · See [README.md](README.md) for current state*
