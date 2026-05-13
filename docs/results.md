# 📊 Detailed Results

> Comprehensive findings from the RAM Pricing Prediction project
> University of Guadalajara · May 2026

---

## 📦 Dataset Summary

| Metric | Value |
|--------|-------|
| **Total products scraped** | 359 |
| **Cleaned and validated** | 350 |
| **Used for ML (post-filter)** | 300 |
| **Features** | 17 (after engineering) |
| **Target variable** | `log(price_usd)` |
| **Date of extraction** | May 8, 2026 |
| **Source** | Newegg.com (USA) |

### Distribution by DDR Generation

| DDR Type | Count | Percentage | Median Price |
|----------|-------|------------|--------------|
| DDR5 | 229 | 65.4% | $358 |
| DDR4 | 110 | 31.4% | $108 |
| DDR3 | 11 | 3.2% | $42 |

### Distribution by Brand

| Brand | Count | Percentage |
|-------|-------|------------|
| CORSAIR | 103 | 29.4% |
| Other | 100 | 28.6% |
| G.SKILL | 59 | 16.9% |
| Kingston | 43 | 12.3% |
| Team | 24 | 6.9% |
| Crucial | 21 | 6.0% |

---

## ⚡ SQL Complexity Analysis (Day 4)

### Pre vs Post Index Benchmarks (n=350)

| Query | Pre-index (ms) | Post-index (ms) | Speedup |
|-------|----------------|-----------------|---------|
| Q1 (selectivity 35%) | 0.42 | 0.39 | 1.08× |
| Q2 (selectivity 28%) | 0.51 | 0.33 | 1.54× |
| Q3 (selectivity 15%) | 0.48 | 0.31 | 1.55× |
| Q4 (covering index) | 0.71 | 0.44 | **1.61×** |

### Scaling Test (n: 350 → 50,000)

| n | Q4 Pre (ms) | Q4 Post (ms) | Speedup |
|---|-------------|--------------|---------|
| 350 | 0.71 | 0.44 | 1.61× |
| 1,000 | 1.34 | 0.50 | 2.66× |
| 5,000 | 4.42 | 0.51 | 8.65× |
| 10,000 | 8.91 | 1.09 | 8.14× |
| 50,000 | 50.24 | 3.64 | **13.79×** |

**Key Finding:** Q4 speedup grows from **1.6× to 13.8×** as data scales 143×.
This empirically validates **O(log n)** complexity for B-Tree indexed queries.

### The Index Paradox

For queries with low selectivity (>30% of rows returned):
- Q1: 1.08× → 0.79× (DEGRADES at scale)
- Q2: 1.54× → 0.61× (DEGRADES at scale)

**Why?** When most rows are returned, sequential scan is faster than
index lookup + table access. This is a documented pattern in database
optimization.

---

## 📊 Statistical Inference (Day 5)

### Normality Tests by DDR Generation

| Group | Shapiro-Wilk W | p-value | Normal? |
|-------|----------------|---------|---------|
| DDR3 | 0.872 | 0.085 | ✅ Yes |
| DDR4 | 0.961 | 0.003 | ❌ No |
| DDR5 | 0.962 | <0.001 | ❌ No |

**Decision:** Use Welch's t-test (handles non-normality better than Student's)
and triangulate with Mann-Whitney U (non-parametric).

### Welch's t-test: DDR4 vs DDR5

| Metric | Value |
|--------|-------|
| t-statistic | **17.83** |
| Degrees of freedom | 217.4 |
| p-value | < 0.000001 |
| Mean DDR4 (log-scale) | 4.69 |
| Mean DDR5 (log-scale) | 5.88 |
| Difference (log-scale) | 1.19 |
| **DDR5 price multiplier** | **3.86×** |

### Effect Size Cohen's d

```
Cohen's d = 2.20  →  "very large effect"

Scale:
  d < 0.2     trivial
  d < 0.5     small
  d < 0.8     medium
  d < 1.2     large
  d > 1.2     very large  ←  WE ARE HERE
```

### ANOVA by DDR Generation

| Statistic | Value |
|-----------|-------|
| F-statistic | **269.24** |
| p-value | < 0.000001 |
| η² (eta-squared) | **0.608** |
| Cohen's f | 1.25 |
| Conclusion | DDR explains 60.8% of variance |

**Tukey HSD post-hoc (all 3 pairs significant):**
- DDR3 vs DDR4: p < 0.001 ✅
- DDR3 vs DDR5: p < 0.001 ✅
- DDR4 vs DDR5: p < 0.001 ✅

### ANOVA by Brand

| Statistic | Value |
|-----------|-------|
| F-statistic | **19.84** |
| p-value | < 0.000001 |
| η² (eta-squared) | **0.224** |
| Cohen's f | 0.54 |
| Conclusion | Brand explains 22.4% of variance |

**Tukey HSD: 6 of 15 pairs significant** (40% significance rate)

### Final Verdict on Brand Premium

> **DDR generation explains 2.7× more variance than brand identity.**
> However, brand still adds **22.4% explanatory power**, confirming a
> **real but secondary** premium effect.

---

## 🤖 Model Results

### Model 1: OLS Linear Regression (Day 6 · Bernardo)

```
Specification:
  log(price_usd) ~ capacity_gb + speed_mhz + cas_latency 
                   + num_sticks + has_rgb + DDR5 
                   + brand (5 dummies)

Validation of Gauss-Markov assumptions:
  ✅ Multicollinearity:  All VIF < 5
  ✅ Normality:           QQ-plot r = 0.94
  ✅ Independence:        Durbin-Watson = 2.02
  ✅ Homoscedasticity:    Scale-location plot flat
  ⚠️  Linearity:          Slight quadratic curvature
```

| Coefficient | Estimate | Std Error | t-value | p-value |
|-------------|----------|-----------|---------|---------|
| Intercept | 3.24 | 0.18 | 18.4 | <0.001 |
| capacity_gb | **+0.49** | 0.03 | 16.7 | **<0.001** |
| speed_mhz | **+0.32** | 0.05 | 6.4 | **<0.001** |
| cas_latency | -0.09 | 0.03 | -3.0 | 0.003 |
| ddr_legacy | -0.15 | 0.04 | -3.7 | <0.001 |
| brand_CORSAIR | (base) | — | — | — |
| brand_G.SKILL | -0.18 | 0.05 | -3.6 | <0.001 |
| brand_Kingston | -0.33 | 0.06 | -5.7 | <0.001 |

**Key finding:** All non-CORSAIR brands have **negative coefficients**,
indicating CORSAIR commands a brand premium of **10-35%**.

### Model 2: K-Means Clustering (Day 7)

| Strategy | Silhouette | n_clusters | Interpretation |
|----------|-----------|------------|----------------|
| **k=2 (principal)** | 0.420 | 2 | Premium vs Economic |
| k=8 (exploratory) | 0.493 | 8 | Fine-grained niches |

**Cluster characteristics (k=2):**

| Cluster | Size | DDR5 % | Median Price | Top Brand |
|---------|------|--------|--------------|-----------|
| 0 · Premium | 219 | 100% | $490 | CORSAIR (39%) |
| 1 · Economic | 81 | 6.2% | $166 | Other (32%) |

**Key finding:** Brands are **MIXED** across both clusters. This validates
the ANOVA finding that **DDR generation segments the market more strongly
than brand**.

### Model 3: Ridge Regression (Day 7)

| Metric | OLS | Ridge | Δ |
|--------|-----|-------|---|
| α (penalty) | 0 | **7.91** | — |
| R² train | 0.9066 | 0.9055 | -0.001 |
| R² test | 0.8758 | 0.8686 | -0.007 |
| RMSE | $203.14 | $198.46 | **-$4.69** |
| MAE | $107.11 | $106.14 | **-$0.97** |
| MAPE | 17.36% | 17.45% | +0.09% |

**Coefficient shrinkage (relative to OLS):**

```
capacity_gb:        -4%   (strong signal, stable)
speed_mhz:         -11%   (strong signal)
brand_G.SKILL:     -31%   (weaker signal)
brand_Kingston:    -73%   (weakest signal)
```

**Key finding:** Ridge **disproportionately shrinks brand coefficients**,
acting as an implicit relevance detector. Brands have weaker statistical
signal than technical features.

### Model 4: Random Forest (Day 8)

**Hyperparameters (via GridSearchCV with 36 combinations):**
```python
{
    'n_estimators': 300,
    'max_depth': 20,
    'min_samples_split': 2,
    'max_features': 'sqrt'
}
```

**Performance:**

| Metric | Train | Test | CV-5 |
|--------|-------|------|------|
| R² | 0.9922 | **0.9020** | 0.9392 ± 0.019 |
| MAPE | — | 10.42% | — |
| MAE | — | $71 | — |

**Feature importances (top 5):**

```
capacity_gb:       46.77%  ████████████
speed_mhz:         16.28%  ████
cas_latency:       11.81%  ███
ddr_legacy:        11.29%  ███
num_sticks:         7.26%  ██
```

### Model 5: Gradient Boosting 🏆 (Day 8)

**Hyperparameters (via GridSearchCV with 54 combinations):**
```python
{
    'n_estimators': 200,
    'learning_rate': 0.05,
    'max_depth': 3,
    'subsample': 1.0
}
```

**Performance:**

| Metric | Train | Test | CV-5 |
|--------|-------|------|------|
| R² | 0.9918 | **0.9616** ✅ | 0.9601 ± 0.018 |
| MAPE | — | **8.32%** ✅ | — |
| MAE | — | **$52** ✅ | — |
| RMSE | — | **$125** ✅ | — |

**Feature importances (top 5):**

```
capacity_gb:       85.6%   ████████████████████████████████████
speed_mhz:          7.1%   ███
ddr_legacy:         3.5%   ██
cas_latency:        1.6%   █
brand_Other:        0.9%   ░
```

**Key insights:**
1. **Best generalization:** train-test gap of only 0.030 (vs 0.090 in RF)
2. **Extreme feature concentration:** capacity_gb at 85.6% (highest of all models)
3. **Implicit regularization:** learning_rate=0.05 + max_depth=3 = stable

---

## ⚡ Empirical Complexity Analysis (Day 9)

### Time Scaling Measurements

```
Model              n=1K     n=5K     n=20K    n=50K     n=100K   α
─────────────────────────────────────────────────────────────────
OLS                2.8ms    2.4ms    6.2ms    10ms      24ms     0.46
Ridge              2.0ms    1.5ms    4.0ms    7ms       12ms     0.42
K-Means            6.8ms    14ms     32ms     65ms      141ms    0.64
Random Forest      0.13s    0.19s    0.57s    1.39s     3.40s    0.72
Gradient Boosting  0.21s    0.97s    4.31s    11.35s    23.74s   1.03 ✅
```

### Theoretical vs Empirical Match

| Model | Theory | Empirical α | Match |
|-------|--------|-------------|-------|
| OLS | O(p³) ≈ O(1) for fixed p | 0.46 | Partial (BLAS optim.) |
| Ridge | O(p³) ≈ O(1) for fixed p | 0.42 | Partial (BLAS optim.) |
| K-Means | O(n·k·i·d) | 0.64 | Partial (iterations) |
| Random Forest | O(n·log n) | 0.72 | Partial (parallel) |
| **Gradient Boosting** | **O(n)** | **1.03** | ✅ **EXACT** |

**Key insight:** Asymptotic exponents emerge only when **n is large enough
relative to runtime overhead**. Gradient Boosting, being inherently
sequential, provides the cleanest theory-to-empirical validation.

---

## 🎯 Summary of Findings

### Question 1: Does brand premium exist?
> ✅ **YES**, but secondary to technical specifications.
> - CORSAIR commands 10-35% premium controlling for features
> - Brand explains 22.4% of variance (η²)
> - All non-CORSAIR brands have negative β coefficients

### Question 2: What predicts RAM price most strongly?
> 🏆 **capacity_gb** is the dominant predictor in all 6 paradigms:
> - OLS β: +0.49 (largest coefficient)
> - Random Forest importance: 46.8%
> - Gradient Boosting importance: 85.6%

### Question 3: Does asymptotic theory apply to ML?
> ✅ **Yes, when n is sufficiently large.**
> - Gradient Boosting α=1.03 validates O(n) exactly
> - Parallelism and BLAS optimization mask growth in other models
> - This is a fundamental observation about empirical complexity

---

## 📊 Visualizations Generated

**26 figures at 300 DPI**, organized by analysis stage:

| Stage | Figures | Examples |
|-------|---------|----------|
| EDA | 01-03 | Correlation heatmap, log transform |
| SQL complexity | 04-05 | Pre/post benchmarks, scaling test |
| Inference | 06-10 | t-test, ANOVA, dashboards |
| OLS regression | 11-20 | Coefficients, residuals, predictions |
| K-Means | 21 | 6-panel clustering analysis |
| Ridge | 22 | α tuning, shrinkage visualization |
| Random Forest | 23 | Feature importance, predictions |
| Gradient Boosting | 24 | Performance, learning curves |
| Complexity ML | 25 | Empirical exponents, log-log plots |
| Master dashboard | 26 | Synthesis of all results |

---

*See also: [📖 methodology.md](methodology.md) | [🤖 models_comparison.md](models_comparison.md) | [⚡ complexity_analysis.md](complexity_analysis.md)*
