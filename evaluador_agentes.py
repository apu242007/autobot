#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chatbot Evaluador de Agentes
Simula clientes con diferentes personalidades y canales de comunicación
para evaluar el desempeño de agentes de servicio al cliente.
"""

import json
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum


class Personalidad(Enum):
    """Personalidades del cliente simulado"""
    ENOJADO = "enojado"
    ANSIOSO = "ansioso"
    NEUTRAL = "neutral"
    CONFUNDIDO = "confundido"
    IMPACIENTE = "impaciente"


class Canal(Enum):
    """Canales de comunicación"""
    WHATSAPP = "whatsapp"
    EMAIL = "email"
    CHAT = "chat"
    TELEFONO = "telefono"


class RubricaEvaluacion:
    """Define los criterios de evaluación"""
    
    CRITERIOS = {
        "empatia": {
            "descripcion": "Capacidad de comprender y responder a las emociones del cliente",
            "peso": 0.35
        },
        "claridad": {
            "descripcion": "Comunicación clara y fácil de entender",
            "peso": 0.30
        },
        "resolucion": {
            "descripcion": "Efectividad en resolver el problema del cliente",
            "peso": 0.35
        }
    }


class AdaptadorCanal:
    """Adapta el estilo de comunicación según el canal"""
    
    @staticmethod
    def adaptar_mensaje(mensaje: str, canal: Canal) -> str:
        """Adapta el mensaje al estilo del canal"""
        if canal == Canal.WHATSAPP:
            # WhatsApp: informal, uso de emojis, mensajes cortos
            emojis = ["😊", "👍", "🙏", "😔", "😤", "😰", "🤔", "⏰"]
            if random.random() > 0.5:
                mensaje += f" {random.choice(emojis)}"
            return mensaje
        
        elif canal == Canal.EMAIL:
            # Email: formal, estructura completa
            return f"Estimado/a,\n\n{mensaje}\n\nSaludos cordiales."
        
        elif canal == Canal.CHAT:
            # Chat: semi-informal, directo
            return mensaje
        
        elif canal == Canal.TELEFONO:
            # Teléfono: conversacional, más expresivo
            return f"[Tono de voz apropiado] {mensaje}"
        
        return mensaje
    
    @staticmethod
    def obtener_caracteristicas(canal: Canal) -> Dict:
        """Obtiene las características del canal"""
        caracteristicas = {
            Canal.WHATSAPP: {
                "longitud_mensaje": "corto",
                "formalidad": "informal",
                "velocidad": "rapida",
                "expresividad": "alta"
            },
            Canal.EMAIL: {
                "longitud_mensaje": "largo",
                "formalidad": "formal",
                "velocidad": "lenta",
                "expresividad": "baja"
            },
            Canal.CHAT: {
                "longitud_mensaje": "medio",
                "formalidad": "semi-formal",
                "velocidad": "rapida",
                "expresividad": "media"
            },
            Canal.TELEFONO: {
                "longitud_mensaje": "variable",
                "formalidad": "informal",
                "velocidad": "rapida",
                "expresividad": "muy alta"
            }
        }
        return caracteristicas.get(canal, {})


class ClienteSimulado:
    """Simula un cliente con personalidad específica"""
    
    def __init__(self, personalidad: Personalidad, canal: Canal, problema: str):
        self.personalidad = personalidad
        self.canal = canal
        self.problema = problema
        self.satisfaccion = 50  # 0-100
        self.paciencia = 100  # 0-100
        self.turnos = 0
        
    def generar_mensaje_inicial(self) -> str:
        """Genera el mensaje inicial del cliente"""
        mensajes_base = {
            Personalidad.ENOJADO: [
                f"¡Estoy HARTO! {self.problema} ¡Quiero una solución YA!",
                f"Esto es INACEPTABLE. {self.problema} ¿Qué van a hacer al respecto?",
                f"¡No puede ser! {self.problema} Llevo esperando mucho tiempo."
            ],
            Personalidad.ANSIOSO: [
                f"Hola, estoy muy preocupado... {self.problema} ¿Me pueden ayudar pronto?",
                f"Disculpe, necesito ayuda urgente. {self.problema} Estoy muy nervioso.",
                f"Por favor, {self.problema} ¿Cuánto tiempo tomará resolverlo?"
            ],
            Personalidad.NEUTRAL: [
                f"Hola, {self.problema} ¿Pueden ayudarme?",
                f"Buenos días, tengo un problema: {self.problema}",
                f"Necesito asistencia con lo siguiente: {self.problema}"
            ],
            Personalidad.CONFUNDIDO: [
                f"No entiendo bien... {self.problema} ¿Qué debo hacer?",
                f"Estoy perdido, {self.problema} ¿Me pueden explicar?",
                f"Disculpe, no sé cómo... {self.problema}"
            ],
            Personalidad.IMPACIENTE: [
                f"{self.problema} Necesito esto resuelto rápido.",
                f"Voy con prisa. {self.problema} ¿Tienen una solución rápida?",
                f"{self.problema} No tengo mucho tiempo."
            ]
        }
        
        mensaje = random.choice(mensajes_base[self.personalidad])
        return AdaptadorCanal.adaptar_mensaje(mensaje, self.canal)
    
    def generar_respuesta(self, mensaje_agente: str, evaluador) -> Tuple[str, bool]:
        """Genera respuesta basada en el mensaje del agente"""
        self.turnos += 1
        
        # Evaluar el mensaje del agente
        puntaje_turno = evaluador.evaluar_turno(mensaje_agente, self)
        
        # Actualizar estado emocional
        self.actualizar_estado(puntaje_turno)
        
        # Verificar si continuar o finalizar
        continuar = self.paciencia > 0 and self.turnos < 10
        
        if not continuar or self.satisfaccion > 80:
            return self._generar_despedida(), False
        
        # Generar respuesta según personalidad y estado
        respuesta = self._generar_respuesta_contextual(mensaje_agente, puntaje_turno)
        return AdaptadorCanal.adaptar_mensaje(respuesta, self.canal), True
    
    def actualizar_estado(self, puntaje: float):
        """Actualiza satisfacción y paciencia"""
        if puntaje > 70:
            self.satisfaccion += 15
            self.paciencia = min(100, self.paciencia + 10)
        elif puntaje > 50:
            self.satisfaccion += 5
        else:
            self.satisfaccion -= 10
            self.paciencia -= 20
    
    def _generar_respuesta_contextual(self, mensaje_agente: str, puntaje: float) -> str:
        """Genera respuesta contextual basada en el puntaje"""
        if self.personalidad == Personalidad.ENOJADO:
            if puntaje > 70:
                respuestas = [
                    "Bueno, eso suena mejor. ¿Y cuándo se resolverá?",
                    "Ok, al menos están haciendo algo. ¿Qué sigue?",
                    "Me parece bien, pero quiero confirmación escrita."
                ]
            else:
                respuestas = [
                    "¡Eso no es suficiente! ¡Necesito más que palabras!",
                    "¿En serio? ¡No me está ayudando en nada!",
                    "Esto es ridículo. ¿Tienen supervisor?"
                ]
        
        elif self.personalidad == Personalidad.ANSIOSO:
            if puntaje > 70:
                respuestas = [
                    "Oh, gracias... eso me tranquiliza un poco. ¿Pero está seguro?",
                    "Vale, pero ¿y si algo sale mal? ¿Qué hago?",
                    "Entiendo, muchas gracias. ¿Me avisarán cuando esté listo?"
                ]
            else:
                respuestas = [
                    "Ay no... no entiendo. Estoy más preocupado ahora...",
                    "¿Y si eso no funciona? ¿Qué hago entonces?",
                    "Me está poniendo más nervioso... ¿hay otra opción?"
                ]
        
        elif self.personalidad == Personalidad.NEUTRAL:
            if puntaje > 70:
                respuestas = [
                    "Entendido. ¿Cuál es el siguiente paso?",
                    "De acuerdo. ¿Cuánto tiempo tomará?",
                    "Perfecto. ¿Necesitan alguna información adicional?"
                ]
            else:
                respuestas = [
                    "No me queda claro. ¿Puede explicar mejor?",
                    "Entiendo, pero eso no resuelve mi problema.",
                    "Ok, pero ¿cuál es la solución concreta?"
                ]
        
        elif self.personalidad == Personalidad.CONFUNDIDO:
            if puntaje > 70:
                respuestas = [
                    "Ah ok, creo que voy entendiendo... ¿entonces debo...?",
                    "Vale, eso tiene más sentido. ¿Y después?",
                    "Gracias por explicar. ¿Podrían enviarme las instrucciones?"
                ]
            else:
                respuestas = [
                    "Sigo sin entender... ¿pueden explicarlo más simple?",
                    "Perdón, pero me confundí más. ¿Qué significa eso?",
                    "No sé de qué me habla... ¿tienen algún tutorial?"
                ]
        
        elif self.personalidad == Personalidad.IMPACIENTE:
            if puntaje > 70:
                respuestas = [
                    "Bien, pero que sea rápido por favor.",
                    "Ok, ¿cuánto tiempo exactamente?",
                    "Perfecto, proceda entonces. Rápido."
                ]
            else:
                respuestas = [
                    "Eso va a tomar mucho tiempo. ¿No hay algo más rápido?",
                    "No tengo tiempo para esto. ¿Solución express?",
                    "Muy lento. Necesito algo inmediato."
                ]
        
        else:
            respuestas = ["¿Y qué más?", "Continúe por favor."]
        
        return random.choice(respuestas)
    
    def _generar_despedida(self) -> str:
        """Genera mensaje de despedida según satisfacción"""
        if self.satisfaccion > 80:
            despedidas = [
                "Muchas gracias por su ayuda. Quedé satisfecho.",
                "Excelente servicio. Muchas gracias.",
                "Perfecto, problema resuelto. Gracias."
            ]
        elif self.satisfaccion > 50:
            despedidas = [
                "Bueno, supongo que está bien. Gracias.",
                "Ok, gracias por el tiempo.",
                "Entiendo. Gracias."
            ]
        else:
            despedidas = [
                "No me ayudaron en nada. Buscaré ayuda en otro lado.",
                "Qué servicio tan malo. Me voy.",
                "Esto fue una pérdida de tiempo."
            ]
        
        return random.choice(despedidas)


class Evaluador:
    """Evalúa el desempeño del agente"""
    
    def __init__(self):
        self.puntajes_turno = []
        self.historial_dialogo = []
        self.puntajes_criterios = {
            "empatia": [],
            "claridad": [],
            "resolucion": []
        }
    
    def evaluar_turno(self, mensaje_agente: str, cliente: ClienteSimulado) -> float:
        """Evalúa un turno individual del agente"""
        # Evaluación de empatía
        empatia = self._evaluar_empatia(mensaje_agente, cliente.personalidad)
        
        # Evaluación de claridad
        claridad = self._evaluar_claridad(mensaje_agente)
        
        # Evaluación de resolución
        resolucion = self._evaluar_resolucion(mensaje_agente, cliente.turnos)
        
        # Guardar puntajes
        self.puntajes_criterios["empatia"].append(empatia)
        self.puntajes_criterios["claridad"].append(claridad)
        self.puntajes_criterios["resolucion"].append(resolucion)
        
        # Calcular puntaje ponderado
        puntaje_total = (
            empatia * RubricaEvaluacion.CRITERIOS["empatia"]["peso"] +
            claridad * RubricaEvaluacion.CRITERIOS["claridad"]["peso"] +
            resolucion * RubricaEvaluacion.CRITERIOS["resolucion"]["peso"]
        )
        
        self.puntajes_turno.append(puntaje_total)
        return puntaje_total
    
    def _evaluar_empatia(self, mensaje: str, personalidad: Personalidad) -> float:
        """Evalúa la empatía del mensaje"""
        mensaje_lower = mensaje.lower()
        puntaje = 50  # Base
        
        # Palabras empáticas
        palabras_empaticas = [
            "entiendo", "comprendo", "lamento", "disculpa", "preocup",
            "ayudar", "tranquilo", "seguro", "confianza", "importante"
        ]
        
        for palabra in palabras_empaticas:
            if palabra in mensaje_lower:
                puntaje += 10
        
        # Reconocimiento de emoción según personalidad
        if personalidad == Personalidad.ENOJADO:
            if any(p in mensaje_lower for p in ["lamento", "disculpa", "entiendo su frustración"]):
                puntaje += 20
        
        elif personalidad == Personalidad.ANSIOSO:
            if any(p in mensaje_lower for p in ["tranquil", "no se preocupe", "seguro"]):
                puntaje += 20
        
        return min(100, puntaje)
    
    def _evaluar_claridad(self, mensaje: str) -> float:
        """Evalúa la claridad del mensaje"""
        puntaje = 70  # Base
        
        # Longitud apropiada (no muy corto ni muy largo)
        longitud = len(mensaje.split())
        if 10 <= longitud <= 50:
            puntaje += 10
        elif longitud < 5:
            puntaje -= 20
        
        # Estructura clara
        if any(palabra in mensaje.lower() for palabra in ["primero", "segundo", "paso", "siguiente"]):
            puntaje += 10
        
        # Evitar jerga excesiva
        palabras_complejas = ["implementar", "ejecutar", "proceder", "gestionar"]
        if sum(1 for p in palabras_complejas if p in mensaje.lower()) > 2:
            puntaje -= 10
        
        return min(100, max(0, puntaje))
    
    def _evaluar_resolucion(self, mensaje: str, turno: int) -> float:
        """Evalúa si el mensaje contribuye a resolver el problema"""
        mensaje_lower = mensaje.lower()
        puntaje = 60  # Base
        
        # Palabras orientadas a solución
        palabras_solucion = [
            "solución", "resolver", "ayudar", "hacer", "realizar",
            "paso", "proceso", "opción", "alternativa"
        ]
        
        for palabra in palabras_solucion:
            if palabra in mensaje_lower:
                puntaje += 8
        
        # Preguntas de clarificación (buenas en turnos iniciales)
        if "?" in mensaje and turno <= 2:
            puntaje += 10
        
        # Acciones concretas
        if any(p in mensaje_lower for p in ["voy a", "haré", "realizaré", "enviaré"]):
            puntaje += 15
        
        return min(100, puntaje)
    
    def obtener_puntaje_actual(self) -> Dict:
        """Obtiene el puntaje actual del agente"""
        if not self.puntajes_turno:
            return {
                "puntaje_general": 0,
                "empatia": 0,
                "claridad": 0,
                "resolucion": 0,
                "turnos": 0
            }
        
        return {
            "puntaje_general": sum(self.puntajes_turno) / len(self.puntajes_turno),
            "empatia": sum(self.puntajes_criterios["empatia"]) / len(self.puntajes_criterios["empatia"]),
            "claridad": sum(self.puntajes_criterios["claridad"]) / len(self.puntajes_criterios["claridad"]),
            "resolucion": sum(self.puntajes_criterios["resolucion"]) / len(self.puntajes_criterios["resolucion"]),
            "turnos": len(self.puntajes_turno)
        }
    
    def generar_informe_narrativo(self, cliente: ClienteSimulado) -> str:
        """Genera un informe narrativo del desempeño"""
        puntajes = self.obtener_puntaje_actual()
        
        informe = f"""
╔══════════════════════════════════════════════════════════════╗
║           INFORME DE EVALUACIÓN - AGENTE                      ║
╚══════════════════════════════════════════════════════════════╝

INFORMACIÓN DE LA PRUEBA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Canal: {cliente.canal.value.upper()}
Personalidad del cliente: {cliente.personalidad.value.upper()}
Problema simulado: {cliente.problema}
Número de turnos: {puntajes['turnos']}

PUNTAJES GENERALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Puntaje General: {puntajes['puntaje_general']:.1f}/100
"""
        
        # Clasificación
        if puntajes['puntaje_general'] >= 90:
            clasificacion = "EXCELENTE ⭐⭐⭐⭐⭐"
        elif puntajes['puntaje_general'] >= 75:
            clasificacion = "MUY BUENO ⭐⭐⭐⭐"
        elif puntajes['puntaje_general'] >= 60:
            clasificacion = "BUENO ⭐⭐⭐"
        elif puntajes['puntaje_general'] >= 45:
            clasificacion = "REGULAR ⭐⭐"
        else:
            clasificacion = "NECESITA MEJORA ⭐"
        
        informe += f"Clasificación: {clasificacion}\n\n"
        
        informe += "DESGLOSE POR CRITERIO\n"
        informe += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        informe += f"├─ Empatía:      {puntajes['empatia']:.1f}/100 (Peso: 35%)\n"
        informe += f"├─ Claridad:     {puntajes['claridad']:.1f}/100 (Peso: 30%)\n"
        informe += f"└─ Resolución:   {puntajes['resolucion']:.1f}/100 (Peso: 35%)\n\n"
        
        informe += "ANÁLISIS DETALLADO\n"
        informe += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        # Análisis de Empatía
        if puntajes['empatia'] >= 75:
            informe += "✓ Empatía: El agente demostró excelente capacidad para comprender\n"
            informe += "  y responder a las emociones del cliente. Uso apropiado de lenguaje\n"
            informe += "  empático y reconocimiento del estado emocional.\n\n"
        elif puntajes['empatia'] >= 50:
            informe += "⚠ Empatía: El agente mostró empatía básica pero puede mejorar en\n"
            informe += "  el reconocimiento y validación de las emociones del cliente.\n\n"
        else:
            informe += "✗ Empatía: El agente necesita trabajar en demostrar comprensión\n"
            informe += "  hacia las emociones del cliente. Respuestas muy técnicas o frías.\n\n"
        
        # Análisis de Claridad
        if puntajes['claridad'] >= 75:
            informe += "✓ Claridad: Comunicación clara y efectiva. Mensajes bien estructurados\n"
            informe += "  y fáciles de entender. Longitud apropiada de respuestas.\n\n"
        elif puntajes['claridad'] >= 50:
            informe += "⚠ Claridad: Comunicación aceptable pero mejorable. Algunas respuestas\n"
            informe += "  podrían ser más claras o mejor estructuradas.\n\n"
        else:
            informe += "✗ Claridad: La comunicación fue confusa o poco clara. Se recomienda\n"
            informe += "  usar lenguaje más simple y estructurar mejor las respuestas.\n\n"
        
        # Análisis de Resolución
        if puntajes['resolucion'] >= 75:
            informe += "✓ Resolución: Excelente enfoque en resolver el problema. Propuso\n"
            informe += "  soluciones concretas y acciones específicas.\n\n"
        elif puntajes['resolucion'] >= 50:
            informe += "⚠ Resolución: Intentó resolver el problema pero podría ser más\n"
            informe += "  proactivo y específico en las soluciones propuestas.\n\n"
        else:
            informe += "✗ Resolución: Poca orientación a la solución del problema.\n"
            informe += "  Se recomienda ser más concreto y ofrecer acciones específicas.\n\n"
        
        # Estado final del cliente
        informe += "ESTADO FINAL DEL CLIENTE\n"
        informe += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        informe += f"Satisfacción: {cliente.satisfaccion}/100\n"
        informe += f"Paciencia restante: {max(0, cliente.paciencia)}/100\n\n"
        
        # Recomendaciones
        informe += "RECOMENDACIONES\n"
        informe += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        recomendaciones = []
        if puntajes['empatia'] < 70:
            recomendaciones.append("• Practicar técnicas de escucha activa y validación emocional")
        if puntajes['claridad'] < 70:
            recomendaciones.append("• Estructurar mejor las respuestas y usar lenguaje más simple")
        if puntajes['resolucion'] < 70:
            recomendaciones.append("• Ser más proactivo en ofrecer soluciones concretas")
        if cliente.satisfaccion < 50:
            recomendaciones.append("• Revisar el enfoque general de atención al cliente")
        
        if not recomendaciones:
            recomendaciones.append("• Mantener el excelente nivel de servicio")
            recomendaciones.append("• Continuar desarrollando las habilidades actuales")
        
        informe += "\n".join(recomendaciones)
        informe += "\n\n╚══════════════════════════════════════════════════════════════╝\n"
        
        return informe
    
    def generar_informe_json(self, cliente: ClienteSimulado) -> Dict:
        """Genera un informe en formato JSON"""
        puntajes = self.obtener_puntaje_actual()
        
        return {
            "fecha_evaluacion": datetime.now().isoformat(),
            "configuracion_prueba": {
                "canal": cliente.canal.value,
                "personalidad": cliente.personalidad.value,
                "problema": cliente.problema
            },
            "metricas": {
                "puntaje_general": round(puntajes['puntaje_general'], 2),
                "numero_turnos": puntajes['turnos'],
                "criterios": {
                    "empatia": {
                        "puntaje": round(puntajes['empatia'], 2),
                        "peso": RubricaEvaluacion.CRITERIOS["empatia"]["peso"],
                        "descripcion": RubricaEvaluacion.CRITERIOS["empatia"]["descripcion"]
                    },
                    "claridad": {
                        "puntaje": round(puntajes['claridad'], 2),
                        "peso": RubricaEvaluacion.CRITERIOS["claridad"]["peso"],
                        "descripcion": RubricaEvaluacion.CRITERIOS["claridad"]["descripcion"]
                    },
                    "resolucion": {
                        "puntaje": round(puntajes['resolucion'], 2),
                        "peso": RubricaEvaluacion.CRITERIOS["resolucion"]["peso"],
                        "descripcion": RubricaEvaluacion.CRITERIOS["resolucion"]["descripcion"]
                    }
                }
            },
            "estado_cliente": {
                "satisfaccion": cliente.satisfaccion,
                "paciencia": max(0, cliente.paciencia)
            },
            "historial": self.historial_dialogo,
            "puntajes_por_turno": self.puntajes_turno
        }


class EvaluadorChatbot:
    """Chatbot principal que coordina la evaluación"""
    
    def __init__(self):
        self.estado = "ESPERANDO"  # ESPERANDO, EN_PRUEBA, FINALIZADO
        self.cliente: Optional[ClienteSimulado] = None
        self.evaluador: Optional[Evaluador] = None
        self.turno_actual = 0
    
    def procesar_comando(self, entrada: str) -> str:
        """Procesa comandos del usuario"""
        entrada = entrada.strip()
        
        if entrada.upper() == "COMENZAR TEST":
            return self._iniciar_test()
        
        elif entrada == "/score_now":
            return self._mostrar_puntaje_actual()
        
        elif entrada == "/finalizar":
            return self._finalizar_test()
        
        elif self.estado == "EN_PRUEBA":
            return self._procesar_respuesta_agente(entrada)
        
        elif self.estado == "ESPERANDO":
            return "⚠️  Para iniciar la evaluación, escriba: COMENZAR TEST"
        
        else:
            return "❌ Comando no reconocido. Comandos disponibles: COMENZAR TEST, /score_now, /finalizar"
    
    def _iniciar_test(self) -> str:
        """Inicia una nueva prueba de evaluación"""
        # Seleccionar personalidad y canal aleatorios
        personalidad = random.choice(list(Personalidad))
        canal = random.choice(list(Canal))
        
        # Problemas simulados comunes
        problemas = [
            "mi pedido no ha llegado después de una semana",
            "me cobraron dos veces el mismo producto",
            "el producto llegó defectuoso y quiero un reembolso",
            "no puedo acceder a mi cuenta, olvidé mi contraseña",
            "el servicio se canceló sin previo aviso",
            "necesito cambiar mi dirección de envío urgentemente",
            "el producto no es lo que esperaba según la descripción",
            "quiero cancelar mi suscripción pero no encuentro cómo"
        ]
        problema = random.choice(problemas)
        
        # Crear cliente y evaluador
        self.cliente = ClienteSimulado(personalidad, canal, problema)
        self.evaluador = Evaluador()
        self.estado = "EN_PRUEBA"
        self.turno_actual = 0
        
        # Generar mensaje inicial
        mensaje_inicial = self.cliente.generar_mensaje_inicial()
        self.evaluador.historial_dialogo.append({
            "turno": 0,
            "rol": "cliente",
            "mensaje": mensaje_inicial
        })
        
        info = f"""
╔══════════════════════════════════════════════════════════════╗
║                    EVALUACIÓN INICIADA                        ║
╚══════════════════════════════════════════════════════════════╝

📋 INFORMACIÓN DE LA PRUEBA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Canal:        {canal.value.upper()}
Personalidad: {personalidad.value.upper()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 INSTRUCCIONES
Responda al cliente como un agente de servicio al cliente.
Su desempeño será evaluado en: Empatía, Claridad y Resolución.

Comandos disponibles:
  /score_now  - Ver puntaje actual
  /finalizar  - Terminar la prueba y ver informe completo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 CLIENTE (vía {canal.value}):
{mensaje_inicial}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Su respuesta (como agente):
"""
        return info
    
    def _procesar_respuesta_agente(self, respuesta: str) -> str:
        """Procesa la respuesta del agente y genera respuesta del cliente"""
        if not self.cliente or not self.evaluador:
            return "❌ Error: No hay una prueba activa."
        
        self.turno_actual += 1
        
        # Guardar respuesta del agente
        self.evaluador.historial_dialogo.append({
            "turno": self.turno_actual,
            "rol": "agente",
            "mensaje": respuesta
        })
        
        # Generar respuesta del cliente
        respuesta_cliente, continuar = self.cliente.generar_respuesta(respuesta, self.evaluador)
        
        self.evaluador.historial_dialogo.append({
            "turno": self.turno_actual,
            "rol": "cliente",
            "mensaje": respuesta_cliente
        })
        
        if not continuar:
            # Finalizar automáticamente
            informe_final = self._finalizar_test()
            return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 CLIENTE:
{respuesta_cliente}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  El cliente ha finalizado la conversación.

{informe_final}
"""
        
        return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 CLIENTE:
{respuesta_cliente}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Su respuesta (como agente):
"""
    
    def _mostrar_puntaje_actual(self) -> str:
        """Muestra el puntaje actual sin finalizar"""
        if not self.evaluador or self.estado != "EN_PRUEBA":
            return "❌ No hay una prueba activa."
        
        puntajes = self.evaluador.obtener_puntaje_actual()
        
        return f"""
╔══════════════════════════════════════════════════════════════╗
║                   PUNTAJE ACTUAL                              ║
╚══════════════════════════════════════════════════════════════╝

Puntaje General: {puntajes['puntaje_general']:.1f}/100
Empatía:         {puntajes['empatia']:.1f}/100
Claridad:        {puntajes['claridad']:.1f}/100
Resolución:      {puntajes['resolucion']:.1f}/100

Turnos completados: {puntajes['turnos']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
La prueba continúa. Escriba su siguiente respuesta o use /finalizar.
"""
    
    def _finalizar_test(self) -> str:
        """Finaliza la prueba y genera informes"""
        if not self.evaluador or not self.cliente or self.estado != "EN_PRUEBA":
            return "❌ No hay una prueba activa para finalizar."
        
        self.estado = "FINALIZADO"
        
        # Generar informes
        informe_narrativo = self.evaluador.generar_informe_narrativo(self.cliente)
        informe_json = self.evaluador.generar_informe_json(self.cliente)
        
        # Guardar JSON en archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"evaluacion_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(informe_json, f, ensure_ascii=False, indent=2)
        
        resultado = f"""
{informe_narrativo}

📄 Informe JSON guardado en: {filename}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Para iniciar una nueva evaluación, escriba: COMENZAR TEST
"""
        
        return resultado


def main():
    """Función principal para ejecutar el chatbot evaluador"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║          CHATBOT EVALUADOR DE AGENTES v1.0                    ║
║                                                               ║
║  Sistema de evaluación de agentes de servicio al cliente     ║
║  mediante simulación de clientes con diferentes               ║
║  personalidades y canales de comunicación.                    ║
╚══════════════════════════════════════════════════════════════╝

Escriba "COMENZAR TEST" para iniciar una evaluación.
Escriba "salir" para terminar el programa.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
    
    chatbot = EvaluadorChatbot()
    
    while True:
        try:
            entrada = input("> ").strip()
            
            if entrada.lower() in ['salir', 'exit', 'quit']:
                print("\n👋 ¡Hasta luego! Gracias por usar el Evaluador de Agentes.")
                break
            
            if not entrada:
                continue
            
            respuesta = chatbot.procesar_comando(entrada)
            print(respuesta)
            
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrumpido. ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Por favor, intente nuevamente.")


if __name__ == "__main__":
    main()
