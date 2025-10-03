#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplo de uso programático del Chatbot Evaluador de Agentes
Muestra cómo integrar el sistema en otras aplicaciones
"""

import json
from evaluador_agentes import (
    EvaluadorChatbot,
    ClienteSimulado,
    Evaluador,
    Personalidad,
    Canal
)


def ejemplo_uso_basico():
    """Ejemplo básico de uso programático"""
    print("=" * 60)
    print("EJEMPLO 1: Uso Básico del Chatbot")
    print("=" * 60 + "\n")
    
    # Crear instancia del chatbot
    chatbot = EvaluadorChatbot()
    
    # Iniciar test
    print("1. Iniciando test...")
    respuesta = chatbot.procesar_comando("COMENZAR TEST")
    print(respuesta[:200] + "...\n")
    
    # Simular respuesta del agente
    print("2. Enviando respuesta del agente...")
    respuesta = chatbot.procesar_comando(
        "Buenos días, lamento su situación. Voy a ayudarle inmediatamente."
    )
    print(respuesta[:200] + "...\n")
    
    # Ver puntaje actual
    print("3. Consultando puntaje actual...")
    respuesta = chatbot.procesar_comando("/score_now")
    print(respuesta[:300] + "...\n")
    
    # Finalizar
    print("4. Finalizando evaluación...")
    respuesta = chatbot.procesar_comando("/finalizar")
    print("Evaluación finalizada. Informe generado.\n")


def ejemplo_creacion_personalizada():
    """Ejemplo de creación personalizada de escenario"""
    print("=" * 60)
    print("EJEMPLO 2: Creación de Escenario Personalizado")
    print("=" * 60 + "\n")
    
    # Crear cliente con parámetros específicos
    cliente = ClienteSimulado(
        personalidad=Personalidad.ENOJADO,
        canal=Canal.WHATSAPP,
        problema="mi producto llegó defectuoso y nadie me responde"
    )
    
    # Crear evaluador
    evaluador = Evaluador()
    
    print(f"Cliente creado:")
    print(f"  Personalidad: {cliente.personalidad.value}")
    print(f"  Canal: {cliente.canal.value}")
    print(f"  Problema: {cliente.problema}")
    print()
    
    # Generar mensaje inicial
    mensaje_inicial = cliente.generar_mensaje_inicial()
    print(f"Mensaje inicial del cliente:")
    print(f"  {mensaje_inicial}\n")
    
    # Simular respuestas del agente
    respuestas_agente = [
        "Lamento mucho escuchar esto. Entiendo lo frustrante que es recibir un producto defectuoso. Voy a ayudarle inmediatamente.",
        "Voy a procesar su reemplazo ahora mismo. Le enviaremos un producto nuevo mañana con envío express gratuito.",
        "También le aplicaré un descuento del 25% en su próxima compra como disculpa. ¿Hay algo más en lo que pueda ayudarle?"
    ]
    
    for i, respuesta_agente in enumerate(respuestas_agente, 1):
        print(f"Turno {i} - Agente dice:")
        print(f"  {respuesta_agente}")
        
        # Evaluar y obtener respuesta del cliente
        respuesta_cliente, continuar = cliente.generar_respuesta(respuesta_agente, evaluador)
        
        print(f"Turno {i} - Cliente responde:")
        print(f"  {respuesta_cliente}")
        print(f"  Satisfacción: {cliente.satisfaccion}/100")
        print(f"  Paciencia: {cliente.paciencia}/100")
        print()
        
        if not continuar:
            print("El cliente ha finalizado la conversación.\n")
            break
    
    # Obtener métricas finales
    puntajes = evaluador.obtener_puntaje_actual()
    print("Puntajes finales:")
    print(f"  Puntaje General: {puntajes['puntaje_general']:.1f}/100")
    print(f"  Empatía: {puntajes['empatia']:.1f}/100")
    print(f"  Claridad: {puntajes['claridad']:.1f}/100")
    print(f"  Resolución: {puntajes['resolucion']:.1f}/100")
    print()


def ejemplo_evaluacion_batch():
    """Ejemplo de evaluación de múltiples agentes"""
    print("=" * 60)
    print("EJEMPLO 3: Evaluación Batch de Múltiples Agentes")
    print("=" * 60 + "\n")
    
    # Definir respuestas de diferentes agentes
    agentes = {
        "Agente A": [
            "Hola, ¿en qué puedo ayudarle?",
            "Entiendo. Voy a revisar eso.",
            "Listo, resuelto."
        ],
        "Agente B": [
            "Buenos días, lamento mucho su situación. Entiendo su frustración.",
            "Voy a resolver esto inmediatamente. Le daré una solución concreta.",
            "He procesado su solicitud. Recibirá una respuesta en 24 horas."
        ],
        "Agente C": [
            "Disculpe las molestias. Comprendo perfectamente su preocupación.",
            "Para ayudarle mejor, voy a hacer tres cosas: primero, verificar su caso; segundo, contactar al departamento correspondiente; y tercero, darle seguimiento personalizado.",
            "Su problema está resuelto. Le he enviado confirmación por email con todos los detalles y mi número directo para cualquier duda."
        ]
    }
    
    resultados = {}
    
    # Evaluar cada agente con el mismo escenario
    for nombre_agente, respuestas in agentes.items():
        # Crear nuevo cliente y evaluador para cada agente
        cliente = ClienteSimulado(
            personalidad=Personalidad.ANSIOSO,
            canal=Canal.CHAT,
            problema="no puedo acceder a mi cuenta"
        )
        evaluador = Evaluador()
        
        # Procesar respuestas
        for respuesta in respuestas:
            cliente.generar_respuesta(respuesta, evaluador)
        
        # Obtener puntajes
        puntajes = evaluador.obtener_puntaje_actual()
        resultados[nombre_agente] = puntajes
    
    # Mostrar comparación
    print("Comparación de Agentes:\n")
    print(f"{'Agente':<15} {'General':<10} {'Empatía':<10} {'Claridad':<10} {'Resolución':<12}")
    print("-" * 60)
    
    for nombre, puntajes in resultados.items():
        print(f"{nombre:<15} "
              f"{puntajes['puntaje_general']:>7.1f}    "
              f"{puntajes['empatia']:>7.1f}    "
              f"{puntajes['claridad']:>7.1f}    "
              f"{puntajes['resolucion']:>7.1f}")
    
    print()
    
    # Identificar mejor agente
    mejor_agente = max(resultados.items(), key=lambda x: x[1]['puntaje_general'])
    print(f"🏆 Mejor agente: {mejor_agente[0]} con {mejor_agente[1]['puntaje_general']:.1f} puntos\n")


def ejemplo_exportar_resultados():
    """Ejemplo de exportación de resultados para análisis"""
    print("=" * 60)
    print("EJEMPLO 4: Exportación de Resultados")
    print("=" * 60 + "\n")
    
    # Crear evaluación
    cliente = ClienteSimulado(
        personalidad=Personalidad.NEUTRAL,
        canal=Canal.EMAIL,
        problema="consulta sobre mi factura"
    )
    evaluador = Evaluador()
    
    # Simular diálogo
    respuestas = [
        "Estimado cliente, gracias por contactarnos. Con gusto le ayudaré con su consulta sobre facturación.",
        "He revisado su cuenta y veo que tiene una factura pendiente de marzo. ¿Se refiere a esa?",
        "Perfecto. Le he enviado una copia de la factura a su correo electrónico registrado."
    ]
    
    for i, respuesta in enumerate(respuestas):
        evaluador.evaluar_turno(respuesta, cliente)
        evaluador.historial_dialogo.append({
            "turno": i + 1,
            "rol": "agente",
            "mensaje": respuesta
        })
    
    # Generar informe JSON
    informe = evaluador.generar_informe_json(cliente)
    
    # Guardar en archivo
    filename = "ejemplo_evaluacion.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(informe, f, ensure_ascii=False, indent=2)
    
    print(f"Informe guardado en: {filename}")
    print("\nResumen del informe:")
    print(f"  Puntaje General: {informe['metricas']['puntaje_general']}")
    print(f"  Turnos: {informe['metricas']['numero_turnos']}")
    print(f"  Satisfacción del cliente: {informe['estado_cliente']['satisfaccion']}/100")
    print()


def ejemplo_uso_en_api():
    """Ejemplo de cómo usar el sistema en una API"""
    print("=" * 60)
    print("EJEMPLO 5: Integración en API (pseudo-código)")
    print("=" * 60 + "\n")
    
    print("""
# Pseudo-código para integración con API REST

from flask import Flask, request, jsonify
from evaluador_agentes import EvaluadorChatbot

app = Flask(__name__)
sesiones = {}  # Almacenar sesiones activas

@app.route('/api/evaluacion/iniciar', methods=['POST'])
def iniciar_evaluacion():
    session_id = generate_session_id()
    chatbot = EvaluadorChatbot()
    respuesta = chatbot.procesar_comando("COMENZAR TEST")
    sesiones[session_id] = chatbot
    return jsonify({
        'session_id': session_id,
        'mensaje': respuesta
    })

@app.route('/api/evaluacion/responder', methods=['POST'])
def responder():
    session_id = request.json['session_id']
    respuesta_agente = request.json['respuesta']
    chatbot = sesiones[session_id]
    respuesta = chatbot.procesar_comando(respuesta_agente)
    return jsonify({
        'mensaje': respuesta,
        'estado': chatbot.estado
    })

@app.route('/api/evaluacion/finalizar', methods=['POST'])
def finalizar():
    session_id = request.json['session_id']
    chatbot = sesiones[session_id]
    respuesta = chatbot.procesar_comando('/finalizar')
    del sesiones[session_id]
    return jsonify({
        'informe': respuesta
    })

if __name__ == '__main__':
    app.run(debug=True)
    """)
    print()


def main():
    """Ejecuta todos los ejemplos"""
    print("\n" + "=" * 60)
    print("EJEMPLOS DE USO PROGRAMÁTICO")
    print("Chatbot Evaluador de Agentes")
    print("=" * 60 + "\n")
    
    ejemplos = [
        ("Uso Básico", ejemplo_uso_basico),
        ("Creación Personalizada", ejemplo_creacion_personalizada),
        ("Evaluación Batch", ejemplo_evaluacion_batch),
        ("Exportación de Resultados", ejemplo_exportar_resultados),
        ("Integración API", ejemplo_uso_en_api)
    ]
    
    for i, (nombre, funcion) in enumerate(ejemplos, 1):
        print(f"\n{'=' * 60}")
        print(f"Ejecutando Ejemplo {i}: {nombre}")
        print('=' * 60 + "\n")
        
        try:
            funcion()
        except Exception as e:
            print(f"Error en ejemplo: {e}")
        
        if i < len(ejemplos):
            input("\nPresione Enter para continuar al siguiente ejemplo...")
    
    print("\n" + "=" * 60)
    print("EJEMPLOS COMPLETADOS")
    print("=" * 60 + "\n")
    print("Para más información, consulte la documentación en README.md")
    print()


if __name__ == "__main__":
    main()
