"""test_minimo.py — Probar el parser v3 aislado, sin importar scraper.py.
   Útil para validar que el regex está correcto antes de tocar el CSV."""

import re


def parse_cas_latency(title: str) -> int:
    """Versión v3 aislada para testing puro."""
    # Estrategia 1: CL explícito
    m = re.search(r'\bCL\s*(\d{1,2})\b', title, re.IGNORECASE)
    if m:
        cl = int(m.group(1))
        if 10 <= cl <= 60:
            return cl
    
    # Estrategia 2: SKU
    model_match = re.search(r'Model\s+([A-Z0-9-]+)', title, re.IGNORECASE)
    if model_match:
        sku = model_match.group(1)
        candidates = re.findall(r'\d+H?C(\d{2})', sku)
        valid_cls = [int(c) for c in candidates if 10 <= int(c) <= 60]
        if valid_cls:
            return valid_cls[0]
    return -1


# Casos de prueba basados en SKUs reales del scraping
casos = [
    ("Kingston Fury ... Model KF556C36BBEK2-16",          36),
    ("Crucial ... Model CP2K32G60C40U5W",                 40),
    ("Patriot Viper ... Model PVV564G600C36K",            36),
    ("CORSAIR ... Model CMW32GX4M2E3200C16",              16),
    ("XPG LANCER ... Model AX5U6000C3016G-DCLABK",        30),
    ("Team T-Force ... Model TF3D432G3200HC16FDC01",      16),
    ("Team T-CREATE ... Model CTCCD564G6000HC48DC01",     48),
    ("CORSAIR Vengeance ... Model CMSX32GX4M2A3200C22",   22),
    # Caso con CL explícito (debe funcionar también)
    ("G.SKILL Trident Z5 RGB 64GB DDR5 6000 CL30",        30),
    # Caso edge: sin CL ni Model
    ("Generic 8GB DDR4 2666",                             -1),
]

print(f"\n{'TÍTULO':<60} | {'ESPERADO':>9} | {'OBTENIDO':>9} | RESULT")
print("─" * 100)

aciertos = 0
for title, esperado in casos:
    obtenido = parse_cas_latency(title)
    estado = "✅" if obtenido == esperado else "❌"
    if obtenido == esperado:
        aciertos += 1
    print(f"{title[:58]:<60} | {esperado:>9} | {obtenido:>9} | {estado}")

print("─" * 100)
print(f"\nAciertos: {aciertos}/{len(casos)}\n")