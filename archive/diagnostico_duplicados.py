"""diagnostico_duplicados.py — Investigar el patrón de duplicación del scraping"""
import pandas as pd
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
df = pd.read_csv(SCRIPT_DIR / "data" / "ram_raw.csv")

print(f"📊 Análisis de duplicados\n")
print(f"  Total filas: {len(df)}")
print(f"  Títulos únicos: {df['title'].nunique()}")
print(f"  Source URLs únicas: {df['source_url'].nunique()}")
print(f"  Combinación title+price única: {df.drop_duplicates(['title', 'price_usd']).shape[0]}")

print(f"\n📋 Top 10 productos más duplicados:")
duplicados = df.groupby('title').size().sort_values(ascending=False).head(10)
print(duplicados.to_string())

print(f"\n📈 Distribución del número de duplicaciones:")
print(df.groupby('title').size().value_counts().sort_index().to_string())

print(f"\n💰 Después de eliminar duplicados:")
df_unico = df.drop_duplicates(subset=['title', 'price_usd'], keep='first').reset_index(drop=True)
print(f"  Registros únicos: {len(df_unico)}")
print(f"  Distribución por DDR:")
print(df_unico['ddr_type'].value_counts().to_string())
print(f"\n  Estadística de precios (sin duplicados):")
print(df_unico['price_usd'].describe().round(2).to_string())