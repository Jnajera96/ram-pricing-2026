"""
bench_pre.py — Día 4 · Bloque 2: Benchmark PRE-índices

Mide empíricamente el tiempo de ejecución de 5 queries representativas
SOBRE LA BASE DE DATOS SIN ÍNDICES MANUALES.

Esta es la "Fase A" del experimento de complejidad. Los tiempos aquí
representan la complejidad 𝒪(n) que compararemos contra la 𝒪(log n)
después de crear índices B-Tree (Bloque 4).

Metodología:
  - Cada query se ejecuta N=100 veces para reducir varianza
  - Usamos time.perf_counter() (precisión nanosegundos)
  - Reportamos mediana (robusta a outliers)
  - EXPLAIN QUERY PLAN antes de cada query como evidencia visual

Autor: Jose Najera · UDG · DS-2025-GDL
"""

import sqlite3
import time
import statistics
import json
import pandas as pd
from pathlib import Path

# ════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ════════════════════════════════════════════════════════════════

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
DB_PATH = DATA_DIR / "ram_market.db"
RESULTS_PATH = DATA_DIR / "bench_pre_results.csv"

N_RUNS = 100  # Ejecuciones por query para reducir varianza


# ════════════════════════════════════════════════════════════════
# QUERIES DEL EXPERIMENTO
# ════════════════════════════════════════════════════════════════

QUERIES = {
    "Q1_filtro_categorico": {
        "sql": "SELECT * FROM ram_products WHERE ddr_type = 'DDR5';",
        "descripcion": "Filtro categórico exacto sobre ddr_type",
        "tipo": "WHERE ="
    },
    "Q2_filtro_numerico": {
        "sql": "SELECT * FROM ram_products WHERE capacity_gb >= 32;",
        "descripcion": "Filtro numérico con operador de rango",
        "tipo": "WHERE >="
    },
    "Q3_topN_ordenado": {
        "sql": "SELECT * FROM ram_products ORDER BY price_usd DESC LIMIT 10;",
        "descripcion": "Top 10 productos más caros (ordenamiento)",
        "tipo": "ORDER BY LIMIT"
    },
    "Q4_agregacion_groupby": {
        "sql": """
            SELECT brand_normalized, COUNT(*) as n, AVG(price_usd) as avg_price
            FROM ram_products
            GROUP BY brand_normalized;
        """,
        "descripcion": "Agregación por marca con conteo y promedio",
        "tipo": "GROUP BY + AVG"
    },
    "Q5_compuesto": {
        "sql": """
            SELECT * FROM ram_products
            WHERE ddr_type = 'DDR5' AND price_usd > 500;
        """,
        "descripcion": "Filtro compuesto AND sobre dos columnas",
        "tipo": "WHERE AND"
    },
}


# ════════════════════════════════════════════════════════════════
# UTILIDADES DE BENCHMARK
# ════════════════════════════════════════════════════════════════

def get_query_plan(conn: sqlite3.Connection, sql: str) -> str:
    """Devuelve el EXPLAIN QUERY PLAN como string legible."""
    cursor = conn.execute(f"EXPLAIN QUERY PLAN {sql}")
    rows = cursor.fetchall()
    # Cada fila es: (id, parent, notused, detail)
    return " | ".join(row[3] for row in rows)


def benchmark_query(conn: sqlite3.Connection, sql: str, n_runs: int) -> dict:
    """
    Ejecuta una query n_runs veces y devuelve estadísticas.
    Usa time.perf_counter() (resolución nanosegundos, monotónico).
    """
    tiempos = []
    
    for _ in range(n_runs):
        start = time.perf_counter()
        cursor = conn.execute(sql)
        cursor.fetchall()  # IMPORTANTE: forzar la lectura completa
        end = time.perf_counter()
        tiempos.append(end - start)
    
    return {
        "n_runs": n_runs,
        "min_ms":    min(tiempos) * 1000,
        "max_ms":    max(tiempos) * 1000,
        "media_ms":  statistics.mean(tiempos) * 1000,
        "mediana_ms": statistics.median(tiempos) * 1000,
        "stdev_ms":  statistics.stdev(tiempos) * 1000 if n_runs > 1 else 0,
        "rows_returned": len(cursor.fetchall()) if False else None,  # placeholder
    }


# ════════════════════════════════════════════════════════════════
# PIPELINE PRINCIPAL
# ════════════════════════════════════════════════════════════════

def main():
    print("═" * 70)
    print("📊 BLOQUE 2 · BENCHMARK PRE-ÍNDICES (Fase A · O(n))")
    print("═" * 70)
    print(f"\nMetodología: N={N_RUNS} ejecuciones por query · mediana robusta")
    print(f"Mediciones: time.perf_counter() (precisión ns)")
    print(f"DB: {DB_PATH.name}")

    if not DB_PATH.exists():
        print(f"\n❌ No encontré {DB_PATH}")
        print(f"   Ejecuta primero: python crear_db.py")
        return

    conn = sqlite3.connect(DB_PATH)
    
    # Verificar conteo total
    n_total = conn.execute("SELECT COUNT(*) FROM ram_products;").fetchone()[0]
    print(f"\nTotal de filas en la tabla: {n_total}")
    
    # Verificar índices manuales (debe ser cero o solo la PK)
    indices = conn.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='index' AND tbl_name='ram_products'
        AND name NOT LIKE 'sqlite_%';
    """).fetchall()
    print(f"Índices manuales activos: {len(indices)} {'(esperado para Bloque 2)' if len(indices) == 0 else '⚠️ ALERTA'}")
    
    # Resultados acumulados
    resultados = []
    
    # Ejecutar cada query
    for query_id, info in QUERIES.items():
        print("\n" + "─" * 70)
        print(f"🔍 {query_id}")
        print(f"   {info['descripcion']}")
        print(f"   Tipo: {info['tipo']}")
        
        sql = info['sql'].strip()
        
        # 1. Mostrar el plan de ejecución (evidencia visual)
        plan = get_query_plan(conn, sql)
        print(f"\n   📋 EXPLAIN QUERY PLAN:")
        print(f"      → {plan}")
        
        # 2. Contar cuántas filas retorna (validación)
        cursor = conn.execute(sql)
        n_rows = len(cursor.fetchall())
        print(f"   📊 Filas retornadas: {n_rows}")
        
        # 3. Benchmark
        print(f"   ⏱️  Ejecutando {N_RUNS} veces...")
        stats = benchmark_query(conn, sql, N_RUNS)
        
        # 4. Reporte
        print(f"   ⏱️  Tiempos (ms):")
        print(f"      min:     {stats['min_ms']:.4f}")
        print(f"      mediana: {stats['mediana_ms']:.4f}  ⭐ (estadística reportada)")
        print(f"      media:   {stats['media_ms']:.4f}")
        print(f"      max:     {stats['max_ms']:.4f}")
        print(f"      stdev:   {stats['stdev_ms']:.4f}")
        
        resultados.append({
            "query_id": query_id,
            "tipo": info['tipo'],
            "descripcion": info['descripcion'],
            "fase": "PRE-INDICE",
            "plan": plan,
            "n_rows": n_rows,
            **stats,
        })
    
    # Guardar resultados a CSV para el bloque 4
    df_results = pd.DataFrame(resultados)
    df_results.to_csv(RESULTS_PATH, index=False)
    print("\n" + "═" * 70)
    print(f"💾 Resultados guardados: {RESULTS_PATH}")
    print(f"   {len(df_results)} queries × {len(df_results.columns)} columnas")
    
    # Resumen final
    print("\n" + "═" * 70)
    print("📊 RESUMEN PRE-ÍNDICES (Fase A · O(n))")
    print("═" * 70)
    print(f"\n{'Query':<25} {'Plan ejecución':<35} {'Mediana (ms)':>15}")
    print("─" * 80)
    for r in resultados:
        plan_corto = r['plan'][:33]
        print(f"{r['query_id']:<25} {plan_corto:<35} {r['mediana_ms']:>13.4f}")
    
    print("\n✅ Bloque 2 COMPLETADO. Listos para Bloque 3 (crear índices).\n")
    print("📌 Apunta para tu cuaderno de defensa:")
    print("   · Todas las queries muestran 'SCAN' = búsqueda lineal O(n)")
    print("   · Estos tiempos son la línea base del experimento")
    print("   · En Bloque 4 compararemos vs 'SEARCH USING INDEX' = O(log n)")
    
    conn.close()


if __name__ == "__main__":
    main()