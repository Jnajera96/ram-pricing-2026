# 📚 Methodology

> Comprehensive methodology for the RAM Pricing Prediction project
> University of Guadalajara · Data Science · May 2026

---

## 🎯 Research Question

> **"Does a real brand premium exist in the RAM memory market, or is price
> explained solely by technical specifications?"**

This dual question drives the methodological framework: simultaneously
**explanatory** (which variables matter) and **predictive** (how well can
we forecast prices).

---

## 🔬 Six Methodological Paradigms

The project deliberately applies six independent analytical paradigms to
**triangulate findings**. Convergence across paradigms strengthens validity.

```
┌─────────────────────────────────────────────────────────────────┐
│  PARADIGM           │  METHOD            │  ROLE                │
├─────────────────────┼────────────────────┼──────────────────────┤
│ 1. Inferential      │ ANOVA + Tukey      │ Variance explained   │
│ 2. Parametric Pred. │ OLS Regression     │ Interpretable coefs  │
│ 3. Regularized      │ Ridge Regression   │ Detect relevance     │
│ 4. Unsupervised     │ K-Means k=2        │ Market segmentation  │
│ 5. Bagging          │ Random Forest      │ Non-linear capture   │
│ 6. Boosting         │ Gradient Boosting  │ Sequential learning  │
└─────────────────────┴────────────────────┴──────────────────────┘
```

**Why triangulation?** A single method can be misleading. Six independent
methods reaching the same conclusion provides robust evidence.

---

## 📊 Data Pipeline

### Stage 1 · Acquisition (Day 1-2)
- Source: **Newegg.com** (USA market)
- Method: HTTP scraping with `requests` + `BeautifulSoup4`
- Volume: 359 raw products → 350 cleaned
- Challenges solved:
  - Brotli compression handling
  - DOM fragmentation in price elements
  - CAS Latency embedded in SKU codes (4-strategy parser)

### Stage 2 · Cleaning (Day 3)
- Feature engineering: 17 final columns
- Bayesian-light imputation: median by DDR generation
- Coverage: 100% for all features (post-imputation)
- Log transformation: `log(price_usd)` due to right skew

### Stage 3 · Storage (Day 4)
- SQLite database with explicit schema
- B-Tree indices on `ddr_type`, `brand_normalized`, `capacity_gb`
- Empirical complexity validated up to n=50,000

### Stage 4 · Inference (Day 5)
- Triangulated tests:
  - Welch's t-test (parametric)
  - Mann-Whitney U (non-parametric)
  - Cohen's d (effect size)
- ANOVA F-tests with Tukey HSD post-hoc
- Eta-squared for effect magnitude

### Stage 5 · Modeling (Day 6-8)
- Five models on **identical train/test split** (80/20, random_state=42)
- GridSearchCV for hyperparameter tuning
- Cross-validation (5-fold) for robustness

### Stage 6 · Complexity (Day 9)
- Empirical measurements with n: 1,000 → 100,000
- Log-log regression for α exponent
- 75 measurements total (5 models × 5 sizes × 3 repetitions)

---

## 🧮 Statistical Decisions

### Why log-transform price?
- Right-skewed distribution (Pearson skewness = 1.87)
- Heteroscedasticity in residuals
- Multiplicative relationships expected (% changes more meaningful than $)

### Why train/test split 80/20?
- Standard practice with n=300 valid samples
- Sufficient train (240) for stable model fitting
- Adequate test (60) for variance estimation

### Why random_state=42?
- Reproducibility across all models
- Comparable evaluations
- Industry convention (HHGTTG reference)

### Why GridSearchCV with 5-fold?
- Balance between bias (high k) and variance (low k)
- 5-fold standard for n<1000 samples
- Reduces hyperparameter overfitting

---

## 📈 Model Selection Philosophy

### The "Two Models" Approach

Rather than crowning a single winner, the project reports **two complementary models**:

```
┌─────────────────────────────────────────────────────────────────┐
│  PURPOSE         │  MODEL              │  WHY                   │
├──────────────────┼─────────────────────┼────────────────────────┤
│ EXPLANATION     │ OLS (Day 6)         │ Interpretable β coefs   │
│                  │                     │ p-values, IC at 95%    │
│                  │                     │ Connects to inference  │
├──────────────────┼─────────────────────┼────────────────────────┤
│ PREDICTION       │ Gradient Boosting   │ Lowest error (MAPE 8.3%)│
│                  │  (Day 8)            │ Non-linear interactions │
│                  │                     │ Robust to outliers     │
└──────────────────┴─────────────────────┴────────────────────────┘
```

This dual reporting respects the **two audiences** of the project:
- **Researchers** need OLS to understand the market
- **Engineers** need GB for production deployment

---

## ⚡ Asymptotic Analysis

### Theoretical Complexity

| Model | Training | Prediction |
|-------|----------|------------|
| OLS | O(p³) | O(p) |
| Ridge | O(p³) | O(p) |
| K-Means | O(n·k·i·d) | O(k·d) |
| Random Forest | O(n·log(n)·m) | O(m·d) |
| Gradient Boosting | O(n·m·d) | O(m·d) |

### Empirical Validation

```
Model              α (empirical)    Theory match
─────────────────────────────────────────────────
OLS                0.46             Sub-linear (BLAS optim.)
Ridge              0.42             Sub-linear (BLAS optim.)
K-Means            0.64             Iterative behavior
Random Forest      0.72             Parallelism masks growth
Gradient Boosting  1.03             ✅ Validates O(n) EXACTLY
```

**Key insight:** Asymptotic theory manifests when n is large enough
relative to runtime overhead. Gradient Boosting, being inherently
sequential, provides the cleanest validation of theoretical complexity.

---

## 🎓 Academic Standards Applied

This methodology adheres to:

1. **Pre-registration** · Methods declared before results
2. **Reproducibility** · `random_state=42` everywhere, full code public
3. **Triangulation** · Multiple methods reach same conclusion
4. **Effect sizes** · Beyond p-values (Cohen's d, eta-squared)
5. **Multiple comparisons** · Tukey HSD controls family-wise error
6. **Honest reporting** · All models reported, not just winners

---

## 📖 Key References

- **Cormen et al.** *Introduction to Algorithms* — Asymptotic framework
- **Cohen (1988)** — Effect size interpretation
- **Tukey (1949)** — Multiple comparisons procedure
- **Breiman (2001)** — Random Forest original
- **Friedman (2001)** — Gradient Boosting Machine
- **Tikhonov (1943)** — Ridge regularization
- **MacQueen (1967)** — K-Means clustering

---

*See `02_architecture.md` for technical implementation details.*
*See `03_results.md` for detailed findings.*
