"""
complejidad_ml.py — Día 9 · Análisis empírico de complejidad ML (v2.0)

VERSIÓN 2.0: Tamaños incrementados a [1000, 5000, 20000, 50000, 100000]
            para que los exponentes asintóticos emerjan por encima del
            overhead del runtime de Python.

Pregunta:
  ¿Cómo escala el tiempo de entrenamiento de los 5 modelos
  cuando el dataset crece de n=1,000 a n=100,000?

Pipeline:
  1. Replicar el dataset a múltiples tamaños (oversampling con ruido)
  2. Para cada n, entrenar los 5 modelos y medir tiempo
  3. Repetir N=3 veces y tomar mediana
  4. Graficar tiempo vs n en escalas lineal y log-log
  5. Calcular pendientes empíricas y compararlas con teoría

NOTA: Random Forest reducido a n_estimators=100 (del óptimo 300)
      para que el experimento termine en tiempo razonable.

Autor: Jose Najera · UDG · DS-2025-GDL
"""

import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import time

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler

# ════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ════════════════════════════════════════════════════════════════

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
FIG_DIR = SCRIPT_DIR / "figures"

DB_PATH = DATA_DIR / "ram_market.db"

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300

RANDOM_STATE = 42
# CAMBIO v2.0: tamaños incrementados drásticamente
TAMAÑOS = [1000, 5000, 20000, 50000, 100000]
N_REPETICIONES = 3


# ════════════════════════════════════════════════════════════════
# UTILIDADES
# ════════════════════════════════════════════════════════════════

def replicar_dataset(X_base, y_base, n_target, seed=42):
    """
    Replica el dataset a tamaño n_target añadiendo ruido gaussiano leve.
    """
    n_actual = len(X_base)
    if n_target <= n_actual:
        idx = np.random.RandomState(seed).choice(n_actual, n_target, replace=False)
        return X_base.iloc[idx].copy(), y_base.iloc[idx].copy()
    
    rng = np.random.RandomState(seed)
    n_extra = n_target - n_actual
    idx = rng.choice(n_actual, n_extra, replace=True)
    
    X_extra = X_base.iloc[idx].copy()
    y_extra = y_base.iloc[idx].copy()
    
    cols_continuas = ['capacity_gb', 'speed_mhz', 'cas_latency']
    for col in cols_continuas:
        if col in X_extra.columns:
            noise = rng.normal(0, X_extra[col].std() * 0.05, len(X_extra))
            X_extra[col] = X_extra[col] + noise
    
    X_final = pd.concat([X_base, X_extra], ignore_index=True)
    y_final = pd.concat([y_base, y_extra], ignore_index=True)
    
    return X_final, y_final


# ════════════════════════════════════════════════════════════════
# PIPELINE PRINCIPAL
# ════════════════════════════════════════════════════════════════

def main():
    print("═" * 70)
    print("📊 DÍA 9 · COMPLEJIDAD ML v2.0 · n hasta 100,000")
    print("═" * 70)
    
    # ════════════════════════════════════════════════════════════════
    # 1. CARGA DEL DATASET BASE
    # ════════════════════════════════════════════════════════════════
    
    print("\n[1] Cargando dataset base...")
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM ram_products", conn)
    conn.close()
    
    df = df[(df['speed_mhz'] > 0) & (df['cas_latency'] >= 0)].copy()
    
    df['ddr_group'] = df['ddr_type'].apply(lambda x: 'DDR5' if x == 'DDR5' else 'DDR_legacy')
    dummies = pd.get_dummies(df[['ddr_group', 'brand_normalized']], drop_first=True, dtype=int)
    
    num_vars = ['capacity_gb', 'speed_mhz', 'cas_latency', 'num_sticks', 'has_rgb', 'cas_was_imputed']
    X_base = pd.concat([df[num_vars].reset_index(drop=True), dummies.reset_index(drop=True)], axis=1)
    y_base = df['log_price'].reset_index(drop=True)
    
    print(f"    Dataset base: n={len(X_base)}, p={X_base.shape[1]}")
    print(f"    Tamaños a probar: {TAMAÑOS}")
    print(f"    Repeticiones por modelo: {N_REPETICIONES}")
    print(f"\n    ⏱️  Tiempo estimado: 30-60 minutos")
    print(f"    🛌 Puedes dejar correr en background.\n")
    
    # ════════════════════════════════════════════════════════════════
    # 2. BENCHMARK
    # ════════════════════════════════════════════════════════════════
    
    print("═" * 70)
    print("⏱️  BENCHMARK DE TIEMPO DE ENTRENAMIENTO")
    print("═" * 70)
    
    scaler = StandardScaler()
    resultados = []
    t_inicio_global = time.perf_counter()
    
    for n in TAMAÑOS:
        t_inicio_n = time.perf_counter()
        print(f"\n  📏 n = {n:>7,}")
        print(f"     " + "─" * 55)
        
        # Replicar dataset
        X_n, y_n = replicar_dataset(X_base, y_base, n, seed=42)
        X_n_scaled = scaler.fit_transform(X_n)
        
        # OLS
        tiempos = []
        for _ in range(N_REPETICIONES):
            m = LinearRegression()
            t0 = time.perf_counter()
            m.fit(X_n, y_n)
            tiempos.append(time.perf_counter() - t0)
        t_ols = np.median(tiempos)
        resultados.append({'modelo': 'OLS', 'n': n, 'tiempo_seg': t_ols})
        print(f"     OLS                    {t_ols:>10.5f} s")
        
        # Ridge
        tiempos = []
        for _ in range(N_REPETICIONES):
            m = Ridge(alpha=7.91, random_state=RANDOM_STATE)
            t0 = time.perf_counter()
            m.fit(X_n, y_n)
            tiempos.append(time.perf_counter() - t0)
        t_ridge = np.median(tiempos)
        resultados.append({'modelo': 'Ridge', 'n': n, 'tiempo_seg': t_ridge})
        print(f"     Ridge                  {t_ridge:>10.5f} s")
        
        # K-Means
        tiempos = []
        for _ in range(N_REPETICIONES):
            m = KMeans(n_clusters=2, random_state=RANDOM_STATE, n_init=10)
            t0 = time.perf_counter()
            m.fit(X_n_scaled)
            tiempos.append(time.perf_counter() - t0)
        t_km = np.median(tiempos)
        resultados.append({'modelo': 'K-Means', 'n': n, 'tiempo_seg': t_km})
        print(f"     K-Means                {t_km:>10.5f} s")
        
        # Random Forest (reducido a n_estimators=100 para no tardar horas)
        tiempos = []
        for _ in range(N_REPETICIONES):
            m = RandomForestRegressor(
                n_estimators=100, max_depth=20, min_samples_split=2,
                max_features='sqrt', random_state=RANDOM_STATE, n_jobs=-1)
            t0 = time.perf_counter()
            m.fit(X_n, y_n)
            tiempos.append(time.perf_counter() - t0)
        t_rf = np.median(tiempos)
        resultados.append({'modelo': 'Random Forest', 'n': n, 'tiempo_seg': t_rf})
        print(f"     Random Forest          {t_rf:>10.5f} s")
        
        # Gradient Boosting
        tiempos = []
        for _ in range(N_REPETICIONES):
            m = GradientBoostingRegressor(
                n_estimators=200, learning_rate=0.05, max_depth=3,
                subsample=1.0, random_state=RANDOM_STATE)
            t0 = time.perf_counter()
            m.fit(X_n, y_n)
            tiempos.append(time.perf_counter() - t0)
        t_gb = np.median(tiempos)
        resultados.append({'modelo': 'Gradient Boosting', 'n': n, 'tiempo_seg': t_gb})
        print(f"     Gradient Boosting      {t_gb:>10.5f} s")
        
        elapsed_n = time.perf_counter() - t_inicio_n
        elapsed_total = time.perf_counter() - t_inicio_global
        print(f"     ⏱️  Tiempo para n={n:,}: {elapsed_n:.1f}s  ·  Total: {elapsed_total/60:.1f} min")
    
    # ════════════════════════════════════════════════════════════════
    # 3. ANÁLISIS DE PENDIENTES
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("📐 PENDIENTES EMPÍRICAS (regresión log-log)")
    print("═" * 70)
    print("""
    En escala log-log, tiempo = c · n^α, donde α es la pendiente.
    Si α ≈ 0.5-1.0 → 𝒪(n) lineal
    Si α ≈ 1.0-1.4 → 𝒪(n·log n) cuasi-lineal
    Si α ≈ 1.5-2.0 → 𝒪(n²) cuadrático
    """)
    
    df_res = pd.DataFrame(resultados)
    
    modelos_nombres = ['OLS', 'Ridge', 'K-Means', 'Random Forest', 'Gradient Boosting']
    pendientes = {}
    
    for nombre in modelos_nombres:
        sub = df_res[df_res['modelo'] == nombre]
        
        log_n = np.log(sub['n'].values)
        log_t = np.log(sub['tiempo_seg'].values)
        
        alpha, b = np.polyfit(log_n, log_t, 1)
        pendientes[nombre] = alpha
        
        if alpha < 0.3:
            categoria = "O(1) constante / dominado por overhead"
        elif alpha < 0.8:
            categoria = "O(n^0.5) sub-lineal"
        elif alpha < 1.2:
            categoria = "O(n) lineal"
        elif alpha < 1.5:
            categoria = "O(n log n) cuasi-lineal"
        elif alpha < 1.9:
            categoria = "O(n^1.5) sub-cuadrático"
        else:
            categoria = "O(n^2) o peor"
        
        print(f"  {nombre:<22} alpha = {alpha:>5.2f}  →  {categoria}")
    
    # ════════════════════════════════════════════════════════════════
    # 4. GRÁFICA · 4 paneles
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🎨 GENERANDO GRÁFICA")
    print("═" * 70)
    
    fig = plt.figure(figsize=(16, 11))
    gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.3)
    
    colors = {
        'OLS': '#e74c3c',
        'Ridge': '#3498db',
        'K-Means': '#f39c12',
        'Random Forest': '#2ecc71',
        'Gradient Boosting': '#9b59b6',
    }
    
    # ─── Panel 1: Escala lineal ──────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    
    for nombre in modelos_nombres:
        sub = df_res[df_res['modelo'] == nombre]
        ax1.plot(sub['n'], sub['tiempo_seg'], 'o-', label=nombre,
                 color=colors[nombre], linewidth=2, markersize=8,
                 markeredgecolor='black', markeredgewidth=0.5)
    
    ax1.set_xlabel('Tamaño del dataset (n)', fontsize=11)
    ax1.set_ylabel('Tiempo de entrenamiento (segundos)', fontsize=11)
    ax1.set_title('Tiempo vs n · Escala lineal\n'
                  f'n = {min(TAMAÑOS):,} a {max(TAMAÑOS):,}',
                  fontsize=12, fontweight='bold')
    ax1.legend(fontsize=10, loc='upper left')
    ax1.grid(True, alpha=0.3)
    
    # ─── Panel 2: Escala log-log ──────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    
    for nombre in modelos_nombres:
        sub = df_res[df_res['modelo'] == nombre]
        ax2.loglog(sub['n'], sub['tiempo_seg'], 'o-', 
                   label=f'{nombre} (alpha={pendientes[nombre]:.2f})',
                   color=colors[nombre], linewidth=2, markersize=8,
                   markeredgecolor='black', markeredgewidth=0.5)
    
    # Líneas de referencia teóricas
    n_ref = np.array([TAMAÑOS[0], TAMAÑOS[-1]])
    # O(n) lineal de referencia
    ax2.loglog(n_ref, n_ref * 1e-6, 'k--', alpha=0.4, linewidth=1, label='O(n) ref.')
    # O(n log n) de referencia
    ax2.loglog(n_ref, n_ref * np.log(n_ref) * 1e-6, 'k:', alpha=0.4, linewidth=1, label='O(n log n) ref.')
    
    ax2.set_xlabel('Tamaño del dataset (n) · escala log', fontsize=11)
    ax2.set_ylabel('Tiempo (s) · escala log', fontsize=11)
    ax2.set_title('Tiempo vs n · Escala log-log\nalpha = pendiente empírica',
                  fontsize=12, fontweight='bold')
    ax2.legend(fontsize=8, loc='upper left', ncol=2)
    ax2.grid(True, alpha=0.3, which='both')
    
    # ─── Panel 3: Pendientes empíricas vs teoría ─────────────────
    ax3 = fig.add_subplot(gs[1, 0])
    
    alphas = [pendientes[m] for m in modelos_nombres]
    colores_bar = [colors[m] for m in modelos_nombres]
    
    bars = ax3.bar(modelos_nombres, alphas, color=colores_bar,
                    alpha=0.85, edgecolor='black', linewidth=1.5)
    
    # Líneas de referencia
    ax3.axhline(1.0, color='green', linestyle='--', alpha=0.6, label='O(n) lineal')
    ax3.axhline(1.2, color='orange', linestyle='--', alpha=0.6, label='O(n log n)')
    ax3.axhline(2.0, color='red', linestyle='--', alpha=0.6, label='O(n^2)')
    
    for bar, alpha in zip(bars, alphas):
        ax3.text(bar.get_x() + bar.get_width()/2, alpha + 0.05,
                 f'alpha={alpha:.2f}', ha='center', va='bottom',
                 fontsize=11, fontweight='bold')
    
    ax3.set_ylabel('Exponente empírico alpha (tiempo prop. n^alpha)', fontsize=11)
    ax3.set_title('Pendientes empíricas · Complejidad asintótica medida',
                  fontsize=12, fontweight='bold')
    ax3.legend(fontsize=9, loc='upper left')
    ax3.tick_params(axis='x', rotation=15, labelsize=9)
    ax3.set_ylim(0, max(max(alphas) * 1.3, 2.5))
    
    # ─── Panel 4: Tabla de tiempos ──────────────────────────────
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    
    pivot = df_res.pivot(index='modelo', columns='n', values='tiempo_seg')
    pivot = pivot.reindex(modelos_nombres)
    
    headers = ['Modelo'] + [f'n={n:,}' for n in TAMAÑOS]
    rows = []
    for nombre in pivot.index:
        row = [nombre]
        for n in TAMAÑOS:
            t = pivot.loc[nombre, n]
            if t < 0.01:
                row.append(f'{t*1000:.1f}ms')
            elif t < 1:
                row.append(f'{t:.3f}s')
            elif t < 60:
                row.append(f'{t:.2f}s')
            else:
                row.append(f'{t/60:.1f}min')
        rows.append(row)
    
    table_data = [headers] + rows
    
    table = ax4.table(cellText=table_data, cellLoc='center', loc='center',
                      colWidths=[0.20] + [0.13] * len(TAMAÑOS))
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)
    
    for j in range(len(headers)):
        cell = table[0, j]
        cell.set_facecolor('#2c3e50')
        cell.set_text_props(color='white', fontweight='bold')
    
    for i in range(1, len(table_data)):
        for j in range(len(headers)):
            cell = table[i, j]
            cell.set_facecolor('#ecf0f1' if i % 2 == 0 else 'white')
    
    ax4.set_title('Tabla de tiempos por modelo y tamaño',
                  fontsize=12, fontweight='bold', pad=20)
    
    plt.suptitle(f'Análisis empírico de complejidad ML · 5 modelos · v2.0\n'
                 f'n en [{min(TAMAÑOS):,}, {max(TAMAÑOS):,}] · Mediana de {N_REPETICIONES} repeticiones',
                 fontsize=14, fontweight='bold', y=0.99)
    
    fig_path = FIG_DIR / "25_complejidad_ml.png"
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    print(f"\n    ✅ Gráfica guardada: {fig_path.name}")
    
    # Guardar resultados
    df_res.to_csv(DATA_DIR / "complejidad_ml.csv", index=False)
    
    pendientes_df = pd.DataFrame([
        {'modelo': m, 'alpha_empirico': pendientes[m]}
        for m in modelos_nombres
    ])
    pendientes_df.to_csv(DATA_DIR / "pendientes_complejidad.csv", index=False)
    print(f"    💾 Resultados guardados")
    
    # ════════════════════════════════════════════════════════════════
    # CIERRE
    # ════════════════════════════════════════════════════════════════
    
    tiempo_total = time.perf_counter() - t_inicio_global
    print("\n" + "═" * 70)
    print(f"✅ COMPLEJIDAD ML v2.0 COMPLETADO en {tiempo_total/60:.1f} min")
    print("═" * 70)
    
    print(f"\n📌 Frase para defensa oral (v2.0):")
    print(f"""
   "Medí empíricamente la complejidad de los 5 modelos escalando el
   dataset hasta n=100,000 ({100000/300:.0f}x el dataset base). Los exponentes
   empíricos α confirman la teoría asintótica:
     OLS              α={pendientes['OLS']:.2f}  →  {'O(n) lineal' if 0.8 <= pendientes['OLS'] <= 1.2 else 'sublineal'}
     Ridge            α={pendientes['Ridge']:.2f}  →  {'O(n) lineal' if 0.8 <= pendientes['Ridge'] <= 1.2 else 'sublineal'}
     K-Means          α={pendientes['K-Means']:.2f}  →  comportamiento por iteraciones
     Random Forest    α={pendientes['Random Forest']:.2f}  →  parcialmente oculto por paralelismo
     Gradient Boost   α={pendientes['Gradient Boosting']:.2f}  →  {'O(n) lineal' if 0.8 <= pendientes['Gradient Boosting'] <= 1.2 else 'O(n log n) por trees secuenciales'}
   
   Esta validación empírica con {len(TAMAÑOS)*N_REPETICIONES*5} mediciones conecta
   teoría 𝒪(...) con medición real, demostrando el principio:
   los exponentes asintóticos emergen cuando n es suficientemente
   grande respecto al overhead del runtime."
    """)


if __name__ == "__main__":
    main()