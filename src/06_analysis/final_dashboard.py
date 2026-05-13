"""
dashboard_final.py — Día 9 · Dashboard maestro del proyecto

Genera figures/26_dashboard_final.png · LA gráfica central del póster A1.

Sintetiza 8 días de análisis en una sola imagen de 6 paneles:
  Panel 1: Pipeline del proyecto (estilo flowchart visual)
  Panel 2: Comparación R² de 4 modelos predictivos
  Panel 3: Comparación MAPE de 4 modelos
  Panel 4: Convergencia de feature importance entre modelos
  Panel 5+6: Tabla maestra de los 5 modelos

Autor: Jose Najera · UDG · DS-2025-GDL
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import seaborn as sns
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
FIG_DIR = SCRIPT_DIR / "figures"

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300


def main():
    print("═" * 70)
    print("📊 DÍA 9 · DASHBOARD FINAL DEL PROYECTO")
    print("═" * 70)
    
    # ════════════════════════════════════════════════════════════════
    # DATOS CONSOLIDADOS (de los días 6-8)
    # ════════════════════════════════════════════════════════════════
    
    modelos_predictivos = ['OLS', 'Ridge', 'Random Forest', 'Gradient Boosting']
    r2_values = [0.8758, 0.8686, 0.9020, 0.9616]
    mape_values = [17.36, 17.45, 10.42, 8.32]
    mae_values = [107.11, 106.14, 71.04, 52.02]
    rmse_values = [203.14, 198.46, 158.74, 125.04]
    
    colores_modelos = {
        'OLS': '#e74c3c',
        'Ridge': '#3498db',
        'Random Forest': '#2ecc71',
        'Gradient Boosting': '#9b59b6',
    }
    
    # Feature importance unificada (top 5 features)
    features_importance = pd.DataFrame({
        'feature': ['capacity_gb', 'speed_mhz', 'cas_latency', 
                    'ddr_legacy', 'num_sticks'],
        'OLS_coef_abs': [0.4926, 0.3176, 0.0937, 0.1497, 0.0592],
        'Ridge_coef_abs': [0.4719, 0.2839, 0.0589, 0.1529, 0.0707],
        'RF_importance': [0.4677, 0.1628, 0.1181, 0.1129, 0.0726],
        'GB_importance': [0.856, 0.071, 0.016, 0.035, 0.007],
    })
    
    # Normalizar para comparabilidad (cada columna suma 1)
    for col in ['OLS_coef_abs', 'Ridge_coef_abs', 'RF_importance', 'GB_importance']:
        features_importance[col] = features_importance[col] / features_importance[col].sum()
    
    print("\n[1] Datos consolidados cargados")
    print(f"    4 modelos predictivos comparables")
    print(f"    Top 5 features con importance normalizada")
    
    # ════════════════════════════════════════════════════════════════
    # CREAR FIGURA · 6 PANELES
    # ════════════════════════════════════════════════════════════════
    
    print("\n[2] Construyendo dashboard de 6 paneles...")
    
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.45, wspace=0.35,
                          height_ratios=[1, 1, 0.8])
    
    # ─── Panel 1 (top-left): Pipeline del proyecto ─────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    
    etapas = [
        ('Scraping\nNewegg', 5, 9, '#3498db'),
        ('Limpieza\n+ EDA', 5, 7.5, '#2ecc71'),
        ('SQL + Indices\n+ Inferencia', 5, 6, '#f39c12'),
        ('5 Modelos\nPredictivos', 5, 4.5, '#9b59b6'),
        ('Complejidad\nML', 5, 3, '#e74c3c'),
        ('Poster +\nDefensa', 5, 1.5, '#95a5a6'),
    ]
    
    for nombre, x, y, color in etapas:
        box = FancyBboxPatch((x-1.8, y-0.6), 3.6, 1.2,
                              boxstyle="round,pad=0.05",
                              edgecolor='black', facecolor=color, 
                              alpha=0.85, linewidth=1.5)
        ax1.add_patch(box)
        ax1.text(x, y, nombre, ha='center', va='center', 
                 fontsize=10, fontweight='bold', color='white')
    
    # Flechas conectando etapas
    for i in range(len(etapas) - 1):
        _, x1, y1, _ = etapas[i]
        _, x2, y2, _ = etapas[i + 1]
        arrow = FancyArrowPatch((x1, y1 - 0.65), (x2, y2 + 0.65),
                                 arrowstyle='->,head_width=0.3,head_length=0.5',
                                 color='black', linewidth=1.5)
        ax1.add_patch(arrow)
    
    ax1.set_title('Pipeline del proyecto\n12 días · 8 etapas',
                  fontsize=12, fontweight='bold', pad=15)
    
    # ─── Panel 2 (top-center): R² comparativo ───────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    
    colores = [colores_modelos[m] for m in modelos_predictivos]
    bars = ax2.bar(range(len(modelos_predictivos)), r2_values,
                    color=colores, alpha=0.85,
                    edgecolor='black', linewidth=1.5)
    
    for bar, r2 in zip(bars, r2_values):
        ax2.text(bar.get_x() + bar.get_width()/2, r2 + 0.005,
                 f'{r2:.4f}', ha='center', va='bottom',
                 fontsize=11, fontweight='bold')
    
    # Resaltar el ganador
    bars[-1].set_edgecolor('gold')
    bars[-1].set_linewidth(3)
    
    ax2.set_xticks(range(len(modelos_predictivos)))
    ax2.set_xticklabels([m.replace(' ', '\n') for m in modelos_predictivos],
                         fontsize=9)
    ax2.set_ylim(min(r2_values) - 0.02, max(r2_values) + 0.02)
    ax2.set_ylabel('R² test', fontsize=11)
    ax2.set_title('Coeficiente de determinación R²\n(mismo split 80/20)',
                  fontsize=12, fontweight='bold')
    
    # ─── Panel 3 (top-right): MAPE comparativo ─────────────────────
    ax3 = fig.add_subplot(gs[0, 2])
    
    bars = ax3.bar(range(len(modelos_predictivos)), mape_values,
                    color=colores, alpha=0.85,
                    edgecolor='black', linewidth=1.5)
    
    for bar, m in zip(bars, mape_values):
        ax3.text(bar.get_x() + bar.get_width()/2, m + 0.3,
                 f'{m:.2f}%', ha='center', va='bottom',
                 fontsize=11, fontweight='bold')
    
    bars[-1].set_edgecolor('gold')
    bars[-1].set_linewidth(3)
    
    ax3.set_xticks(range(len(modelos_predictivos)))
    ax3.set_xticklabels([m.replace(' ', '\n') for m in modelos_predictivos],
                         fontsize=9)
    ax3.set_ylim(0, max(mape_values) + 3)
    ax3.set_ylabel('MAPE (%)', fontsize=11)
    ax3.set_title('Error porcentual medio MAPE\n(menor = mejor)',
                  fontsize=12, fontweight='bold')
    
    # ─── Panel 4 (middle-left): Convergencia de features ───────────
    ax4 = fig.add_subplot(gs[1, 0])
    
    n_features = len(features_importance)
    x_pos = np.arange(n_features)
    width = 0.2
    
    ax4.bar(x_pos - 1.5*width, features_importance['OLS_coef_abs'], width,
             label='OLS', color=colores_modelos['OLS'], alpha=0.85, edgecolor='black')
    ax4.bar(x_pos - 0.5*width, features_importance['Ridge_coef_abs'], width,
             label='Ridge', color=colores_modelos['Ridge'], alpha=0.85, edgecolor='black')
    ax4.bar(x_pos + 0.5*width, features_importance['RF_importance'], width,
             label='RF', color=colores_modelos['Random Forest'], alpha=0.85, edgecolor='black')
    ax4.bar(x_pos + 1.5*width, features_importance['GB_importance'], width,
             label='GB', color=colores_modelos['Gradient Boosting'], alpha=0.85, edgecolor='black')
    
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(features_importance['feature'], fontsize=9, rotation=20)
    ax4.set_ylabel('Importancia relativa\n(normalizada)', fontsize=11)
    ax4.set_title('Convergencia de feature importance\n4 modelos coinciden: capacity_gb es #1',
                  fontsize=12, fontweight='bold')
    ax4.legend(fontsize=9, loc='upper right')
    
    # ─── Panel 5 (middle-center + right): Tabla maestra ────────────
    ax5 = fig.add_subplot(gs[1, 1:])
    ax5.axis('off')
    
    table_data = [
        ['Modelo', 'Tipo', 'R²', 'MAPE', 'MAE', 'RMSE', 'Veredicto'],
        ['OLS (Día 6)', 'Lineal', '0.876', '17.4%', '$107', '$203', 
         'Mejor para INFERENCIA'],
        ['Ridge (Día 7)', 'Regularizado', '0.869', '17.5%', '$106', '$198',
         'Empate técnico con OLS'],
        ['K-Means (Día 7)', 'Clustering', 'N/A', 'N/A', 'N/A', 'N/A',
         'Segmenta mercado k=2'],
        ['Random Forest (Día 8)', 'Bagging', '0.902', '10.4%', '$71', '$159',
         'Captura no-linealidad'],
        ['Gradient Boost (Día 8)', 'Boosting', '0.962', '8.3%', '$52', '$125',
         'MEJOR para PREDICCIÓN'],
    ]
    
    table = ax5.table(cellText=table_data, cellLoc='center', loc='center',
                      colWidths=[0.18, 0.13, 0.08, 0.08, 0.08, 0.08, 0.27])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.0)
    
    # Header
    for j in range(7):
        cell = table[0, j]
        cell.set_facecolor('#2c3e50')
        cell.set_text_props(color='white', fontweight='bold')
    
    # Filas alternadas
    for i in range(1, len(table_data)):
        for j in range(7):
            cell = table[i, j]
            cell.set_facecolor('#ecf0f1' if i % 2 == 0 else 'white')
    
    # Resaltar el ganador (Gradient Boosting)
    for j in range(7):
        cell = table[5, j]
        cell.set_facecolor('#f1c40f')
        cell.set_text_props(fontweight='bold')
    
    # Resaltar OLS como inferencial
    for j in range(7):
        cell = table[1, j]
        cell.set_facecolor('#aed6f1')
    
    ax5.set_title('Tabla maestra · 5 modelos del proyecto\n'
                  'Amarillo = ganador en predicción · Azul = ganador en inferencia',
                  fontsize=12, fontweight='bold', pad=20)
    
    # ─── Panel 6 (bottom): Conclusión visual ──────────────────────
    ax6 = fig.add_subplot(gs[2, :])
    ax6.axis('off')
    
    # Caja de conclusión
    box = FancyBboxPatch((0.05, 0.1), 0.9, 0.8,
                          boxstyle="round,pad=0.02",
                          edgecolor='#2c3e50', facecolor='#ecf0f1',
                          alpha=0.95, linewidth=2,
                          transform=ax6.transAxes)
    ax6.add_patch(box)
    
    texto_conclusion = (
        "HALLAZGO CENTRAL DEL PROYECTO\n\n"
        "Los 6 paradigmas analíticos convergen: capacity_gb es el predictor #1 del precio\n"
        "(OLS β=+0.49, RF importance=46.8%, GB importance=85.6%), seguido por la generación DDR\n"
        "(η² ANOVA = 60.8%). La marca es secundaria (η² = 22.4%) pero existe un premium\n"
        "real de marca: CORSAIR cobra 10-35% más controlando por features técnicos.\n\n"
        "DECISIÓN ACADÉMICA: OLS para INFERENCIA (interpretabilidad) + Gradient Boosting para PREDICCIÓN (MAPE 8.3%)"
    )
    
    ax6.text(0.5, 0.5, texto_conclusion, ha='center', va='center',
             fontsize=11, fontweight='normal',
             transform=ax6.transAxes,
             color='#2c3e50',
             linespacing=1.5)
    
    plt.suptitle('OPTIMIZACIÓN ASINTÓTICA EN LA PREDICCIÓN DEL MERCADO DE MEMORIA RAM\n'
                 'Universidad de Guadalajara · Mayo 2026 · n=350 productos · 5 modelos predictivos',
                 fontsize=14, fontweight='bold', y=0.995)
    
    fig_path = FIG_DIR / "26_dashboard_final.png"
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    print(f"\n✅ Dashboard guardado: {fig_path.name}")
    
    print("\n" + "═" * 70)
    print("✅ DASHBOARD DEL POSTER COMPLETADO")
    print("═" * 70)
    
    print("""
📌 Características del dashboard:
   · 6 paneles informativos
   · 4 modelos comparados en R² y MAPE
   · Convergencia de feature importance entre paradigmas
   · Tabla maestra de los 5 modelos con veredicto
   · Conclusión central destacada
   · Resaltado visual del ganador (Gradient Boosting)
   · Resaltado del modelo de inferencia (OLS)

🎯 Esta gráfica va al CENTRO del póster A1
   Es la imagen que sintetiza 12 días de trabajo en una vista
    """)


if __name__ == "__main__":
    main()