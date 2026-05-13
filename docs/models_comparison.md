# 🤖 Models Comparison

> In-depth comparison of the 5 predictive models trained
> University of Guadalajara · May 2026

---

## 📋 The Five Models

The project trains and compares **5 models** across different paradigms,
all on the **identical train/test split** for fair comparison.

| # | Model | Paradigm | Day Implemented |
|---|-------|----------|-----------------|
| 1 | OLS | Linear regression | Day 6 |
| 2 | K-Means | Clustering (unsupervised) | Day 7 |
| 3 | Ridge | L2 regularized regression | Day 7 |
| 4 | Random Forest | Bagging ensemble | Day 8 |
| 5 | Gradient Boosting | Boosting ensemble | Day 8 |

---

## 🏆 Performance Comparison

### Test Set Metrics (n_test = 60)

| Model | R² | RMSE | MAE | MAPE |
|-------|-----|------|-----|------|
| OLS | 0.876 | $203 | $107 | 17.36% |
| Ridge | 0.869 | $198 | $106 | 17.45% |
| K-Means | N/A | N/A | N/A | N/A |
| Random Forest | 0.902 | $159 | $71 | 10.42% |
| **Gradient Boosting** | **0.962** | **$125** | **$52** | **8.32%** |

### Visual Ranking by MAPE

```
🥇 Gradient Boosting   ██░ 8.32%
🥈 Random Forest       ████░ 10.42%
🥉 OLS                 ████████████░ 17.36%
   Ridge               ████████████░ 17.45%
```

### Cross-Validation Robustness (5-fold)

| Model | CV R² Mean | CV R² Std | CV R² Range |
|-------|-----------|-----------|-------------|
| Ridge | 0.885 | 0.024 | [0.84, 0.91] |
| Random Forest | 0.939 | 0.019 | [0.92, 0.97] |
| **Gradient Boosting** | **0.960** | **0.018** | **[0.94, 0.98]** |

Gradient Boosting has the **highest mean AND lowest variance** — best on both
axes of model selection.

---

## 🔬 Detailed Comparison Per Model

### OLS · The Baseline

**Strengths:**
- ✅ Highly interpretable coefficients
- ✅ p-values and confidence intervals
- ✅ Direct connection to inferential statistics
- ✅ Fastest training (3 ms)
- ✅ Validates Gauss-Markov assumptions

**Weaknesses:**
- ❌ Assumes linearity (real world is non-linear)
- ❌ Cannot capture interactions
- ❌ MAPE 17.36% is mediocre for production

**When to use:** Research and policy analysis where **why** matters more than **how accurate**.

---

### Ridge · The Stable Sibling

**Strengths:**
- ✅ Same interpretability as OLS
- ✅ Robust to multicollinearity
- ✅ Reveals **relative feature relevance** via shrinkage

**Weaknesses:**
- ❌ Performance virtually identical to OLS (Δ R² = -0.007)
- ❌ Adds complexity (α tuning) without significant gain

**Verdict:** Ridge **confirms** that OLS was well-specified. The lack of
significant improvement validates that multicollinearity wasn't a problem.
Ridge's value is **diagnostic, not predictive**.

---

### K-Means · The Outsider

**Strengths:**
- ✅ Reveals **natural market structure** without supervision
- ✅ Validates ANOVA finding (DDR > brand) from completely different paradigm
- ✅ Useful for **segmentation and discovery**

**Weaknesses:**
- ❌ Does NOT predict prices directly
- ❌ Silhouette 0.420 is moderate (not strong)
- ❌ Sensitive to feature scaling

**Key insight:** Brands are **MIXED** in both clusters. The market segments
by DDR generation, not by brand. This is a powerful finding.

---

### Random Forest · The Non-linear Workhorse

**Strengths:**
- ✅ Captures non-linear interactions automatically
- ✅ Feature importance available (interpretable proxy)
- ✅ Robust to outliers
- ✅ R² gain of +2.6% over OLS (significant)
- ✅ MAPE drops from 17.4% → 10.4% (huge in absolute terms)

**Weaknesses:**
- ❌ Coefficients not interpretable
- ❌ More complex to deploy
- ❌ Slight overfitting (gap train-test = 0.09)

**When to use:** Production prediction systems where interpretability isn't critical.

---

### Gradient Boosting · The Champion 🏆

**Strengths:**
- ✅ **Best R² across all metrics** (0.962)
- ✅ **Lowest MAPE** (8.32%)
- ✅ **Best generalization** (gap = 0.030, very low)
- ✅ Best cross-validation stability
- ✅ Implicit regularization (low lr + shallow trees)

**Weaknesses:**
- ❌ Black-box predictions (despite feature importance)
- ❌ Sensitive to hyperparameters (needed GridSearchCV)
- ❌ Slower than RF (sequential, not parallelizable)

**Why it wins:** Sequential learning corrects residuals iteratively. Each
tree fixes mistakes from previous trees. This is fundamentally more
efficient than parallel bagging for this dataset.

---

## 🎯 Feature Importance Across Models

```
Feature           OLS    Ridge   RF     GB
────────────────────────────────────────────
capacity_gb       +0.49  +0.47  46.8%  85.6%
speed_mhz         +0.32  +0.28  16.3%   7.1%
cas_latency       -0.09  -0.06  11.8%   1.6%
ddr_legacy        -0.15  -0.15  11.3%   3.5%
num_sticks        +0.06  +0.07   7.3%   0.7%
brand_Other       (var)  (var)  3.0%    0.9%
brand_others      (var)  (var)  <2%    <1%
```

**Convergence:** All four models agree that:
1. `capacity_gb` is dominant
2. `speed_mhz` is secondary
3. `cas_latency` and `ddr_legacy` are tertiary
4. Brand effects are minimal (<10% each)

**Divergence:** GB concentrates more importance in `capacity_gb` (85.6% vs
46.8% for RF). This reflects the **sequential nature** of boosting: the
first tree captures the dominant signal, subsequent trees add fine
adjustments.

---

## 🎓 The "Two Models" Philosophy

Rather than crowning a single winner, the project reports **two complementary models**:

### Model for Inference: **OLS**
```
WHY:
  • Interpretable β coefficients with p-values
  • Direct link to inferential statistics
  • Brand premium quantifiable (-10 to -35% vs CORSAIR)
  • Validates Gauss-Markov theorem assumptions

WHEN TO USE:
  • Academic research
  • Policy analysis
  • Explaining "why" prices behave as they do
  • Defending findings statistically
```

### Model for Prediction: **Gradient Boosting**
```
WHY:
  • Lowest error (MAPE 8.32%)
  • Best generalization (gap 0.030)
  • Captures non-linear interactions
  • Robust to outliers

WHEN TO USE:
  • Production deployment
  • Price prediction APIs
  • Recommendation systems
  • When accuracy > interpretability
```

---

## 📊 Decision Matrix for Practitioners

| Criterion | OLS | Ridge | K-Means | RF | GB |
|-----------|-----|-------|---------|----|----|
| Interpretability | 🏆 High | High | High | Medium | Medium |
| Prediction accuracy | Medium | Medium | N/A | High | 🏆 Highest |
| Speed (training) | 🏆 ms | ms | s | s | s |
| Speed (inference) | 🏆 μs | μs | μs | ms | ms |
| Robustness to outliers | Low | Low | Medium | High | 🏆 Highest |
| Hyperparameter sensitivity | None | Low | Medium | Medium | High |
| Handles non-linearity | No | No | Yes | 🏆 Yes | 🏆 Yes |
| Memory footprint | 🏆 KB | KB | KB | MB | MB |

---

## 🚀 Production Deployment Considerations

If deploying to production, here's the practical guidance:

### For a price prediction API
**→ Use Gradient Boosting**
- 200 trees × max_depth 3 = small model (~5 MB)
- Single prediction in 1-3 ms
- 91.7% accuracy in real terms (1 - MAPE)
- Serialization via `joblib.dump()`

### For an explanatory dashboard
**→ Use OLS coefficients**
- Show brand premium as direct percentage
- Display p-values for credibility
- Update quarterly with new data

### For market research
**→ Use K-Means cluster assignments**
- Categorize new products as Premium/Economic
- Show distribution per cluster over time
- Inform pricing strategy

---

## 📈 Improvement Roadmap

### To improve Gradient Boosting further:
1. **More data:** Scrape from Amazon, Best Buy (~2,000 products)
2. **Engineered features:** $/GB, $/MHz, value scores
3. **Try XGBoost:** Faster + often better than sklearn GB
4. **Try LightGBM:** Even faster, leaf-wise growth
5. **Stacking:** Combine GB + RF + OLS predictions

### Expected improvements:
- MAPE: 8.32% → 5-7%
- R²: 0.962 → 0.97-0.98
- Training time: maintained or improved

---

*See: [📊 results.md](results.md) for detailed numerical findings*
*See: [📖 methodology.md](methodology.md) for the research framework*
*See: [⚡ complexity_analysis.md](complexity_analysis.md) for asymptotic analysis*
