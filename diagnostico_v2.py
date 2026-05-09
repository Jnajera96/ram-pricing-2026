"""diagnostico_v2.py — Investigar productos sospechosos del nuevo dataset"""
import pandas as pd
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
df = pd.read_csv(SCRIPT_DIR / "data" / "ram_raw.csv")

print("=" * 90)
print("🔍 DIAGNÓSTICO 1 · Productos sospechosamente baratos (< $50)")
print("=" * 90)
baratos = df[df['price_usd'] < 50].sort_values('price_usd')
print(f"Cantidad: {len(baratos)}\n")
for _, row in baratos.iterrows():
    print(f"  ${row['price_usd']:>6.2f} | {row['ddr_type']:<8} | {row['capacity_gb']:>3}GB | {row['title'][:80]}")

print("\n" + "=" * 90)
print("🔍 DIAGNÓSTICO 2 · Productos con DDR='unknown'")
print("=" * 90)
unknowns = df[df['ddr_type'] == 'unknown']
print(f"Cantidad: {len(unknowns)}\n")
for _, row in unknowns.iterrows():
    print(f"  {row['title'][:100]}")

print("\n" + "=" * 90)
print("🔍 DIAGNÓSTICO 3 · Análisis de cas_latency faltante por marca")
print("=" * 90)
df_sin_cl = df[df['cas_latency'] == -1]
print(f"Total sin CL detectado: {len(df_sin_cl)} ({len(df_sin_cl)/len(df)*100:.1f}%)\n")
print("Distribución por marca:")
print(df_sin_cl['brand'].value_counts().head(10).to_string())

print(f"\n📋 5 títulos sin CL (para ver el patrón):")
for i, title in enumerate(df_sin_cl['title'].head(5), 1):
    print(f"\n[{i}] {title}")

print("\n" + "=" * 90)
print("🔍 DIAGNÓSTICO 4 · Verificar duplicados (debe ser <5%)")
print("=" * 90)
print(f"Filas totales:    {len(df)}")
print(f"Títulos únicos:   {df['title'].nunique()}")
print(f"Duplicación:      {(1 - df['title'].nunique()/len(df))*100:.1f}%")
print(f"\nTop 5 productos repetidos (esperable hasta ~10% por productos featured):")
top_repe = df.groupby('title').size().sort_values(ascending=False).head(5)
print(top_repe.to_string())