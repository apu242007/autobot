"""Gestión de contexto y utilidades auxiliares para la simulación."""

from __future__ import annotations

import json
import re
from dataclasses import asdict
from datetime import UTC, datetime
from enum import Enum
from typing import Dict, Iterable, List, Optional

from .models import ContextoConversacion, MensajeConversacion


class GestorContexto:
    """Mantiene el estado de la conversación con soporte de almacenamiento externo."""

    def __init__(self, almacenamiento, ventana_contexto: int = 10) -> None:
        self._almacenamiento = almacenamiento
        self._ventana_contexto = ventana_contexto

    def agregar_mensaje(self, sesion_id: str, mensaje: MensajeConversacion) -> None:
        """Agrega un mensaje al historial y actualiza los datos persistidos."""

        contexto = self.obtener_contexto(sesion_id)
        contexto.historial.append(mensaje)

        if mensaje.rol == "cliente":
            self._extraer_datos_clave(contexto, mensaje.contenido)

        self._guardar_contexto(sesion_id, contexto)

    def obtener_contexto(self, sesion_id: str) -> ContextoConversacion:
        """Recupera el contexto desde el almacenamiento o crea uno vacío."""

        datos = self._almacenamiento.get(self._clave(sesion_id))
        if datos is None:
            raise KeyError(f"No existe contexto para la sesión {sesion_id!r}")

        if isinstance(datos, bytes):
            datos = datos.decode("utf-8")
        payload = json.loads(datos)
        return _contexto_desde_dict(payload)

    def obtener_contexto_para_llm(self, sesion_id: str) -> str:
        """Construye una representación textual de los últimos turnos."""

        contexto = self.obtener_contexto(sesion_id)
        mensajes_recientes = contexto.historial[-self._ventana_contexto :]
        lineas: List[str] = ["# HISTORIAL DE CONVERSACIÓN:"]
        for mensaje in mensajes_recientes:
            rol = "TÚ (Cliente)" if mensaje.rol == "cliente" else "AGENTE"
            lineas.append(f"[Turno {mensaje.turno}] {rol}:\n{mensaje.contenido}\n")
        return "\n".join(lineas)

    def inicializar_contexto(self, contexto: ContextoConversacion) -> None:
        """Persiste un contexto recién creado."""

        self._guardar_contexto(contexto.sesion_id, contexto)

    def _guardar_contexto(self, sesion_id: str, contexto: ContextoConversacion) -> None:
        payload = json.dumps(asdict(contexto), default=_serializar_valor)
        self._almacenamiento.setex(self._clave(sesion_id), 86400, payload)

    @staticmethod
    def _extraer_datos_clave(contexto: ContextoConversacion, texto: str) -> None:
        """Extrae identificadores relevantes a partir de la conversación."""

        if re.findall(r"#[\w-]+", texto):
            contexto.datos_clave_mencionados["numero_pedido"] = True

        if any(palabra in texto.lower() for palabra in ("hace", "días", "semanas")):
            contexto.datos_clave_mencionados["fecha_problema"] = True

    @staticmethod
    def _clave(sesion_id: str) -> str:
        return f"contexto:{sesion_id}"


class AlmacenamientoEnMemoria:
    """Implementación simple que emula las operaciones esenciales de Redis."""

    def __init__(self) -> None:
        self._datos: Dict[str, Dict[str, str]] = {}

    def get(self, clave: str) -> Optional[str]:
        elemento = self._datos.get(clave)
        if elemento is None:
            return None
        return elemento["valor"]

    def setex(self, clave: str, _ttl: int, valor: str) -> None:  # noqa: D401
        self._datos[clave] = {
            "valor": valor,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    def items(self) -> Iterable:
        return self._datos.items()


def _serializar_valor(valor):  # noqa: D401
    if isinstance(valor, datetime):
        return valor.isoformat()
    if isinstance(valor, Enum):
        return valor.value
    raise TypeError(f"Tipo no serializable: {type(valor)!r}")


def _contexto_desde_dict(payload: Dict) -> ContextoConversacion:
    configuracion = payload["configuracion"]
    escenario = configuracion["escenario"]
    from .models import (
        CanalComunicacion,
        ConfiguracionSimulacion,
        EscenarioObra,
        PersonalidadCliente,
    )

    contexto = ContextoConversacion(
        sesion_id=payload["sesion_id"],
        configuracion=ConfiguracionSimulacion(
            personalidad=PersonalidadCliente(configuracion["personalidad"]),
            canal=CanalComunicacion(configuracion["canal"]),
            escenario=EscenarioObra(**escenario),
            duracion_maxima=configuracion.get("duracion_maxima", 20),
            nivel_dificultad=configuracion.get("nivel_dificultad", 0.7),
            timestamp_inicio=datetime.fromisoformat(configuracion["timestamp_inicio"]),
        ),
        historial=[
            MensajeConversacion(
                turno=entrada["turno"],
                rol=entrada["rol"],
                contenido=entrada["contenido"],
                timestamp=datetime.fromisoformat(entrada["timestamp"]),
                metadatos=entrada.get("metadatos", {}),
            )
            for entrada in payload.get("historial", [])
        ],
        estado_actual=payload["estado_actual"],
        datos_clave_mencionados=payload.get("datos_clave_mencionados", {}),
        emociones_cliente=payload.get("emociones_cliente", []),
    )
    return contexto
