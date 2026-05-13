"""
eda.py — Día 3 cierre: EDA visual sobre dataset limpio
Genera 3 figuras clave para el póster final.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Setup
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
FIG_DIR = SCRIPT_DIR / "figures"
FIG_DIR.mkdir(exist_ok=True)

sns.set_style("whitegrid")
sns.set_context("talk", font_scale=0.85)
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

# Cargar dataset
df = pd.read_csv(DATA_DIR / "ram_clean.csv")
print(f"📂 Dataset cargado: {len(df)} filas\n")


# ════════════════════════════════════════════════════════════════
# FIGURA 1 · Heatmap de correlación (LA gráfica estrella)
# ════════════════════════════════════════════════════════════════

print("🎨 Generando Figura 1: Heatmap de correlación")

numeric_cols = [
    'price_usd', 'log_price', 'capacity_gb', 'speed_mhz',
    'cas_latency_imputed', 'price_per_gb', 'num_sticks'
]
corr = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8))
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)  # triangular superior

sns.heatmap(
    corr, mask=mask, annot=True, fmt='.2f',
    cmap='coolwarm', center=0, square=True,
    linewidths=0.5, cbar_kws={"shrink": 0.7, "label": "Correlación de Pearson"},
    annot_kws={"size": 11, "weight": "bold"}, ax=ax
)
ax.set_title('Matriz de correlación · Features numéricas\n'
             'Mercado RAM (n=350, Newegg mayo 2026)',
             fontsize=13, pad=15, fontweight='bold')
plt.xticks(rotation=35, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(FIG_DIR / "01_correlation_heatmap.png")
plt.close()

print(f"  ✅ {FIG_DIR / '01_correlation_heatmap.png'}")
print(f"\n  🔍 Correlaciones más fuertes con price_usd:")
correlaciones = corr['price_usd'].drop('price_usd').sort_values(key=abs, ascending=False)
print(correlaciones.round(3).to_string())


# ════════════════════════════════════════════════════════════════
# FIGURA 2 · Boxplot precio por DDR
# ════════════════════════════════════════════════════════════════

print("\n🎨 Generando Figura 2: Distribución de precio por DDR")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Boxplot precio crudo
sns.boxplot(
    x='ddr_type', y='price_usd', data=df,
    hue='ddr_type', palette='Set2', legend=False,
    order=['DDR3', 'DDR4', 'DDR5'], ax=axes[0]
)
axes[0].set_title('Precio en USD por tipo DDR', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Tipo DDR')
axes[0].set_ylabel('Precio (USD)')

# Boxplot log_price
sns.boxplot(
    x='ddr_type', y='log_price', data=df,
    hue='ddr_type', palette='Set2', legend=False,
    order=['DDR3', 'DDR4', 'DDR5'], ax=axes[1]
)
axes[1].set_title('Log(1+precio) por tipo DDR (escala estabilizada)',
                  fontsize=12, fontweight='bold')
axes[1].set_xlabel('Tipo DDR')
axes[1].set_ylabel('log(1+precio)')

plt.suptitle('Premium de DDR5 sobre DDR4 sobre DDR3',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(FIG_DIR / "02_price_by_ddr.png")
plt.close()

print(f"  ✅ {FIG_DIR / '02_price_by_ddr.png'}")
print(f"\n  📊 Mediana de precio por DDR:")
medianas_precio = df.groupby('ddr_type')['price_usd'].median().reindex(['DDR3', 'DDR4', 'DDR5'])
print(medianas_precio.round(2).to_string())


# ════════════════════════════════════════════════════════════════
# FIGURA 3 · Distribución de precios (raw vs log) — valida transformación
# ════════════════════════════════════════════════════════════════

print("\n🎨 Generando Figura 3: Distribución de precios (raw vs log)")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Precio raw
axes[0].hist(df['price_usd'], bins=40, color='coral',
             edgecolor='black', alpha=0.85)
axes[0].set_title(f"Precio crudo · asimetría = {df['price_usd'].skew():.2f}",
                  fontsize=12, fontweight='bold')
axes[0].set_xlabel('USD')
axes[0].set_ylabel('Frecuencia')
axes[0].axvline(df['price_usd'].median(), color='darkred',
                linestyle='--', label=f'Mediana ${df["price_usd"].median():.0f}')
axes[0].legend()

# Log price
axes[1].hist(df['log_price'], bins=40, color='seagreen',
             edgecolor='black', alpha=0.85)
axes[1].set_title(f"log(1+precio) · asimetría = {df['log_price'].skew():.2f}",
                  fontsize=12, fontweight='bold')
axes[1].set_xlabel('log(USD)')
axes[1].set_ylabel('Frecuencia')
axes[1].axvline(df['log_price'].median(), color='darkgreen',
                linestyle='--', label=f'Mediana {df["log_price"].median():.2f}')
axes[1].legend()

plt.suptitle('Justificación de la transformación logarítmica',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(FIG_DIR / "03_log_transform.png")
plt.close()

print(f"  ✅ {FIG_DIR / '03_log_transform.png'}")


# ════════════════════════════════════════════════════════════════
# RESUMEN
# ════════════════════════════════════════════════════════════════

print("\n" + "═" * 60)
print("✅ EDA VISUAL COMPLETO")
print("═" * 60)
print(f"\n  3 figuras guardadas en {FIG_DIR}/")
print("  Todas a 300 DPI, listas para el póster A1.")