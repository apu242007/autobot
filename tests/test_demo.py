"""Pruebas para la ejecución de la demo integrada."""

from autobot.demo import ejecutar_demo


def test_ejecutar_demo_devuelve_informe() -> None:
    """La demo debe generar un informe con puntaje global."""

    resultado = ejecutar_demo()
    assert "Puntaje global" in resultado
    assert "Evaluación de la sesión" in resultado
