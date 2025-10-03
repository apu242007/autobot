"""Motor de evaluación y rúbrica para medir el desempeño del agente."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Dict, Iterable, List, Protocol, Tuple

from .models import (
    ContextoConversacion,
    CriterioEvaluacion,
    EvidenciaEvaluacion,
    ResultadoEvaluacion,
)


class LLMClient(Protocol):
    """Interfaz mínima requerida para interactuar con un modelo de lenguaje."""

    async def generate(
        self, prompt: str, *, temperature: float, max_tokens: int
    ) -> str:
        """Genera una respuesta a partir de un prompt."""


@dataclass
class DefinicionCriterio:
    """Encapsula la configuración de un criterio de evaluación."""

    peso: float
    descripcion: str
    escala: Dict[int, str]
    indicadores_positivos: Iterable[str]
    indicadores_negativos: Iterable[str]


class RubricaEvaluacion:
    """Define los criterios que se aplican durante la evaluación."""

    def __init__(self) -> None:
        self.criterios: Dict[str, DefinicionCriterio] = {
            "empatia_y_tono": DefinicionCriterio(
                peso=0.18,
                descripcion="Capacidad de conectar emocionalmente con el cliente",
                escala={
                    1: "Sin empatía. Respuestas frías o robotizadas.",
                    2: "Empatía mínima y poco personalizada.",
                    3: "Empatía moderada con reconocimiento parcial del impacto.",
                    4: "Buena empatía con validación emocional clara.",
                    5: "Empatía excepcional y proactiva.",
                },
                indicadores_positivos=[
                    "Usa el nombre del cliente",
                    "Reconoce específicamente el problema",
                    "Valida emociones",
                    "Pide disculpas genuinas",
                ],
                indicadores_negativos=[
                    "Ignora el tono emocional",
                    "Usa plantillas genéricas",
                    "No ofrece disculpas",
                    "Adopta un tono defensivo",
                ],
            ),
            "claridad_y_comunicacion": DefinicionCriterio(
                peso=0.15,
                descripcion="Mensajes comprensibles, bien estructurados y sin ambigüedades",
                escala={
                    1: "Mensajes confusos o con contradicciones.",
                    2: "Información desordenada que requiere aclaraciones.",
                    3: "Comunicación aceptable con algunas dudas.",
                    4: "Mensajes claros y completos.",
                    5: "Comunicación impecable con resúmenes y énfasis correctos.",
                },
                indicadores_positivos=[
                    "Uso de listas",
                    "Resumen de pasos",
                    "Lenguaje simple",
                    "Confirmación de entendimiento",
                ],
                indicadores_negativos=[
                    "Respuestas ambiguas",
                    "Uso excesivo de jerga",
                    "Falta de estructura",
                    "Bloques extensos sin separación",
                ],
            ),
            "resolucion_y_proactividad": DefinicionCriterio(
                peso=0.20,
                descripcion="Capacidad de resolver el problema o avanzar hacia la solución",
                escala={
                    1: "No ofrece solución y deriva sin ownership.",
                    2: "Propuestas vagas o insuficientes.",
                    3: "Solución correcta pero con esfuerzo del cliente.",
                    4: "Solución concreta y responsable.",
                    5: "Solución excepcional con alternativas y anticipación.",
                },
                indicadores_positivos=[
                    "Ofrece solución temprana",
                    "Propone alternativas",
                    "Asume responsabilidad",
                    "Ofrece compensación",
                    "Entrega plazos concretos",
                ],
                indicadores_negativos=[
                    "Deriva sin intento",
                    "Soluciones vagas",
                    "Sin compensación",
                    "Sin comprometer plazos",
                ],
            ),
        }

    def obtener(self, nombre: str) -> DefinicionCriterio:
        return self.criterios[nombre]

    def nombres(self) -> Iterable[str]:
        return self.criterios.keys()


class AnalizadorConversacion:
    """Evalúa conversaciones completas para generar informes estructurados."""

    def __init__(
        self, llm_client: LLMClient, rubrica: RubricaEvaluacion | None = None
    ) -> None:
        self._llm = llm_client
        self._rubrica = rubrica or RubricaEvaluacion()

    async def evaluar_conversacion(
        self, contexto: ContextoConversacion
    ) -> ResultadoEvaluacion:
        criterios_evaluados: List[CriterioEvaluacion] = []
        for nombre in self._rubrica.nombres():
            definicion = self._rubrica.obtener(nombre)
            criterios_evaluados.append(
                await self._evaluar_criterio(contexto, nombre, definicion)
            )

        puntaje_global = sum(
            criterio.puntaje * criterio.peso * 20 for criterio in criterios_evaluados
        )
        fortalezas, oportunidades = self._extraer_fortalezas_oportunidades(
            criterios_evaluados
        )
        recomendaciones = self._generar_recomendaciones(oportunidades)

        metricas = {
            "turnos_totales": len(contexto.historial),
            "turnos_hasta_empatia": None,
            "turnos_hasta_solucion": None,
            "confirmaciones_entendimiento": 0,
            "interrupciones": 0,
            "tiempo_respuesta_promedio": 0.0,
        }

        resumen = self._generar_resumen_ejecutivo(
            puntaje_global, fortalezas, oportunidades
        )

        return ResultadoEvaluacion(
            sesion_id=contexto.sesion_id,
            timestamp_evaluacion=datetime.now(UTC),
            personalidad_cliente=contexto.configuracion.personalidad,
            canal=contexto.configuracion.canal,
            escenario=contexto.configuracion.escenario,
            criterios=criterios_evaluados,
            puntaje_global=puntaje_global,
            fortalezas=fortalezas,
            oportunidades_mejora=oportunidades,
            recomendaciones=recomendaciones,
            metricas=metricas,
            resumen_ejecutivo=resumen,
        )

    async def _evaluar_criterio(
        self,
        contexto: ContextoConversacion,
        nombre: str,
        definicion: DefinicionCriterio,
    ) -> CriterioEvaluacion:
        prompt = self._construir_prompt(contexto, nombre, definicion)
        respuesta = await self._llm.generate(prompt, temperature=0.3, max_tokens=800)
        puntaje, justificacion, evidencias = self._parsear_respuesta(respuesta, nombre)
        return CriterioEvaluacion(
            nombre=nombre,
            puntaje=puntaje,
            peso=definicion.peso,
            justificacion=justificacion,
            evidencias=evidencias,
        )

    @staticmethod
    def _construir_prompt(
        contexto: ContextoConversacion,
        nombre: str,
        definicion: DefinicionCriterio,
    ) -> str:
        historial = "\n".join(
            f"Turno {mensaje.turno} ({mensaje.rol}): {mensaje.contenido}"
            for mensaje in contexto.historial
        )
        escala = "\n".join(
            f"{nivel}: {detalle}" for nivel, detalle in definicion.escala.items()
        )
        indicadores_positivos = "\n".join(
            f"- {texto}" for texto in definicion.indicadores_positivos
        )
        indicadores_negativos = "\n".join(
            f"- {texto}" for texto in definicion.indicadores_negativos
        )
        return (
            f"Evalúa el criterio {nombre} para la siguiente conversación.\n\n"
            f"Descripción: {definicion.descripcion}\n"
            f"Escala:\n{escala}\n\n"
            f"Indicadores positivos:\n{indicadores_positivos}\n\n"
            f"Indicadores negativos:\n{indicadores_negativos}\n\n"
            f"Conversación completa:\n{historial}\n\n"
            "Responde en formato estructurado:\n"
            "PUNTAJE: <número>\n"
            "JUSTIFICACION: <texto>\n"
            "EVIDENCIAS:\n"
            '- Turno <número>: "cita literal" (impacto=<positivo|negativo|neutral>)'
        )

    @staticmethod
    def _parsear_respuesta(
        respuesta: str, criterio: str
    ) -> Tuple[int, str, List[EvidenciaEvaluacion]]:
        puntaje_match = re.search(r"PUNTAJE:\s*(\d)", respuesta)
        if puntaje_match is None:
            raise ValueError(
                f"No se encontró puntaje en la respuesta del criterio {criterio}"
            )
        puntaje = int(puntaje_match.group(1))

        justificacion_match = re.search(
            r"JUSTIFICACION:\s*(.+?)(?:\nEVIDENCIAS:|$)", respuesta, re.S
        )
        if justificacion_match is None:
            raise ValueError(
                f"No se encontró justificación en la respuesta del criterio {criterio}"
            )
        justificacion = justificacion_match.group(1).strip()

        evidencias: List[EvidenciaEvaluacion] = []
        for coincidencia in re.finditer(
            r"- Turno (\d+): \"(.+?)\" \(impacto=(positivo|negativo|neutral)\)",
            respuesta,
        ):
            evidencias.append(
                EvidenciaEvaluacion(
                    criterio=criterio,
                    turno=int(coincidencia.group(1)),
                    extracto=coincidencia.group(2),
                    impacto=coincidencia.group(3),
                )
            )

        return puntaje, justificacion, evidencias

    @staticmethod
    def _extraer_fortalezas_oportunidades(
        criterios: Iterable[CriterioEvaluacion],
    ) -> Tuple[List[str], List[str]]:
        fortalezas = [
            f"{criterio.nombre} destacado con puntaje {criterio.puntaje}/5"
            for criterio in criterios
            if criterio.puntaje >= 4
        ]
        oportunidades = [
            f"Mejorar {criterio.nombre} (puntaje {criterio.puntaje}/5)"
            for criterio in criterios
            if criterio.puntaje <= 3
        ]
        return fortalezas, oportunidades

    @staticmethod
    def _generar_recomendaciones(oportunidades: Iterable[str]) -> List[str]:
        return [f"Desarrollar plan específico para: {texto}" for texto in oportunidades]

    @staticmethod
    def _generar_resumen_ejecutivo(
        puntaje_global: float, fortalezas: List[str], oportunidades: List[str]
    ) -> str:
        encabezado = (
            "Desempeño general bueno" if puntaje_global >= 70 else "Desempeño a mejorar"
        )
        fortalezas_texto = (
            ", ".join(fortalezas) if fortalezas else "sin fortalezas destacadas"
        )
        oportunidades_texto = (
            ", ".join(oportunidades) if oportunidades else "sin oportunidades críticas"
        )
        return (
            f"{encabezado}. Puntaje global {puntaje_global:.1f}/100."
            f" Fortalezas: {fortalezas_texto}."
            f" Oportunidades: {oportunidades_texto}."
        )
