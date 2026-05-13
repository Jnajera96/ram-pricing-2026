"""
limpiar.py — Día 3: Limpieza y feature engineering del dataset RAM
Pipeline completo:
  1. Carga de ram_raw.csv
  2. Filtros de calidad (eliminar productos no-RAM o inválidos)
  3. Mejora del parser de CAS Latency v4
  4. Imputación condicional de CL faltantes
  5. Deduplicación
  6. Normalización de marcas (Top-5 + Other)
  7. Features derivados (price_per_gb, log_price)
  8. Auditoría y export a ram_clean.csv
"""

import re
import shutil
import numpy as np
import pandas as pd
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
INPUT = DATA_DIR / "ram_raw.csv"
OUTPUT = DATA_DIR / "ram_clean.csv"
BACKUP = DATA_DIR / "ram_raw_backup.csv"


# ════════════════════════════════════════════════════════════════
# 1. CARGA + BACKUP DEFENSIVO
# ════════════════════════════════════════════════════════════════

print("═" * 70)
print("📂 CARGA DE DATOS")
print("═" * 70)

shutil.copy2(INPUT, BACKUP)
print(f"💾 Backup creado: {BACKUP}")

df = pd.read_csv(INPUT)
print(f"📊 Cargado: {len(df)} filas × {len(df.columns)} columnas\n")


# ════════════════════════════════════════════════════════════════
# 2. FILTROS DE CALIDAD
# ════════════════════════════════════════════════════════════════

print("═" * 70)
print("🧹 FILTROS DE CALIDAD")
print("═" * 70)

n0 = len(df)

# 2.1 Solo DDR3, DDR4, DDR5 (eliminar 'unknown' y antiguos)
df = df[df['ddr_type'].isin(['DDR3', 'DDR4', 'DDR5'])].copy()
n1 = len(df)
print(f"  -{n0-n1:>3} filas removidas: ddr_type fuera de DDR3/DDR4/DDR5")

# 2.2 Solo productos con capacidad válida (>0 GB)
df = df[df['capacity_gb'] > 0].copy()
n2 = len(df)
print(f"  -{n1-n2:>3} filas removidas: capacity_gb = 0 (no son RAM, son accesorios)")

# 2.3 Filtrar productos sin precio (>0)
df = df[df['price_usd'] > 0].copy()
n3 = len(df)
print(f"  -{n2-n3:>3} filas removidas: price_usd inválido")

print(f"\n📊 Después de filtros: {len(df)} filas (antes {n0}, removidas {n0-n3})")


# ════════════════════════════════════════════════════════════════
# 3. PARSER CAS LATENCY v4 — incluye G.SKILL J#### y CORSAIR Z##
# ════════════════════════════════════════════════════════════════

print("\n" + "═" * 70)
print("🔧 PARSER CL v4 (incluye patrones G.SKILL J#### y CORSAIR Z##)")
print("═" * 70)


def parse_cas_v4(title: str) -> int:
    """
    Parser de CAS Latency v4 con triple estrategia:
    
    1. CL explícito en título: 'CL16', 'CAS Latency 30'
    2. Patrón estándar SKU: '...3200C16', '...HC18'
    3. Patrón G.SKILL: 'F5-6000J3636' → 36 (los primeros 2 dígitos de J)
    4. Patrón CORSAIR moderno: 'Z40' al final del SKU
    
    Validación: 10 ≤ CL ≤ 60. Devuelve -1 si no encuentra.
    """
    if not isinstance(title, str):
        return -1
    
    # Estrategia 1: CL explícito
    m = re.search(r'\bCL\s*(\d{1,2})\b', title, re.IGNORECASE)
    if m:
        cl = int(m.group(1))
        if 10 <= cl <= 60:
            return cl
    
    # Extraer SKU del bloque "Model XXXX"
    model_match = re.search(r'Model\s+([A-Z0-9-]+)', title, re.IGNORECASE)
    if not model_match:
        return -1
    
    sku = model_match.group(1)
    
    # Estrategia 2: patrón estándar (CORSAIR clásico, Kingston, Team, etc.)
    candidates = re.findall(r'\d+H?C(\d{2})', sku)
    valid = [int(c) for c in candidates if 10 <= int(c) <= 60]
    if valid:
        return valid[0]
    
    # Estrategia 3: patrón G.SKILL (F#-####J####...)
    # En F5-6000J3636F32GX2-RS5K, después de J vienen 4 dígitos
    # cuyos primeros 2 son el CL
    gskill = re.search(r'J(\d{2})\d{2}', sku)
    if gskill:
        cl = int(gskill.group(1))
        if 10 <= cl <= 60:
            return cl
    
    # Estrategia 4: CORSAIR moderno con Z##
    corsair_z = re.search(r'Z(\d{2})(?:[A-Z]|$)', sku)
    if corsair_z:
        cl = int(corsair_z.group(1))
        if 10 <= cl <= 60:
            return cl
    
    return -1


# Aplicar el parser nuevo
df['cas_latency'] = df['title'].apply(parse_cas_v4)
nuevo_pct = (df['cas_latency'] > 0).mean() * 100
print(f"  Cobertura CL después del parser v4: {nuevo_pct:.1f}%")


# ════════════════════════════════════════════════════════════════
# 4. IMPUTACIÓN CONDICIONAL POR DDR (concepto bayesiano simplificado)
# ════════════════════════════════════════════════════════════════

print("\n" + "═" * 70)
print("📐 IMPUTACIÓN CONDICIONAL DE CL FALTANTES")
print("═" * 70)

# Calcular medianas por DDR (solo de valores válidos)
df_validos = df[df['cas_latency'] > 0]
medianas = df_validos.groupby('ddr_type')['cas_latency'].median().astype(int)
print(f"\n  Medianas condicionales por DDR (priors informativos):")
for ddr, med in medianas.items():
    print(f"    {ddr}: CL={med}")

# Marcar cuáles se imputaron (importante para defensa)
df['cas_was_imputed'] = (df['cas_latency'] == -1)

# Imputar
df['cas_latency_imputed'] = df['cas_latency'].copy()
for ddr, med in medianas.items():
    mask = (df['cas_latency_imputed'] == -1) & (df['ddr_type'] == ddr)
    df.loc[mask, 'cas_latency_imputed'] = int(med)

n_imputados = df['cas_was_imputed'].sum()
print(f"\n  Productos imputados: {n_imputados} ({n_imputados/len(df)*100:.1f}%)")
print(f"  Cobertura final cas_latency_imputed: {(df['cas_latency_imputed']>0).mean()*100:.1f}%")


# ════════════════════════════════════════════════════════════════
# 5. DEDUPLICACIÓN
# ════════════════════════════════════════════════════════════════

print("\n" + "═" * 70)
print("🔁 DEDUPLICACIÓN")
print("═" * 70)

n_antes = len(df)
df = df.drop_duplicates(subset=['title', 'price_usd'], keep='first').reset_index(drop=True)
n_despues = len(df)
print(f"  Filas antes: {n_antes}")
print(f"  Filas después: {n_despues}")
print(f"  Duplicados removidos: {n_antes - n_despues}")


# ════════════════════════════════════════════════════════════════
# 6. NORMALIZACIÓN DE MARCAS (Top-5 + Other)
# ════════════════════════════════════════════════════════════════

print("\n" + "═" * 70)
print("🏷️  NORMALIZACIÓN DE MARCAS")
print("═" * 70)

top5 = df['brand'].value_counts().head(5).index.tolist()
print(f"  Top-5 marcas: {top5}")

df['brand_normalized'] = df['brand'].apply(
    lambda x: x if x in top5 else 'Other'
)
print(f"\n  Distribución final:")
print(df['brand_normalized'].value_counts().to_string())


# ════════════════════════════════════════════════════════════════
# 7. FEATURES DERIVADOS
# ════════════════════════════════════════════════════════════════

print("\n" + "═" * 70)
print("🧬 FEATURES DERIVADOS")
print("═" * 70)

# Price per GB
df['price_per_gb'] = (df['price_usd'] / df['capacity_gb']).round(2)

# Log del precio (para regresión)
df['log_price'] = np.log1p(df['price_usd'])

print(f"  ✅ price_per_gb calculado")
print(f"     min:  ${df['price_per_gb'].min():.2f}")
print(f"     max:  ${df['price_per_gb'].max():.2f}")
print(f"     mean: ${df['price_per_gb'].mean():.2f}")

print(f"\n  ✅ log_price calculado")
print(f"     Asimetría price_usd:  {df['price_usd'].skew():.2f}")
print(f"     Asimetría log_price:  {df['log_price'].skew():.2f}")


# ════════════════════════════════════════════════════════════════
# 8. AUDITORÍA FINAL Y EXPORT
# ════════════════════════════════════════════════════════════════

print("\n" + "═" * 70)
print("📊 AUDITORÍA FINAL DEL DATASET LIMPIO")
print("═" * 70)

print(f"\n• Total registros: {len(df)}")
print(f"• Columnas: {len(df.columns)}")

print(f"\n• Distribución por DDR:")
print(df['ddr_type'].value_counts().to_string())

print(f"\n• Top-5 marcas + Other:")
print(df['brand_normalized'].value_counts().to_string())

print(f"\n• Estadísticas de precio:")
print(df['price_usd'].describe().round(2).to_string())

print(f"\n• Cobertura final de features (deben estar en ✅):")
features_check = {
    'ddr_type':              (df['ddr_type'] != 'unknown').mean() * 100,
    'capacity_gb':           (df['capacity_gb'] > 0).mean() * 100,
    'speed_mhz':             (df['speed_mhz'] > 0).mean() * 100,
    'cas_latency_imputed':   (df['cas_latency_imputed'] > 0).mean() * 100,
    'brand_normalized':      (df['brand_normalized'] != '').mean() * 100,
    'price_per_gb':          (df['price_per_gb'] > 0).mean() * 100,
    'log_price':             (df['log_price'] > 0).mean() * 100,
}
for f, pct in features_check.items():
    icon = "✅" if pct >= 95 else "⚠️ " if pct >= 80 else "❌"
    print(f"  {icon} {f:<25s}: {pct:5.1f}%")


# Reordenar columnas: targets, features, metadata
column_order = [
    # Identificación
    'title', 'brand', 'brand_normalized', 'source_url',
    # Categóricas
    'ddr_type', 'form_factor', 'has_rgb',
    # Numéricas crudas
    'capacity_gb', 'speed_mhz',
    # CL (cruda + imputada + flag)
    'cas_latency', 'cas_latency_imputed', 'cas_was_imputed',
    # Otras numéricas
    'num_sticks',
    # Derivadas
    'price_per_gb',
    # Targets
    'price_usd', 'log_price',
    # Metadata
    'scraped_at',
]

df_final = df[column_order]
df_final.to_csv(OUTPUT, index=False)

print(f"\n✅ Dataset limpio exportado: {OUTPUT}")
print(f"   {len(df_final)} filas × {len(df_final.columns)} columnas")
print(f"\n📋 Primeras 3 filas:")
print(df_final.head(3).to_string())