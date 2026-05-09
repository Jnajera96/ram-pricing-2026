"""test_parsers.py — Validación de los regex parsers con casos reales."""

from scraper import (
    parse_capacity_gb, parse_speed_mhz, parse_cas_latency,
    parse_ddr_type, parse_num_sticks, parse_brand, parse_has_rgb,
    parse_form_factor
)

# Títulos REALES del día 1 + casos edge para detectar bugs temprano
test_titles = [
    "CORSAIR Vengeance RGB Pro 32GB (2 x 16GB) 288-Pin PC RAM DDR4 3200 (PC4 25600) Desktop Memory CL16",
    "Kingston Fury 16GB (2 x 8GB) 288-Pin PC RAM DDR5 5600 (PC5 44800) Memory CL36",
    "Team T-Force Delta RGB 16GB (2 x 8GB) 288-Pin PC RAM DDR4 3200 (PC4 25600) Desktop Memory CL16",
    "G.SKILL Trident Z5 RGB 64GB (2 x 32GB) DDR5 6000 CL30",
    "Crucial 8GB SO-DIMM DDR4 2666 CL19 Laptop Memory",
    "OLOy 32GB (2 x 16GB) 288-Pin DDR5 6000 (PC5 48000) MD5 Series CL36",
]

print(f"\n{'TÍTULO':<48} | {'GB':>3} | {'MHz':>4} | {'CL':>3} | {'TYPE':<6} | STK | RGB | FORM    | BRAND")
print("─" * 130)

for t in test_titles:
    print(
        f"{t[:46]:<48} | "
        f"{parse_capacity_gb(t):>3} | "
        f"{parse_speed_mhz(t):>4} | "
        f"{parse_cas_latency(t):>3} | "
        f"{parse_ddr_type(t):<6} | "
        f"{parse_num_sticks(t):>3} | "
        f"{'T' if parse_has_rgb(t) else 'F':>3} | "
        f"{parse_form_factor(t):<7} | "
        f"{parse_brand(t)}"
    )

print("\n✅ Si todos los valores se ven coherentes, los parsers están listos.\n")