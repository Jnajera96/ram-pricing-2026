"""test_paginacion.py — Probar diferentes URLs de Newegg para encontrar
   una que sí respete &page=N correctamente."""

import requests
from bs4 import BeautifulSoup
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
}

# Diferentes URLs candidatas
URLS_TEST = [
    # URL actual (problemática)
    {
        "name": "Original (Category ID-17)",
        "url_template": "https://www.newegg.com/Memory/Category/ID-17?PageSize=36&page={}",
    },
    # Search-based (suele funcionar mejor)
    {
        "name": "Search desktop memory",
        "url_template": "https://www.newegg.com/p/pl?N=100007611%204131&page={}",
    },
    # Sub-category alternativa
    {
        "name": "SubCategory desktop memory",
        "url_template": "https://www.newegg.com/Desktop-Memory/SubCategory/ID-147?Order=BESTMATCH&page={}",
    },
    # Búsqueda explícita por keyword
    {
        "name": "Search keyword DDR5",
        "url_template": "https://www.newegg.com/p/pl?d=ddr5+ram&page={}",
    },
]

def get_first_titles(url):
    """Obtiene los primeros 3 títulos de productos en la página."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return None, f"Status {resp.status_code}"
        soup = BeautifulSoup(resp.text, "lxml")
        items = soup.select(".item-cell")
        if not items:
            return None, "Sin .item-cell encontrados"
        titles = []
        for item in items[:3]:
            t_el = item.select_one("a.item-title")
            if t_el:
                titles.append(t_el.text.strip()[:60])
        return titles, f"OK ({len(items)} items en página)"
    except Exception as e:
        return None, str(e)

print("🔬 Comparando paginación entre URLs:\n")
print("Si las páginas 1, 2 y 3 muestran productos DIFERENTES, la URL pagina bien.")
print("Si muestran los MISMOS 3 productos, la paginación está rota.\n")

for config in URLS_TEST:
    print("=" * 90)
    print(f"📍 {config['name']}")
    print(f"   URL base: {config['url_template']}")
    
    page_results = {}
    for page_num in [1, 2, 3]:
        url = config['url_template'].format(page_num)
        titles, status = get_first_titles(url)
        page_results[page_num] = (titles, status)
        print(f"\n   Página {page_num} → {status}")
        if titles:
            for i, t in enumerate(titles, 1):
                print(f"      [{i}] {t}")
        time.sleep(2.5)
    
    # Veredicto
    if all(r[0] for r in page_results.values()):
        p1 = set(page_results[1][0])
        p2 = set(page_results[2][0])
        p3 = set(page_results[3][0])
        
        if p1 == p2 == p3:
            print(f"\n   ❌ VEREDICTO: paginación ROTA (las 3 páginas son idénticas)")
        elif len(p1 & p2) > 0 or len(p2 & p3) > 0:
            print(f"\n   ⚠️  VEREDICTO: paginación PARCIAL (hay productos repetidos)")
        else:
            print(f"\n   ✅ VEREDICTO: paginación FUNCIONA (productos diferentes en cada página)")
    print()