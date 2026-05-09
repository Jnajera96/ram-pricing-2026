# 🧠 Optimización Asintótica en la Predicción del Mercado de Memoria RAM

> **Proyecto académico** · Universidad de Guadalajara · Mayo 2026
> **Autor:** José Carmen Najera Ortiz (coordinador técnico)
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
| 3 | sáb 9 may | Limpieza, feature engineering y EDA visual | ✅ Completo |
| 4 | dom 10 may | SQLite + benchmark de complejidad O() | ⏳ Próximo |
| 5 | lun 11 may | Análisis estadístico inferencial | ⏳ |
| 6 | mar 12 may | Modelo 1 — Regresión lineal multivariada | ⏳ |
| 7 | mié 13 may | Modelo 2 — K-Means clustering | ⏳ |
| 8 | jue 14 may | Análisis empírico de complejidad | ⏳ |
| 9 | vie 15 may | Diseño del póster académico | ⏳ |
| 10 | sáb 16 may | Redacción y pulido del póster | ⏳ |
| 11 | dom 17 may | Ensayo de defensa oral | ⏳ |
| 12 | lun 18 may | Buffer + ensayo final | ⏳ |
| 🎯 | **mar 19 may** | **Entrega + defensa oral** | 🔒 |

**Progreso actual: 33% · 5 commits · 0 bloqueos**

---

## 📊 Resultados actuales (cierre Día 3)

### Dataset extraído y limpio

| Métrica | Día 2 (raw) | Día 3 (clean) |
|---|---|---|
| **Total productos** | 359 | **350** |
| **Filas duplicadas** | 0 (deduplicación 0.8%) | 0 |
| **Tipos DDR distintos** | 4 (3 + unknown) | **3** (DDR3, DDR4, DDR5) |
| **Marcas únicas (originales)** | 25+ | 5 + Other |
| **Tiempo de extracción** | ~38 s | — |
| **Columnas finales** | 12 | **17** (con features derivados) |

### Cobertura final de features (Día 3)

| Feature | Cobertura | Estado |
|---|---|---|
| `ddr_type` | 100.0% | ✅ |
| `capacity_gb` | 100.0% | ✅ |
| `speed_mhz` | 99.7% | ✅ |
| `cas_latency_imputed` | 100.0% | ✅ (imputación condicional) |
| `brand_normalized` | 100.0% | ✅ |
| `price_per_gb` | 100.0% | ✅ |
| `log_price` | 100.0% | ✅ |

### Distribución del dataset limpio

```
Tipos DDR:
  DDR5: 229 productos (65.4%) · gama actual
  DDR4: 110 productos (31.4%) · mainstream
  DDR3:  11 productos  (3.2%) · legacy

Top marcas (Top-5 + Other):
  CORSAIR    103
  Other      100
  G.SKILL     59
  Kingston    43
  Team        24
  Crucial     21

Estadísticas de precio:
  min:        $14.51
  max:     $4,999.99
  media:     $503.12
  mediana:   $409.99
  std:       $510.50

Estadísticas de price_per_gb:
  min:    $2.75 / GB   (RAM económica DDR3)
  max:   $27.73 / GB   (premium DDR5)
  media: $13.16 / GB   (mercado balanceado)
```

### Hallazgos estadísticos del Día 3

**Correlaciones más fuertes con `price_usd`:**

| Variable | Pearson r | Interpretación |
|---|---|---|
| `capacity_gb` | **0.95** | Predictor dominante (R²≈0.90) |
| `log_price` | 0.78 | Validación de la transformación |
| `price_per_gb` | 0.56 | Feature derivado útil para clustering |
| `cas_latency_imputed` | 0.45 | Importa más en escala log (0.69) |
| `num_sticks` | 0.41 | Captura efecto kit dual/quad-channel |
| `speed_mhz` | 0.37 | Sube a 0.58 con log_price |

**Validación de la transformación logarítmica:**

```
Asimetría price_usd:  +3.61   ← muy asimétrica (cola pesada)
Asimetría log_price:  -0.61   ← prácticamente normal
```

La asimetría se reduce ~6× tras aplicar `log(1+x)`, cumpliendo el supuesto de normalidad aproximada de los residuos requerido por el teorema de Gauss-Markov.

---

## 🛠️ Stack tecnológico

| Capa | Herramientas |
|---|---|
| **Web Scraping** | `requests` + `BeautifulSoup4` + `lxml` |
| **Procesamiento** | `pandas` + `numpy` |
| **Visualización** | `matplotlib` + `seaborn` |
| **Modelado ML** *(próximo)* | `scikit-learn` (LinearRegression + KMeans) |
| **Persistencia** *(Día 4)* | `SQLite` + `SQLAlchemy` |
| **Versionado** | Git + GitHub |

---

## 🔬 Hallazgos técnicos clave

Cinco historias técnicas documentadas que demuestran resiliencia y rigor del pipeline.

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
| **G.SKILL (DDR5)** | **`F5-6000J3636F32GX2-RS5K`** | **36** (patrón `J####`) |
| **CORSAIR moderno** | **`CMK16GX5M2B5200Z40`** | **40** (patrón `Z##`) |

**Solución:** parser **v4** con cuádruple estrategia en cascada:

1. **Estrategia 1** — buscar `CL\d+` explícito (compatibilidad legacy)
2. **Estrategia 2** — extraer patrón `\d+H?C\d{2}` del bloque `Model XXXX`
3. **Estrategia 3** — patrón G.SKILL `J\d{2}\d{2}` (los primeros 2 dígitos son el CL)
4. **Estrategia 4** — patrón CORSAIR moderno `Z\d{2}` al final del SKU
5. **Validación** — el CL aceptado debe estar en el rango razonable [10, 60]

**Impacto:** cobertura del feature `cas_latency` subió de **0% → 85.5% nativo → 100% tras imputación**.

### 4. Bug de paginación rota en Newegg (Día 3)

Durante el análisis exploratorio se detectó que el dataset original presentaba **duplicación masiva**: 180 filas con solo 12 productos únicos (cada producto aparecía 15 veces, una por cada página scrapeada). La URL original (`/Memory/Category/ID-17`) ignoraba el parámetro `&page=N` y devolvía siempre la misma primera página.

**Diagnóstico:** se probaron empíricamente 4 URLs alternativas comparando los primeros productos de páginas consecutivas. Tres URLs respondieron correctamente, una falló (la original).

**Solución:** adoptar la URL de búsqueda con filtros `https://www.newegg.com/p/pl?N=100007611%204131&page={N}` que sí respeta paginación. Resultado: **dataset multiplicado por 30× (12 → 359 productos únicos)**, con 3 generaciones de DDR (incluyendo DDR3 legacy) y 4× más diversidad de marcas.

Esta validación de paginación es ahora un paso obligatorio del pipeline.

### 5. Imputación bayesiana ligera de `cas_latency` (Día 3)

51 productos (~14.5%) no tenían CAS Latency detectable ni en el título ni en el SKU. En lugar de eliminar las filas (sesgo) o imputar con la media global (incorrecto), se aplicó **imputación condicional por mediana de DDR**:

```
DDR3: CL=10  ← prior informativo legacy
DDR4: CL=16  ← prior informativo mainstream
DDR5: CL=36  ← prior informativo actual
```

Esta es la versión simplificada de un razonamiento bayesiano: incorporar conocimiento del dominio (las latencias típicas por generación) como **prior informativo** en lugar de tratar el missing data como aleatorio. El flag `cas_was_imputed` permite diferenciar valores observados vs imputados para análisis posterior.

---

## 📁 Estructura del proyecto

```
Web_scraping/
├── README.md                       ← Este archivo
├── .gitignore                      ← Exclusiones de Git
│
├── Scraping de producción
│   ├── scraper.py                  ← Scraper principal (~250 líneas)
│   └── recalcular_cas.py           ← Reaplicar parser CL sin re-scrapear
│
├── Pipeline de datos (Día 3)
│   ├── limpiar.py                  ← Pipeline de limpieza completo
│   └── eda.py                      ← EDA visual + 3 figuras
│
├── Tests y validación
│   ├── test_parsers.py             ← Validación de los 7 parsers regex
│   ├── test_minimo.py              ← Test aislado del parser CAS v3
│   └── test_paginacion.py          ← Test de URLs alternativas Newegg
│
├── Diagnósticos y debugging
│   ├── diagnostico.py              ← HTTP debugging (Día 1, Brotli)
│   ├── diagnostico_cas.py          ← Cobertura CAS (Día 2)
│   ├── diagnostico_duplicados.py   ← Detección de duplicación (Día 3)
│   └── diagnostico_v2.py           ← Análisis post re-scraping (Día 3)
│
├── Referencia histórica
│   └── web_scraping.py             ← Hello world inicial (Día 1)
│
├── figures/                        ← Visualizaciones a 300 DPI
│   ├── 01_correlation_heatmap.png
│   ├── 02_price_by_ddr.png
│   └── 03_log_transform.png
│
└── data/                           ← Excluido del repo (regenerable)
    ├── ram_raw.csv                 ← Dataset original 350 productos
    ├── ram_clean.csv               ← Dataset limpio (Día 3)
    ├── ram_raw_backup.csv          ← Backup defensivo
    └── ram_checkpoint_p*.csv       ← Checkpoints intermedios
```

---

## ⚙️ Reproducir el pipeline

### Requisitos previos

- Python 3.10 o superior
- ~40 segundos para scraping completo
- Conexión a internet estable

### Setup del entorno

```bash
# Clonar el repo
git clone https://github.com/Jnajera96/ram-pricing-2026.git
cd ram-pricing-2026

# Crear entorno virtual
python -m venv venv

# Activar venv
source venv/bin/activate          # Linux/Mac
venv\Scripts\activate             # Windows

# Instalar dependencias
pip install requests beautifulsoup4 lxml pandas numpy scikit-learn \
            matplotlib seaborn sqlalchemy jupyter
```

### Ejecutar el pipeline completo

```bash
# 1. Extracción (~40 s)
python scraper.py

# 2. Limpieza + Feature Engineering (~5 s)
python limpiar.py

# 3. EDA visual (genera 3 figuras en /figures/)
python eda.py

# (Opcional) Validación aislada
python test_parsers.py
python test_minimo.py
```

### Salida esperada

```
🚀 Iniciando scraping de Newegg RAM
   ...
✅ Scraping completado en ~38s
💾 Dataset final: data/ram_raw.csv (359 filas)

═════════════════════════════════════════════
🧹 LIMPIEZA Y FEATURE ENGINEERING
═════════════════════════════════════════════
  -7 filas removidas (4 unknown DDR + 3 capacity=0)
  Cobertura CL: 63.8% → 85.5% nativo → 100% imputado
  Asimetría: 3.61 → -0.61
✅ ram_clean.csv (350 filas × 17 columnas)

🎨 Generando 3 figuras a 300 DPI:
  ✅ figures/01_correlation_heatmap.png
  ✅ figures/02_price_by_ddr.png
  ✅ figures/03_log_transform.png
```

---

## 🧮 Análisis asintótico del pipeline

El proyecto entero cuenta una historia única: **cada etapa reduce la complejidad efectiva**, demostrando los conceptos de Asymptotic Notation aplicados a un caso real.

```
EXTRACCIÓN  · 𝒪(n · t_red)   → scraping secuencial dominado por I/O
LIMPIEZA    · 𝒪(n)           → regex amortizado 𝒪(1) por fila
SQL SCAN    · 𝒪(n)           → búsqueda sin índice (Día 4)
SQL B-TREE  · 𝒪(log n)       → búsqueda con índice (Día 4)
INFERENCIA  · 𝒪(1)           → modelo entrenado, predicción constante (Día 6)
```

La **medición empírica** de estos tiempos será evidencia central del póster académico final.

---

## 📖 Decisiones de diseño defendibles

Cada decisión técnica fue tomada con criterio académico justificable:

- **`dataclass` en lugar de `dict`:** impone tipado estricto desde el origen y evita bugs silenciosos como `cas_latency` siendo `str` en algunas filas. Filosofía contract-driven.

- **`try/except` por item, no por página:** granularidad de fallo correcta. Perder 1 producto cuesta 1 fila; abortar la página perdería 36. Filosofía *fail soft, log loud*.

- **`time.sleep(2.5)` sin paralelismo:** los sitios web son I/O bound, no CPU bound. Paralelizar desde la misma IP solo acelera el bloqueo. La constante de espera es el costo de operar éticamente.

- **Checkpoints intermedios cada 5 páginas:** misma lógica que un commit incremental en Git. Si Newegg me bloquea en página 8, ya tengo seguros los datos de las páginas 1-5.

- **Rutas con `Path(__file__).parent`:** robustez ante CWD distintos. Práctica de portabilidad estándar.

- **`log(1+x)` en lugar de `log(x)`:** robusto ante valores potenciales de 0 (no aplica en este dataset, pero es la mejor práctica).

- **Imputación condicional por mediana de DDR:** evita el sesgo de la media global y respeta la jerarquía de generaciones del hardware.

- **Backup defensivo antes de sobrescribir CSV:** lección aprendida del Día 2, ahora aplicada sistemáticamente en `limpiar.py`.

- **Validación empírica de paginación:** lección aprendida del Día 3. Antes de confiar en un endpoint paginado, comparar productos entre páginas 1, 2, 3 para validar que el servidor respeta el parámetro `&page=N`.

---

## 🔮 Próximas etapas

- **Día 4 (dom 10 may):** carga a SQLite, creación de índices B-Tree, benchmark empírico pre/post indexación con `EXPLAIN QUERY PLAN` y `time.perf_counter()`. Generar la **tabla y gráfica empírica de complejidad O(n) → O(log n)** que será el slide central del póster.
- **Día 5 (lun 11 may):** estadística inferencial, tests de hipótesis (¿DDR5 es significativamente más caro que DDR4?), análisis ANOVA por marca.
- **Día 6 (mar 12 may):** regresión lineal multivariada con one-hot encoding de marcas y DDR. Métricas R², MAE, RMSE.
- **Día 7 (mié 13 may):** K-Means clustering por segmento de mercado (precio_per_gb × cas_latency × capacity).
- **Día 8 (jue 14 may):** medición empírica de complejidad de los modelos ML.
- **Día 9-11 (vie 15 - dom 17):** póster A1 + ensayo de defensa oral.
- **Día 12 (lun 18 may):** buffer + ensayo final.

---

## 📈 Visualizaciones disponibles

Ver la carpeta `/figures/` para las 3 visualizaciones generadas en el Día 3:

1. **`01_correlation_heatmap.png`** — Matriz de correlación de Pearson entre todas las features numéricas. La gráfica estrella del proyecto.

2. **`02_price_by_ddr.png`** — Comparación lado a lado de boxplots en escala USD lineal vs `log(1+precio)`. Demuestra el premium DDR5 sobre DDR4 sobre DDR3 y la estabilización de varianza con la transformación log.

3. **`03_log_transform.png`** — Histogramas comparativos de la distribución original (asimetría +3.61) versus la log-transformada (asimetría -0.61). Justifica matemáticamente la transformación para regresión.

---

## 📚 Referencias y aprendizajes documentados

- **Cormen, Leiserson, Rivest & Stein.** *Introduction to Algorithms* — marco asintótico y complejidad.
- **Gauss-Markov theorem** — supuestos de normalidad de residuos en regresión OLS.
- **Pearson, K. (1895).** Coeficiente de asimetría — base de la decisión de transformación log.
- **Documentación de `requests`** sobre [content negotiation](https://requests.readthedocs.io/) — origen del bug de Brotli del Día 1.
- **Convenciones de SKU de fabricantes** (Kingston, Corsair, G.SKILL, XPG, Crucial, Patriot, Team Group) — derivadas empíricamente del scraping y documentadas.
- **JEDEC standards for DDR memory** — referencia de timings típicos por generación.

---

## 📝 Licencia

Proyecto académico de uso educativo. El código se puede reusar bajo MIT License. Los datos extraídos pertenecen a Newegg.com y se usan únicamente con fines académicos no comerciales.

---

> *"Programar bien no es tener todo perfecto al primer intento — es saber diagnosticar, ajustar y documentar el aprendizaje."*

**Última actualización:** sábado 9 de mayo de 2026 · cierre del Día 3 · 33% del sprint completado · 5 historias técnicas documentadas
