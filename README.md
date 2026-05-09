# 🧠 Optimización Asintótica en la Predicción del Mercado de Memoria RAM
 
> **Proyecto académico** · Universidad de Guadalajara · Mayo 2026
> **Autores:** 
-José Najera Ortiz
-Bernadro Mariel Perez
-Juan Pablo Cruz
-Diego 
> **Materia:** Ciencia de Datos · Asymptotic Notation + Bayesian Inference
 
Pipeline integral de Ciencia de Datos aplicado al mercado de memoria RAM: desde la extracción vía web scraping en Newegg hasta el análisis de complejidad computacional y modelado predictivo. El proyecto integra programación, bases de datos SQL, estadística, matemáticas aplicadas y análisis asintótico bajo un sprint comprimido de 12 días.
 
---
 
## 🎯 Pregunta de investigación
 
> ¿Qué variables técnicas de un módulo de RAM (capacidad, frecuencia, tipo DDR, latencia CAS, marca) son los predictores más fuertes del precio de mercado, y cómo se reduce la complejidad computacional del pipeline desde 𝒪(n) hasta 𝒪(1) en cada etapa del análisis?
 
---
 
## 📅 Estado del Sprint (12 días · deadline 19-may-2026)
 
| Día | Fecha | Sprint | Estado |
|---|---|---|---|
| 1 | jue 7 may | Reconocimiento de Newegg + setup del entorno | ✅ Completo |
| 2 | vie 8 may | Scraper de producción + parsers regex | ✅ Completo |
| 3 | sáb 9 may | Limpieza y feature engineering | ⏳ Próximo |
| 4 | dom 10 may | SQLite + benchmark de complejidad O() | ⏳ |
| 5 | lun 11 may | Análisis exploratorio (EDA) | ⏳ |
| 6 | mar 12 may | Modelo 1 — Regresión lineal multivariada | ⏳ |
| 7 | mié 13 may | Modelo 2 — K-Means clustering | ⏳ |
| 8 | jue 14 may | Análisis empírico de complejidad | ⏳ |
| 9 | vie 15 may | Diseño del póster académico | ⏳ |
| 10 | sáb 16 may | Redacción y pulido del póster | ⏳ |
| 11 | dom 17 may | Ensayo de defensa oral | ⏳ |
| 12 | lun 18 may | Buffer + ensayo final | ⏳ |
| 🎯 | **mar 19 may** | **Entrega + defensa oral** | 🔒 |
 
---
 
## 📊 Resultados actuales (cierre Día 2)
 
### Dataset extraído
 
| Métrica | Valor |
|---|---|
| **Total productos** | 180 |
| **Páginas scrapeadas** | 15 |
| **Tiempo de extracción** | ~45-50 s |
| **Tiempo promedio por página** | ~3 s |
| **Bloqueos / errores** | 0 |
 
### Cobertura de features críticas
 
| Feature | Cobertura | Estado |
|---|---|---|
| `ddr_type` | 100.0% | ✅ |
| `capacity_gb` | 100.0% | ✅ |
| `speed_mhz` | 100.0% | ✅ |
| `cas_latency` | 90.6% | ✅ (después de v3 del parser) |
 
### Distribución del dataset
 
```
DDR4: 75 productos (41.7%)
DDR5: 105 productos (58.3%)
 
Top 5 marcas:
  CORSAIR     59
  Team        59
  Kingston    31
  G.SKILL     17
  V-COLOR     14
 
Precio (USD):
  min      $157.99
  max     $2,799.99
  media    $438.56
  mediana  $296.99
```
 
---
 
## 🛠️ Stack tecnológico
 
| Capa | Herramientas |
|---|---|
| **Web Scraping** | `requests` + `BeautifulSoup4` + `lxml` |
| **Procesamiento** | `pandas` + `numpy` |
| **Modelado ML** *(próximo)* | `scikit-learn` (LinearRegression + KMeans) |
| **Persistencia** *(próximo)* | `SQLite` + `SQLAlchemy` |
| **Visualización** *(próximo)* | `matplotlib` + `seaborn` |
| **Versionado** | Git + GitHub |
 
---
 
## 🔬 Hallazgos técnicos clave
 
### 1. Bug de compresión Brotli (Día 1)
 
La librería `requests` de Python no descomprime el formato Brotli (`br`) sin el paquete adicional. Cuando Newegg recibe `Accept-Encoding: gzip, deflate, br` responde en Brotli y `requests` entrega un blob corrupto de ~58 KB en lugar de la página real (~1.2 MB).
 
**Solución:** forzar `gzip` removiendo `br` del header de negociación HTTP.
 
### 2. Fragmentación del DOM en el precio (Día 2)
 
Newegg presenta el precio fragmentado en dos elementos HTML por razones de renderizado tipográfico:
 
```html
<li class="price-current">
    <strong>309</strong>
    <sup>.99</sup>
</li>
```
 
Usar `.text` directamente sobre el contenedor producía contaminación con texto de descuentos y promociones. **Solución:** parser específico que reconstruye el `float` desde sus átomos del DOM, alcanzando 100% de cobertura.
 
### 3. CAS Latency embebido en SKU (Día 2)
 
Newegg dejó de exponer el CAS Latency como `CL{n}` legible en los títulos. Ahora aparece codificado dentro del SKU del fabricante:
 
| Fabricante | SKU | CL real |
|---|---|---|
| Kingston Fury | `KF556C36BBEK2-16` | 36 |
| XPG Lancer | `AX5U6000C3016G-DCLABK` | 30 |
| Corsair | `CMW32GX4M2E3200C16` | 16 |
| Crucial Pro | `CP2K32G60C40U5W` | 40 |
| Patriot Viper | `PVV564G600C36K` | 36 |
| Team T-Force | `TF3D432G3200HC16FDC01` | 16 |
 
**Solución:** parser dual con estrategia en cascada:
 
1. **Estrategia 1** — buscar `CL\d+` explícito (compatibilidad con formatos legacy)
2. **Estrategia 2** — extraer patrón `\d+H?C\d{2}` del bloque `Model XXXX`
3. **Validación** — el CL aceptado debe estar en el rango razonable [10, 60]
**Impacto:** cobertura del feature `cas_latency` subió de 0% → 90.6%.
 
---
 
## 📁 Estructura del proyecto
 
```
Web_scraping/
├── README.md                  ← Este archivo
├── .gitignore                 ← Exclusiones de Git
│
├── scraper.py                 ← Scraper principal de producción (~250 líneas)
├── recalcular_cas.py          ← Reaplicar parser CL sin re-scrapear
│
├── test_parsers.py            ← Validación de los 7 parsers regex
├── test_minimo.py             ← Test aislado del parser CAS v3
│
├── diagnostico.py             ← Diagnóstico HTTP del Día 1 (Brotli)
├── diagnostico_cas.py         ← Diagnóstico de cobertura CL (Día 2)
│
├── web_scraping.py            ← Hello world inicial (Día 1, referencia)
│
└── data/                      ← Excluido del repo (regenerable)
    ├── ram_raw.csv            ← 180 productos extraídos
    ├── ram_raw_backup.csv     ← Backup defensivo del CSV
    └── ram_checkpoint_p*.csv  ← Checkpoints intermedios
```
 
---
 
## ⚙️ Reproducir el pipeline
 
### Requisitos previos
 
- Python 3.10 o superior
- ~50 s de tiempo de extracción
- Conexión a internet estable
### Setup del entorno
 
```bash
# Clonar el repo
git clone https://github.com/<usuario>/<repo>.git
cd <repo>
 
# Crear entorno virtual
python -m venv venv
 
# Activar venv
source venv/bin/activate          # Linux/Mac
venv\Scripts\activate             # Windows
 
# Instalar dependencias
pip install requests beautifulsoup4 lxml pandas numpy scikit-learn \
            matplotlib seaborn sqlalchemy jupyter
```
 
### Ejecutar el scraper
 
```bash
# Extracción completa (15 páginas × 12 productos = ~180 SKUs)
python scraper.py
 
# Validación aislada de los regex parsers
python test_parsers.py
python test_minimo.py
 
# Si quieres recalcular CL sin re-scrapear:
python recalcular_cas.py
```
 
### Salida esperada
 
```
🚀 Iniciando scraping de Newegg RAM
   Páginas objetivo: 15
   Sleep entre requests: 2.5s
   ...
✅ Scraping completado en ~45-50s
💾 Dataset final: data/ram_raw.csv (180 filas)
 
📊 AUDITORÍA DE CALIDAD
✅ ddr_type       : 100.0%
✅ capacity_gb    : 100.0%
✅ speed_mhz      : 100.0%
✅ cas_latency    :  90.6%
```
 
---
 
## 🧮 Análisis asintótico del pipeline
 
El proyecto entero cuenta una historia única: **cada etapa reduce la complejidad efectiva**, demostrando los conceptos de Asymptotic Notation aplicados a un caso real.
 
```
EXTRACCIÓN  · 𝒪(n · t_red)   → scraping secuencial dominado por I/O
LIMPIEZA    · 𝒪(n)           → regex amortizado 𝒪(1) por fila
SQL SCAN    · 𝒪(n)           → búsqueda sin índice
SQL B-TREE  · 𝒪(log n)       → búsqueda con índice (próximo)
INFERENCIA  · 𝒪(1)           → modelo entrenado, predicción constante (próximo)
```
 
La **medición empírica** de estos tiempos será evidencia central del póster académico final.
 
---
 
## 📚 Decisiones de diseño defendibles
 
Cada decisión técnica fue tomada con criterio académico justificable:
 
- **`dataclass` en lugar de `dict`:** impone tipado estricto desde el origen y evita bugs silenciosos como `cas_latency` siendo `str` en algunas filas. Filosofía contract-driven.
- **`try/except` por item, no por página:** granularidad de fallo correcta. Perder 1 producto cuesta 1 fila; abortar la página perdería 12. Filosofía *fail soft, log loud*.
- **`time.sleep(2.5)` sin paralelismo:** los sitios web son I/O bound, no CPU bound. Paralelizar desde la misma IP solo acelera el bloqueo. La constante de espera es el costo de operar éticamente.
- **Checkpoints intermedios cada 5 páginas:** misma lógica que un commit incremental en Git. Si Newegg me bloquea en página 12, ya tengo seguros los datos de las páginas 1-10.
- **Rutas con `Path(__file__).parent`:** robustez ante CWD distintos. Práctica de portabilidad estándar.
---
 
## 🔮 Próximas etapas
 
- **Día 3:** limpieza, manejo de outliers, imputación condicional de `cas_latency` faltante por mediana de DDR, normalización de marcas Top-5.
- **Día 4:** carga a SQLite, creación de índices B-Tree, benchmark empírico pre/post indexación con `EXPLAIN QUERY PLAN`.
- **Día 5-8:** EDA estadístico, regresión lineal multivariada, K-Means clustering por segmento de mercado, medición empírica de complejidad O().
- **Día 9-11:** póster académico A1 + ensayo de defensa oral.
---
 
## 📖 Referencias y aprendizajes documentados
 
- Cormen, Leiserson, Rivest & Stein. *Introduction to Algorithms* — para el marco asintótico.
- Documentación de `requests` sobre [content negotiation](https://requests.readthedocs.io/) — origen del bug de Brotli.
- Convenciones de SKU de fabricantes (Kingston, Corsair, G.Skill, XPG, Crucial, Patriot, Team Group) — derivadas empíricamente del scraping.
---
 
## 📝 Licencia
 
Proyecto académico de uso educativo. El código se puede reusar bajo MIT License. Los datos extraídos pertenecen a Newegg.com y se usan únicamente con fines académicos no comerciales.
 
---
 
> *"Programar bien no es tener todo perfecto al primer intento — es saber diagnosticar, ajustar y documentar el aprendizaje."*
