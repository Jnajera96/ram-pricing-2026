"""
scraper.py — Día 2: Scraper de producción para Newegg RAM
Proyecto: Optimización Asintótica en la Predicción del Mercado de RAM
Autor: Jose Najera · UDG · DS-2025-GDL

Versión: v3 (parser dual de cas_latency)
"""

import requests
import time
import re
from dataclasses import dataclass, asdict, field
from typing import Optional
from pathlib import Path
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup


# ════════════════════════════════════════════════════════════════
# CONFIGURACIÓN GLOBAL
# ════════════════════════════════════════════════════════════════

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",  # SIN br (lección día 1)
}

BASE_URL = "https://www.newegg.com/Memory/Category/ID-17?PageSize=36&page={}"
MAX_PAGES = 15
SLEEP_BETWEEN_REQUESTS = 2.5
CHECKPOINT_EVERY = 5

# Rutas robustas: basadas en la ubicación del script, no del CWD
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


# ════════════════════════════════════════════════════════════════
# DATACLASS · Contrato de datos fuerte
# ════════════════════════════════════════════════════════════════

@dataclass
class RAMProduct:
    """Representa un producto de RAM extraído de Newegg con tipado estricto."""
    title: str
    brand: str
    source_url: str
    ddr_type: str           # "DDR3", "DDR4", "DDR5", "unknown"
    capacity_gb: int        # 0 si no parseado
    speed_mhz: int          # 0 si no parseado
    cas_latency: int        # -1 si no parseado
    num_sticks: int         # 1 por defecto
    form_factor: str        # "DIMM" o "SO-DIMM"
    has_rgb: bool
    price_usd: float
    scraped_at: str = field(default_factory=lambda: datetime.now().isoformat())


# ════════════════════════════════════════════════════════════════
# PARSERS · Funciones puras, fáciles de testear
# ════════════════════════════════════════════════════════════════

def parse_price(price_li) -> Optional[float]:
    """
    Reconstruye el precio desde <strong>dolares</strong><sup>.cents</sup>.
    Complejidad: O(1)
    """
    if price_li is None:
        return None
    
    dollars_el = price_li.select_one("strong")
    if dollars_el is None:
        return None
    
    cents_el = price_li.select_one("sup")
    dollars = dollars_el.text.strip().replace(",", "")
    cents = cents_el.text.strip() if cents_el else ".00"
    
    if not cents.startswith("."):
        cents = "." + cents
    
    try:
        return float(dollars + cents)
    except ValueError:
        return None


def parse_capacity_gb(title: str) -> int:
    """
    Extrae capacidad total en GB. Maneja kits 'N x MGB' multiplicando.
    Complejidad: O(k) donde k = len(title), amortizado O(1).
    """
    kit_match = re.search(r'(\d+)\s*x\s*(\d+)\s*GB', title, re.IGNORECASE)
    if kit_match:
        return int(kit_match.group(1)) * int(kit_match.group(2))
    
    simple_match = re.search(r'(\d+)\s*GB', title, re.IGNORECASE)
    if simple_match:
        return int(simple_match.group(1))
    
    return 0


def parse_num_sticks(title: str) -> int:
    """Detecta kits 'N x MGB'. Default = 1."""
    m = re.search(r'(\d+)\s*x\s*\d+\s*GB', title, re.IGNORECASE)
    return int(m.group(1)) if m else 1


def parse_speed_mhz(title: str) -> int:
    """Extrae frecuencia. Múltiples patrones por robustez."""
    # Patrón fuerte: "DDR4-3200" o "DDR5 5600"
    ddr_match = re.search(r'DDR[345]\s*-?\s*(\d{4,5})', title, re.IGNORECASE)
    if ddr_match:
        return int(ddr_match.group(1))
    
    # Patrón con MHz/MT/s explícito
    mhz_match = re.search(r'(\d{4,5})\s*(MHz|MT/?s)', title, re.IGNORECASE)
    if mhz_match:
        return int(mhz_match.group(1))
    
    # Fallback: PC4-XXXXX, PC5-XXXXX (PC4-25600 → 3200 MHz)
    pc_match = re.search(r'PC[345]?-?(\d{5})', title, re.IGNORECASE)
    if pc_match:
        return int(pc_match.group(1)) // 8
    
    return 0


def parse_cas_latency(title: str) -> int:
    """
    Latencia CAS con doble estrategia en cascada.
    
    Estrategia 1: CL explícito en el título ('CL16', 'CL36').
    Estrategia 2: patrón embebido en el SKU del modelo ('Model KF556C36BBEK2'
                  donde 'C36' es el CL después de la frecuencia codificada).
    
    Validación: el CL razonable está entre 10 y 60. Cualquier número
    fuera de ese rango se descarta como falso positivo.
    
    Devuelve -1 si no encuentra valor confiable.
    Complejidad: O(k) donde k = len(title), amortizado O(1).
    """
    # Estrategia 1: CL explícito
    m = re.search(r'\bCL\s*(\d{1,2})\b', title, re.IGNORECASE)
    if m:
        cl = int(m.group(1))
        if 10 <= cl <= 60:
            return cl
    
    # Estrategia 2: parsear desde el SKU del modelo
    model_match = re.search(r'Model\s+([A-Z0-9-]+)', title, re.IGNORECASE)
    if model_match:
        sku = model_match.group(1)
        # Patrón flexible: dígito(s) + (C|HC) + 2 dígitos
        candidates = re.findall(r'\d+H?C(\d{2})', sku)
        valid_cls = [int(c) for c in candidates if 10 <= int(c) <= 60]
        if valid_cls:
            return valid_cls[0]
    
    return -1


def parse_ddr_type(title: str) -> str:
    """Detecta DDR3/DDR4/DDR5 con word boundary para evitar falsos positivos."""
    m = re.search(r'\bDDR([345])\b', title, re.IGNORECASE)
    return f"DDR{m.group(1)}" if m else "unknown"


def parse_form_factor(title: str) -> str:
    """SO-DIMM (laptop) vs DIMM (desktop). Default DIMM."""
    if re.search(r'\bSO[-\s]?DIMM\b', title, re.IGNORECASE):
        return "SO-DIMM"
    return "DIMM"


def parse_brand(title: str) -> str:
    """Primera palabra del título. Maneja repeticiones tipo 'Kingston Kingston'."""
    return title.split()[0] if title else "Unknown"


def parse_has_rgb(title: str) -> bool:
    """RGB o ARGB indicado en el título."""
    return bool(re.search(r'\b(A?RGB)\b', title, re.IGNORECASE))


# ════════════════════════════════════════════════════════════════
# SCRAPER · Función por página
# ════════════════════════════════════════════════════════════════

def scrape_page(page: int) -> list[RAMProduct]:
    """
    Extrae productos de una página. Tolerante a fallos por item.
    Complejidad: O(n × m) por página.
    """
    url = BASE_URL.format(page)
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
    except requests.RequestException as e:
        print(f"  ⚠ Error de red en página {page}: {e}")
        return []
    
    if resp.status_code != 200:
        print(f"  ⚠ Status {resp.status_code} en página {page}")
        return []
    
    soup = BeautifulSoup(resp.text, "lxml")
    items = soup.select(".item-cell")
    
    products = []
    for item in items:
        try:
            title_el = item.select_one("a.item-title")
            if title_el is None:
                continue
            
            title = title_el.text.strip()
            href = title_el.get("href", "")
            
            price = parse_price(item.select_one("li.price-current"))
            if price is None:
                continue  # skip sin precio
            
            product = RAMProduct(
                title=title,
                brand=parse_brand(title),
                source_url=href,
                ddr_type=parse_ddr_type(title),
                capacity_gb=parse_capacity_gb(title),
                speed_mhz=parse_speed_mhz(title),
                cas_latency=parse_cas_latency(title),
                num_sticks=parse_num_sticks(title),
                form_factor=parse_form_factor(title),
                has_rgb=parse_has_rgb(title),
                price_usd=price,
            )
            products.append(product)
        
        except Exception as e:
            print(f"  ⚠ Item saltado: {type(e).__name__}: {e}")
            continue
    
    return products


# ════════════════════════════════════════════════════════════════
# PIPELINE · Orquestación con checkpoints
# ════════════════════════════════════════════════════════════════

def run_scraper(max_pages: int = MAX_PAGES) -> pd.DataFrame:
    """Ejecuta el scraper completo con checkpoints cada N páginas."""
    all_products = []
    start_time = time.time()
    
    print(f"\n🚀 Iniciando scraping de Newegg RAM")
    print(f"   Páginas objetivo: {max_pages}")
    print(f"   Sleep entre requests: {SLEEP_BETWEEN_REQUESTS}s")
    print(f"   Checkpoint cada: {CHECKPOINT_EVERY} páginas\n")
    
    for page in range(1, max_pages + 1):
        page_start = time.time()
        products = scrape_page(page)
        page_time = time.time() - page_start
        
        all_products.extend(products)
        
        print(f"  [{page:2d}/{max_pages}] {len(products):2d} productos · "
              f"{page_time:.1f}s · acumulado: {len(all_products)}")
        
        if page % CHECKPOINT_EVERY == 0:
            checkpoint_path = DATA_DIR / f"ram_checkpoint_p{page}.csv"
            pd.DataFrame([asdict(p) for p in all_products]).to_csv(
                checkpoint_path, index=False
            )
            print(f"  💾 Checkpoint: {checkpoint_path}")
        
        if page < max_pages:
            time.sleep(SLEEP_BETWEEN_REQUESTS)
    
    total_time = time.time() - start_time
    print(f"\n✅ Scraping completado en {total_time:.1f}s "
          f"({total_time/max_pages:.1f}s/página promedio)")
    
    df = pd.DataFrame([asdict(p) for p in all_products])
    final_path = DATA_DIR / "ram_raw.csv"
    df.to_csv(final_path, index=False)
    print(f"💾 Dataset final: {final_path} ({len(df)} filas)")
    
    return df


# ════════════════════════════════════════════════════════════════
# AUDITORÍA · Reporte de calidad
# ════════════════════════════════════════════════════════════════

def audit_dataframe(df: pd.DataFrame) -> None:
    """Reporte de calidad del dataset extraído."""
    print("\n" + "═" * 60)
    print("📊 AUDITORÍA DE CALIDAD")
    print("═" * 60)
    
    print(f"\n• Total registros: {len(df)}")
    print(f"• Columnas: {len(df.columns)}")
    
    print(f"\n• Distribución por DDR:")
    print(df['ddr_type'].value_counts().to_string())
    
    print(f"\n• Top 5 marcas:")
    print(df['brand'].value_counts().head(5).to_string())
    
    print(f"\n• Precio (USD):")
    print(f"  - min:    ${df['price_usd'].min():.2f}")
    print(f"  - max:    ${df['price_usd'].max():.2f}")
    print(f"  - media:  ${df['price_usd'].mean():.2f}")
    print(f"  - mediana:${df['price_usd'].median():.2f}")
    
    print(f"\n• Cobertura de features:")
    coverage = {
        "ddr_type":    (df['ddr_type'] != 'unknown').mean() * 100,
        "capacity_gb": (df['capacity_gb'] > 0).mean() * 100,
        "speed_mhz":   (df['speed_mhz'] > 0).mean() * 100,
        "cas_latency": (df['cas_latency'] > 0).mean() * 100,
    }
    for feat, pct in coverage.items():
        symbol = "✅" if pct >= 85 else "⚠️ " if pct >= 70 else "❌"
        print(f"  {symbol} {feat:15s}: {pct:5.1f}%")
    
    print("\n" + "═" * 60)


# ════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    df = run_scraper(max_pages=MAX_PAGES)
    audit_dataframe(df)
