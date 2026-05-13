"""recalcular_cas.py — Recalcular cas_latency en el CSV existente
   usando el parser v3 actualizado de scraper.py.
   
   Hace backup defensivo antes de sobrescribir.
   No vuelve a hacer scraping (preserva el dataset ya extraído)."""

import shutil
from pathlib import Path
import pandas as pd

from scraper import parse_cas_latency

SCRIPT_DIR = Path(__file__).parent
CSV_PATH = SCRIPT_DIR / "data" / "ram_raw.csv"
BACKUP_PATH = SCRIPT_DIR / "data" / "ram_raw_backup.csv"

# 1. Backup defensivo del CSV actual
shutil.copy2(CSV_PATH, BACKUP_PATH)
print(f"💾 Backup creado: {BACKUP_PATH}")

# 2. Cargar CSV actual
df = pd.read_csv(CSV_PATH)
print(f"📂 Cargado: {len(df)} filas\n")

# 3. Recalcular cas_latency con el parser nuevo
df['cas_latency'] = df['title'].apply(parse_cas_latency)

# 4. Reportar ANTES de sobrescribir
nuevo_pct = (df['cas_latency'] > 0).mean() * 100
print(f"📊 Nueva cobertura cas_latency: {nuevo_pct:.1f}%\n")

print("Distribución de valores detectados:")
print(df['cas_latency'].value_counts().sort_index().to_string())

# 5. Solo sobrescribir si la cobertura es razonable
if nuevo_pct >= 70:
    df.to_csv(CSV_PATH, index=False)
    print(f"\n✅ CSV actualizado: {CSV_PATH}")
    print(f"   Backup disponible en: {BACKUP_PATH}")
else:
    print(f"\n⚠️ Cobertura insuficiente ({nuevo_pct:.1f}% < 70%). NO se sobrescribió el CSV.")
    print("   Revisa el parser parse_cas_latency() en scraper.py antes de reintentar.")