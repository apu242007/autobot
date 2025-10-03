"""Servidor HTTP sencillo para ejecutar la demo desde el navegador."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _parse_args() -> argparse.Namespace:
    """Define y procesa los argumentos disponibles."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1", help="Dirección de enlace")
    parser.add_argument("--port", type=int, default=8000, help="Puerto del servidor")
    return parser.parse_args()


def main() -> None:
    """Arranca el servidor HTTP y mantiene la ejecución hasta Ctrl+C."""

    proyecto = Path(__file__).resolve().parent
    ruta_src = proyecto / "src"
    if ruta_src.exists():
        ruta_str = str(ruta_src)
        if ruta_str not in sys.path:
            sys.path.insert(0, ruta_str)

    from autobot.web_demo import crear_servidor, obtener_directorio_estatico

    args = _parse_args()
    servidor = crear_servidor((args.host, args.port), obtener_directorio_estatico(proyecto))

    try:
        print(f"Sirviendo demo en http://{args.host}:{servidor.server_address[1]}")
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()
