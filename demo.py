#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplo de uso del Chatbot Evaluador de Agentes
Muestra un diálogo completo de ejemplo
"""

from evaluador_agentes import EvaluadorChatbot


def ejecutar_demo():
    """Ejecuta una demostración del chatbot evaluador"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║              DEMO: CHATBOT EVALUADOR DE AGENTES               ║
╚══════════════════════════════════════════════════════════════╝

Este es un ejemplo de cómo funciona el sistema de evaluación.
Se simula una conversación entre un agente y un cliente.

""")
    
    chatbot = EvaluadorChatbot()
    
    # Iniciar test
    print("Comando: COMENZAR TEST")
    print("-" * 60)
    respuesta = chatbot.procesar_comando("COMENZAR TEST")
    print(respuesta)
    
    # Simulación de respuestas del agente
    respuestas_agente = [
        "Buenos días, lamento mucho escuchar sobre su situación. Entiendo su frustración y voy a ayudarle inmediatamente a resolver este problema.",
        
        "He verificado su caso y veo que efectivamente hay un retraso. Voy a hacer lo siguiente: primero, enviaré su pedido con envío express sin costo adicional; segundo, le aplicaré un descuento del 20% en su próxima compra como disculpa.",
        
        "Su pedido saldrá hoy mismo y llegará mañana antes de las 3 PM. Le enviaré el número de rastreo a su correo en los próximos 30 minutos. ¿Hay algo más en lo que pueda ayudarle?"
    ]
    
    for i, respuesta_agente in enumerate(respuestas_agente, 1):
        print(f"\nRespuesta del agente #{i}:")
        print("-" * 60)
        print(respuesta_agente)
        print("\n")
        
        respuesta = chatbot.procesar_comando(respuesta_agente)
        print(respuesta)
        
        # Si el cliente finalizó, terminar
        if "finalizado" in respuesta.lower():
            break
    
    # Ver puntaje actual si aún está en prueba
    if chatbot.estado == "EN_PRUEBA":
        print("\nComando: /score_now")
        print("-" * 60)
        respuesta = chatbot.procesar_comando("/score_now")
        print(respuesta)
        
        # Finalizar
        print("\nComando: /finalizar")
        print("-" * 60)
        respuesta = chatbot.procesar_comando("/finalizar")
        print(respuesta)
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETADA")
    print("=" * 60)
    print("\nPara ejecutar el chatbot interactivo, use:")
    print("  python evaluador_agentes.py")
    print()


if __name__ == "__main__":
    ejecutar_demo()
