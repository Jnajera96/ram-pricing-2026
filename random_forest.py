"""
random_forest.py — Día 8 · Modelo 4: Random Forest Regressor

Pregunta:
  ¿Mejora un modelo no-lineal (bagging de árboles) sobre OLS?

Pipeline:
  1. Mismas features que OLS/Ridge (consistencia comparativa)
  2. Baseline con hiperparámetros default
  3. GridSearchCV con 4 hiperparámetros clave
  4. Validación con CV-5
  5. Feature importances + comparación con coeficientes OLS
  6. Evaluación en test set (mismo split=42)

Autor: Jose Najera · UDG · DS-2025-GDL
"""

import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import time

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
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
    print("📊 DÍA 8 · MODELO 4 · RANDOM FOREST REGRESSOR")
    print("═" * 70)
    
    # ════════════════════════════════════════════════════════════════
    # 1. CARGA Y PREPROCESAMIENTO (idéntico a regresion.py y ridge.py)
    # ════════════════════════════════════════════════════════════════
    
    print("\n[1] Cargando datos desde ram_market.db...")
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM ram_products", conn)
    conn.close()
    
    df = df[(df['speed_mhz'] > 0) & (df['cas_latency'] >= 0)].copy()
    print(f"    Filas válidas: {len(df)}")
    
    # Mismo preprocesamiento que regresion.py y ridge.py
    df['ddr_group'] = df['ddr_type'].apply(lambda x: 'DDR5' if x == 'DDR5' else 'DDR_legacy')
    dummies = pd.get_dummies(df[['ddr_group', 'brand_normalized']], drop_first=True, dtype=int)
    
    num_vars = ['capacity_gb', 'speed_mhz', 'cas_latency', 'num_sticks', 'has_rgb', 'cas_was_imputed']
    X = pd.concat([df[num_vars].reset_index(drop=True), dummies.reset_index(drop=True)], axis=1)
    y = df['log_price'].reset_index(drop=True)
    
    feature_names = list(X.columns)
    print(f"    Features: {len(feature_names)}")
    print(f"    NOTA: Random Forest NO requiere estandarización (insensible a escala)")
    
    # ════════════════════════════════════════════════════════════════
    # 2. SPLIT (mismo random_state que OLS y Ridge para comparabilidad)
    # ════════════════════════════════════════════════════════════════
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE)
    print(f"\n[2] Train: {len(X_train)}  Test: {len(X_test)}")
    
    # ════════════════════════════════════════════════════════════════
    # 3. BASELINE · Random Forest sin tuning
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🌲 BASELINE · Random Forest con defaults")
    print("═" * 70)
    
    rf_baseline = RandomForestRegressor(
        n_estimators=100,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )
    
    t0 = time.perf_counter()
    rf_baseline.fit(X_train, y_train)
    t_baseline = time.perf_counter() - t0
    
    y_pred_baseline = rf_baseline.predict(X_test)
    r2_baseline = r2_score(y_test, y_pred_baseline)
    
    print(f"\n    Hiperparámetros: n_estimators=100 (todo lo demás default)")
    print(f"    Tiempo de entrenamiento: {t_baseline:.3f} s")
    print(f"    R² test (baseline): {r2_baseline:.4f}")
    print(f"    (comparación: OLS=0.876, Ridge=0.869)")
    
    # ════════════════════════════════════════════════════════════════
    # 4. GRIDSEARCHCV · Búsqueda de hiperparámetros óptimos
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🔍 BÚSQUEDA DE HIPERPARÁMETROS · GridSearchCV con 5-fold CV")
    print("═" * 70)
    
    # Grid moderado (no demasiado grande para no tardar mucho)
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5],
        'max_features': ['sqrt', 'log2'],
    }
    
    n_combinaciones = 3 * 3 * 2 * 2  # = 36 combinaciones × 5 folds = 180 fits
    print(f"\n    Probando {n_combinaciones} combinaciones × 5 folds = {n_combinaciones*5} fits")
    print(f"    Hiperparámetros:")
    for k, v in param_grid.items():
        print(f"      · {k}: {v}")
    
    print(f"\n    ⏳ Ejecutando GridSearchCV (puede tardar 1-3 minutos)...")
    
    t0 = time.perf_counter()
    grid = GridSearchCV(
        RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=-1),
        param_grid=param_grid,
        cv=5,
        scoring='r2',
        n_jobs=-1,
        verbose=0
    )
    grid.fit(X_train, y_train)
    t_grid = time.perf_counter() - t0
    
    print(f"\n    ✅ GridSearchCV completado en {t_grid:.1f} s")
    print(f"\n    🎯 Mejores hiperparámetros encontrados:")
    for k, v in grid.best_params_.items():
        print(f"      · {k}: {v}")
    print(f"\n    CV-5 R² óptimo: {grid.best_score_:.4f}")
    
    # ════════════════════════════════════════════════════════════════
    # 5. EVALUACIÓN FINAL DEL MODELO OPTIMIZADO
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("📊 EVALUACIÓN FINAL · Random Forest optimizado")
    print("═" * 70)
    
    rf_final = grid.best_estimator_
    
    # Predicciones
    y_pred_train = rf_final.predict(X_train)
    y_pred_test = rf_final.predict(X_test)
    
    # Métricas escala log
    r2_train = r2_score(y_train, y_pred_train)
    r2_test = r2_score(y_test, y_pred_test)
    
    # Métricas escala USD
    y_test_usd = np.exp(y_test)
    y_pred_test_usd = np.exp(y_pred_test)
    
    rmse_usd = np.sqrt(mean_squared_error(y_test_usd, y_pred_test_usd))
    mae_usd = mean_absolute_error(y_test_usd, y_pred_test_usd)
    mape = np.mean(np.abs((y_test_usd - y_pred_test_usd) / y_test_usd)) * 100
    
    # Cross-validation final
    cv_scores = cross_val_score(rf_final, X, y, cv=5, scoring='r2', n_jobs=-1)
    
    print(f"\n    Métricas escala log:")
    print(f"      R² train: {r2_train:.4f}")
    print(f"      R² test:  {r2_test:.4f}")
    print(f"      Gap train-test: {r2_train-r2_test:+.4f} (señal de overfitting si >0.1)")
    
    print(f"\n    Métricas escala USD:")
    print(f"      RMSE: ${rmse_usd:.2f}")
    print(f"      MAE:  ${mae_usd:.2f}")
    print(f"      MAPE: {mape:.2f}%")
    
    print(f"\n    Cross-validation 5-fold:")
    print(f"      R² medio: {cv_scores.mean():.4f}")
    print(f"      R² std:   {cv_scores.std():.4f}")
    print(f"      R² folds: {[f'{s:.3f}' for s in cv_scores]}")
    
    # ════════════════════════════════════════════════════════════════
    # 6. COMPARACIÓN VS OLS y RIDGE
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🆚 COMPARACIÓN CON MODELOS LINEALES (OLS y Ridge)")
    print("═" * 70)
    
    # Valores de OLS y Ridge desde los días anteriores
    r2_ols = 0.8758
    rmse_ols = 203.14
    mae_ols = 107.11
    mape_ols = 17.36
    
    r2_ridge = 0.8686
    rmse_ridge = 198.46
    mae_ridge = 106.14
    mape_ridge = 17.45
    
    print(f"\n    {'Métrica':<10} {'OLS':>10} {'Ridge':>10} {'RF':>10} {'RF vs OLS':>12}")
    print(f"    " + "─" * 60)
    print(f"    {'R² test':<10} {r2_ols:>10.4f} {r2_ridge:>10.4f} {r2_test:>10.4f} {r2_test-r2_ols:>+11.4f}")
    print(f"    {'RMSE':<10} ${rmse_ols:>9.2f} ${rmse_ridge:>9.2f} ${rmse_usd:>9.2f} ${rmse_usd-rmse_ols:>+10.2f}")
    print(f"    {'MAE':<10} ${mae_ols:>9.2f} ${mae_ridge:>9.2f} ${mae_usd:>9.2f} ${mae_usd-mae_ols:>+10.2f}")
    print(f"    {'MAPE':<10} {mape_ols:>9.2f}% {mape_ridge:>9.2f}% {mape:>9.2f}% {mape-mape_ols:>+11.2f}%")
    
    if r2_test > r2_ols + 0.01:
        veredicto = f"🏆 Random Forest GANA por margen significativo (+{r2_test-r2_ols:.3f})"
    elif r2_test > r2_ols:
        veredicto = f"⚠️  Random Forest gana por margen pequeño (+{r2_test-r2_ols:.3f})"
    else:
        veredicto = f"📊 OLS sigue siendo competitivo"
    
    print(f"\n    Veredicto: {veredicto}")
    
    # ════════════════════════════════════════════════════════════════
    # 7. FEATURE IMPORTANCES
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("📊 FEATURE IMPORTANCES")
    print("═" * 70)
    
    importances = rf_final.feature_importances_
    feat_imp = pd.DataFrame({
        'feature': feature_names,
        'importance': importances,
    }).sort_values('importance', ascending=False)
    
    print(f"\n    {'Feature':<35} {'Importance':>12} {'% Acumulado':>14}")
    print(f"    " + "─" * 65)
    
    feat_imp['cumsum'] = feat_imp['importance'].cumsum() * 100
    
    for _, row in feat_imp.iterrows():
        print(f"    {row['feature']:<35} {row['importance']:>12.4f} {row['cumsum']:>13.2f}%")
    
    print(f"\n    🎯 Top 3 features explican el {feat_imp.head(3)['importance'].sum()*100:.1f}% del modelo")

    # ════════════════════════════════════════════════════════════════
    # 8. GRÁFICA · 4 paneles
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🎨 GENERANDO GRÁFICA")
    print("═" * 70)
    
    fig = plt.figure(figsize=(16, 11))
    gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.3)
    
    # ─── Panel 1: Feature importances ────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    
    top_features = feat_imp.head(10)
    colors = sns.color_palette("RdYlBu_r", len(top_features))
    
    bars = ax1.barh(top_features['feature'], top_features['importance'],
                     color=colors, edgecolor='black', alpha=0.85)
    
    for bar, imp in zip(bars, top_features['importance']):
        ax1.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2,
                 f'{imp:.3f}', va='center', fontsize=10, fontweight='bold')
    
    ax1.set_xlabel('Feature Importance', fontsize=11)
    ax1.set_title(f'Top 10 Feature Importances · Random Forest\n'
                  f'Top 3 explican {feat_imp.head(3)["importance"].sum()*100:.1f}% del modelo',
                  fontsize=12, fontweight='bold')
    ax1.invert_yaxis()
    
    # ─── Panel 2: Real vs Predicho ──────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    
    ax2.scatter(y_test_usd, y_pred_test_usd, alpha=0.6, color='#2ecc71',
                edgecolors='black', linewidth=0.5, s=60)
    
    max_val = max(y_test_usd.max(), y_pred_test_usd.max())
    ax2.plot([0, max_val], [0, max_val], 'k--', linewidth=2, label='Identidad')
    
    ax2.set_xlabel('Precio real (USD)', fontsize=11)
    ax2.set_ylabel('Precio predicho (USD)', fontsize=11)
    ax2.set_title(f'Random Forest · Predicción en test set\n'
                  f'R²={r2_test:.4f} · RMSE=${rmse_usd:.0f} · MAPE={mape:.1f}%',
                  fontsize=12, fontweight='bold')
    ax2.legend(fontsize=10)
    
    # ─── Panel 3: Comparación de R² entre 3 modelos ──────────────
    ax3 = fig.add_subplot(gs[1, 0])
    
    modelos = ['OLS\n(Día 6)', 'Ridge\n(Día 7)', 'Random Forest\n(Día 8)']
    r2_values = [r2_ols, r2_ridge, r2_test]
    colors_models = ['#e74c3c', '#3498db', '#2ecc71']
    
    bars = ax3.bar(modelos, r2_values, color=colors_models, alpha=0.85,
                    edgecolor='black', linewidth=1.5)
    
    for bar, r2 in zip(bars, r2_values):
        ax3.text(bar.get_x() + bar.get_width()/2, r2 + 0.005,
                 f'{r2:.4f}', ha='center', va='bottom',
                 fontsize=12, fontweight='bold')
    
    ax3.set_ylim(min(r2_values) - 0.02, max(r2_values) + 0.02)
    ax3.set_ylabel('R² en test set', fontsize=11)
    ax3.set_title('Comparación de R² test entre modelos predictivos\n'
                  '(mismo split 80/20 y random_state=42)',
                  fontsize=12, fontweight='bold')
    ax3.axhline(r2_ols, color='gray', linestyle=':', alpha=0.5)
    
    # ─── Panel 4: Tabla resumen ──────────────────────────────────
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    
    table_data = [
        ['Métrica', 'OLS', 'Ridge', 'Random Forest'],
        ['R² train', '0.9066', '0.9055', f'{r2_train:.4f}'],
        ['R² test', f'{r2_ols:.4f}', f'{r2_ridge:.4f}', f'{r2_test:.4f}'],
        ['CV-5 R²', '—', '0.8851', f'{cv_scores.mean():.4f}'],
        ['RMSE USD', f'${rmse_ols:.2f}', f'${rmse_ridge:.2f}', f'${rmse_usd:.2f}'],
        ['MAE USD', f'${mae_ols:.2f}', f'${mae_ridge:.2f}', f'${mae_usd:.2f}'],
        ['MAPE %', f'{mape_ols:.2f}%', f'{mape_ridge:.2f}%', f'{mape:.2f}%'],
        ['Tiempo entrenamiento', '~0.01s', '~0.02s', f'~{t_grid/n_combinaciones/5:.2f}s'],
        ['Interpretabilidad', '✅ Alta', '✅ Alta', '⚠️  Parcial'],
    ]
    
    table = ax4.table(cellText=table_data, cellLoc='center', loc='center',
                      colWidths=[0.30, 0.22, 0.22, 0.26])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.9)
    
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
    
    ax4.set_title('Comparativa de 3 modelos predictivos · mismo split 80/20',
                  fontsize=12, fontweight='bold', pad=20)
    
    plt.suptitle(f'Random Forest Regressor · Modelo 4 de 5\n'
                 f'Mejores hiperparámetros: n_estimators={grid.best_params_["n_estimators"]}, '
                 f'max_depth={grid.best_params_["max_depth"]}',
                 fontsize=14, fontweight='bold', y=0.99)
    
    fig_path = FIG_DIR / "23_random_forest.png"
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    print(f"\n    ✅ Gráfica guardada: {fig_path.name}")
    
    # Guardar resultados
    resultados = pd.DataFrame({
        'modelo': ['OLS', 'Ridge', 'Random Forest'],
        'R²_train': [0.9066, 0.9055, r2_train],
        'R²_test': [r2_ols, r2_ridge, r2_test],
        'CV_5_R²': [None, 0.8851, cv_scores.mean()],
        'RMSE_USD': [rmse_ols, rmse_ridge, rmse_usd],
        'MAE_USD': [mae_ols, mae_ridge, mae_usd],
        'MAPE': [mape_ols, mape_ridge, mape],
    })
    resultados.to_csv(DATA_DIR / "rf_comparison.csv", index=False)
    
    feat_imp.to_csv(DATA_DIR / "rf_feature_importances.csv", index=False)
    print(f"    💾 Resultados: rf_comparison.csv, rf_feature_importances.csv")
    
    # ════════════════════════════════════════════════════════════════
    # CIERRE
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("✅ MODELO 4 (RANDOM FOREST) COMPLETADO")
    print("═" * 70)
    
    print(f"\n📌 Resumen para defensa oral:")
    print(f"\n   Modelo 4 · Random Forest:")
    print(f"     · R² test: {r2_test:.4f} (vs OLS 0.876, vs Ridge 0.869)")
    print(f"     · Ganancia sobre OLS: {(r2_test-r2_ols)*100:+.2f} puntos porcentuales")
    print(f"     · Top 3 features explican {feat_imp.head(3)['importance'].sum()*100:.1f}% del modelo")
    print(f"     · {grid.best_params_['n_estimators']} árboles, max_depth={grid.best_params_['max_depth']}")
    
    print(f"\n📌 Frase para defensa oral:")
    print(f"""
   "Random Forest con {grid.best_params_['n_estimators']} árboles y max_depth={grid.best_params_['max_depth']}
   (encontrados via GridSearchCV en 36 combinaciones) alcanzó R² test
   de {r2_test:.4f}, ganando {(r2_test-r2_ols)*100:+.2f} puntos porcentuales sobre OLS.
   Las feature importances confirman el hallazgo de los días anteriores:
   capacity_gb y speed_mhz dominan el modelo, las marcas individuales
   tienen importancia secundaria. La ganancia marginal sobre OLS
   no justifica la pérdida de interpretabilidad por Occam's razor."
    """)
    
    print(f"\n🎯 Siguiente: Modelo 5 · Gradient Boosting (bloque tarde Día 8)")


if __name__ == "__main__":
    main()