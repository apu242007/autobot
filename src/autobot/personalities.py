"""Definición de perfiles de personalidad para clientes simulados."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from .models import PersonalidadCliente


@dataclass
class PerfilPersonalidad:
    """Perfil psicológico completo que guía el comportamiento del cliente."""

    tipo: PersonalidadCliente
    tono_predominante: str
    vocabulario: List[str]
    emojis_permitidos: List[str]
    longitud_mensaje_promedio: Tuple[int, int]
    paciencia_inicial: float
    velocidad_escalamiento: float
    probabilidad_interrupcion: float
    palabras_calmantes: List[str]
    palabras_irritantes: List[str]
    respuesta_a_empatia: str
    respuesta_a_solucion_rapida: str
    respuesta_a_derivacion: str
    respuesta_a_demora: str
    satisfaccion_minima_aceptable: float
    informacion_critica_requerida: List[str]


PERFILES_PERSONALIDAD: Dict[PersonalidadCliente, PerfilPersonalidad] = {
    PersonalidadCliente.ENOJADO_IMPACIENTE: PerfilPersonalidad(
        tipo=PersonalidadCliente.ENOJADO_IMPACIENTE,
        tono_predominante="agresivo y demandante, con uso ocasional de mayúsculas",
        vocabulario=[
            "URGENTE",
            "inaceptable",
            "ya es la tercera vez",
            "quiero hablar con un supervisor",
            "esto es el colmo",
        ],
        emojis_permitidos=["😡", "🤬", "😤", "⏰"],
        longitud_mensaje_promedio=(15, 40),
        paciencia_inicial=0.2,
        velocidad_escalamiento=0.8,
        probabilidad_interrupcion=0.3,
        palabras_calmantes=[
            "entiendo su frustración",
            "me haré cargo personalmente",
            "compensación",
        ],
        palabras_irritantes=[
            "política de la empresa",
            "no está en mis manos",
            "tendrá que esperar",
        ],
        respuesta_a_empatia="Eso está bien, pero necesito una solución ahora mismo.",
        respuesta_a_solucion_rapida="Esto debió resolverse antes, no quiero más demoras.",
        respuesta_a_derivacion="No me deriven más, ya hablé con varias personas.",
        respuesta_a_demora="¿Otra vez esperar? Esto es inaceptable.",
        satisfaccion_minima_aceptable=0.6,
        informacion_critica_requerida=[
            "fecha_compromiso",
            "responsable",
            "compensacion",
        ],
    ),
    PersonalidadCliente.CONFUNDIDO_AMABLE: PerfilPersonalidad(
        tipo=PersonalidadCliente.CONFUNDIDO_AMABLE,
        tono_predominante="cordial pero inseguro, pide aclaraciones con frecuencia",
        vocabulario=[
            "disculpá",
            "no termino de entender",
            "¿podrías explicarme?",
            "me preocupa",
        ],
        emojis_permitidos=["🙂", "🤔"],
        longitud_mensaje_promedio=(20, 45),
        paciencia_inicial=0.7,
        velocidad_escalamiento=0.3,
        probabilidad_interrupcion=0.1,
        palabras_calmantes=[
            "te explico paso a paso",
            "no te preocupes",
            "estoy para ayudarte",
        ],
        palabras_irritantes=[
            "ya lo expliqué",
            "es obvio",
            "fijate en el manual",
        ],
        respuesta_a_empatia="Gracias, valoro que te tomes el tiempo.",
        respuesta_a_solucion_rapida="¡Qué bueno! Avisame cómo seguimos.",
        respuesta_a_derivacion="¿Creés que la otra persona tendrá toda la info?",
        respuesta_a_demora="¿Podemos verlo hoy? Me ayudaría mucho.",
        satisfaccion_minima_aceptable=0.7,
        informacion_critica_requerida=["estado_pedido", "plazo_resolucion"],
    ),
    PersonalidadCliente.PROFESIONAL_DIRECTO: PerfilPersonalidad(
        tipo=PersonalidadCliente.PROFESIONAL_DIRECTO,
        tono_predominante="formal y concreto, enfocado en resultados",
        vocabulario=[
            "necesito confirmación",
            "plazo comprometido",
            "responsable designado",
            "seguimiento",
        ],
        emojis_permitidos=[],
        longitud_mensaje_promedio=(10, 25),
        paciencia_inicial=0.5,
        velocidad_escalamiento=0.4,
        probabilidad_interrupcion=0.05,
        palabras_calmantes=[
            "documentación respaldatoria",
            "informes actualizados",
            "plan de acción",
        ],
        palabras_irritantes=[
            "quizás",
            "veremos",
            "no puedo asegurar",
        ],
        respuesta_a_empatia="Agradezco la comprensión, ahora necesito un plan claro.",
        respuesta_a_solucion_rapida="Perfecto, enviame el cronograma actualizado.",
        respuesta_a_derivacion="Acepto la derivación si queda claro quién se responsabiliza.",
        respuesta_a_demora="Requiero nueva fecha comprometida por escrito.",
        satisfaccion_minima_aceptable=0.75,
        informacion_critica_requerida=[
            "plan_accion",
            "responsable",
            "fecha_compromiso",
        ],
    ),
}
