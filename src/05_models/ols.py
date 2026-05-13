# ============================================================
# PROYECTO FINAL: ANÁLISIS DE PRECIOS DE MEMORIAS RAM
# Regresión Lineal Múltiple — Enfoque Inferencial (OLS)
# Dataset: ram_market.db  (Newegg web scraping, mayo 2026)
# ============================================================
# Variables del dataset:
#   capacity_gb, speed_mhz, cas_latency, num_sticks,
#   has_rgb, brand_normalized, ddr_type, log_price, price_usd
# ============================================================

import sqlite3, warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats
from scipy.stats import shapiro, jarque_bera
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
warnings.filterwarnings("ignore")

OUT = "./"   # carpeta de salida para figuras
P   = ["#2C3E7A","#E74C3C","#27AE60","#F39C12","#8E44AD","#16A085","#D35400"]
plt.rcParams.update({
    "figure.facecolor":"#FAFAFA", "axes.facecolor":"#F5F5F5",
    "axes.edgecolor":"#CCCCCC",   "axes.grid":True,
    "grid.color":"#E0E0E0",       "grid.linewidth":0.6,
    "font.family":"DejaVu Sans",  "font.size":11,
    "axes.titlesize":13,          "axes.titleweight":"bold",
    "figure.dpi":150,
})

# ── 1. CARGA ──────────────────────────────────────────────────────────────────
conn = sqlite3.connect("ram_market.db")
df   = pd.read_sql("SELECT * FROM ram_products", conn)
conn.close()
print(f"[1] Dataset cargado: {df.shape}")

# Limpiar registros con speed_mhz=0 o cas_latency negativo (inválidos)
df = df[(df["speed_mhz"] > 0) & (df["cas_latency"] >= 0)].copy()
print(f"    Tras limpieza: {len(df)} filas")

# ── 2. PREPROCESAMIENTO ───────────────────────────────────────────────────────
# DDR3 tiene solo 2 obs → agrupa con DDR4 como "DDR_legacy"
df["ddr_group"] = df["ddr_type"].apply(lambda x: "DDR5" if x=="DDR5" else "DDR_legacy")
dummies = pd.get_dummies(df[["ddr_group","brand_normalized"]], drop_first=True, dtype=int)

num_vars = ["capacity_gb","speed_mhz","cas_latency","num_sticks","has_rgb","cas_was_imputed"]
X = pd.concat([df[num_vars].reset_index(drop=True), dummies.reset_index(drop=True)], axis=1)
y = df["log_price"].reset_index(drop=True)

# ── 3. VIF MANUAL ─────────────────────────────────────────────────────────────
def calc_vif(X_df):
    rows = []
    for col in X_df.columns:
        y_v = X_df[col].values
        X_v = X_df.drop(columns=[col]).values
        r2  = LinearRegression().fit(X_v, y_v).score(X_v, y_v)
        rows.append({"Feature": col, "VIF": round(1/(1-r2) if r2 < 1 else np.inf, 2)})
    return pd.DataFrame(rows).sort_values("VIF", ascending=False)

vif = calc_vif(X)
print("\n[3] VIF inicial:"); print(vif.to_string(index=False))
high_vif = vif[vif["VIF"] > 10]["Feature"].tolist()
if high_vif:
    print(f"    Eliminando VIF>10: {high_vif}")
    X = X.drop(columns=high_vif)

feature_names = list(X.columns)

# ── 4. SPLIT TRAIN / TEST (80/20) ────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"\n[4] Train: {len(X_train)}  Test: {len(X_test)}")

# ── 5. OLS MATRICIAL ─────────────────────────────────────────────────────────
Xm      = np.column_stack([np.ones(len(X_train)), X_train.values])
beta    = np.linalg.pinv(Xm.T @ Xm) @ Xm.T @ y_train.values
y_hat   = Xm @ beta
res     = y_train.values - y_hat
n, k    = Xm.shape
s2      = np.sum(res**2) / (n - k)
se      = np.sqrt(np.diag(s2 * np.linalg.pinv(Xm.T @ Xm)))
t_stats = beta / se
p_vals  = 2 * (1 - stats.t.cdf(np.abs(t_stats), df=n-k))
ci_lo   = beta - stats.t.ppf(0.975, df=n-k) * se
ci_hi   = beta + stats.t.ppf(0.975, df=n-k) * se
SST     = np.sum((y_train.values - y_train.mean())**2)
SSE     = np.sum(res**2)
R2      = 1 - SSE/SST
R2adj   = 1 - (1-R2)*(n-1)/(n-k-1)
F_stat  = ((SST-SSE)/(k-1)) / (SSE/(n-k))
F_pval  = 1 - stats.f.cdf(F_stat, k-1, n-k)
labs    = ["const"] + feature_names
sig     = lambda p: "***" if p<0.001 else "**" if p<0.01 else "*" if p<0.05 else "." if p<0.1 else ""

print("\n" + "="*72)
print("  RESULTADOS OLS — Variable dependiente: log(precio_usd)")
print("="*72)
res_df = pd.DataFrame({"Variable":labs,"β":beta.round(5),"SE":se.round(5),
                        "t":t_stats.round(4),"p-value":p_vals.round(5),
                        "IC 2.5%":ci_lo.round(5),"IC 97.5%":ci_hi.round(5),
                        "Sig":[sig(p) for p in p_vals]})
print(res_df.to_string(index=False))
print(f"\n  R²={R2:.4f}  R²adj={R2adj:.4f}  F={F_stat:.2f}  p(F)={F_pval:.2e}")

# ── 6. PREDICCIÓN TEST ────────────────────────────────────────────────────────
Xt     = np.column_stack([np.ones(len(X_test)), X_test.values])
y_pred = Xt @ beta
r2t    = r2_score(y_test, y_pred)
rmse_l = np.sqrt(mean_squared_error(y_test, y_pred))
mae_l  = mean_absolute_error(y_test, y_pred)
yu_r, yu_p = np.exp(y_test), np.exp(y_pred)
rmse_u = np.sqrt(mean_squared_error(yu_r, yu_p))
mae_u  = mean_absolute_error(yu_r, yu_p)
mape   = np.mean(np.abs((yu_r - yu_p)/yu_r))*100
print(f"\n  TEST → R²={r2t:.4f}  RMSE=${rmse_u:.0f}  MAE=${mae_u:.0f}  MAPE={mape:.1f}%")

cv = cross_val_score(LinearRegression(), X, y, cv=5, scoring="r2")
print(f"  CV-5   → R²={cv.mean():.4f} ± {cv.std():.4f}")

# ── 7. FIGURAS ────────────────────────────────────────────────────────────────
# (ver ram_regression_pipeline_full.py para todas las figuras)
print("\n[✓] Pipeline completado.")
