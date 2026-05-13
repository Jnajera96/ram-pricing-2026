# diagnostico.py
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
}

URL = "https://www.newegg.com/Memory/Category/ID-17?PageSize=36&page=1"
resp = requests.get(URL, headers=HEADERS, timeout=15)

# Guardamos la respuesta cruda en un archivo HTML para abrirla en el navegador
with open("debug_newegg.html", "w", encoding="utf-8") as f:
    f.write(resp.text)

print(f"Status: {resp.status_code}")
print(f"Tamaño: {len(resp.text):,} bytes")
print(f"\n--- HEADERS DE RESPUESTA ---")
for k, v in resp.headers.items():
    print(f"  {k}: {v}")

print(f"\n--- PRIMEROS 1500 CHARS DEL HTML ---")
print(resp.text[:1500])

print(f"\n--- BÚSQUEDAS DE PALABRAS CLAVE ---")
keywords = ["captcha", "robot", "blocked", "cloudflare", "perimeter",
            "are you a human", "challenge", "verify", "country",
            "item-cell", "item-container", "price-current"]
for kw in keywords:
    count = resp.text.lower().count(kw.lower())
    if count > 0:
        print(f"  ✓ '{kw}' aparece {count} veces")