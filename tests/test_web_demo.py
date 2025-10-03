"""Pruebas para el servidor HTTP de la demo web."""

from __future__ import annotations

import json
import threading
import time
import urllib.request
from http.server import ThreadingHTTPServer
from typing import Iterator

import pytest

from autobot.web_demo import crear_servidor, obtener_directorio_estatico


@pytest.fixture()
def servidor_demo() -> Iterator[ThreadingHTTPServer]:
    """Levanta el servidor en un hilo paralelo y lo cierra al finalizar."""

    directorio_estatico = obtener_directorio_estatico()
    servidor = crear_servidor(("127.0.0.1", 0), directorio_estatico)

    hilo = threading.Thread(target=servidor.serve_forever, daemon=True)
    hilo.start()

    # Esperar a que el servidor esté listo.
    time.sleep(0.1)

    yield servidor

    servidor.shutdown()
    hilo.join(timeout=5)
    servidor.server_close()


def test_api_demo_devuelve_informe(servidor_demo) -> None:
    """El endpoint ``/api/demo`` retorna un informe en formato JSON."""

    _, puerto = servidor_demo.server_address
    with urllib.request.urlopen(f"http://127.0.0.1:{puerto}/api/demo") as respuesta:
        assert respuesta.status == 200
        datos = json.loads(respuesta.read().decode("utf-8"))

    assert "report" in datos
    assert "Evaluación" in datos["report"]
