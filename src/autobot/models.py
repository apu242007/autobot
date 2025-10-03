"""Modelos de datos centrales para el sistema de simulación."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Literal, Optional


class PersonalidadCliente(str, Enum):
    """Enumeración de personalidades disponibles para los clientes simulados."""

    ENOJADO_IMPACIENTE = "enojado_impaciente"
    ANSIOSO_DETALLISTA = "ansioso_detallista"
    SARCASTICO_EXIGENTE = "sarcastico_exigente"
    CONFUNDIDO_AMABLE = "confundido_amable"
    PROFESIONAL_DIRECTO = "profesional_directo"
    AGRESIVO_DEMANDANTE = "agresivo_demandante"
    RESIGNADO_CANSADO = "resignado_cansado"


class CanalComunicacion(str, Enum):
    """Canales de comunicación soportados por la simulación."""

    WHATSAPP = "whatsapp"
    EMAIL = "email"
    CHAT = "chat"
    TELEFONO = "telefono"


@dataclass
class EscenarioObra:
    """Representa un escenario realista dentro de la industria de construcción."""

    id: str
    titulo: str
    descripcion: str
    complejidad: Literal["baja", "media", "alta"]
    area: str
    palabras_clave: List[str]
    solucion_esperada: str
    tiempo_estimado_resolucion: int


@dataclass
class ConfiguracionSimulacion:
    """Parámetros iniciales que definen una simulación."""

    personalidad: PersonalidadCliente
    canal: CanalComunicacion
    escenario: EscenarioObra
    timestamp_inicio: datetime
    duracion_maxima: int = 20
    nivel_dificultad: float = 0.7


@dataclass
class MensajeConversacion:
    """Unidad básica del diálogo entre cliente y agente."""

    turno: int
    rol: Literal["cliente", "agente"]
    contenido: str
    timestamp: datetime
    metadatos: Dict[str, str] = field(default_factory=dict)


@dataclass
class ContextoConversacion:
    """Estado completo de la conversación en curso."""

    sesion_id: str
    configuracion: ConfiguracionSimulacion
    estado_actual: Literal["iniciando", "en_progreso", "resolviendo", "finalizado"]
    historial: List[MensajeConversacion] = field(default_factory=list)
    datos_clave_mencionados: Dict[str, bool] = field(default_factory=dict)
    emociones_cliente: List[str] = field(default_factory=list)


@dataclass
class EvidenciaEvaluacion:
    """Fragmento textual que respalda un puntaje obtenido."""

    criterio: str
    turno: int
    extracto: str
    impacto: Literal["positivo", "negativo", "neutral"]


@dataclass
class CriterioEvaluacion:
    """Resultado asociado a un criterio individual de la rúbrica."""

    nombre: str
    puntaje: int
    peso: float
    justificacion: str
    evidencias: List[EvidenciaEvaluacion]


@dataclass
class ResultadoEvaluacion:
    """Informe integral que resume la evaluación del desempeño."""

    sesion_id: str
    timestamp_evaluacion: datetime
    personalidad_cliente: PersonalidadCliente
    canal: CanalComunicacion
    escenario: EscenarioObra
    criterios: List[CriterioEvaluacion]
    puntaje_global: float
    fortalezas: List[str]
    oportunidades_mejora: List[str]
    recomendaciones: List[str]
    metricas: Dict[str, Optional[float]]
    resumen_ejecutivo: str
