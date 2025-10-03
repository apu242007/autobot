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
    entorno["PYTHONPATH"] = (f"{ruta_src}{os.pathsep}{pythonpath}" if pythonpath else ruta_src)

    proceso = subprocess.run(
        [sys.executable, "-m", "autobot"],
        check=True,
        capture_output=True,
        text=True,
        env=entorno,
    )
    assert "Puntaje global" in proceso.stdout
