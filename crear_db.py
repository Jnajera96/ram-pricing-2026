"""
crear_db.py — Día 4 · Bloque 1: Construir ram_market.db desde cero

Carga ram_clean.csv en una base de datos SQLite con schema explícito.
Deliberadamente NO crea índices — eso viene en el Bloque 3 para
medir empíricamente el cambio de complejidad O(n) -> O(log n).

Autor: Jose Najera · UDG · DS-2025-GDL
"""

import sqlite3
import pandas as pd
from pathlib import Path

# ════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ════════════════════════════════════════════════════════════════

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
CSV_INPUT = DATA_DIR / "ram_clean.csv"
DB_OUTPUT = DATA_DIR / "ram_market.db"


# ════════════════════════════════════════════════════════════════
# SCHEMA · Tipado explícito (defendible en oral)
# ════════════════════════════════════════════════════════════════

SCHEMA = """
CREATE TABLE IF NOT EXISTS ram_products (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    title               TEXT    NOT NULL,
    brand               TEXT,
    brand_normalized    TEXT,
    source_url          TEXT,
    ddr_type            TEXT    NOT NULL,
    form_factor         TEXT,
    has_rgb             INTEGER,
    capacity_gb         INTEGER NOT NULL,
    speed_mhz           INTEGER,
    cas_latency         INTEGER,
    cas_latency_imputed INTEGER,
    cas_was_imputed     INTEGER,
    num_sticks          INTEGER,
    price_per_gb        REAL,
    price_usd           REAL    NOT NULL,
    log_price           REAL,
    scraped_at          TEXT
);
"""


# ════════════════════════════════════════════════════════════════
# UTILIDADES
# ════════════════════════════════════════════════════════════════

def get_db_size_kb(db_path: Path) -> float:
    """Devuelve el tamaño del archivo .db en KB."""
    return db_path.stat().st_size / 1024 if db_path.exists() else 0


def show_table_info(conn: sqlite3.Connection):
    """Imprime info estructural de la tabla (PRAGMA table_info)."""
    cursor = conn.execute("PRAGMA table_info(ram_products);")
    print(f"\n📋 SCHEMA DE LA TABLA `ram_products`:")
    print(f"  {'col':<5} {'nombre':<25} {'tipo':<10} {'NOT NULL':<10} {'PK'}")
    print(f"  " + "─" * 60)
    for cid, name, ctype, notnull, _, pk in cursor.fetchall():
        print(f"  {cid:<5} {name:<25} {ctype:<10} "
              f"{'YES' if notnull else 'no':<10} {'PK' if pk else ''}")


def show_indexes(conn: sqlite3.Connection):
    """Lista todos los índices de la tabla (debería estar casi vacío en este Bloque)."""
    cursor = conn.execute("""
        SELECT name, sql FROM sqlite_master
        WHERE type='index' AND tbl_name='ram_products'
        ORDER BY name;
    """)
    indexes = cursor.fetchall()
    print(f"\n🔑 ÍNDICES ACTIVOS: {len(indexes)}")
    for name, sql in indexes:
        # Los índices auto-creados (PK) tienen sql=None y nombre 'sqlite_*'
        kind = "AUTO (PK)" if name.startswith("sqlite_") else "MANUAL"
        print(f"  · {name:<35} [{kind}]")
        if sql:
            print(f"      {sql}")


# ════════════════════════════════════════════════════════════════
# PIPELINE PRINCIPAL
# ════════════════════════════════════════════════════════════════

def main():
    print("═" * 70)
    print("📦 BLOQUE 1 · CONSTRUCCIÓN DE ram_market.db")
    print("═" * 70)

    # 1. Verificar que el CSV existe
    if not CSV_INPUT.exists():
        print(f"❌ No encontré {CSV_INPUT}")
        print(f"   Ejecuta primero: python limpiar.py")
        return

    # 2. Si la DB existe, borrarla (queremos partir limpio)
    if DB_OUTPUT.exists():
        print(f"\n⚠️  DB anterior detectada, eliminando para empezar limpio...")
        DB_OUTPUT.unlink()
        print(f"   ✓ Eliminado {DB_OUTPUT}")

    # 3. Cargar CSV
    print(f"\n📂 Leyendo {CSV_INPUT.name}...")
    df = pd.read_csv(CSV_INPUT)
    print(f"   ✓ {len(df)} filas × {len(df.columns)} columnas")

    # 4. Conexión + creación del schema
    print(f"\n🛠️  Creando {DB_OUTPUT.name} con schema explícito...")
    conn = sqlite3.connect(DB_OUTPUT)
    conn.execute(SCHEMA)
    conn.commit()
    print(f"   ✓ Tabla `ram_products` creada")

    # 5. Cargar datos con pandas (preserva tipos)
    #    Usamos if_exists='append' porque la tabla ya está creada con nuestro schema
    print(f"\n💾 Insertando {len(df)} filas (búsqueda lineal O(n) sin índices)...")
    df.to_sql("ram_products", conn, if_exists="append", index=False)
    conn.commit()
    print(f"   ✓ Datos cargados")

    # 6. Verificación
    cursor = conn.execute("SELECT COUNT(*) FROM ram_products;")
    n_rows = cursor.fetchone()[0]
    print(f"\n✅ Verificación: {n_rows} filas en la base de datos")

    # 7. Mostrar info estructural
    show_table_info(conn)
    show_indexes(conn)

    # 8. Test query rápido (sanity check)
    print(f"\n🧪 SANITY CHECK · primeros 3 productos DDR5:")
    cursor = conn.execute("""
        SELECT brand, capacity_gb, speed_mhz, price_usd
        FROM ram_products
        WHERE ddr_type = 'DDR5'
        LIMIT 3;
    """)
    print(f"  {'brand':<12} {'GB':>4} {'MHz':>6} {'price':>10}")
    print(f"  " + "─" * 38)
    for brand, gb, mhz, price in cursor.fetchall():
        print(f"  {brand:<12} {gb:>4} {mhz:>6} ${price:>8.2f}")

    # 9. Tamaño del archivo
    size_kb = get_db_size_kb(DB_OUTPUT)
    print(f"\n📊 Archivo final: {DB_OUTPUT.name} ({size_kb:.1f} KB)")

    # 10. Cerrar conexión
    conn.close()
    print(f"\n✅ Bloque 1 COMPLETADO. Listos para Bloque 2 (queries pre-índice).\n")


if __name__ == "__main__":
    main()