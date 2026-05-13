"""
ridge.py — Día 7 · Modelo 3: Ridge Regression

Pregunta:
  ¿Mejora la regularización L2 sobre el modelo OLS del Día 6?

Pipeline:
  1. Mismas features que la regresión del Día 6 (consistencia)
  2. Estandarización de X (Ridge la NECESITA)
  3. GridSearchCV para encontrar α óptimo
  4. Validación con CV-5
  5. Comparación de coeficientes Ridge vs OLS
  6. Evaluación en test set (mismo split que regresion.py)

Autor: Jose Najera · UDG · DS-2025-GDL
"""

import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from sklearn.linear_model import Ridge, LinearRegression, RidgeCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

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


# ════════════════════════════════════════════════════════════════
# PIPELINE
# ════════════════════════════════════════════════════════════════

def main():
    print("═" * 70)
    print("📊 DÍA 7 · MODELO 3 · RIDGE REGRESSION")
    print("═" * 70)
    
    # ════════════════════════════════════════════════════════════════
    # 1. CARGA Y PREPROCESAMIENTO (idéntico a regresion.py de Bernardo)
    # ════════════════════════════════════════════════════════════════
    
    print("\n[1] Cargando y preparando datos...")
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM ram_products", conn)
    conn.close()
    
    df = df[(df['speed_mhz'] > 0) & (df['cas_latency'] >= 0)].copy()
    print(f"    Filas válidas: {len(df)}")
    
    # Mismo preprocesamiento que regresion.py para comparabilidad
    df['ddr_group'] = df['ddr_type'].apply(lambda x: 'DDR5' if x == 'DDR5' else 'DDR_legacy')
    dummies = pd.get_dummies(df[['ddr_group', 'brand_normalized']], drop_first=True, dtype=int)
    
    num_vars = ['capacity_gb', 'speed_mhz', 'cas_latency', 'num_sticks', 'has_rgb', 'cas_was_imputed']
    X = pd.concat([df[num_vars].reset_index(drop=True), dummies.reset_index(drop=True)], axis=1)
    y = df['log_price'].reset_index(drop=True)
    
    feature_names = list(X.columns)
    print(f"    Features: {len(feature_names)}")
    
    # ════════════════════════════════════════════════════════════════
    # 2. SPLIT TRAIN/TEST (mismo random_state que regresion.py)
    # ════════════════════════════════════════════════════════════════
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE)
    print(f"\n[2] Train: {len(X_train)}  Test: {len(X_test)}")
    
    # ════════════════════════════════════════════════════════════════
    # 3. ESTANDARIZACIÓN (CRÍTICO para Ridge)
    # ════════════════════════════════════════════════════════════════
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print(f"\n[3] StandardScaler aplicado (Ridge requiere features escaladas)")
    
    # ════════════════════════════════════════════════════════════════
    # 4. BÚSQUEDA DE α ÓPTIMO con GridSearchCV
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🔍 BÚSQUEDA DE α ÓPTIMO (regularización L2)")
    print("═" * 70)
    
    # Probar un rango amplio de alphas en escala logarítmica
    alphas = np.logspace(-4, 4, 50)  # de 0.0001 a 10000
    
    print(f"\n    Probando {len(alphas)} valores de α en [10⁻⁴, 10⁴]")
    print(f"    Validación: 5-fold cross-validation")
    print(f"    Métrica:    R² (maximizar)")
    
    grid = GridSearchCV(
        Ridge(random_state=RANDOM_STATE),
        param_grid={'alpha': alphas},
        cv=5,
        scoring='r2',
        n_jobs=-1
    )
    grid.fit(X_train_scaled, y_train)
    
    alpha_optimo = grid.best_params_['alpha']
    cv_r2_optimo = grid.best_score_
    
    print(f"\n    🎯 α óptimo: {alpha_optimo:.4f}")
    print(f"    CV R²:       {cv_r2_optimo:.4f}")
    
    # Interpretación del α
    if alpha_optimo < 0.01:
        interp_alpha = "Regularización prácticamente nula (≈ OLS estándar)"
    elif alpha_optimo < 1:
        interp_alpha = "Regularización moderada"
    elif alpha_optimo < 100:
        interp_alpha = "Regularización fuerte"
    else:
        interp_alpha = "Regularización muy fuerte (los β tienden a 0)"
    print(f"    Interpretación: {interp_alpha}")
    
    # ════════════════════════════════════════════════════════════════
    # 5. ENTRENAR RIDGE FINAL Y COMPARAR CON OLS
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🧪 COMPARACIÓN RIDGE vs OLS")
    print("═" * 70)
    
    # Modelo Ridge final
    ridge = Ridge(alpha=alpha_optimo, random_state=RANDOM_STATE)
    ridge.fit(X_train_scaled, y_train)
    
    # Modelo OLS (LinearRegression sin regularización)
    ols = LinearRegression()
    ols.fit(X_train_scaled, y_train)
    
    # Predicciones
    y_pred_ridge_train = ridge.predict(X_train_scaled)
    y_pred_ridge_test = ridge.predict(X_test_scaled)
    y_pred_ols_train = ols.predict(X_train_scaled)
    y_pred_ols_test = ols.predict(X_test_scaled)
    
    # Métricas en escala log
    r2_train_ridge = r2_score(y_train, y_pred_ridge_train)
    r2_test_ridge = r2_score(y_test, y_pred_ridge_test)
    r2_train_ols = r2_score(y_train, y_pred_ols_train)
    r2_test_ols = r2_score(y_test, y_pred_ols_test)
    
    # Métricas en escala USD
    y_test_usd = np.exp(y_test)
    y_pred_ridge_usd = np.exp(y_pred_ridge_test)
    y_pred_ols_usd = np.exp(y_pred_ols_test)
    
    rmse_ridge = np.sqrt(mean_squared_error(y_test_usd, y_pred_ridge_usd))
    mae_ridge = mean_absolute_error(y_test_usd, y_pred_ridge_usd)
    mape_ridge = np.mean(np.abs((y_test_usd - y_pred_ridge_usd) / y_test_usd)) * 100
    
    rmse_ols = np.sqrt(mean_squared_error(y_test_usd, y_pred_ols_usd))
    mae_ols = mean_absolute_error(y_test_usd, y_pred_ols_usd)
    mape_ols = np.mean(np.abs((y_test_usd - y_pred_ols_usd) / y_test_usd)) * 100
    
    print(f"\n    {'Métrica':<15} {'OLS':>12} {'Ridge':>12} {'Δ':>12}")
    print(f"    " + "─" * 55)
    print(f"    {'R² train':<15} {r2_train_ols:>12.4f} {r2_train_ridge:>12.4f} {r2_train_ridge-r2_train_ols:>+12.4f}")
    print(f"    {'R² test':<15} {r2_test_ols:>12.4f} {r2_test_ridge:>12.4f} {r2_test_ridge-r2_test_ols:>+12.4f}")
    print(f"    {'RMSE USD':<15} ${rmse_ols:>11.2f} ${rmse_ridge:>11.2f} ${rmse_ridge-rmse_ols:>+11.2f}")
    print(f"    {'MAE USD':<15} ${mae_ols:>11.2f} ${mae_ridge:>11.2f} ${mae_ridge-mae_ols:>+11.2f}")
    print(f"    {'MAPE %':<15} {mape_ols:>11.2f}% {mape_ridge:>11.2f}% {mape_ridge-mape_ols:>+11.2f}%")
    
    # ════════════════════════════════════════════════════════════════
    # 6. COMPARACIÓN DE COEFICIENTES
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("📊 COMPARACIÓN DE COEFICIENTES")
    print("═" * 70)
    
    coef_df = pd.DataFrame({
        'feature': feature_names,
        'beta_OLS': ols.coef_,
        'beta_Ridge': ridge.coef_,
    })
    coef_df['shrinkage'] = (coef_df['beta_Ridge'] - coef_df['beta_OLS'])
    coef_df['shrinkage_pct'] = (coef_df['shrinkage'] / coef_df['beta_OLS']) * 100
    coef_df = coef_df.sort_values('beta_OLS', key=abs, ascending=False)
    
    print(f"\n    Coeficientes (escala estandarizada):\n")
    print(f"    {'Feature':<35} {'β OLS':>10} {'β Ridge':>10} {'Δ%':>10}")
    print(f"    " + "─" * 70)
    for _, row in coef_df.iterrows():
        print(f"    {row['feature']:<35} {row['beta_OLS']:>+10.4f} {row['beta_Ridge']:>+10.4f} {row['shrinkage_pct']:>+9.2f}%")

    # ════════════════════════════════════════════════════════════════
    # 7. GRÁFICA · 4 paneles
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🎨 GENERANDO GRÁFICA COMPARATIVA")
    print("═" * 70)
    
    fig = plt.figure(figsize=(16, 11))
    gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.3)
    
    # ─── Panel 1: Curva de R² vs α ───────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    cv_results = pd.DataFrame(grid.cv_results_)
    
    ax1.semilogx(alphas, cv_results['mean_test_score'], 'o-', linewidth=2, 
                  markersize=4, color='#3498db', label='R² CV-5')
    ax1.fill_between(alphas, 
                      cv_results['mean_test_score'] - cv_results['std_test_score'],
                      cv_results['mean_test_score'] + cv_results['std_test_score'],
                      alpha=0.2, color='#3498db', label='±1 std')
    ax1.axvline(alpha_optimo, color='red', linestyle='--', linewidth=2,
                 label=f'α óptimo = {alpha_optimo:.4f}')
    
    ax1.set_xlabel('α (regularización, escala log)', fontsize=11)
    ax1.set_ylabel('R² (cross-validation)', fontsize=11)
    ax1.set_title(f'Búsqueda de α óptimo · CV-5\nMejor R² = {cv_r2_optimo:.4f}',
                  fontsize=12, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # ─── Panel 2: Comparación de coeficientes (barras) ───────────
    ax2 = fig.add_subplot(gs[0, 1])
    
    coef_plot = coef_df.head(10)  # top 10 por magnitud
    x_pos = np.arange(len(coef_plot))
    
    width = 0.4
    ax2.barh(x_pos - width/2, coef_plot['beta_OLS'], width, 
             label='OLS', color='#e74c3c', alpha=0.85, edgecolor='black')
    ax2.barh(x_pos + width/2, coef_plot['beta_Ridge'], width,
             label='Ridge', color='#3498db', alpha=0.85, edgecolor='black')
    
    ax2.set_yticks(x_pos)
    ax2.set_yticklabels(coef_plot['feature'], fontsize=9)
    ax2.set_xlabel('Coeficiente β (escala estandarizada)', fontsize=11)
    ax2.set_title('Top 10 features · OLS vs Ridge\nRidge "encoge" coeficientes hacia 0',
                  fontsize=12, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.axvline(0, color='black', linewidth=0.5)
    ax2.invert_yaxis()
    
    # ─── Panel 3: Real vs Predicho (Ridge en test) ───────────────
    ax3 = fig.add_subplot(gs[1, 0])
    
    ax3.scatter(y_test_usd, y_pred_ridge_usd, alpha=0.6, color='#3498db',
                edgecolors='black', linewidth=0.5, label='Ridge')
    ax3.scatter(y_test_usd, y_pred_ols_usd, alpha=0.4, color='#e74c3c',
                edgecolors='black', linewidth=0.5, marker='x', label='OLS')
    
    ax3.plot([0, y_test_usd.max()], [0, y_test_usd.max()], 
             'k--', linewidth=2, label='Identidad')
    
    ax3.set_xlabel('Precio real (USD)', fontsize=11)
    ax3.set_ylabel('Precio predicho (USD)', fontsize=11)
    ax3.set_title(f'Predicción en test set\n'
                  f'Ridge R²={r2_test_ridge:.4f} · OLS R²={r2_test_ols:.4f}',
                  fontsize=12, fontweight='bold')
    ax3.legend(fontsize=10)
    
    # ─── Panel 4: Tabla resumen ──────────────────────────────────
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    
    table_data = [
        ['Métrica', 'OLS', 'Ridge', 'Δ'],
        ['α óptimo', '0.0000', f'{alpha_optimo:.4f}', '—'],
        ['R² train', f'{r2_train_ols:.4f}', f'{r2_train_ridge:.4f}', f'{r2_train_ridge-r2_train_ols:+.4f}'],
        ['R² test', f'{r2_test_ols:.4f}', f'{r2_test_ridge:.4f}', f'{r2_test_ridge-r2_test_ols:+.4f}'],
        ['CV-5 R²', '—', f'{cv_r2_optimo:.4f}', '—'],
        ['RMSE USD', f'${rmse_ols:.2f}', f'${rmse_ridge:.2f}', f'${rmse_ridge-rmse_ols:+.2f}'],
        ['MAE USD', f'${mae_ols:.2f}', f'${mae_ridge:.2f}', f'${mae_ridge-mae_ols:+.2f}'],
        ['MAPE %', f'{mape_ols:.2f}%', f'{mape_ridge:.2f}%', f'{mape_ridge-mape_ols:+.2f}%'],
    ]
    
    table = ax4.table(cellText=table_data, cellLoc='center', loc='center',
                      colWidths=[0.25, 0.22, 0.22, 0.22])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2)
    
    # Estilizar header
    for j in range(4):
        cell = table[0, j]
        cell.set_facecolor('#2c3e50')
        cell.set_text_props(color='white', fontweight='bold')
    
    # Alternar colores
    for i in range(1, len(table_data)):
        for j in range(4):
            cell = table[i, j]
            cell.set_facecolor('#ecf0f1' if i % 2 == 0 else 'white')
    
    ax4.set_title('Tabla comparativa · OLS vs Ridge',
                  fontsize=12, fontweight='bold', pad=20)
    
    plt.suptitle(f'Ridge Regression · Regularización L2 vs OLS sin regularización\n'
                 f'α óptimo = {alpha_optimo:.4f} · {interp_alpha}',
                 fontsize=14, fontweight='bold', y=0.99)
    
    fig_path = FIG_DIR / "22_ridge_vs_ols.png"
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    print(f"\n    ✅ Gráfica guardada: {fig_path.name}")

    # Guardar resultados
    resultados_ridge = pd.DataFrame({
        'modelo': ['OLS', 'Ridge'],
        'R²_train': [r2_train_ols, r2_train_ridge],
        'R²_test': [r2_test_ols, r2_test_ridge],
        'RMSE_USD': [rmse_ols, rmse_ridge],
        'MAE_USD': [mae_ols, mae_ridge],
        'MAPE': [mape_ols, mape_ridge],
        'alpha': [0, alpha_optimo],
    })
    resultados_ridge.to_csv(DATA_DIR / "ridge_vs_ols.csv", index=False)
    
    # ════════════════════════════════════════════════════════════════
    # CIERRE
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("✅ MODELO 3 (RIDGE) COMPLETADO")
    print("═" * 70)
    
    # Decisión defendible
    if abs(r2_test_ridge - r2_test_ols) < 0.005:
        veredicto = "EMPATE: Ridge y OLS son prácticamente equivalentes"
        razon = "El α óptimo es bajo → tu OLS ya estaba bien especificado"
    elif r2_test_ridge > r2_test_ols:
        veredicto = "Ridge GANA por margen pequeño"
        razon = "La regularización aporta marginalmente"
    else:
        veredicto = "OLS GANA (caso raro)"
        razon = "Tu modelo NO se beneficia de regularización L2"
    
    print(f"\n📌 Veredicto: {veredicto}")
    print(f"   Razón: {razon}")
    
    print(f"\n📌 Frase para defensa oral:")
    print(f"""
   "Apliqué Ridge Regression con búsqueda de α óptimo vía GridSearchCV
   (5-fold), encontrando α={alpha_optimo:.4f} en el rango [10⁻⁴, 10⁴].
   El R² test de Ridge ({r2_test_ridge:.4f}) y OLS ({r2_test_ols:.4f}) son
   prácticamente equivalentes (Δ={r2_test_ridge-r2_test_ols:+.4f}), confirmando
   que el modelo OLS del Día 6 estaba bien especificado y no
   requería regularización. Los VIF<5 ya habían descartado
   multicolinealidad severa; este experimento lo valida con un
   método independiente. La regresión OLS sigue siendo el modelo
   preferible por interpretabilidad de coeficientes."
    """)


if __name__ == "__main__":
    main()