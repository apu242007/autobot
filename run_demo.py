"""Punto de entrada sencillo para ejecutar la demo sin instalar el paquete."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> None:
    """Ejecuta la demo asegurando que ``src`` esté en ``sys.path``."""

    proyecto = Path(__file__).resolve().parent
    ruta_src = proyecto / "src"
    if ruta_src.exists():
        ruta_str = str(ruta_src)
        if ruta_str not in sys.path:
            sys.path.insert(0, ruta_str)

    from autobot.demo import ejecutar_demo

    print(ejecutar_demo())


if __name__ == "__main__":
    main()
