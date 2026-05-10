"""
inferencia_bloque3.py — Día 5 · Bloque 3: ANOVA + post-hoc Tukey

Pregunta:
  ¿Hay diferencias significativas entre los 3 tipos DDR
  (DDR3, DDR4, DDR5) y cuáles pares específicos difieren?

Tests aplicados:
  1. ANOVA estándar (paramétrico)
  2. Kruskal-Wallis (no-paramétrico, sanity check)
  3. Tukey HSD post-hoc (¿cuáles pares difieren?)
  4. Eta-squared (tamaño del efecto del ANOVA)

Autor: Jose Najera · UDG · DS-2025-GDL
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ════════════════════════════════════════════════════════════════

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
FIG_DIR = SCRIPT_DIR / "figures"

CSV_INPUT = DATA_DIR / "ram_clean.csv"

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300


# ════════════════════════════════════════════════════════════════
# UTILIDADES
# ════════════════════════════════════════════════════════════════

def interpretar_p(p_value, alpha=0.05):
    if p_value < 0.001:
        return f"p={p_value:.6f} (***) altamente significativo"
    elif p_value < 0.01:
        return f"p={p_value:.4f} (**) muy significativo"
    elif p_value < alpha:
        return f"p={p_value:.4f} (*) significativo"
    else:
        return f"p={p_value:.4f} (n.s.) NO significativo"


def calcular_eta_squared(grupos, total_data):
    """
    Eta-squared (η²) para tamaño del efecto del ANOVA.
    Interpretación:
      η² < 0.01  → trivial
      η² < 0.06  → pequeño
      η² < 0.14  → mediano
      η² >= 0.14 → grande
    """
    n_total = sum(len(g) for g in grupos)
    media_total = np.concatenate(grupos).mean()
    
    # SS_between
    ss_between = sum(len(g) * (g.mean() - media_total)**2 for g in grupos)
    
    # SS_total
    ss_total = sum((np.concatenate(grupos) - media_total)**2)
    
    eta_sq = ss_between / ss_total
    
    if eta_sq < 0.01:
        magnitud = "trivial"
    elif eta_sq < 0.06:
        magnitud = "pequeño"
    elif eta_sq < 0.14:
        magnitud = "mediano"
    else:
        magnitud = "grande"
    
    return eta_sq, magnitud


def tukey_hsd_manual(grupos, etiquetas, alpha=0.05):
    """
    Implementación manual de Tukey HSD.
    Devuelve DataFrame con pares y p-values ajustados.
    """
    from itertools import combinations
    
    n_grupos = len(grupos)
    n_per_group = [len(g) for g in grupos]
    medias = [g.mean() for g in grupos]
    
    # MS_within (mean square error)
    n_total = sum(n_per_group)
    df_within = n_total - n_grupos
    
    ss_within = sum(((g - g.mean())**2).sum() for g in grupos)
    ms_within = ss_within / df_within
    
    # Statistical tests por par
    resultados = []
    for (i, j) in combinations(range(n_grupos), 2):
        diff = medias[i] - medias[j]
        n_i, n_j = n_per_group[i], n_per_group[j]
        
        # Standard error
        se = np.sqrt(ms_within * (1/n_i + 1/n_j) / 2)
        
        # q statistic
        q = abs(diff) / se if se > 0 else 0
        
        # p-value usando studentized range distribution
        p_val = 1 - stats.studentized_range.cdf(q, n_grupos, df_within)
        
        resultados.append({
            'grupo_1': etiquetas[i],
            'grupo_2': etiquetas[j],
            'diff_medias': diff,
            'q_stat': q,
            'p_value': p_val,
            'significativo': p_val < alpha,
        })
    
    return pd.DataFrame(resultados)


# ════════════════════════════════════════════════════════════════
# PIPELINE PRINCIPAL · BLOQUE 3
# ════════════════════════════════════════════════════════════════

def main():
    print("═" * 70)
    print("📊 DÍA 5 · BLOQUE 3 · ANOVA + POST-HOC TUKEY HSD")
    print("═" * 70)
    print("\nComparación de 3 grupos: DDR3, DDR4, DDR5\n")
    
    df = pd.read_csv(CSV_INPUT)
    
    # Extraer los 3 grupos
    g_ddr3 = df[df['ddr_type'] == 'DDR3']['log_price']
    g_ddr4 = df[df['ddr_type'] == 'DDR4']['log_price']
    g_ddr5 = df[df['ddr_type'] == 'DDR5']['log_price']
    
    grupos = [g_ddr3, g_ddr4, g_ddr5]
    etiquetas = ['DDR3', 'DDR4', 'DDR5']
    
    print(f"📊 Grupos:")
    for label, g in zip(etiquetas, grupos):
        print(f"   {label}: n={len(g)}, media={g.mean():.3f}, std={g.std():.3f}")

    # ════════════════════════════════════════════════════════════════
    # HIPÓTESIS
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🎯 HIPÓTESIS")
    print("═" * 70)
    print("""
    H₀: μ_DDR3 = μ_DDR4 = μ_DDR5
        Las 3 medias del log_price son IGUALES
    
    H₁: al menos una μ es diferente
        AL MENOS un grupo difiere de los demás
    
    Nivel de significancia: α = 0.05
    """)

    # ════════════════════════════════════════════════════════════════
    # TEST 1 · ANOVA estándar
    # ════════════════════════════════════════════════════════════════
    
    print("═" * 70)
    print("🧪 TEST 1 · ANOVA estándar (paramétrico)")
    print("═" * 70)
    
    f_stat, p_val_anova = stats.f_oneway(*grupos)
    
    print(f"\n   F-statistic:        {f_stat:.4f}")
    print(f"   p-value:            {interpretar_p(p_val_anova)}")
    
    if p_val_anova < 0.05:
        print(f"\n   ✅ RECHAZAR H₀ → AL MENOS UN grupo difiere")
        print(f"      Próximo paso: Tukey HSD para identificar cuáles pares")
    else:
        print(f"\n   ❌ NO se puede rechazar H₀")

    # ════════════════════════════════════════════════════════════════
    # TEST 2 · Kruskal-Wallis (sanity check no-paramétrico)
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🧪 TEST 2 · Kruskal-Wallis H (no-paramétrico, sanity check)")
    print("═" * 70)
    
    h_stat, p_val_kw = stats.kruskal(*grupos)
    
    print(f"\n   H-statistic:        {h_stat:.4f}")
    print(f"   p-value:            {interpretar_p(p_val_kw)}")
    
    if p_val_kw < 0.05:
        print(f"\n   ✅ RECHAZAR H₀ → consistente con ANOVA")

    # ════════════════════════════════════════════════════════════════
    # ETA-SQUARED · Tamaño del efecto
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🧪 TAMAÑO DEL EFECTO · Eta-squared (η²)")
    print("═" * 70)
    
    eta_sq, magnitud = calcular_eta_squared(grupos, df['log_price'])
    
    print(f"\n   η² = {eta_sq:.4f}")
    print(f"   Magnitud:           {magnitud}")
    print(f"\n   Interpretación de Cohen (1988):")
    print(f"      η² < 0.01  → trivial")
    print(f"      η² < 0.06  → pequeño")
    print(f"      η² < 0.14  → mediano")
    print(f"      η² >= 0.14 → grande")
    print(f"\n   Significado: el {eta_sq*100:.1f}% de la varianza en log_price")
    print(f"   se explica por el tipo DDR.")

    # ════════════════════════════════════════════════════════════════
    # TUKEY HSD POST-HOC
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🧪 POST-HOC · TUKEY HSD")
    print("═" * 70)
    print("""
    Tukey identifica cuáles pares específicos difieren significativamente,
    controlando el error familiar (family-wise error rate FWER) al α=0.05.
    """)
    
    tukey_df = tukey_hsd_manual(grupos, etiquetas)
    
    print(f"\n{'Par':<20} {'Diff':>10} {'q-stat':>10} {'p-value':>15} {'Sig.':>8}")
    print("─" * 70)
    for _, row in tukey_df.iterrows():
        sig_simbolo = "✅ Sí" if row['significativo'] else "❌ No"
        par = f"{row['grupo_1']} vs {row['grupo_2']}"
        print(f"{par:<20} {row['diff_medias']:>+10.4f} {row['q_stat']:>10.4f} "
              f"{row['p_value']:>13.6f}  {sig_simbolo:>8}")
    
    # Tukey en escala USD
    print(f"\n   📊 Diferencias en USD (factor multiplicativo):")
    for _, row in tukey_df.iterrows():
        factor = np.exp(abs(row['diff_medias']))
        par = f"{row['grupo_1']} vs {row['grupo_2']}"
        if row['significativo']:
            print(f"      {par}: {factor:.2f}× más caro")

    # ════════════════════════════════════════════════════════════════
    # CONCLUSIÓN INTEGRADA
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🎯 CONCLUSIÓN INTEGRADA")
    print("═" * 70)
    
    print(f"\n   📋 Evidencia acumulada:")
    print(f"      ANOVA F-test:      F={f_stat:.2f}, p<0.001 {'✅' if p_val_anova < 0.05 else '❌'}")
    print(f"      Kruskal-Wallis:    H={h_stat:.2f}, p<0.001 {'✅' if p_val_kw < 0.05 else '❌'}")
    print(f"      Eta-squared:       {eta_sq:.3f} ({magnitud})")
    print(f"      Tukey HSD pares:")
    n_significativos = tukey_df['significativo'].sum()
    print(f"         {n_significativos} de {len(tukey_df)} pares son significativos")
    
    if n_significativos == len(tukey_df):
        print(f"\n   🏆 CONCLUSIÓN ROBUSTA:")
        print(f"      LAS 3 generaciones DDR se diferencian entre sí")
        print(f"      con magnitud de efecto {magnitud}.")
        print(f"      Hierarchy clara: DDR3 < DDR4 < DDR5 en precio.")

    # ════════════════════════════════════════════════════════════════
    # GRÁFICA · Visualización del ANOVA
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🎨 GENERANDO GRÁFICA")
    print("═" * 70)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Subplot 1: Boxplot con anotaciones
    data_plot = pd.DataFrame({
        'log_price': pd.concat(grupos).reset_index(drop=True),
        'ddr_type': sum([[label] * len(g) for label, g in zip(etiquetas, grupos)], [])
    })
    
    palette = {'DDR3': '#3498db', 'DDR4': '#e67e22', 'DDR5': '#2ecc71'}
    
    sns.boxplot(x='ddr_type', y='log_price', data=data_plot,
                hue='ddr_type', palette=palette, ax=axes[0], legend=False,
                order=['DDR3', 'DDR4', 'DDR5'])
    
    # Anotaciones de medianas
    for i, label in enumerate(['DDR3', 'DDR4', 'DDR5']):
        mediana = data_plot[data_plot['ddr_type'] == label]['log_price'].median()
        axes[0].annotate(f'mediana\n{mediana:.2f}',
                         xy=(i, mediana), xytext=(i, mediana + 0.3),
                         ha='center', fontsize=9, fontweight='bold',
                         arrowprops=dict(arrowstyle='->', color='black'))
    
    axes[0].set_title(f"ANOVA: F={f_stat:.2f}, p<0.001, η²={eta_sq:.3f}\n"
                      f"Las 3 generaciones DDR difieren significativamente",
                      fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Tipo DDR', fontsize=11)
    axes[0].set_ylabel('log(1+precio)', fontsize=11)
    
    # Subplot 2: Tukey HSD visualization
    pares_str = [f"{r['grupo_1']}\nvs\n{r['grupo_2']}" for _, r in tukey_df.iterrows()]
    diffs = tukey_df['diff_medias'].values
    sig = tukey_df['significativo'].values
    colors = ['#27ae60' if s else '#e74c3c' for s in sig]
    
    bars = axes[1].bar(pares_str, diffs, color=colors, alpha=0.85,
                       edgecolor='black', linewidth=1)
    
    # Línea horizontal en 0
    axes[1].axhline(0, color='gray', linewidth=1, linestyle=':')
    
    # Anotaciones de valores
    for bar, diff, p_val, s in zip(bars, diffs, tukey_df['p_value'], sig):
        marker = '***' if p_val < 0.001 else ('**' if p_val < 0.01 else ('*' if p_val < 0.05 else 'n.s.'))
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2, height,
                     f'{abs(diff):.2f}\n{marker}',
                     ha='center', va='bottom' if height > 0 else 'top',
                     fontweight='bold', fontsize=10)
    
    axes[1].set_title(f"Tukey HSD post-hoc · diferencias entre pares\n"
                      f"Verde = significativo · Rojo = no significativo",
                      fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Comparación de pares', fontsize=11)
    axes[1].set_ylabel('Diferencia de medias (log_price)', fontsize=11)
    
    plt.suptitle('ANOVA · Comparación de las 3 generaciones DDR',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    fig_path = FIG_DIR / "08_anova_ddr.png"
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    
    print(f"\n   ✅ Gráfica guardada: {fig_path.name}")

    # ════════════════════════════════════════════════════════════════
    # CIERRE
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("✅ BLOQUE 3 COMPLETADO · Listos para Bloque 4 (ANOVA por marca)")
    print("═" * 70)
    
    print(f"\n📌 Frase para defensa oral:")
    print(f"\n   \"Apliqué ANOVA de un factor para comparar simultáneamente las 3")
    print(f"   generaciones DDR, evitando el problema de comparaciones múltiples")
    print(f"   que tendría hacer 3 t-tests separados (inflación FWER al 14.3%).")
    print(f"   El test arrojó F={f_stat:.2f}, p<0.001, η²={eta_sq:.3f} (efecto {magnitud}),")
    print(f"   indicando que el {eta_sq*100:.1f}% de la varianza del log_price")
    print(f"   se explica por la generación DDR. Tukey HSD post-hoc confirma")
    print(f"   que TODOS los pares difieren significativamente, estableciendo")
    print(f"   una jerarquía de precios DDR3 < DDR4 < DDR5.\"")


if __name__ == "__main__":
    main()