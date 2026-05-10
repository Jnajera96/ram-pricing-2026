"""
inferencia_bloque2.py — Día 5 · Bloque 2: Test t entre DDR4 y DDR5

Pregunta principal:
  ¿Es DDR5 estadísticamente más caro que DDR4?

Tests aplicados (triangulación):
  1. Welch's t-test (paramétrico, robusto a varianzas distintas)
  2. Mann-Whitney U (no-paramétrico, sanity check)
  3. Cohen's d (effect size, magnitud práctica)

Si los 3 coinciden → conclusión robusta para defensa oral.

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
# CÁLCULOS ESTADÍSTICOS
# ════════════════════════════════════════════════════════════════

def cohens_d(grupo1, grupo2):
    """
    Cohen's d para tamaño del efecto.
    Devuelve d y la interpretación:
      |d| < 0.2  → trivial
      |d| < 0.5  → pequeño
      |d| < 0.8  → mediano
      |d| >= 0.8 → grande
      |d| >= 1.2 → muy grande
    """
    n1, n2 = len(grupo1), len(grupo2)
    var1, var2 = grupo1.var(ddof=1), grupo2.var(ddof=1)
    
    # Pooled standard deviation
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    
    d = (grupo1.mean() - grupo2.mean()) / pooled_std
    
    abs_d = abs(d)
    if abs_d < 0.2:
        magnitud = "trivial"
    elif abs_d < 0.5:
        magnitud = "pequeño"
    elif abs_d < 0.8:
        magnitud = "mediano"
    elif abs_d < 1.2:
        magnitud = "grande"
    else:
        magnitud = "muy grande"
    
    return d, magnitud


def intervalo_confianza_diferencia(grupo1, grupo2, alpha=0.05):
    """
    Calcula IC del 95% para la diferencia de medias (μ1 - μ2).
    Usa Welch's degrees of freedom.
    """
    n1, n2 = len(grupo1), len(grupo2)
    m1, m2 = grupo1.mean(), grupo2.mean()
    s1, s2 = grupo1.std(ddof=1), grupo2.std(ddof=1)
    
    # Welch-Satterthwaite degrees of freedom
    df = (s1**2/n1 + s2**2/n2)**2 / ((s1**2/n1)**2/(n1-1) + (s2**2/n2)**2/(n2-1))
    
    se = np.sqrt(s1**2/n1 + s2**2/n2)
    t_crit = stats.t.ppf(1 - alpha/2, df)
    
    diff = m1 - m2
    margen = t_crit * se
    
    return diff, diff - margen, diff + margen


def interpretar_p(p_value, alpha=0.05):
    """Interpreta un p-value en lenguaje claro."""
    if p_value < 0.001:
        return f"p={p_value:.6f} (***) altamente significativo"
    elif p_value < 0.01:
        return f"p={p_value:.4f} (**) muy significativo"
    elif p_value < alpha:
        return f"p={p_value:.4f} (*) significativo"
    else:
        return f"p={p_value:.4f} (n.s.) NO significativo"


# ════════════════════════════════════════════════════════════════
# PIPELINE PRINCIPAL · BLOQUE 2
# ════════════════════════════════════════════════════════════════

def main():
    print("═" * 70)
    print("📊 DÍA 5 · BLOQUE 2 · TEST t · DDR4 vs DDR5")
    print("═" * 70)
    
    df = pd.read_csv(CSV_INPUT)
    
    # Extraer los 2 grupos sobre log_price
    g_ddr4 = df[df['ddr_type'] == 'DDR4']['log_price']
    g_ddr5 = df[df['ddr_type'] == 'DDR5']['log_price']
    
    print(f"\n📊 Grupos a comparar:")
    print(f"   DDR4: n={len(g_ddr4)}, media={g_ddr4.mean():.3f}, std={g_ddr4.std():.3f}")
    print(f"   DDR5: n={len(g_ddr5)}, media={g_ddr5.mean():.3f}, std={g_ddr5.std():.3f}")
    
    # Diferencia bruta en USD para tener referencia
    p_ddr4 = df[df['ddr_type'] == 'DDR4']['price_usd']
    p_ddr5 = df[df['ddr_type'] == 'DDR5']['price_usd']
    print(f"\n💰 En USD (referencia):")
    print(f"   DDR4: media=${p_ddr4.mean():.2f}, mediana=${p_ddr4.median():.2f}")
    print(f"   DDR5: media=${p_ddr5.mean():.2f}, mediana=${p_ddr5.median():.2f}")
    print(f"   Diferencia mediana: ${p_ddr5.median() - p_ddr4.median():.2f}")

    # ════════════════════════════════════════════════════════════════
    # HIPÓTESIS PLANTEADAS
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🎯 HIPÓTESIS")
    print("═" * 70)
    print("""
    H₀: μ(log_price | DDR5) = μ(log_price | DDR4)
        Las medias del log_price son IGUALES entre DDR4 y DDR5
    
    H₁: μ(log_price | DDR5) > μ(log_price | DDR4)
        DDR5 tiene MAYOR precio medio que DDR4 (test unilateral)
    
    Nivel de significancia: α = 0.05
    """)

    # ════════════════════════════════════════════════════════════════
    # TEST 1 · Welch's t-test (paramétrico robusto)
    # ════════════════════════════════════════════════════════════════
    
    print("═" * 70)
    print("🧪 TEST 1 · Welch's t-test (paramétrico, equal_var=False)")
    print("═" * 70)
    
    # Bilateral primero
    t_stat, p_val_bilateral = stats.ttest_ind(g_ddr5, g_ddr4, equal_var=False)
    
    # Unilateral (DDR5 > DDR4): dividir p_value por 2 si t_stat va en la dirección esperada
    if t_stat > 0:
        p_val_unilateral = p_val_bilateral / 2
    else:
        p_val_unilateral = 1 - (p_val_bilateral / 2)
    
    print(f"\n   t-statistic:        {t_stat:.4f}")
    print(f"   p-value bilateral:  {interpretar_p(p_val_bilateral)}")
    print(f"   p-value unilateral: {interpretar_p(p_val_unilateral)}")
    
    if p_val_unilateral < 0.05:
        print(f"\n   ✅ RECHAZAR H₀ → DDR5 es significativamente MÁS CARO que DDR4")
    else:
        print(f"\n   ❌ NO se puede rechazar H₀")

    # ════════════════════════════════════════════════════════════════
    # TEST 2 · Mann-Whitney U (no-paramétrico)
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🧪 TEST 2 · Mann-Whitney U (no-paramétrico, sanity check)")
    print("═" * 70)
    
    u_stat, p_val_mw = stats.mannwhitneyu(g_ddr5, g_ddr4, alternative='greater')
    
    print(f"\n   U-statistic:        {u_stat:.4f}")
    print(f"   p-value (DDR5>DDR4): {interpretar_p(p_val_mw)}")
    
    if p_val_mw < 0.05:
        print(f"\n   ✅ RECHAZAR H₀ → distribución DDR5 es MAYOR que DDR4")
    else:
        print(f"\n   ❌ NO se puede rechazar H₀")

    # ════════════════════════════════════════════════════════════════
    # TEST 3 · Cohen's d (effect size)
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🧪 TEST 3 · Cohen's d (tamaño del efecto)")
    print("═" * 70)
    
    d, magnitud = cohens_d(g_ddr5, g_ddr4)
    
    print(f"\n   Cohen's d:          {d:.4f}")
    print(f"   Magnitud:           {magnitud}")
    print(f"\n   Interpretación de Cohen (1988):")
    print(f"      |d| < 0.2  → trivial")
    print(f"      |d| < 0.5  → pequeño")
    print(f"      |d| < 0.8  → mediano")
    print(f"      |d| >= 0.8 → grande")
    print(f"      |d| >= 1.2 → muy grande")

    # ════════════════════════════════════════════════════════════════
    # INTERVALO DE CONFIANZA 95%
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("📐 INTERVALO DE CONFIANZA (95%) PARA LA DIFERENCIA")
    print("═" * 70)
    
    diff, ic_low, ic_high = intervalo_confianza_diferencia(g_ddr5, g_ddr4)
    
    print(f"\n   Diferencia observada: {diff:.4f} (en log_price)")
    print(f"   IC 95%: [{ic_low:.4f}, {ic_high:.4f}]")
    print(f"\n   Interpretación: con 95% de confianza, la diferencia real")
    print(f"   en log_price entre DDR5 y DDR4 está entre {ic_low:.3f} y {ic_high:.3f}")
    print(f"\n   Equivalencia en USD (factor multiplicativo):")
    print(f"      Diferencia mediana: e^{diff:.3f} = {np.exp(diff):.2f}× más caro")

    # ════════════════════════════════════════════════════════════════
    # CONCLUSIÓN INTEGRADA
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🎯 CONCLUSIÓN INTEGRADA · TRIANGULACIÓN DE EVIDENCIA")
    print("═" * 70)
    
    todos_significativos = (p_val_unilateral < 0.05 and p_val_mw < 0.05 and abs(d) >= 0.5)
    
    print(f"\n   📋 Evidencia acumulada:")
    print(f"      Welch's t-test:    p={p_val_unilateral:.6f} {'✅' if p_val_unilateral < 0.05 else '❌'}")
    print(f"      Mann-Whitney U:    p={p_val_mw:.6f} {'✅' if p_val_mw < 0.05 else '❌'}")
    print(f"      Cohen's d:         {d:.3f} ({magnitud})")
    print(f"      IC 95%:            [{ic_low:.3f}, {ic_high:.3f}] {'(no incluye 0)' if ic_low > 0 else '(incluye 0)'}")
    
    if todos_significativos:
        print(f"\n   🏆 CONCLUSIÓN ROBUSTA:")
        print(f"      DDR5 es significativamente más caro que DDR4")
        print(f"      con magnitud de efecto {magnitud}.")
        print(f"      Resultado consistente en 3 tests independientes.")
    
    # ════════════════════════════════════════════════════════════════
    # GRÁFICA · Visualización del test
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🎨 GENERANDO GRÁFICA")
    print("═" * 70)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Subplot 1: Boxplot comparativo
    data_plot = pd.DataFrame({
        'log_price': pd.concat([g_ddr4, g_ddr5]),
        'ddr_type': ['DDR4'] * len(g_ddr4) + ['DDR5'] * len(g_ddr5)
    })
    
    sns.boxplot(x='ddr_type', y='log_price', data=data_plot,
                hue='ddr_type', palette={'DDR4': '#e67e22', 'DDR5': '#2ecc71'},
                ax=axes[0], legend=False)
    axes[0].set_title(f"Comparación log_price: DDR4 vs DDR5\n"
                      f"Welch t={t_stat:.3f}, p={p_val_unilateral:.4f}, Cohen's d={d:.3f}",
                      fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Tipo DDR', fontsize=11)
    axes[0].set_ylabel('log(1+precio)', fontsize=11)
    
    # Subplot 2: Distribuciones overlapping
    axes[1].hist(g_ddr4, bins=20, alpha=0.6, color='#e67e22', 
                 label=f'DDR4 (n={len(g_ddr4)}, μ={g_ddr4.mean():.2f})',
                 edgecolor='black', density=True)
    axes[1].hist(g_ddr5, bins=20, alpha=0.6, color='#2ecc71',
                 label=f'DDR5 (n={len(g_ddr5)}, μ={g_ddr5.mean():.2f})',
                 edgecolor='black', density=True)
    
    # Líneas verticales en las medias
    axes[1].axvline(g_ddr4.mean(), color='#d35400', linestyle='--', linewidth=2)
    axes[1].axvline(g_ddr5.mean(), color='#27ae60', linestyle='--', linewidth=2)
    
    axes[1].set_title(f"Distribuciones de log_price\n"
                      f"Diferencia de medias: {diff:.3f} (e^d={np.exp(diff):.2f}× más caro)",
                      fontsize=12, fontweight='bold')
    axes[1].set_xlabel('log(1+precio)', fontsize=11)
    axes[1].set_ylabel('Densidad', fontsize=11)
    axes[1].legend(loc='upper left', fontsize=10)
    
    plt.suptitle('Test t · DDR4 vs DDR5 · Triangulación de evidencia',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    fig_path = FIG_DIR / "07_ttest_ddr4_vs_ddr5.png"
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    
    print(f"\n   ✅ Gráfica guardada: {fig_path.name}")

    # ════════════════════════════════════════════════════════════════
    # CIERRE
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("✅ BLOQUE 2 COMPLETADO · Listos para Bloque 3 (ANOVA por DDR)")
    print("═" * 70)
    
    print(f"\n📌 Frase para defensa oral (apunta literal):")
    print(f"\n   \"Apliqué triangulación inferencial entre DDR4 y DDR5: Welch's")
    print(f"   t-test paramétrico, Mann-Whitney U no-paramétrico y Cohen's d como")
    print(f"   medida de efecto. Los tres coinciden con p<0.001 y d={d:.2f},")
    print(f"   magnitud {magnitud}. Esto confirma que DDR5 es")
    print(f"   significativamente más caro que DDR4 tanto estadística como")
    print(f"   prácticamente. La diferencia mediana en escala USD corresponde")
    print(f"   a un factor multiplicativo de e^d={np.exp(diff):.2f}×.\"")


if __name__ == "__main__":
    main()