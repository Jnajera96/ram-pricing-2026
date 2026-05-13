"""
inferencia.py — Día 5 · Bloque 1: Validación de supuestos paramétricos

Antes de aplicar tests t y ANOVA, validamos:
  1. Normalidad dentro de cada grupo (Shapiro-Wilk + QQ-plots)
  2. Homocedasticidad entre grupos (Levene's test)
  3. Estadísticas descriptivas comparativas

El resultado guía la elección del test inferencial apropiado:
  · Si supuestos OK    → Student's t-test, ANOVA paramétrico
  · Si rechaza normalidad → Mann-Whitney U, Kruskal-Wallis
  · Si rechaza homocedasticidad → Welch's t-test (robusto)

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
FIG_DIR.mkdir(exist_ok=True)

CSV_INPUT = DATA_DIR / "ram_clean.csv"

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300


# ════════════════════════════════════════════════════════════════
# UTILIDADES
# ════════════════════════════════════════════════════════════════

def interpretar_p(p_value: float, alpha: float = 0.05) -> str:
    """Interpreta un p-value en lenguaje claro."""
    if p_value < 0.001:
        return f"p={p_value:.4f} (***) altamente significativo"
    elif p_value < 0.01:
        return f"p={p_value:.4f} (**) muy significativo"
    elif p_value < alpha:
        return f"p={p_value:.4f} (*) significativo"
    else:
        return f"p={p_value:.4f} (n.s.) NO significativo"


def shapiro_test(serie: pd.Series, etiqueta: str) -> dict:
    """
    Shapiro-Wilk test de normalidad.
    H₀: los datos provienen de distribución normal
    Si p < 0.05 → rechazar H₀ → datos NO normales
    """
    if len(serie) < 3:
        return {"label": etiqueta, "n": len(serie), "p_value": None,
                "es_normal": None, "warning": "muestra muy pequeña (n<3)"}
    
    # Shapiro-Wilk requiere muestra <= 5000
    sample = serie.sample(min(len(serie), 5000), random_state=42) if len(serie) > 5000 else serie
    stat, p_value = stats.shapiro(sample)
    
    return {
        "label": etiqueta,
        "n": len(serie),
        "stat": stat,
        "p_value": p_value,
        "es_normal": p_value >= 0.05,
        "interpretacion": interpretar_p(p_value),
    }


def levene_test(grupos: list, etiquetas: list) -> dict:
    """
    Levene's test de homocedasticidad.
    H₀: las varianzas de los grupos son iguales
    Si p < 0.05 → rechazar H₀ → varianzas distintas → usar Welch's t
    """
    stat, p_value = stats.levene(*grupos)
    return {
        "grupos": etiquetas,
        "stat": stat,
        "p_value": p_value,
        "varianzas_iguales": p_value >= 0.05,
        "interpretacion": interpretar_p(p_value),
    }


# ════════════════════════════════════════════════════════════════
# PIPELINE PRINCIPAL · BLOQUE 1
# ════════════════════════════════════════════════════════════════

def main():
    print("═" * 70)
    print("📊 DÍA 5 · BLOQUE 1 · VALIDACIÓN DE SUPUESTOS PARAMÉTRICOS")
    print("═" * 70)

    # 1. Cargar dataset
    if not CSV_INPUT.exists():
        print(f"❌ No encontré {CSV_INPUT}")
        return
    
    df = pd.read_csv(CSV_INPUT)
    print(f"\n📂 Dataset cargado: {len(df)} filas\n")

    # ════════════════════════════════════════════════════════════════
    # PARTE A · ESTADÍSTICAS DESCRIPTIVAS POR GRUPO
    # ════════════════════════════════════════════════════════════════
    
    print("═" * 70)
    print("📈 PARTE A · DESCRIPTIVAS POR GRUPO DDR (sobre log_price)")
    print("═" * 70)
    
    # Agrupar por DDR y reportar
    desc_ddr = df.groupby('ddr_type')['log_price'].agg([
        ('n', 'count'),
        ('media', 'mean'),
        ('mediana', 'median'),
        ('std', 'std'),
        ('min', 'min'),
        ('max', 'max'),
    ]).round(3)
    print(f"\n{desc_ddr.to_string()}")
    
    # También en escala USD para tener referencia
    print(f"\n📊 Equivalencia en USD (mediana por grupo):")
    medianas_usd = df.groupby('ddr_type')['price_usd'].median().round(2)
    for ddr, mediana in medianas_usd.items():
        print(f"   {ddr}: ${mediana:,.2f}")

    # ════════════════════════════════════════════════════════════════
    # PARTE B · TEST DE NORMALIDAD POR GRUPO (SHAPIRO-WILK)
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🔍 PARTE B · TEST DE NORMALIDAD (Shapiro-Wilk)")
    print("═" * 70)
    print("""
    H₀: la distribución es normal
    H₁: la distribución NO es normal
    Nivel de significancia: α = 0.05
    
    Si p < 0.05 → rechazar H₀ → datos NO son normales
    Si p ≥ 0.05 → no rechazar H₀ → asumir normalidad
    """)
    
    shapiro_results = []
    for ddr in ['DDR3', 'DDR4', 'DDR5']:
        grupo = df[df['ddr_type'] == ddr]['log_price']
        result = shapiro_test(grupo, f"log_price · {ddr}")
        shapiro_results.append(result)
        
        print(f"\n  📋 {result['label']} (n={result['n']})")
        if result.get('warning'):
            print(f"      ⚠️  {result['warning']}")
        else:
            print(f"      Statistic: {result['stat']:.4f}")
            print(f"      {result['interpretacion']}")
            simbolo = "✅" if result['es_normal'] else "❌"
            estado = "ASUMIR normalidad" if result['es_normal'] else "RECHAZAR normalidad"
            print(f"      {simbolo} {estado}")

    # ════════════════════════════════════════════════════════════════
    # PARTE C · TEST DE HOMOCEDASTICIDAD (LEVENE)
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🔍 PARTE C · TEST DE HOMOCEDASTICIDAD (Levene)")
    print("═" * 70)
    print("""
    H₀: las varianzas de los grupos son iguales (homocedasticidad)
    H₁: al menos una varianza es diferente (heterocedasticidad)
    
    Si p < 0.05 → rechazar H₀ → varianzas distintas → usar Welch's t-test
    """)
    
    # Levene entre los 3 grupos DDR
    grupos_ddr = [df[df['ddr_type'] == ddr]['log_price'].values for ddr in ['DDR3', 'DDR4', 'DDR5']]
    levene_ddr = levene_test(grupos_ddr, ['DDR3', 'DDR4', 'DDR5'])
    
    print(f"\n  📋 Test entre DDR3, DDR4, DDR5:")
    print(f"      Statistic: {levene_ddr['stat']:.4f}")
    print(f"      {levene_ddr['interpretacion']}")
    simbolo = "✅" if levene_ddr['varianzas_iguales'] else "❌"
    estado = "varianzas iguales" if levene_ddr['varianzas_iguales'] else "varianzas DISTINTAS → usar Welch's t"
    print(f"      {simbolo} {estado}")

    # ════════════════════════════════════════════════════════════════
    # PARTE D · QQ-PLOTS · validación VISUAL
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🎨 PARTE D · GENERANDO QQ-PLOTS Y HISTOGRAMAS")
    print("═" * 70)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    
    for idx, ddr in enumerate(['DDR3', 'DDR4', 'DDR5']):
        grupo = df[df['ddr_type'] == ddr]['log_price'].dropna()
        
        # Fila 1: histogramas con curva normal teórica
        ax_hist = axes[0, idx]
        ax_hist.hist(grupo, bins=15, density=True, alpha=0.7, 
                     color=['#3498db', '#e67e22', '#2ecc71'][idx],
                     edgecolor='black')
        
        # Curva normal teórica
        mu, sigma = grupo.mean(), grupo.std()
        x = np.linspace(grupo.min(), grupo.max(), 100)
        ax_hist.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', linewidth=2, 
                     label='Normal teórica')
        ax_hist.set_title(f'{ddr} · log_price (n={len(grupo)})', fontweight='bold')
        ax_hist.set_xlabel('log(1+precio)')
        ax_hist.set_ylabel('Densidad')
        ax_hist.legend(fontsize=8)
        
        # Fila 2: QQ-plots
        ax_qq = axes[1, idx]
        stats.probplot(grupo, dist="norm", plot=ax_qq)
        
        p_val = shapiro_results[idx].get('p_value', None)
        if p_val is not None:
            interpretacion = "✅ Normal" if p_val >= 0.05 else "❌ No normal"
            ax_qq.set_title(f'{ddr} QQ-plot · {interpretacion} (p={p_val:.4f})',
                           fontweight='bold')
        ax_qq.get_lines()[0].set_markerfacecolor(['#3498db', '#e67e22', '#2ecc71'][idx])
        ax_qq.get_lines()[0].set_markeredgecolor('black')
        ax_qq.get_lines()[0].set_markersize(6)
    
    plt.suptitle('Validación de normalidad por grupo DDR\nHistogramas (curva normal teórica) + QQ-plots',
                 fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    fig_path = FIG_DIR / "06_normality_check.png"
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    
    print(f"\n  ✅ Gráfica guardada: {fig_path.name}")

    # ════════════════════════════════════════════════════════════════
    # RESUMEN Y MAPA DE DECISIONES
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("📋 RESUMEN Y MAPA DE DECISIONES PARA BLOQUES 2-4")
    print("═" * 70)
    
    print("\n  🔍 Hallazgos:")
    for r in shapiro_results:
        if r.get('p_value') is not None:
            estado = "✅ Normal" if r['es_normal'] else "❌ No normal"
            print(f"     · {r['label']:<25} {estado:<15} (p={r['p_value']:.4f})")
        else:
            print(f"     · {r['label']:<25} ⚠️  {r.get('warning', 'datos insuficientes')}")
    
    print(f"\n     · Homocedasticidad (Levene): "
          f"{'✅ Iguales' if levene_ddr['varianzas_iguales'] else '❌ Diferentes'} "
          f"(p={levene_ddr['p_value']:.4f})")
    
    print("\n  🎯 Decisiones para los siguientes bloques:")
    
    # Decisión sobre test t (DDR4 vs DDR5)
    ddr4_normal = shapiro_results[1].get('es_normal', False)
    ddr5_normal = shapiro_results[2].get('es_normal', False)
    
    if ddr4_normal and ddr5_normal:
        if levene_ddr['varianzas_iguales']:
            print(f"     ✅ Bloque 2 (DDR4 vs DDR5): Student's t-test (paramétrico)")
        else:
            print(f"     ⚠️  Bloque 2 (DDR4 vs DDR5): Welch's t-test (robusto a varianzas distintas)")
    else:
        print(f"     ⚠️  Bloque 2 (DDR4 vs DDR5): Welch's t-test (robusto, justificado por TCL n>30)")
        print(f"          ALTERNATIVA: Mann-Whitney U test (no-paramétrico) como sanity check")
    
    # Decisión sobre ANOVA
    todos_normales = all(r.get('es_normal', False) for r in shapiro_results 
                         if r.get('p_value') is not None)
    
    if todos_normales and levene_ddr['varianzas_iguales']:
        print(f"     ✅ Bloque 3 (ANOVA por DDR): ANOVA estándar")
    else:
        print(f"     ⚠️  Bloque 3 (ANOVA por DDR): ANOVA estándar + verificación con Kruskal-Wallis")
    
    print("\n" + "═" * 70)
    print("✅ BLOQUE 1 COMPLETADO. Listos para el Bloque 2 (test t DDR4 vs DDR5)")
    print("═" * 70)
    
    print("\n📌 Para tu cuaderno de defensa:")
    print("   · Validé supuestos paramétricos antes de aplicar tests")
    print("   · Shapiro-Wilk es ultra-sensible con n grande (>100)")
    print("   · Por TCL, la distribución de la MEDIA es ~normal aunque los datos no lo sean")
    print("   · Welch's t-test es robusto ante violaciones moderadas")


if __name__ == "__main__":
    main()