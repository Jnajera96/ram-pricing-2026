"""
inferencia_dashboard.py — Día 5 · Bloque 5: Dashboard consolidado

Genera una figura única (figures/10_inferential_dashboard.png) que
resume todos los hallazgos inferenciales del Día 5:
  · Test t DDR4 vs DDR5 (Cohen's d=2.20)
  · ANOVA por DDR (η²=0.608)
  · ANOVA por marca (η²=0.224)
  · Resumen de p-values y effect sizes

Esta figura es la "slide central" del póster para la sección inferencial.

Autor: Jose Najera · UDG · DS-2025-GDL
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import seaborn as sns
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
FIG_DIR = SCRIPT_DIR / "figures"

CSV_INPUT = DATA_DIR / "ram_clean.csv"
RESULTS_PATH = DATA_DIR / "inferential_results.csv"

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300


def cohens_d(g1, g2):
    n1, n2 = len(g1), len(g2)
    pooled = np.sqrt(((n1-1)*g1.var(ddof=1) + (n2-1)*g2.var(ddof=1)) / (n1+n2-2))
    return (g1.mean() - g2.mean()) / pooled


def main():
    print("═" * 70)
    print("📊 DÍA 5 · BLOQUE 5 · DASHBOARD INFERENCIAL CONSOLIDADO")
    print("═" * 70)
    
    df = pd.read_csv(CSV_INPUT)
    
    # Recalcular todos los tests para tenerlos en memoria
    g_ddr3 = df[df['ddr_type'] == 'DDR3']['log_price']
    g_ddr4 = df[df['ddr_type'] == 'DDR4']['log_price']
    g_ddr5 = df[df['ddr_type'] == 'DDR5']['log_price']
    
    # Bloque 2: t-test DDR4 vs DDR5
    t_stat, p_t = stats.ttest_ind(g_ddr5, g_ddr4, equal_var=False)
    d_t = cohens_d(g_ddr5, g_ddr4)
    
    # Bloque 3: ANOVA DDR
    f_ddr, p_ddr = stats.f_oneway(g_ddr3, g_ddr4, g_ddr5)
    eta_ddr = 0.608  # del bloque 3
    
    # Bloque 4: ANOVA Marca
    grupos_marca = [df[df['brand_normalized']==m]['log_price'] 
                    for m in df['brand_normalized'].value_counts().index]
    f_marca, p_marca = stats.f_oneway(*grupos_marca)
    eta_marca = 0.224
    
    print(f"\n📋 Recap de tests del Día 5:")
    print(f"   · Welch t (DDR4 vs DDR5): t={t_stat:.2f}, p<0.001, d={d_t:.2f}")
    print(f"   · ANOVA por DDR:           F={f_ddr:.2f}, p<0.001, η²={eta_ddr:.3f}")
    print(f"   · ANOVA por marca:         F={f_marca:.2f}, p<0.001, η²={eta_marca:.3f}")

    # ════════════════════════════════════════════════════════════════
    # GUARDAR RESULTADOS A CSV (para futura referencia)
    # ════════════════════════════════════════════════════════════════
    
    resultados = pd.DataFrame([
        {
            'test': 'Welch t-test',
            'pregunta': 'DDR4 vs DDR5',
            'estadistico': f'{t_stat:.4f}',
            'p_value': p_t,
            'effect_size': f'd={d_t:.3f}',
            'magnitud_efecto': 'muy grande',
            'conclusion': 'DDR5 significativamente más caro (3.86x)',
        },
        {
            'test': 'ANOVA + Tukey',
            'pregunta': 'Diferencias por DDR',
            'estadistico': f'F={f_ddr:.4f}',
            'p_value': p_ddr,
            'effect_size': f'η²={eta_ddr:.3f}',
            'magnitud_efecto': 'grande (60.8%)',
            'conclusion': 'Jerarquía DDR3 < DDR4 < DDR5 (todos pares sig.)',
        },
        {
            'test': 'ANOVA + Tukey',
            'pregunta': 'Diferencias por marca',
            'estadistico': f'F={f_marca:.4f}',
            'p_value': p_marca,
            'effect_size': f'η²={eta_marca:.3f}',
            'magnitud_efecto': 'grande (22.4%)',
            'conclusion': 'Premium (CORSAIR, G.SKILL, Kingston) vs económica (Team, Crucial, Other)',
        },
    ])
    
    resultados.to_csv(RESULTS_PATH, index=False)
    print(f"\n💾 Resultados guardados: {RESULTS_PATH}")

    # ════════════════════════════════════════════════════════════════
    # GRÁFICA · DASHBOARD CONSOLIDADO
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🎨 GENERANDO DASHBOARD CONSOLIDADO")
    print("═" * 70)
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 3, hspace=0.4, wspace=0.3)
    
    # ─── PANEL 1 (top-left): Boxplot por DDR ────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    sns.boxplot(x='ddr_type', y='log_price', data=df, hue='ddr_type',
                palette={'DDR3': '#3498db', 'DDR4': '#e67e22', 'DDR5': '#2ecc71'},
                order=['DDR3', 'DDR4', 'DDR5'], ax=ax1, legend=False)
    ax1.set_title(f"ANOVA por DDR\nF={f_ddr:.1f}, p<0.001, η²={eta_ddr:.2f}",
                  fontsize=11, fontweight='bold')
    ax1.set_xlabel('Generación DDR', fontsize=10)
    ax1.set_ylabel('log(1+precio)', fontsize=10)
    
    # ─── PANEL 2 (top-center): Boxplot por marca ────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    orden_marcas = df.groupby('brand_normalized')['price_usd'].median().sort_values(ascending=False).index
    sns.boxplot(x='brand_normalized', y='log_price', data=df,
                hue='brand_normalized', order=orden_marcas,
                palette='Set2', ax=ax2, legend=False)
    ax2.set_title(f"ANOVA por Marca\nF={f_marca:.1f}, p<0.001, η²={eta_marca:.2f}",
                  fontsize=11, fontweight='bold')
    ax2.set_xlabel('Marca (orden por mediana descendente)', fontsize=10)
    ax2.set_ylabel('log(1+precio)', fontsize=10)
    ax2.tick_params(axis='x', rotation=20, labelsize=9)
    
    # ─── PANEL 3 (top-right): t-test DDR4 vs DDR5 ───────────────────
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.hist(g_ddr4, bins=20, alpha=0.6, color='#e67e22',
             label=f'DDR4 (n={len(g_ddr4)})', density=True, edgecolor='black')
    ax3.hist(g_ddr5, bins=20, alpha=0.6, color='#2ecc71',
             label=f'DDR5 (n={len(g_ddr5)})', density=True, edgecolor='black')
    ax3.axvline(g_ddr4.mean(), color='#d35400', linestyle='--', linewidth=2)
    ax3.axvline(g_ddr5.mean(), color='#27ae60', linestyle='--', linewidth=2)
    ax3.set_title(f"Welch t-test DDR4 vs DDR5\nt={t_stat:.2f}, p<0.001, d={d_t:.2f}",
                  fontsize=11, fontweight='bold')
    ax3.set_xlabel('log(1+precio)', fontsize=10)
    ax3.set_ylabel('Densidad', fontsize=10)
    ax3.legend(fontsize=9)
    
    # ─── PANEL 4 (bottom-left): Effect sizes comparados ─────────────
    ax4 = fig.add_subplot(gs[1, 0])
    
    factores = ['DDR\n(Bloque 3)', 'Marca\n(Bloque 4)']
    eta_values = [eta_ddr, eta_marca]
    colors = ['#2ecc71', '#3498db']
    
    bars = ax4.bar(factores, [v*100 for v in eta_values], color=colors,
                   alpha=0.85, edgecolor='black', linewidth=1)
    
    # Líneas de referencia para magnitud
    ax4.axhline(14, color='gray', linestyle=':', alpha=0.5, label='Umbral "grande" (14%)')
    ax4.axhline(6, color='gray', linestyle=':', alpha=0.3, label='Umbral "mediano" (6%)')
    
    for bar, value in zip(bars, eta_values):
        ax4.text(bar.get_x() + bar.get_width()/2, value*100 + 1,
                 f'{value*100:.1f}%', ha='center', va='bottom',
                 fontweight='bold', fontsize=11)
    
    ax4.set_ylim(0, 70)
    ax4.set_ylabel('Varianza explicada (η² × 100)', fontsize=10)
    ax4.set_title('Comparación de tamaños de efecto\nη² = % de varianza explicada por cada factor',
                  fontsize=11, fontweight='bold')
    ax4.legend(loc='upper right', fontsize=8)
    
    # ─── PANEL 5 (bottom-center): Tabla resumen visual ──────────────
    ax5 = fig.add_subplot(gs[1, 1:])
    ax5.axis('off')
    
    table_data = [
        ['Test', 'Pregunta', 'Estadístico', 'p-value', 'Effect Size', 'Conclusión'],
        ['Welch t', 'DDR4 vs DDR5', f't={t_stat:.2f}', '<0.001 (***)', f'd={d_t:.2f} (muy grande)', 
         'DDR5 más caro (3.86×)'],
        ['ANOVA + Tukey', '3 generaciones DDR', f'F={f_ddr:.1f}', '<0.001 (***)', f'η²={eta_ddr:.2f} (grande)', 
         'DDR3 < DDR4 < DDR5'],
        ['ANOVA + Tukey', '6 marcas', f'F={f_marca:.1f}', '<0.001 (***)', f'η²={eta_marca:.2f} (grande)', 
         '2 segmentos: Premium/Económico'],
    ]
    
    table = ax5.table(cellText=table_data, cellLoc='center', loc='center',
                      colWidths=[0.13, 0.18, 0.13, 0.13, 0.18, 0.25])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.2)
    
    # Estilizar header
    for j in range(len(table_data[0])):
        cell = table[0, j]
        cell.set_facecolor('#2c3e50')
        cell.set_text_props(color='white', fontweight='bold')
    
    # Alternar colores en filas de datos
    for i in range(1, len(table_data)):
        for j in range(len(table_data[0])):
            cell = table[i, j]
            cell.set_facecolor('#ecf0f1' if i % 2 == 0 else 'white')
    
    ax5.set_title('Resumen ejecutivo · Tests inferenciales del Día 5',
                  fontsize=12, fontweight='bold', pad=20)
    
    # ─── Título superior ────────────────────────────────────────────
    fig.suptitle('Análisis Inferencial · Mercado RAM Newegg (n=350)\n'
                 'Triangulación Welch t + ANOVA + Tukey HSD + Effect Sizes',
                 fontsize=15, fontweight='bold', y=0.99)
    
    fig_path = FIG_DIR / "10_inferential_dashboard.png"
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    
    print(f"\n   ✅ Dashboard guardado: {fig_path.name}")

    # ════════════════════════════════════════════════════════════════
    # CIERRE DEL DÍA 5
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("✅ DÍA 5 COMPLETADO · ESTADÍSTICA INFERENCIAL")
    print("═" * 70)
    
    print(f"\n📌 Hallazgos clave para defensa oral:")
    print(f"\n   1. DDR5 es 3.86× más caro que DDR4 (Welch t, d=2.20)")
    print(f"   2. La generación DDR explica el 60.8% de la varianza (η²=0.608)")
    print(f"   3. La marca explica el 22.4% de la varianza (η²=0.224)")
    print(f"   4. Las marcas se dividen en 2 clusters (Premium / Económico)")
    print(f"   5. CORSAIR es la marca premium (mediana $580)")
    print(f"   6. Other es el segmento más económico (mediana $200)")
    
    print(f"\n📦 Artefactos del Día 5:")
    print(f"   · inferencia.py            (Bloque 1: validación supuestos)")
    print(f"   · inferencia_bloque2.py    (test t DDR4 vs DDR5)")
    print(f"   · inferencia_bloque3.py    (ANOVA por DDR)")
    print(f"   · inferencia_bloque4.py    (ANOVA por marca)")
    print(f"   · inferencia_dashboard.py  (este script)")
    print(f"   · figures/06_normality_check.png")
    print(f"   · figures/07_ttest_ddr4_vs_ddr5.png")
    print(f"   · figures/08_anova_ddr.png")
    print(f"   · figures/09_anova_marca.png")
    print(f"   · figures/10_inferential_dashboard.png  ← CLAVE PARA PÓSTER")
    print(f"   · data/inferential_results.csv")
    
    print(f"\n🎯 Sprint completion: 42% → 50% (¡a la mitad!)")
    print(f"📅 Días restantes hasta deadline: 7")


if __name__ == "__main__":
    main()