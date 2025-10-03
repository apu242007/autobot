"""Sistema de comandos para controlar simulaciones y evaluaciones."""

from __future__ import annotations

import random
from datetime import UTC, datetime

from .context import GestorContexto
from .evaluation import AnalizadorConversacion, RubricaEvaluacion
from .models import (
    CanalComunicacion,
    ConfiguracionSimulacion,
    ContextoConversacion,
    PersonalidadCliente,
)
from .personalities import PERFILES_PERSONALIDAD
from .scenarios import ESCENARIOS_OBRA


class SistemaComandos:
    """Procesa comandos administrativos recibidos durante la simulación."""

    def __init__(
        self, gestor_contexto: GestorContexto, analizador: AnalizadorConversacion
    ) -> None:
        self._gestor_contexto = gestor_contexto
        self._analizador = analizador

    async def procesar(self, comando: str, sesion_id: str) -> str:
        """Despacha la ejecución del comando solicitado."""

        comando_normalizado = comando.strip().lower()
        if comando_normalizado == "comenzar test":
            return self._iniciar_simulacion(sesion_id)
        if comando_normalizado == "/finalizar":
            return await self._finalizar_simulacion(sesion_id)
        raise ValueError(f"Comando no reconocido: {comando}")

    def _iniciar_simulacion(self, sesion_id: str) -> str:
        personalidad = random.choice(list(PersonalidadCliente))
        canal = random.choice(list(CanalComunicacion))
        escenario = random.choice(ESCENARIOS_OBRA)

        configuracion = ConfiguracionSimulacion(
            personalidad=personalidad,
            canal=canal,
            escenario=escenario,
            timestamp_inicio=datetime.now(UTC),
        )
        contexto = ContextoConversacion(
            sesion_id=sesion_id,
            configuracion=configuracion,
            estado_actual="iniciando",
        )
        self._gestor_contexto.inicializar_contexto(contexto)

        perfil = PERFILES_PERSONALIDAD.get(personalidad)
        mensaje_inicial = (
            "Inicia la conversación con tu cliente."
            if perfil is None
            else (
                f"Cliente {personalidad.value} listo para interactuar en {canal.value}."
            )
        )
        return (
            "✅ TEST INICIADO\n\n"
            f"🎭 Personalidad: {personalidad.value}\n"
            f"📱 Canal: {canal.value}\n"
            f"📋 Escenario: {escenario.titulo}\n\n"
            f"{mensaje_inicial}"
        )

    async def _finalizar_simulacion(self, sesion_id: str) -> str:
        contexto = self._gestor_contexto.obtener_contexto(sesion_id)
        resultado = await self._analizador.evaluar_conversacion(contexto)
        return self._formatear_informe(resultado)

    @staticmethod
    def _formatear_informe(resultado) -> str:
        encabezado = f"# Evaluación de la sesión {resultado.sesion_id}\n"
        puntaje = f"Puntaje global: {resultado.puntaje_global:.1f}/100\n"
        fortalezas = (
            "\n".join(f"- {texto}" for texto in resultado.fortalezas)
            or "- Sin fortalezas"
        )
        oportunidades = (
            "\n".join(f"- {texto}" for texto in resultado.oportunidades_mejora)
            or "- Sin oportunidades"
        )
        return (
            f"{encabezado}\n{puntaje}\n"
            "## Fortalezas\n"
            f"{fortalezas}\n\n"
            "## Oportunidades\n"
            f"{oportunidades}\n\n"
            f"## Resumen\n{resultado.resumen_ejecutivo}"
        )


def construir_sistema_comandos(gestor: GestorContexto, llm_client) -> SistemaComandos:
    """Facilita la creación del sistema de comandos con dependencias configuradas."""

    analizador = AnalizadorConversacion(llm_client, RubricaEvaluacion())
    return SistemaComandos(gestor, analizador)
