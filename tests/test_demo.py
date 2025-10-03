"""Pruebas para la ejecución de la demo integrada."""

import os
import subprocess
import sys
from pathlib import Path

from autobot.demo import ejecutar_demo


def test_ejecutar_demo_devuelve_informe() -> None:
    """La demo debe generar un informe con puntaje global."""

    resultado = ejecutar_demo()
    assert "Puntaje global" in resultado
    assert "Evaluación de la sesión" in resultado


def test_paquete_exponible_como_modulo() -> None:
    """Permite ejecutar la demo con `python -m autobot`."""

    entorno = os.environ.copy()
    pythonpath = entorno.get("PYTHONPATH", "")
    ruta_src = str(Path("src").resolve())
codex/add-documentation-for-chatbot-evaluation-system-vvbk9l
    entorno["PYTHONPATH"] = (
        f"{ruta_src}{os.pathsep}{pythonpath}" if pythonpath else ruta_src
    )
=======
    entorno["PYTHONPATH"] = (f"{ruta_src}{os.pathsep}{pythonpath}" if pythonpath else ruta_src)
main

    proceso = subprocess.run(
        [sys.executable, "-m", "autobot"],
        check=True,
        capture_output=True,
        text=True,
        env=entorno,
    )
    assert "Puntaje global" in proceso.stdout
codex/add-documentation-for-chatbot-evaluation-system-vvbk9l


def test_script_run_demo_se_ejecuta_desde_raiz() -> None:
    """El script ``run_demo.py`` debe funcionar sin modificar PYTHONPATH."""

    proceso = subprocess.run(
        [sys.executable, "run_demo.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Puntaje global" in proceso.stdout
=======
main
