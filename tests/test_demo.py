"""Tests for running the integrated demo."""

from autobot.demo import ejecutar_demo


def test_ejecutar_demo_devuelve_informe() -> None:
    """The demo should generate a report with a global score."""

    resultado = ejecutar_demo()
    assert "Puntaje global" in resultado
    assert "Evaluación de la sesión" in resultado
