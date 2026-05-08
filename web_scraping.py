# hello_newegg.py — Día 1 v2 (precio fragmentado correctamente)
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
}

URL = "https://www.newegg.com/Memory/Category/ID-17?PageSize=36&page=1"


def parse_price(price_li):
    """
    Newegg fragmenta el precio en <strong>dólares</strong><sup>.centavos</sup>.
    Reconstruimos a float manejando ausencias y formatos raros.
    Retorna None si el item no tiene precio (out-of-stock, etc.)
    """
    if price_li is None:
        return None
    
    dollars_el = price_li.select_one("strong")
    cents_el = price_li.select_one("sup")
    
    if dollars_el is None:
        return None  # item sin precio (probablemente "See price in cart")
    
    # Limpiar dólares: "1,234" → "1234"
    dollars = dollars_el.text.strip().replace(",", "")
    cents = cents_el.text.strip() if cents_el else ".00"
    
    # cents viene como ".99" — ya incluye el punto
    if not cents.startswith("."):
        cents = "." + cents
    
    try:
        return float(dollars + cents)
    except ValueError:
        return None


print(f"📡 Solicitando: {URL}")
resp = requests.get(URL, headers=HEADERS, timeout=15)
print(f"   Status: {resp.status_code}")
print(f"   Tamaño: {len(resp.text):,} bytes")

if resp.status_code != 200:
    print("❌ Status no es 200. Aborto.")
    exit()

if "captcha" in resp.text.lower():
    print("⚠️  CAPTCHA detectado.")

soup = BeautifulSoup(resp.text, "lxml")

# Probamos los DOS selectores que identificaste para ver cuál tiene más items
items_cell = soup.select(".item-cell")
items_container = soup.select(".item-container")
print(f"\n🔍 .item-cell      → {len(items_cell)} elementos")
print(f"🔍 .item-container → {len(items_container)} elementos")

# Usamos el que tenga ~36 items (uno suele incluir banners y duplicados)
items = items_cell if len(items_cell) >= len(items_container) else items_container
print(f"   → Usando: {'item-cell' if items is items_cell else 'item-container'}")

# ── Auditoría de los primeros 3 productos ──
print(f"\n📦 PRIMEROS 3 PRODUCTOS (auditoría manual):\n")

for i, item in enumerate(items[:3], 1):
    title_el = item.select_one("a.item-title")
    price_li = item.select_one("li.price-current")
    
    title = title_el.text.strip() if title_el else "[NO TITLE]"
    href = title_el.get("href", "[NO HREF]") if title_el else "[NO HREF]"
    price = parse_price(price_li)
    
    print(f"  [{i}] {title[:80]}...")
    print(f"      Precio: ${price}" if price else f"      Precio: [NO DETECTADO]")
    print(f"      URL: {href[:90]}...\n")

# ── Métricas de cobertura: cuántos items tienen precio válido ──
total = len(items)
con_precio = sum(1 for it in items if parse_price(it.select_one("li.price-current")))
con_titulo = sum(1 for it in items if it.select_one("a.item-title"))

print(f"📊 COBERTURA EN ESTA PÁGINA:")
print(f"   Items totales:         {total}")
print(f"   Items con título:      {con_titulo} ({con_titulo/total*100:.0f}%)")
print(f"   Items con precio:      {con_precio} ({con_precio/total*100:.0f}%)")

if con_precio / total < 0.7:
    print(f"\n⚠️  Cobertura de precio baja. Revisar parser.")
else:
    print(f"\n✅ Cobertura aceptable. Listos para Día 2.")