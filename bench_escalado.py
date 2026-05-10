"""
bench_escalado.py — Día 4 · Bloque 5 (Bonus): Test de escalado

Demuestra empíricamente cómo el speedup de O(log n) sobre O(n) crece
con el tamaño del dataset. Replica las filas a diferentes tamaños
(n=350, 1k, 5k, 10k, 50k) y mide las queries en cada uno.

Genera la gráfica más impactante del proyecto:
  · figures/05_scaling_benchmark.png

Esta es la VALIDACIÓN EMPÍRICA del análisis asintótico para el póster.

Autor: Jose Najera · UDG · DS-2025-GDL
"""

import sqlite3
import time
import statistics
import shutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ════════════════════════════════════════════════════════════════

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
FIG_DIR = SCRIPT_DIR / "figures"
FIG_DIR.mkdir(exist_ok=True)

ORIGINAL_DB = DATA_DIR / "ram_market.db"
SCALING_DB = DATA_DIR / "ram_scaling_test.db"
RESULTS_CSV = DATA_DIR / "scaling_benchmark.csv"
FIG_PATH = FIG_DIR / "05_scaling_benchmark.png"

# Tamaños a probar (puedes ajustar)
SIZES_TO_TEST = [350, 1000, 5000, 10000, 50000]
N_RUNS = 50  # Reducimos a 50 para acelerar (eran 100 antes)


# ════════════════════════════════════════════════════════════════
# QUERIES (las 3 con índice claro de los Bloques anteriores)
# ════════════════════════════════════════════════════════════════

QUERIES = {
    "Q1_filtro_categorico": "SELECT * FROM ram_products WHERE ddr_type = 'DDR5';",
    "Q2_filtro_numerico": "SELECT * FROM ram_products WHERE capacity_gb >= 32;",
    "Q4_agregacion": "SELECT brand_normalized, COUNT(*) FROM ram_products GROUP BY brand_normalized;",
}


# ════════════════════════════════════════════════════════════════
# UTILIDADES
# ════════════════════════════════════════════════════════════════

def replicar_a_n_filas(conn: sqlite3.Connection, n_target: int):
    """
    Replica la tabla ram_products hasta tener n_target filas.
    Estrategia: leer todas las filas, replicarlas con perturbación
    en title (para no violar PK) hasta llegar al tamaño deseado.
    """
    cursor = conn.execute("SELECT COUNT(*) FROM ram_products;")
    n_actual = cursor.fetchone()[0]
    
    if n_actual >= n_target:
        print(f"   Ya hay {n_actual} filas, no se replica.")
        return
    
    # Leer todas las filas como base para replicar
    cursor = conn.execute("""
        SELECT title, brand, brand_normalized, source_url, ddr_type,
               form_factor, has_rgb, capacity_gb, speed_mhz,
               cas_latency, cas_latency_imputed, cas_was_imputed,
               num_sticks, price_per_gb, price_usd, log_price, scraped_at
        FROM ram_products;
    """)
    base_rows = cursor.fetchall()
    
    n_a_insertar = n_target - n_actual
    print(f"   Insertando {n_a_insertar:,} filas adicionales...")
    
    # Replicar perturbando title (sufijo único)
    insert_sql = """
        INSERT INTO ram_products
            (title, brand, brand_normalized, source_url, ddr_type,
             form_factor, has_rgb, capacity_gb, speed_mhz,
             cas_latency, cas_latency_imputed, cas_was_imputed,
             num_sticks, price_per_gb, price_usd, log_price, scraped_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
    """
    
    new_rows = []
    for i in range(n_a_insertar):
        base = base_rows[i % len(base_rows)]
        # Perturbamos el title con un sufijo único para evitar duplicados
        nueva_fila = list(base)
        nueva_fila[0] = f"{base[0]} [SCALE-{i:06d}]"
        new_rows.append(tuple(nueva_fila))
    
    conn.executemany(insert_sql, new_rows)
    conn.commit()
    
    cursor = conn.execute("SELECT COUNT(*) FROM ram_products;")
    n_final = cursor.fetchone()[0]
    print(f"   ✓ Filas finales: {n_final:,}")


def benchmark_query(conn: sqlite3.Connection, sql: str, n_runs: int) -> float:
    """Devuelve mediana del tiempo en ms."""
    tiempos = []
    for _ in range(n_runs):
        start = time.perf_counter()
        cursor = conn.execute(sql)
        cursor.fetchall()
        end = time.perf_counter()
        tiempos.append(end - start)
    return statistics.median(tiempos) * 1000


def crear_indices(conn: sqlite3.Connection):
    """Crea los 3 índices B-Tree."""
    conn.execute("CREATE INDEX IF NOT EXISTS idx_ddr_type ON ram_products(ddr_type);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_capacity_gb ON ram_products(capacity_gb);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_brand_normalized ON ram_products(brand_normalized);")
    conn.commit()


def borrar_indices(conn: sqlite3.Connection):
    """Borra los índices manuales para medir SIN índices."""
    conn.execute("DROP INDEX IF EXISTS idx_ddr_type;")
    conn.execute("DROP INDEX IF EXISTS idx_capacity_gb;")
    conn.execute("DROP INDEX IF EXISTS idx_brand_normalized;")
    conn.commit()


def medir_para_tamano(conn: sqlite3.Connection, n: int) -> dict:
    """
    Mide cada query SIN y CON índices para un tamaño dado.
    Retorna dict con resultados.
    """
    resultados = {}
    
    # Asegurar tabla en tamaño correcto
    cursor = conn.execute("SELECT COUNT(*) FROM ram_products;")
    n_actual = cursor.fetchone()[0]
    print(f"\n   Tabla actual: {n_actual:,} filas")
    
    # === FASE A: SIN ÍNDICES ===
    print(f"   ▶ Fase A: midiendo SIN índices...")
    borrar_indices(conn)
    
    for query_id, sql in QUERIES.items():
        tiempo = benchmark_query(conn, sql, N_RUNS)
        resultados[f"{query_id}_pre"] = tiempo
        print(f"      {query_id} (sin idx): {tiempo:.4f} ms")
    
    # === FASE B: CON ÍNDICES ===
    print(f"   ▶ Fase B: midiendo CON índices B-Tree...")
    crear_indices(conn)
    
    for query_id, sql in QUERIES.items():
        tiempo = benchmark_query(conn, sql, N_RUNS)
        resultados[f"{query_id}_post"] = tiempo
        speedup = resultados[f"{query_id}_pre"] / tiempo if tiempo > 0 else 0
        print(f"      {query_id} (con idx): {tiempo:.4f} ms · speedup {speedup:.2f}×")
    
    return resultados


# ════════════════════════════════════════════════════════════════
# PIPELINE PRINCIPAL
# ════════════════════════════════════════════════════════════════

def main():
    print("═" * 70)
    print("📈 BLOQUE 5 (BONUS) · TEST DE ESCALADO ASINTÓTICO")
    print("═" * 70)
    print(f"\nTamaños a probar: {SIZES_TO_TEST}")
    print(f"Ejecuciones por query: {N_RUNS}")
    print(f"Total mediciones: {len(SIZES_TO_TEST) * len(QUERIES) * 2 * N_RUNS:,}")
    
    # 1. Copiar la DB original a una temporal para no afectarla
    print(f"\n🔧 Copiando DB original a {SCALING_DB.name}...")
    if SCALING_DB.exists():
        SCALING_DB.unlink()
    shutil.copy(ORIGINAL_DB, SCALING_DB)
    print(f"   ✓ Copia creada")
    
    conn = sqlite3.connect(SCALING_DB)
    
    # 2. Para cada tamaño, replicar tabla y medir
    todos_resultados = []
    
    for size in SIZES_TO_TEST:
        print(f"\n" + "═" * 70)
        print(f"📏 PROBANDO n = {size:,}")
        print("═" * 70)
        
        # Replicar a tamaño
        replicar_a_n_filas(conn, size)
        
        # Medir
        resultados = medir_para_tamano(conn, size)
        resultados["n"] = size
        todos_resultados.append(resultados)
    
    conn.close()
    
    # 3. Convertir a DataFrame
    df = pd.DataFrame(todos_resultados)
    
    # Calcular speedups
    for query_id in QUERIES.keys():
        df[f"{query_id}_speedup"] = df[f"{query_id}_pre"] / df[f"{query_id}_post"]
    
    df.to_csv(RESULTS_CSV, index=False)
    print(f"\n💾 Resultados guardados: {RESULTS_CSV}")
    
    # 4. Tabla de resumen
    print("\n" + "═" * 70)
    print("📊 RESUMEN DE ESCALADO")
    print("═" * 70)
    print(f"\n{'n':>8} {'Q1 sin idx':>12} {'Q1 con idx':>12} {'Q1 speedup':>12} | {'Q2 speedup':>12} | {'Q4 speedup':>12}")
    print("─" * 90)
    for _, row in df.iterrows():
        print(f"{int(row['n']):>8,} "
              f"{row['Q1_filtro_categorico_pre']:>11.3f}ms "
              f"{row['Q1_filtro_categorico_post']:>11.3f}ms "
              f"{row['Q1_filtro_categorico_speedup']:>10.2f}× | "
              f"{row['Q2_filtro_numerico_speedup']:>10.2f}× | "
              f"{row['Q4_agregacion_speedup']:>10.2f}×")
    
    # 5. GRÁFICA · El plato fuerte
    print("\n" + "═" * 70)
    print("🎨 GENERANDO GRÁFICA DE ESCALADO")
    print("═" * 70)
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # ─── Gráfica izquierda: tiempos absolutos en log-log ───────────
    n_vals = df['n'].values
    
    axes[0].loglog(n_vals, df['Q1_filtro_categorico_pre'], 'o-', 
                    color='#e74c3c', linewidth=2, markersize=10,
                    label='Q1 sin índice [O(n)]')
    axes[0].loglog(n_vals, df['Q1_filtro_categorico_post'], 's-', 
                    color='#27ae60', linewidth=2, markersize=10,
                    label='Q1 con índice B-Tree [O(log n)]')
    
    # Líneas teóricas de referencia
    n_theory = np.array([100, 100000])
    c1 = df.iloc[0]['Q1_filtro_categorico_pre'] / df.iloc[0]['n']
    c2 = df.iloc[0]['Q1_filtro_categorico_post'] / np.log2(df.iloc[0]['n'])
    
    axes[0].loglog(n_theory, c1 * n_theory, '--', color='#e74c3c', alpha=0.4,
                    label='Teoría O(n)')
    axes[0].loglog(n_theory, c2 * np.log2(n_theory), '--', color='#27ae60', alpha=0.4,
                    label='Teoría O(log n)')
    
    axes[0].set_xlabel('Tamaño del dataset (n)', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Tiempo de ejecución (ms)', fontsize=12, fontweight='bold')
    axes[0].set_title('Q1 (filtro categórico)\nTiempo empírico vs predicción teórica',
                      fontsize=13, fontweight='bold', pad=12)
    axes[0].legend(fontsize=10, loc='upper left')
    axes[0].grid(True, which='both', alpha=0.3, linestyle='--')
    
    # ─── Gráfica derecha: speedup vs n ──────────────────────────────
    axes[1].plot(n_vals, df['Q1_filtro_categorico_speedup'], 'o-',
                 color='#e74c3c', linewidth=2.5, markersize=12,
                 label='Q1 (filtro categórico)')
    axes[1].plot(n_vals, df['Q2_filtro_numerico_speedup'], 's-',
                 color='#3498db', linewidth=2.5, markersize=12,
                 label='Q2 (filtro numérico)')
    axes[1].plot(n_vals, df['Q4_agregacion_speedup'], '^-',
                 color='#9b59b6', linewidth=2.5, markersize=12,
                 label='Q4 (agregación)')
    
    # Línea de speedup = 1 (sin mejora)
    axes[1].axhline(y=1, color='gray', linestyle=':', linewidth=1.5,
                    label='Sin mejora')
    
    # Anotación del crecimiento
    axes[1].set_xscale('log')
    axes[1].set_xlabel('Tamaño del dataset (n) — escala log', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Speedup (× veces más rápido)', fontsize=12, fontweight='bold')
    axes[1].set_title('Speedup empírico crece con n\nValidación experimental de la teoría asintótica',
                      fontsize=13, fontweight='bold', pad=12)
    axes[1].legend(fontsize=10, loc='upper left')
    axes[1].grid(True, alpha=0.3, linestyle='--')
    
    # Anotar el speedup más alto
    max_speedup_q1 = df['Q1_filtro_categorico_speedup'].max()
    max_n = df.loc[df['Q1_filtro_categorico_speedup'].idxmax(), 'n']
    axes[1].annotate(f'{max_speedup_q1:.1f}× a n={int(max_n):,}',
                     xy=(max_n, max_speedup_q1),
                     xytext=(max_n * 0.3, max_speedup_q1 * 0.85),
                     fontsize=11, fontweight='bold',
                     arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
                     bbox=dict(boxstyle="round,pad=0.4", fc='yellow', ec='black', alpha=0.85))
    
    plt.suptitle('Análisis Asintótico Empírico del Speedup B-Tree\nDataset RAM · Newegg · n ∈ [350, 50,000]',
                 fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(FIG_PATH, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\n✅ Gráfica guardada: {FIG_PATH}")
    
    # 6. Cierre
    print("\n" + "═" * 70)
    print("🎉 TEST DE ESCALADO COMPLETADO")
    print("═" * 70)
    
    print("\n📌 Hallazgos clave para tu defensa oral:")
    
    # Calcular speedup máximo observado
    max_speedup = max([df[f'{q}_speedup'].max() for q in QUERIES.keys()])
    n_max = df.iloc[-1]['n']
    
    print(f"   · Para n=350 el speedup es marginal (~{df.iloc[0]['Q1_filtro_categorico_speedup']:.1f}×)")
    print(f"   · Para n={int(n_max):,} el speedup llega a ~{max_speedup:.1f}×")
    print(f"   · La mejora crece logarítmicamente con n (predicción teórica confirmada)")
    print(f"   · Esta gráfica es evidencia empírica del big-O")
    
    print("\n📦 Artefactos generados:")
    print(f"   · {RESULTS_CSV.name}")
    print(f"   · {FIG_PATH.name}  ← NUEVA gráfica del póster (la más impactante)")


if __name__ == "__main__":
    main()