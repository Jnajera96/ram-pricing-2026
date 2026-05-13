"""diagnostico_cas.py — Investigar por qué cas_latency tiene baja cobertura."""

import pandas as pd
import re
from pathlib import Path

# Ruta relativa al archivo del script, no al CWD
SCRIPT_DIR = Path(__file__).parent
CSV_PATH = SCRIPT_DIR / "data" / "ram_raw.csv"

print(f"📂 Leyendo: {CSV_PATH}\n")
df = pd.read_csv(CSV_PATH)

# Productos SIN CL detectado
sin_cl = df[df['cas_latency'] == -1]
print(f"Total sin CL: {len(sin_cl)} de {len(df)} ({len(sin_cl)/len(df)*100:.1f}%)\n")

# Mostrar 15 títulos donde el parser falló
print("─" * 110)
print("TÍTULOS DONDE NO SE DETECTÓ CL (primeros 15):")
print("─" * 110)
for i, title in enumerate(sin_cl['title'].head(15), 1):
    print(f"\n[{i}] {title}")

# Buscar patrones manualmente para ver si hay CL "escondido" con otra forma
print("\n" + "═" * 110)
print("BÚSQUEDA AVANZADA — patrones alternativos de CL en títulos sin CL:")
print("═" * 110)

patterns = [
    r'CAS\s*Latency\s*(\d+)',
    r'CAS-?(\d+)',
    r'C(\d{1,2})\s',          # C16, C36 sin la "L"
    r'Latency\s*(\d+)',
    r'-CL?(\d{1,2})-',        # "-16-" en timings 16-18-18-38
]

for pattern in patterns:
    found_count = 0
    for title in sin_cl['title']:
        if re.search(pattern, title, re.IGNORECASE):
            found_count += 1
    if found_count > 0:
        print(f"\nPatrón {pattern!r}: detectaría {found_count} títulos adicionales")
        # Mostrar 3 ejemplos
        examples = [t for t in sin_cl['title'].head(50) if re.search(pattern, t, re.IGNORECASE)][:3]
        for ex in examples:
            print(f"   → {ex[:90]}")