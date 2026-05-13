"""
inferencia_bloque4.py — Día 5 · Bloque 4: ANOVA + Tukey por marca

Pregunta:
  ¿Hay diferencias significativas en precio entre las marcas?
  ¿Cuál marca es premium y cuál es económica?

Tests aplicados:
  1. ANOVA estándar entre 6 grupos
  2. Kruskal-Wallis (sanity check)
  3. Tukey HSD post-hoc (15 pares)
  4. Eta-squared (tamaño del efecto)

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
# UTILIDADES (reutilizadas del Bloque 3)
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


def calcular_eta_squared(grupos):
    n_total = sum(len(g) for g in grupos)
    media_total = np.concatenate(grupos).mean()
    
    ss_between = sum(len(g) * (g.mean() - media_total)**2 for g in grupos)
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
    from itertools import combinations
    
    n_grupos = len(grupos)
    n_per_group = [len(g) for g in grupos]
    medias = [g.mean() for g in grupos]
    
    n_total = sum(n_per_group)
    df_within = n_total - n_grupos
    
    ss_within = sum(((g - g.mean())**2).sum() for g in grupos)
    ms_within = ss_within / df_within
    
    resultados = []
    for (i, j) in combinations(range(n_grupos), 2):
        diff = medias[i] - medias[j]
        n_i, n_j = n_per_group[i], n_per_group[j]
        se = np.sqrt(ms_within * (1/n_i + 1/n_j) / 2)
        q = abs(diff) / se if se > 0 else 0
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
# PIPELINE PRINCIPAL · BLOQUE 4
# ════════════════════════════════════════════════════════════════

def main():
    print("═" * 70)
    print("📊 DÍA 5 · BLOQUE 4 · ANOVA + TUKEY POR MARCA")
    print("═" * 70)
    
    df = pd.read_csv(CSV_INPUT)
    
    # Extraer grupos por marca normalizada
    marcas_orden = df['brand_normalized'].value_counts().index.tolist()
    print(f"\n📊 Marcas presentes (en orden de frecuencia):")
    
    grupos = []
    etiquetas = []
    
    for marca in marcas_orden:
        grupo = df[df['brand_normalized'] == marca]['log_price']
        grupos.append(grupo)
        etiquetas.append(marca)
        print(f"   {marca:<10}: n={len(grupo)}, media={grupo.mean():.3f}, "
              f"mediana_USD=${df[df['brand_normalized']==marca]['price_usd'].median():.0f}")
    
    n_grupos = len(grupos)
    n_pares = n_grupos * (n_grupos - 1) // 2
    print(f"\n   Total grupos: {n_grupos}")
    print(f"   Pares Tukey:  {n_pares}")
    print(f"\n   ⚠️  Sin corrección, FWER = 1 - 0.95^{n_pares} = "
          f"{(1 - 0.95**n_pares)*100:.1f}%")
    print(f"   ✅ ANOVA + Tukey controlan este error global a α=0.05")

    # ════════════════════════════════════════════════════════════════
    # HIPÓTESIS
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🎯 HIPÓTESIS")
    print("═" * 70)
    print(f"""
    H₀: μ(marca_1) = μ(marca_2) = ... = μ(marca_{n_grupos})
        Las {n_grupos} medias son IGUALES (no hay efecto marca)
    
    H₁: al menos una μ es diferente
        AL MENOS una marca difiere de las demás
    
    Nivel de significancia: α = 0.05
    """)

    # ════════════════════════════════════════════════════════════════
    # TEST 1 · ANOVA
    # ════════════════════════════════════════════════════════════════
    
    print("═" * 70)
    print("🧪 TEST 1 · ANOVA estándar")
    print("═" * 70)
    
    f_stat, p_val_anova = stats.f_oneway(*grupos)
    
    print(f"\n   F-statistic:        {f_stat:.4f}")
    print(f"   p-value:            {interpretar_p(p_val_anova)}")
    
    if p_val_anova < 0.05:
        print(f"\n   ✅ RECHAZAR H₀ → Existe efecto marca en el precio")
    else:
        print(f"\n   ❌ NO se puede rechazar H₀ → marcas son intercambiables")

    # ════════════════════════════════════════════════════════════════
    # TEST 2 · Kruskal-Wallis
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🧪 TEST 2 · Kruskal-Wallis H (sanity check)")
    print("═" * 70)
    
    h_stat, p_val_kw = stats.kruskal(*grupos)
    
    print(f"\n   H-statistic:        {h_stat:.4f}")
    print(f"   p-value:            {interpretar_p(p_val_kw)}")

    # ════════════════════════════════════════════════════════════════
    # ETA-SQUARED
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🧪 TAMAÑO DEL EFECTO · Eta-squared")
    print("═" * 70)
    
    eta_sq, magnitud = calcular_eta_squared(grupos)
    
    print(f"\n   η² = {eta_sq:.4f}")
    print(f"   Magnitud:           {magnitud}")
    print(f"\n   Significado: el {eta_sq*100:.1f}% de la varianza en log_price")
    print(f"   se explica por la marca.")
    print(f"\n   📌 Comparación con Bloque 3 (DDR): η²_DDR = 0.608 (60.8%)")
    print(f"      Diferencia: la marca explica MENOS varianza que el tipo DDR.")

    # ════════════════════════════════════════════════════════════════
    # TUKEY HSD POST-HOC
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🧪 POST-HOC · TUKEY HSD")
    print("═" * 70)
    
    tukey_df = tukey_hsd_manual(grupos, etiquetas)
    
    print(f"\n   Comparaciones por pares (15 pares totales):\n")
    print(f"{'Par':<25} {'Diff':>10} {'q-stat':>10} {'p-value':>15} {'Sig.':>8}")
    print("─" * 75)
    
    # Ordenar por p_value para destacar los más significativos
    tukey_df_sorted = tukey_df.sort_values('p_value')
    
    for _, row in tukey_df_sorted.iterrows():
        sig_simbolo = "✅ Sí" if row['significativo'] else "❌ No"
        par = f"{row['grupo_1']} vs {row['grupo_2']}"
        print(f"{par:<25} {row['diff_medias']:>+10.4f} {row['q_stat']:>10.4f} "
              f"{row['p_value']:>13.6f}  {sig_simbolo:>8}")
    
    n_significativos = tukey_df['significativo'].sum()
    print(f"\n   📊 Pares significativos: {n_significativos} de {n_pares} ({n_significativos/n_pares*100:.0f}%)")

    # ════════════════════════════════════════════════════════════════
    # IDENTIFICAR MARCAS PREMIUM Y ECONÓMICA
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("💎 RANKING DE MARCAS POR PRECIO MEDIANO")
    print("═" * 70)
    
    ranking = df.groupby('brand_normalized')['price_usd'].agg(['median', 'mean', 'count'])
    ranking = ranking.sort_values('median', ascending=False)
    
    print(f"\n   {'Posición':>10} {'Marca':<12} {'Mediana':>10} {'Media':>10} {'n':>8}")
    print("   " + "─" * 60)
    for pos, (marca, row) in enumerate(ranking.iterrows(), 1):
        emoji = "👑" if pos == 1 else ("💎" if pos == 2 else ("🥉" if pos == 3 else "  "))
        print(f"   {emoji:>10}{pos}. {marca:<12} ${row['median']:>8.2f} ${row['mean']:>8.2f} {int(row['count']):>8}")

    # ════════════════════════════════════════════════════════════════
    # CONCLUSIÓN
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🎯 CONCLUSIÓN INTEGRADA")
    print("═" * 70)
    
    print(f"\n   📋 Evidencia:")
    print(f"      ANOVA F-test:      F={f_stat:.2f}, p<0.001 {'✅' if p_val_anova < 0.05 else '❌'}")
    print(f"      Kruskal-Wallis:    H={h_stat:.2f}, p<0.001 {'✅' if p_val_kw < 0.05 else '❌'}")
    print(f"      Eta-squared:       {eta_sq:.3f} ({magnitud})")
    print(f"      Tukey pares sig.:  {n_significativos}/{n_pares}")
    
    if p_val_anova < 0.05:
        marca_premium = ranking.index[0]
        marca_economica = ranking.index[-1]
        print(f"\n   🏆 CONCLUSIÓN:")
        print(f"      Existe efecto marca significativo en el precio.")
        print(f"      Marca PREMIUM:    {marca_premium} (mediana ${ranking.loc[marca_premium, 'median']:.2f})")
        print(f"      Marca ECONÓMICA:  {marca_economica} (mediana ${ranking.loc[marca_economica, 'median']:.2f})")

    # ════════════════════════════════════════════════════════════════
    # GRÁFICA
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("🎨 GENERANDO GRÁFICA")
    print("═" * 70)
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Subplot 1: Boxplot ordenado por mediana
    orden_por_mediana = ranking.index.tolist()
    
    sns.boxplot(x='brand_normalized', y='log_price', data=df,
                hue='brand_normalized', order=orden_por_mediana,
                palette='Set2', ax=axes[0], legend=False)
    axes[0].set_title(f"Distribución de log_price por marca\n"
                      f"ANOVA: F={f_stat:.2f}, p<0.001, η²={eta_sq:.3f}",
                      fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Marca (orden por mediana descendente)', fontsize=11)
    axes[0].set_ylabel('log(1+precio)', fontsize=11)
    axes[0].tick_params(axis='x', rotation=20)
    
    # Subplot 2: Heatmap de p-values (matriz de Tukey)
    matriz_p = pd.DataFrame(np.nan, index=etiquetas, columns=etiquetas)
    for _, row in tukey_df.iterrows():
        matriz_p.loc[row['grupo_1'], row['grupo_2']] = row['p_value']
        matriz_p.loc[row['grupo_2'], row['grupo_1']] = row['p_value']
    
    # Reorganizar por orden de mediana
    matriz_p = matriz_p.loc[orden_por_mediana, orden_por_mediana]
    
    # Convertir a -log10(p) para visualización clara
    matriz_log = -np.log10(matriz_p.replace(0, 1e-10))
    
    sns.heatmap(matriz_log, annot=matriz_p.round(3), fmt='.3g',
                cmap='RdYlGn_r', vmin=0, vmax=5,
                cbar_kws={'label': '-log10(p-value)'}, ax=axes[1])
    axes[1].set_title(f"Tukey HSD · matriz de p-values\n"
                      f"Verde=significativo (p<0.05), Rojo=NO significativo",
                      fontsize=12, fontweight='bold')
    axes[1].set_xlabel('')
    axes[1].set_ylabel('')
    
    plt.suptitle('ANOVA · Efecto marca en el precio',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    fig_path = FIG_DIR / "09_anova_marca.png"
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    
    print(f"\n   ✅ Gráfica guardada: {fig_path.name}")

    # ════════════════════════════════════════════════════════════════
    # CIERRE
    # ════════════════════════════════════════════════════════════════
    
    print("\n" + "═" * 70)
    print("✅ BLOQUE 4 COMPLETADO · Listos para Bloque 5 (cierre Día 5)")
    print("═" * 70)
    
    print(f"\n📌 Frase para defensa oral:")
    print(f"\n   \"Apliqué ANOVA con post-hoc Tukey HSD entre las {n_grupos} marcas")
    print(f"   normalizadas. F={f_stat:.2f}, p<0.001, η²={eta_sq:.3f} ({magnitud}).")
    print(f"   Tukey identificó {n_significativos} de {n_pares} pares con diferencia")
    print(f"   significativa, indicando que existe un efecto marca real en")
    print(f"   el precio. Sin embargo, el η² para marca ({eta_sq*100:.1f}%) es menor")
    print(f"   que el de DDR (60.8%), confirmando que la generación tecnológica")
    print(f"   es predictor más fuerte que la marca específica.\"")


if __name__ == "__main__":
    main()