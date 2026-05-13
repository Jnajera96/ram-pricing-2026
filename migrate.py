"""
migrate.py - Reestructura profesional del repositorio ram-pricing-2026

Mueve archivos a su nueva ubicacion profesional SIN tocar el codigo interno.
Los scripts siguen funcionando porque usan Path(__file__).parent que se adapta
automaticamente a la nueva ubicacion.

ESTRATEGIA DE SEGURIDAD:
  1. Modo --dry-run: simula los movimientos sin tocar nada
  2. Modo real: ejecuta los movimientos con confirmacion
  3. Modo --revert: deshace los cambios usando el log

EJECUCION:
  python migrate.py --dry-run    # Simulacion (no modifica nada)
  python migrate.py              # Ejecucion real (pide confirmacion)
  python migrate.py --revert     # Deshace el ultimo movimiento

Autor: Jose Najera - UDG - 2026
"""

import os
import sys
import shutil
import json
from pathlib import Path
from datetime import datetime

# ============================================================
# CONFIGURACION
# ============================================================

SCRIPT_DIR = Path(__file__).parent
LOG_FILE = SCRIPT_DIR / ".migration_log.json"

# Mapeo de movimientos: archivo_origen -> ruta_destino
MOVIMIENTOS = {
    # ===== SCRAPING (Dia 1-2) =====
    'scraper.py':              'src/01_scraping/scraper.py',
    'recalcular_cas.py':       'src/01_scraping/recalcular_cas.py',
    'web_scraping.py':         'src/01_scraping/web_scraping.py',

    # ===== DATA PROCESSING (Dia 3) =====
    'limpiar.py':              'src/02_data_processing/clean.py',
    'eda.py':                  'src/02_data_processing/eda.py',

    # ===== DATABASE (Dia 4) =====
    'crear_db.py':             'src/03_database/create_db.py',
    'crear_indices.py':        'src/03_database/create_indices.py',
    'bench_pre.py':            'src/03_database/benchmark_pre.py',
    'bench_post.py':           'src/03_database/benchmark_post.py',
    'bench_escalado.py':       'src/03_database/benchmark_scaling.py',

    # ===== INFERENCE (Dia 5) =====
    'inferencia.py':           'src/04_inference/normality_tests.py',
    'inferencia_bloque2.py':   'src/04_inference/ttest_ddr.py',
    'inferencia_bloque3.py':   'src/04_inference/anova_ddr.py',
    'inferencia_bloque4.py':   'src/04_inference/anova_brand.py',
    'inferencia_dashboard.py': 'src/04_inference/dashboard.py',

    # ===== MODELS (Dia 6-8) =====
    'regresion.py':            'src/05_models/ols.py',
    'kmeans.py':               'src/05_models/kmeans.py',
    'ridge.py':                'src/05_models/ridge.py',
    'random_forest.py':        'src/05_models/random_forest.py',
    'gradient_boosting.py':    'src/05_models/gradient_boosting.py',

    # ===== ANALYSIS (Dia 9) =====
    'complejidad_ml.py':       'src/06_analysis/ml_complexity.py',
    'dashboard_final.py':      'src/06_analysis/final_dashboard.py',

    # ===== TESTS =====
    'test_parsers.py':         'tests/test_parsers.py',
    'test_minimo.py':          'tests/test_minimo.py',
    'test_paginacion.py':      'tests/test_paginacion.py',

    # ===== ARCHIVE (diagnosticos historicos) =====
    'diagnostico.py':              'archive/diagnostico.py',
    'diagnostico_cas.py':          'archive/diagnostico_cas.py',
    'diagnostico_duplicados.py':   'archive/diagnostico_duplicados.py',
    'diagnostico_v2.py':           'archive/diagnostico_v2.py',
}

# Carpetas que se crean (con un __init__.py para hacerlas paquetes)
CARPETAS_CON_INIT = [
    'src',
    'src/01_scraping',
    'src/02_data_processing',
    'src/03_database',
    'src/04_inference',
    'src/05_models',
    'src/06_analysis',
    'tests',
]

# Carpetas que se crean sin __init__.py
CARPETAS_SIMPLES = [
    'archive',
    'docs',
    'scripts',
]


# ============================================================
# UTILIDADES VISUALES
# ============================================================

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_step(text):
    print(f"\n[*] {text}")


def print_success(text):
    print(f"  [OK] {text}")


def print_warning(text):
    print(f"  [!] {text}")


def print_error(text):
    print(f"  [X] {text}")


# ============================================================
# FUNCIONES PRINCIPALES
# ============================================================

def crear_carpetas(dry_run=False):
    """Crea todas las carpetas nuevas necesarias."""
    print_step("Creando estructura de carpetas...")

    todas_las_carpetas = CARPETAS_CON_INIT + CARPETAS_SIMPLES
    creadas = []

    for carpeta in todas_las_carpetas:
        ruta = SCRIPT_DIR / carpeta
        if not ruta.exists():
            if not dry_run:
                ruta.mkdir(parents=True, exist_ok=True)
            print_success(f"Carpeta: {carpeta}/")
            creadas.append(carpeta)
        else:
            print_warning(f"Ya existe: {carpeta}/")

    # Crear __init__.py en carpetas que lo necesitan
    print_step("Creando archivos __init__.py...")
    for carpeta in CARPETAS_CON_INIT:
        init_file = SCRIPT_DIR / carpeta / "__init__.py"
        if not init_file.exists():
            if not dry_run:
                init_file.write_text("", encoding='utf-8')
            print_success(f"__init__.py en: {carpeta}/")

    return creadas


def mover_archivos(dry_run=False):
    """Mueve cada archivo a su nueva ubicacion."""
    print_step("Moviendo archivos a su nueva ubicacion...")

    movimientos_exitosos = []
    movimientos_fallidos = []

    for origen, destino in MOVIMIENTOS.items():
        origen_path = SCRIPT_DIR / origen
        destino_path = SCRIPT_DIR / destino

        if not origen_path.exists():
            print_warning(f"NO EXISTE (se omite): {origen}")
            continue

        # Verificar que la carpeta destino existe
        if not destino_path.parent.exists():
            if not dry_run:
                destino_path.parent.mkdir(parents=True, exist_ok=True)

        # Verificar que no se sobrescriba algo
        if destino_path.exists() and not dry_run:
            print_warning(f"DESTINO YA EXISTE (se omite): {destino}")
            movimientos_fallidos.append((origen, destino, "destino existe"))
            continue

        # Hacer el movimiento
        try:
            if not dry_run:
                shutil.move(str(origen_path), str(destino_path))
            print_success(f"{origen} -> {destino}")
            movimientos_exitosos.append({'origen': origen, 'destino': destino})
        except Exception as e:
            print_error(f"FALLO {origen}: {e}")
            movimientos_fallidos.append((origen, destino, str(e)))

    return movimientos_exitosos, movimientos_fallidos


def guardar_log(movimientos):
    """Guarda un log JSON con todos los movimientos para poder revertir."""
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'movimientos': movimientos,
    }
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)
    print_success(f"Log guardado: {LOG_FILE.name}")


def revertir():
    """Deshace los movimientos del ultimo run usando el log."""
    print_header("MODO REVERT - Deshaciendo movimientos anteriores")

    if not LOG_FILE.exists():
        print_error("No se encontro log de migracion. Nada que revertir.")
        return

    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        log_data = json.load(f)

    print(f"\nLog del: {log_data['timestamp']}")
    print(f"Movimientos a revertir: {len(log_data['movimientos'])}")

    respuesta = input("\n¿Confirmar revert? [s/N]: ").strip().lower()
    if respuesta != 's':
        print_warning("Revert cancelado por el usuario")
        return

    print_step("Deshaciendo movimientos...")
    revertidos = 0
    for mov in reversed(log_data['movimientos']):
        origen_actual = SCRIPT_DIR / mov['destino']  # Lo que ahora es destino
        destino_original = SCRIPT_DIR / mov['origen']  # Volver al origen

        if origen_actual.exists():
            try:
                shutil.move(str(origen_actual), str(destino_original))
                print_success(f"{mov['destino']} -> {mov['origen']}")
                revertidos += 1
            except Exception as e:
                print_error(f"FALLO al revertir {mov['destino']}: {e}")
        else:
            print_warning(f"No existe en destino: {mov['destino']}")

    print_step(f"Revertidos: {revertidos}/{len(log_data['movimientos'])}")

    if revertidos == len(log_data['movimientos']):
        LOG_FILE.unlink()
        print_success("Log eliminado")


def listar_archivos_no_mapeados():
    """Lista archivos .py en la raiz que NO estan en el mapeo (alerta)."""
    print_step("Verificando archivos no mapeados...")

    archivos_raiz = [f.name for f in SCRIPT_DIR.iterdir()
                     if f.is_file() and f.suffix == '.py']

    archivos_mapeados = set(MOVIMIENTOS.keys())
    archivos_mapeados.add('migrate.py')  # Este script no se mueve

    no_mapeados = [f for f in archivos_raiz if f not in archivos_mapeados]

    if no_mapeados:
        print_warning(f"Archivos .py en raiz NO mapeados ({len(no_mapeados)}):")
        for archivo in no_mapeados:
            print(f"      - {archivo}")
        print_warning("Estos archivos NO se moveran. Verifica si quieres incluirlos.")
    else:
        print_success("Todos los archivos .py de la raiz estan mapeados")


# ============================================================
# MAIN
# ============================================================

def main():
    args = sys.argv[1:]
    dry_run = '--dry-run' in args
    revert = '--revert' in args
    skip_confirmation = '--yes' in args

    if revert:
        revertir()
        return

    if dry_run:
        print_header("MODO DRY-RUN (simulacion sin cambios reales)")
    else:
        print_header("MIGRACION REAL DEL REPOSITORIO")

    # Verificacion de seguridad
    if not dry_run and not skip_confirmation:
        print("\nESTRATEGIA:")
        print(f"  - Mover {len(MOVIMIENTOS)} archivos a estructura profesional")
        print(f"  - Crear {len(CARPETAS_CON_INIT) + len(CARPETAS_SIMPLES)} carpetas nuevas")
        print(f"  - Generar log de movimientos para poder revertir")
        print(f"\nDIRECTORIO: {SCRIPT_DIR}")

        respuesta = input("\n¿Continuar con la migracion? [s/N]: ").strip().lower()
        if respuesta != 's':
            print_warning("Migracion cancelada por el usuario")
            return

    # Verificar archivos no mapeados antes de empezar
    listar_archivos_no_mapeados()

    # 1. Crear carpetas
    crear_carpetas(dry_run=dry_run)

    # 2. Mover archivos
    exitosos, fallidos = mover_archivos(dry_run=dry_run)

    # 3. Guardar log (solo si NO es dry-run)
    if not dry_run and exitosos:
        guardar_log(exitosos)

    # 4. Reporte final
    print_header("REPORTE FINAL")
    print(f"\n  Movimientos exitosos: {len(exitosos)}")
    print(f"  Movimientos fallidos: {len(fallidos)}")

    if fallidos:
        print("\n  DETALLE DE FALLOS:")
        for origen, destino, razon in fallidos:
            print(f"    - {origen} -> {destino} ({razon})")

    if dry_run:
        print("\n  [MODO DRY-RUN] No se hicieron cambios reales.")
        print("  Si todo se ve bien, ejecuta:")
        print("    python migrate.py")
    else:
        print("\n  [OK] Migracion completada.")
        print("\n  Proximos pasos:")
        print("    1. Verifica con: dir src tests archive")
        print("    2. Confirma que cada script aun funciona desde su nueva ubicacion")
        print("    3. Si todo OK: git add -A && git commit -m 'Restructure to professional layout'")
        print("    4. Si algo fallo: python migrate.py --revert")


if __name__ == "__main__":
    main()