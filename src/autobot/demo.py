"""Utilidades para ejecutar una simulación de ejemplo del sistema Autobot."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from typing import Iterable

from .commands import construir_sistema_comandos
from .context import AlmacenamientoEnMemoria, GestorContexto
from .evaluation import LLMClient
from .models import MensajeConversacion


class LLMDePrueba(LLMClient):
    """Cliente de LLM determinista pensado para pruebas manuales."""

    async def generate(  # type: ignore[override]
        self, prompt: str, *, temperature: float, max_tokens: int
    ) -> str:
        """Genera una respuesta predecible compatible con el motor de evaluación."""

        _ = (prompt, temperature, max_tokens)
        return (
            "PUNTAJE: 4\n"
            "JUSTIFICACION: Evaluación simulada para el criterio analizado.\n"
            "EVIDENCIAS:\n"
            '- Turno 2: "El agente ofreció una solución concreta." (impacto=positivo)\n'
            '- Turno 4: "Se resumieron los próximos pasos." (impacto=positivo)'
        )


async def _generar_historial_demo(gestor: GestorContexto, sesion_id: str) -> None:
    """Carga un intercambio básico entre cliente y agente para la demo."""

    mensajes: Iterable[MensajeConversacion] = (
        MensajeConversacion(
            turno=1,
            rol="cliente",
            contenido=(
                "Hola, hice un pedido de acero y aún no tengo confirmación de entrega. "
                "¿Pueden ayudarme?"
            ),
            timestamp=datetime.now(UTC),
        ),
        MensajeConversacion(
            turno=2,
            rol="agente",
            contenido=(
                "Hola, lamento la demora. Verifiqué el pedido y el camión sale hoy a las "
                "16:00 con seguimiento en tiempo real."
            ),
            timestamp=datetime.now(UTC),
        ),
        MensajeConversacion(
            turno=3,
            rol="cliente",
            contenido="Perfecto, gracias por la confirmación y el horario exacto.",
            timestamp=datetime.now(UTC),
        ),
        MensajeConversacion(
            turno=4,
            rol="agente",
            contenido=(
                "Queda agendado el envío y te contactaré cuando llegue al obrador. "
                "¿Necesitas algo más?"
            ),
            timestamp=datetime.now(UTC),
        ),
    )

    for mensaje in mensajes:
        gestor.agregar_mensaje(sesion_id, mensaje)


async def _ejecutar_demo_asincrona() -> str:
    """Orquesta la simulación de ejemplo completa y devuelve el informe final."""

    almacenamiento = AlmacenamientoEnMemoria()
    gestor = GestorContexto(almacenamiento)
    llm = LLMDePrueba()
    sistema = construir_sistema_comandos(gestor, llm)

    sesion_id = "demo-local"
    inicio = await sistema.procesar("comenzar test", sesion_id)
    await _generar_historial_demo(gestor, sesion_id)
    informe = await sistema.procesar("/finalizar", sesion_id)

    return f"{inicio}\n\n{informe}"


def ejecutar_demo() -> str:
    """Ejecuta la demo en un nuevo bucle de eventos y devuelve el resultado."""

    return asyncio.run(_ejecutar_demo_asincrona())


if __name__ == "__main__":
    print(ejecutar_demo())
