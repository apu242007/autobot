"""Servidor HTTP básico para exponer la demo en un navegador web."""

from __future__ import annotations

import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Tuple

from .demo import ejecutar_demo

Address = Tuple[str, int]


class _DemoRequestHandler(SimpleHTTPRequestHandler):
    """Atiende solicitudes HTTP y expone el endpoint ``/api/demo``."""

    directorio_estatico: Path

    def __init__(self, *args, directory: str | None = None, **kwargs) -> None:
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, format: str, *args) -> None:  # noqa: D401, N802
        """Silencia el log por consola del ``SimpleHTTPRequestHandler`` base."""

    def do_GET(self) -> None:  # noqa: N802
        """Gestiona solicitudes GET para recursos estáticos y la API."""

        if self.path in ("/", "/index.html"):
            self.path = "/demo.html"
            return super().do_GET()

        if self.path == "/api/demo":
            resultado = ejecutar_demo()
            payload = json.dumps({"report": resultado}, ensure_ascii=False).encode(
                "utf-8"
            )

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        return super().do_GET()


def obtener_directorio_estatico(base: Path | None = None) -> Path:
    """Devuelve el directorio desde donde se servirán los archivos estáticos."""

    raiz = base or Path(__file__).resolve().parents[2]
    directorio = raiz / "web"
    if not directorio.exists():
        raise FileNotFoundError(
            f"No se encontró el directorio estático esperado en {directorio}."
        )
    return directorio


def crear_servidor(
    direccion: Address, directorio_estatico: Path | None = None
) -> ThreadingHTTPServer:
    """Crea un servidor HTTP listo para ejecutarse con ``serve_forever``."""

    static_dir = directorio_estatico or obtener_directorio_estatico()

    class Handler(_DemoRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(static_dir), **kwargs)

    return ThreadingHTTPServer(direccion, Handler)


__all__ = ["crear_servidor", "obtener_directorio_estatico"]
