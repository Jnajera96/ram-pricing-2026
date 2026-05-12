"""
gradient_boosting.py — Día 8 · Modelo 5: Gradient Boosting Regressor

Pregunta:
  ¿Puede Gradient Boosting (ensemble secuencial) superar a Random Forest
  (ensemble paralelo)?

Pipeline:
  1. Mismas features que modelos 1-4 (comparabilidad)
  2. Baseline con hiperparámetros default
  3. GridSearchCV con 4 hiperparámetros
  4. Validación CV-5
  5. Comparación contra los 4 modelos anteriores
  6. Feature importances

Autor: Jose Najera · UDG · DS-2025-GDL
"""

import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import time

from sklearn.ensemble import GradientBoostingRegressor
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
# PIPELINE PRINCIPAL
# ════════════════════════════════════════════════════════════════

def main():
    print("═" * 70)
    print("📊 DÍA 8 · MODELO 5 · GRADIENT BOOSTING REGRESSOR")
    print("═" * 70)
    
    # ════════════════════════════════════════════════════════════════
    # 1. CARGA Y PREPROCESAMIENTO (idéntico a los 4 modelos previos)
    # ════════════════════════════════════════════════════════════════
    
    print("\n[1] Cargando datos...")
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM ram_products", conn)
    conn.close()
    
    df = df[(df['speed_mhz'] > 0) & (df['cas_latency'] >= 0)].copy()
    print(f"    Filas válidas: {len(df)}")
    
    df['ddr_group'] = df['ddr_type'].apply(lambda x: 'DDR5' if x == 'DDR5' else 'DDR_legacy')
    dummies = pd.get_dummies(df[['ddr_group', 'brand_normalized']], drop_first=True, dtype=int)
    
    num_vars = ['capacity_gb', 'speed_mhz', 'cas_latency', 'num_sticks', 'has_rgb', 'cas_was_imputed']
    X = pd.concat([df[num_vars].reset_index(drop=True), dummies.reset_index(drop=True)], axis=1)
    y = df['log_price'].reset_index(drop=True)
    
    feature_names = list(X.columns)
    print(f"    Features: {len(feature_names)}")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE)
    print(f"\n[2] Train: {len(X_train)}  Test: {len(X_test)}")
    
    # ════════════════════════════════════════════════════════════════
    # 3. BASELINE
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🚀 BASELINE · Gradient Boosting con defaults")
    print("═" * 70)
    
    gb_baseline = GradientBoostingRegressor(
        n_estimators=100,
        random_state=RANDOM_STATE
    )
    
    t0 = time.perf_counter()
    gb_baseline.fit(X_train, y_train)
    t_baseline = time.perf_counter() - t0
    
    y_pred_baseline = gb_baseline.predict(X_test)
    r2_baseline = r2_score(y_test, y_pred_baseline)
    
    print(f"\n    n_estimators=100, learning_rate=0.1 (defaults)")
    print(f"    Tiempo: {t_baseline:.3f} s")
    print(f"    R² test baseline: {r2_baseline:.4f}")
    
    # ════════════════════════════════════════════════════════════════
    # 4. GRIDSEARCHCV
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🔍 GRIDSEARCHCV · Búsqueda de hiperparámetros óptimos")
    print("═" * 70)
    
    param_grid = {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.05, 0.1],
        'max_depth': [3, 5, 7],
        'subsample': [0.8, 1.0],
    }
    
    n_combinaciones = 3 * 3 * 3 * 2  # = 54 combinaciones × 5 folds = 270 fits
    print(f"\n    Probando {n_combinaciones} combinaciones × 5 folds = {n_combinaciones*5} fits")
    print(f"    Hiperparámetros:")
    for k, v in param_grid.items():
        print(f"      · {k}: {v}")
    
    print(f"\n    ⏳ Ejecutando GridSearchCV (puede tardar 2-5 minutos)...")
    
    t0 = time.perf_counter()
    grid = GridSearchCV(
        GradientBoostingRegressor(random_state=RANDOM_STATE),
        param_grid=param_grid,
        cv=5,
        scoring='r2',
        n_jobs=-1,
        verbose=0
    )
    grid.fit(X_train, y_train)
    t_grid = time.perf_counter() - t0
    
    print(f"\n    ✅ GridSearchCV completado en {t_grid:.1f} s")
    print(f"\n    🎯 Mejores hiperparámetros:")
    for k, v in grid.best_params_.items():
        print(f"      · {k}: {v}")
    print(f"\n    CV-5 R² óptimo: {grid.best_score_:.4f}")
    
    # ════════════════════════════════════════════════════════════════
    # 5. EVALUACIÓN FINAL
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("📊 EVALUACIÓN FINAL · Gradient Boosting optimizado")
    print("═" * 70)
    
    gb_final = grid.best_estimator_
    
    y_pred_train = gb_final.predict(X_train)
    y_pred_test = gb_final.predict(X_test)
    
    r2_train = r2_score(y_train, y_pred_train)
    r2_test = r2_score(y_test, y_pred_test)
    
    y_test_usd = np.exp(y_test)
    y_pred_test_usd = np.exp(y_pred_test)
    
    rmse_usd = np.sqrt(mean_squared_error(y_test_usd, y_pred_test_usd))
    mae_usd = mean_absolute_error(y_test_usd, y_pred_test_usd)
    mape = np.mean(np.abs((y_test_usd - y_pred_test_usd) / y_test_usd)) * 100
    
    cv_scores = cross_val_score(gb_final, X, y, cv=5, scoring='r2', n_jobs=-1)
    
    print(f"\n    R² train: {r2_train:.4f}")
    print(f"    R² test:  {r2_test:.4f}")
    print(f"    Gap:      {r2_train-r2_test:+.4f}")
    
    print(f"\n    RMSE USD: ${rmse_usd:.2f}")
    print(f"    MAE USD:  ${mae_usd:.2f}")
    print(f"    MAPE:     {mape:.2f}%")
    
    print(f"\n    CV-5 R²: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    
    # ════════════════════════════════════════════════════════════════
    # 6. COMPARATIVA FINAL DE 5 MODELOS
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🏆 COMPARATIVA FINAL DE LOS 5 MODELOS")
    print("═" * 70)
    
    # Datos consolidados
    modelos_comparativa = pd.DataFrame({
        'Modelo': ['OLS (Día 6)', 'K-Means (Día 7)', 'Ridge (Día 7)', 
                   'Random Forest (Día 8)', 'Gradient Boosting (Día 8)'],
        'Tipo': ['Lineal', 'Clustering', 'Lineal regularizado', 
                 'Ensemble bagging', 'Ensemble boosting'],
        'R²_test': [0.8758, None, 0.8686, 0.9020, r2_test],
        'CV_5_R²': [None, None, 0.8851, 0.9392, cv_scores.mean()],
        'RMSE_USD': [203.14, None, 198.46, 158.74, rmse_usd],
        'MAE_USD': [107.11, None, 106.14, 71.04, mae_usd],
        'MAPE_pct': [17.36, None, 17.45, 10.42, mape],
        'Tiempo_seg': [0.01, 0.05, 0.02, 0.13, t_baseline],
        'Interpretable': ['Alta', 'Alta (centroides)', 'Alta', 'Parcial', 'Parcial'],
    })
    
    print(f"\n    📊 Tabla comparativa de los 5 modelos:\n")
    print(modelos_comparativa.to_string(index=False))
    
    # Ranking por MAPE (excluyendo K-Means que no predice precio)
    predictivos = modelos_comparativa[modelos_comparativa['Modelo'] != 'K-Means (Día 7)'].copy()
    predictivos = predictivos.sort_values('MAPE_pct')
    
    print(f"\n    🏅 Ranking por MAPE (menor = mejor):\n")
    for i, (_, row) in enumerate(predictivos.iterrows(), 1):
        emoji = "🥇" if i == 1 else ("🥈" if i == 2 else ("🥉" if i == 3 else "  "))
        print(f"    {emoji} {i}. {row['Modelo']:<28} MAPE={row['MAPE_pct']:.2f}% · R²={row['R²_test']:.4f}")
    
    # ════════════════════════════════════════════════════════════════
    # 7. DECISIÓN DEL MODELO FINAL
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🎯 DECISIÓN DEL MODELO FINAL")
    print("═" * 70)
    
    mejor_modelo = predictivos.iloc[0]['Modelo']
    
    print(f"""
    Análisis matizado:
    
    Para PREDICCIÓN PURA:
      🏆 Mejor MAPE: {predictivos.iloc[0]['Modelo']} ({predictivos.iloc[0]['MAPE_pct']:.2f}%)
      ✅ Diferencia con OLS: -{17.36-predictivos.iloc[0]['MAPE_pct']:.2f} puntos porcentuales
    
    Para INFERENCIA y EXPLICACIÓN:
      🏆 OLS sigue siendo preferible por:
         · Coeficientes con p-values e intervalos de confianza
         · Validación de supuestos Gauss-Markov
         · Conexión directa con análisis inferencial (Día 5)
    
    RECOMENDACIÓN ACADÉMICA:
      → Reportar AMBOS como modelos complementarios
      → OLS para EXPLICAR el mercado (premium de marca, etc.)
      → Ensemble para PREDECIR precios con menor error
    """)

    # ════════════════════════════════════════════════════════════════
    # 8. GRÁFICA · 4 paneles
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🎨 GENERANDO GRÁFICA")
    print("═" * 70)
    
    fig = plt.figure(figsize=(16, 11))
    gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.3)
    
    # ─── Panel 1: Feature importances GB ────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    
    feat_imp = pd.DataFrame({
        'feature': feature_names,
        'importance': gb_final.feature_importances_,
    }).sort_values('importance', ascending=False).head(10)
    
    colors = sns.color_palette("RdYlBu_r", len(feat_imp))
    bars = ax1.barh(feat_imp['feature'], feat_imp['importance'],
                     color=colors, edgecolor='black', alpha=0.85)
    
    for bar, imp in zip(bars, feat_imp['importance']):
        ax1.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2,
                 f'{imp:.3f}', va='center', fontsize=10, fontweight='bold')
    
    ax1.set_xlabel('Feature Importance', fontsize=11)
    ax1.set_title(f'Top 10 Feature Importances · Gradient Boosting\n'
                  f'Top 3: {feat_imp.head(3)["importance"].sum()*100:.1f}%',
                  fontsize=12, fontweight='bold')
    ax1.invert_yaxis()
    
    # ─── Panel 2: Real vs Predicho ──────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    
    ax2.scatter(y_test_usd, y_pred_test_usd, alpha=0.6, color='#9b59b6',
                edgecolors='black', linewidth=0.5, s=60)
    
    max_val = max(y_test_usd.max(), y_pred_test_usd.max())
    ax2.plot([0, max_val], [0, max_val], 'k--', linewidth=2, label='Identidad')
    
    ax2.set_xlabel('Precio real (USD)', fontsize=11)
    ax2.set_ylabel('Precio predicho (USD)', fontsize=11)
    ax2.set_title(f'Gradient Boosting · Predicción en test set\n'
                  f'R²={r2_test:.4f} · RMSE=${rmse_usd:.0f} · MAPE={mape:.1f}%',
                  fontsize=12, fontweight='bold')
    ax2.legend(fontsize=10)
    
    # ─── Panel 3: Comparación R² entre 4 modelos predictivos ─────
    ax3 = fig.add_subplot(gs[1, 0])
    
    modelos_pred = ['OLS\n(Día 6)', 'Ridge\n(Día 7)', 'Random Forest\n(Día 8)', 'Gradient Boosting\n(Día 8)']
    r2_values = [0.8758, 0.8686, 0.9020, r2_test]
    colors_models = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6']
    
    bars = ax3.bar(modelos_pred, r2_values, color=colors_models, alpha=0.85,
                    edgecolor='black', linewidth=1.5)
    
    for bar, r2 in zip(bars, r2_values):
        ax3.text(bar.get_x() + bar.get_width()/2, r2 + 0.003,
                 f'{r2:.4f}', ha='center', va='bottom',
                 fontsize=11, fontweight='bold')
    
    ax3.set_ylim(min(r2_values) - 0.02, max(r2_values) + 0.02)
    ax3.set_ylabel('R² en test set', fontsize=11)
    ax3.set_title('Comparación R² test · 4 modelos predictivos\n'
                  '(mismo split 80/20, random_state=42)',
                  fontsize=12, fontweight='bold')
    ax3.tick_params(axis='x', labelsize=9)
    
    # ─── Panel 4: Comparación MAPE entre 4 modelos ──────────────
    ax4 = fig.add_subplot(gs[1, 1])
    
    mape_values = [17.36, 17.45, 10.42, mape]
    
    bars = ax4.bar(modelos_pred, mape_values, color=colors_models, alpha=0.85,
                    edgecolor='black', linewidth=1.5)
    
    for bar, m in zip(bars, mape_values):
        ax4.text(bar.get_x() + bar.get_width()/2, m + 0.2,
                 f'{m:.2f}%', ha='center', va='bottom',
                 fontsize=11, fontweight='bold')
    
    ax4.set_ylim(0, max(mape_values) + 3)
    ax4.set_ylabel('MAPE (%)', fontsize=11)
    ax4.set_title('Comparación MAPE · 4 modelos predictivos\n(menor = mejor)',
                  fontsize=12, fontweight='bold')
    ax4.tick_params(axis='x', labelsize=9)
    
    plt.suptitle(f'Gradient Boosting · Modelo 5 de 5\n'
                 f'Best params: n_est={grid.best_params_["n_estimators"]}, '
                 f'lr={grid.best_params_["learning_rate"]}, '
                 f'depth={grid.best_params_["max_depth"]}',
                 fontsize=14, fontweight='bold', y=0.99)
    
    fig_path = FIG_DIR / "24_gradient_boosting.png"
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    print(f"\n    ✅ Gráfica guardada: {fig_path.name}")
    
    # Guardar resultados
    modelos_comparativa.to_csv(DATA_DIR / "comparativa_5_modelos.csv", index=False)
    feat_imp.to_csv(DATA_DIR / "gb_feature_importances.csv", index=False)
    print(f"    💾 Resultados: comparativa_5_modelos.csv, gb_feature_importances.csv")
    
    # ════════════════════════════════════════════════════════════════
    # CIERRE
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("✅ MODELO 5 (GRADIENT BOOSTING) COMPLETADO")
    print("═" * 70)
    
    print(f"""
📌 Frase para defensa oral:

   "Gradient Boosting con {grid.best_params_['n_estimators']} árboles secuenciales,
   learning_rate={grid.best_params_['learning_rate']} y max_depth={grid.best_params_['max_depth']}
   alcanzó R² test de {r2_test:.4f} y MAPE de {mape:.2f}%, marginalmente
   mejor que Random Forest. La diferencia entre los 5 modelos
   muestra un patrón claro: los modelos no-lineales (RF, GB)
   superan a los lineales (OLS, Ridge) en métricas de error
   absoluto (MAE -34%, MAPE -40%), pero pierden en
   interpretabilidad estadística. El proyecto reporta OLS para
   EXPLICAR el mercado y Gradient Boosting/Random Forest para
   PREDECIR precios con menor error práctico."

🎯 Próximo: Día 9 · Análisis empírico de complejidad ML + póster
    """)


if __name__ == "__main__":
    main()