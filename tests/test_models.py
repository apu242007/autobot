"""Pruebas básicas para los modelos del sistema."""

import asyncio
from datetime import UTC, datetime

import pytest

from autobot.context import AlmacenamientoEnMemoria, GestorContexto
from autobot.evaluation import AnalizadorConversacion, RubricaEvaluacion
from autobot.models import (
    CanalComunicacion,
    ConfiguracionSimulacion,
    ContextoConversacion,
    MensajeConversacion,
    PersonalidadCliente,
)
from autobot.scenarios import ESCENARIOS_OBRA


class DummyLLM:
    """Cliente LLM que devuelve respuestas deterministas para pruebas."""

    async def generate(
        self, prompt: str, *, temperature: float, max_tokens: int
    ) -> str:  # noqa: D401
        del prompt, temperature, max_tokens
        return (
            "PUNTAJE: 4\n"
            "JUSTIFICACION: Respuesta de ejemplo consistente.\n"
            "EVIDENCIAS:\n"
            '- Turno 1: "Mensaje" (impacto=positivo)'
        )


@pytest.fixture()
def contexto() -> ContextoConversacion:
    configuracion = ConfiguracionSimulacion(
        personalidad=PersonalidadCliente.ENOJADO_IMPACIENTE,
        canal=CanalComunicacion.CHAT,
        escenario=ESCENARIOS_OBRA[0],
        timestamp_inicio=datetime.now(UTC),
    )
    return ContextoConversacion(
        sesion_id="test",
        configuracion=configuracion,
        historial=[
            MensajeConversacion(
                turno=1,
                rol="cliente",
                contenido="Necesito ayuda urgente",
                timestamp=datetime.now(UTC),
            ),
            MensajeConversacion(
                turno=2,
                rol="agente",
                contenido="Te ayudo a continuación",
                timestamp=datetime.now(UTC),
            ),
        ],
        estado_actual="en_progreso",
    )


def test_escenarios_disponibles() -> None:
    assert len(ESCENARIOS_OBRA) >= 4


def test_evaluacion_generica(contexto: ContextoConversacion) -> None:
    analizador = AnalizadorConversacion(DummyLLM(), RubricaEvaluacion())
    resultado = asyncio_run(analizador.evaluar_conversacion(contexto))
    assert resultado.puntaje_global > 0


def asyncio_run(coro):
    """Ejecuta una corrutina dentro del loop de pruebas."""

    return asyncio.run(coro)


def test_gestor_contexto(contexto: ContextoConversacion) -> None:
    almacenamiento = AlmacenamientoEnMemoria()
    gestor = GestorContexto(almacenamiento)
    gestor.inicializar_contexto(contexto)
    mensaje = MensajeConversacion(
        turno=3,
        rol="cliente",
        contenido="Pedido #12345 hace 5 días",
        timestamp=datetime.now(UTC),
    )
    gestor.agregar_mensaje(contexto.sesion_id, mensaje)
    contexto_recuperado = gestor.obtener_contexto(contexto.sesion_id)
    assert contexto_recuperado.datos_clave_mencionados["numero_pedido"]
    assert contexto_recuperado.datos_clave_mencionados["fecha_problema"]
