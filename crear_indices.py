"""
crear_indices.py — Día 4 · Bloque 3: Crear índices B-Tree

Crea 3 índices selectivos sobre la base de datos ram_market.db.
Cada índice usa estructura B-Tree (única opción de SQLite),
implementando búsqueda en O(log n) sobre la columna indexada.

Estrategia de indexación selectiva:
  · idx_ddr_type        → filtro categórico (Q1, Q5)
  · idx_capacity_gb     → filtro numérico de rango (Q2)
  · idx_brand           → agregación GROUP BY (Q4)

NO indexamos price_usd porque su query (Q3) ya es rápida con
B-Tree temporal en memoria. Trade-off costo/beneficio.

Autor: Jose Najera · UDG · DS-2025-GDL
"""

import sqlite3
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR / "data" / "ram_market.db"


# ════════════════════════════════════════════════════════════════
# DEFINICIÓN DE ÍNDICES
# ════════════════════════════════════════════════════════════════

INDICES = [
    {
        "name": "idx_ddr_type",
        "sql": "CREATE INDEX IF NOT EXISTS idx_ddr_type ON ram_products(ddr_type);",
        "razon": "Acelera Q1 (filtro categórico) y Q5 (compuesto)",
        "queries_afectadas": ["Q1", "Q5"],
    },
    {
        "name": "idx_capacity_gb",
        "sql": "CREATE INDEX IF NOT EXISTS idx_capacity_gb ON ram_products(capacity_gb);",
        "razon": "Acelera Q2 (filtro numérico con operador de rango)",
        "queries_afectadas": ["Q2"],
    },
    {
        "name": "idx_brand_normalized",
        "sql": "CREATE INDEX IF NOT EXISTS idx_brand_normalized ON ram_products(brand_normalized);",
        "razon": "Acelera Q4 (agregación GROUP BY brand_normalized)",
        "queries_afectadas": ["Q4"],
    },
]


# ════════════════════════════════════════════════════════════════
# UTILIDADES
# ════════════════════════════════════════════════════════════════

def get_db_size_kb(db_path: Path) -> float:
    return db_path.stat().st_size / 1024


def list_all_indexes(conn: sqlite3.Connection):
    """Lista todos los índices manuales y automáticos."""
    cursor = conn.execute("""
        SELECT name, sql FROM sqlite_master
        WHERE type='index' AND tbl_name='ram_products'
        ORDER BY name;
    """)
    return cursor.fetchall()


def show_index_explain(conn: sqlite3.Connection, index_name: str):
    """
    Muestra cómo SQLite usaría el índice ahora con un EXPLAIN.
    """
    if "ddr_type" in index_name:
        sql = "SELECT * FROM ram_products WHERE ddr_type = 'DDR5';"
    elif "capacity_gb" in index_name:
        sql = "SELECT * FROM ram_products WHERE capacity_gb >= 32;"
    elif "brand" in index_name:
        sql = "SELECT * FROM ram_products WHERE brand_normalized = 'CORSAIR';"
    else:
        return None
    
    cursor = conn.execute(f"EXPLAIN QUERY PLAN {sql}")
    return " | ".join(row[3] for row in cursor.fetchall())


# ════════════════════════════════════════════════════════════════
# PIPELINE PRINCIPAL
# ════════════════════════════════════════════════════════════════

def main():
    print("═" * 70)
    print("🔑 BLOQUE 3 · CREACIÓN DE ÍNDICES B-TREE")
    print("═" * 70)
    
    if not DB_PATH.exists():
        print(f"\n❌ No encontré {DB_PATH}")
        print(f"   Ejecuta primero: python crear_db.py")
        return
    
    # Tamaño antes
    size_before = get_db_size_kb(DB_PATH)
    print(f"\n📊 Tamaño de la DB ANTES de índices: {size_before:.1f} KB")
    
    conn = sqlite3.connect(DB_PATH)
    
    # 1. Mostrar índices existentes
    print("\n📋 Índices existentes ANTES:")
    indices_before = list_all_indexes(conn)
    if not indices_before:
        print("   (ninguno · solo PK auto-gestionada por SQLite)")
    else:
        for name, sql in indices_before:
            kind = "AUTO" if name.startswith("sqlite_") else "MANUAL"
            print(f"   · {name:<35} [{kind}]")
    
    # 2. Crear cada índice + reportar
    print("\n🛠️  Creando índices B-Tree...\n")
    for idx in INDICES:
        print(f"   ▶ {idx['name']}")
        print(f"     Razón: {idx['razon']}")
        print(f"     Queries afectadas: {', '.join(idx['queries_afectadas'])}")
        print(f"     SQL: {idx['sql'].strip()}")
        
        conn.execute(idx['sql'])
        conn.commit()
        
        # Verificar EXPLAIN PLAN para ver si SQLite usará el índice
        plan = show_index_explain(conn, idx['name'])
        if plan:
            usa_indice = "USING INDEX" in plan or "USING COVERING INDEX" in plan
            simbolo = "✅" if usa_indice else "⚠️"
            print(f"     {simbolo} Plan post-creación: {plan}")
        print()
    
    # 3. Listar índices después
    print("─" * 70)
    print("\n📋 Índices DESPUÉS:")
    indices_after = list_all_indexes(conn)
    for name, sql in indices_after:
        kind = "AUTO" if name.startswith("sqlite_") else "MANUAL B-TREE"
        print(f"   · {name:<35} [{kind}]")
    
    print(f"\n   Total índices manuales creados: {len([i for i in indices_after if not i[0].startswith('sqlite_')])}")
    
    # 4. Comparar tamaño
    size_after = get_db_size_kb(DB_PATH)
    overhead = ((size_after - size_before) / size_before) * 100
    print(f"\n📊 IMPACTO EN STORAGE:")
    print(f"   Antes:    {size_before:.1f} KB")
    print(f"   Después:  {size_after:.1f} KB")
    print(f"   Overhead: +{size_after - size_before:.1f} KB (+{overhead:.1f}%)")
    
    # 5. Test rápido — verificar que la búsqueda ahora usa el índice
    print("\n" + "═" * 70)
    print("🧪 VERIFICACIÓN VISUAL · EXPLAIN QUERY PLAN con índices activos")
    print("═" * 70)
    
    test_queries = [
        ("Q1 con idx_ddr_type", 
         "SELECT * FROM ram_products WHERE ddr_type = 'DDR5';"),
        ("Q2 con idx_capacity_gb", 
         "SELECT * FROM ram_products WHERE capacity_gb >= 32;"),
        ("Q4 con idx_brand_normalized", 
         "SELECT brand_normalized, COUNT(*) FROM ram_products GROUP BY brand_normalized;"),
    ]
    
    for label, sql in test_queries:
        cursor = conn.execute(f"EXPLAIN QUERY PLAN {sql}")
        plan = " | ".join(row[3] for row in cursor.fetchall())
        usa = "USING" in plan and "INDEX" in plan
        simbolo = "✅" if usa else "⚠️ "
        print(f"\n{simbolo} {label}:")
        print(f"   → {plan}")
    
    print("\n" + "═" * 70)
    print("✅ Bloque 3 COMPLETADO. Listos para Bloque 4 (benchmark POST-índices).")
    print("═" * 70)
    
    print("\n📌 Para tu cuaderno de defensa:")
    print(f"   · Creé 3 índices B-Tree con overhead de +{overhead:.1f}% en storage")
    print(f"   · Trade-off: más espacio, pero búsquedas O(log n) en lugar de O(n)")
    print(f"   · Plan de ejecución cambió de SCAN a SEARCH USING INDEX (verificable arriba)")
    print(f"   · Próximo paso: medir empíricamente esta mejora con time.perf_counter()")
    
    conn.close()


if __name__ == "__main__":
    main()