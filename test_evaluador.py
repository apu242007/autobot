#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para el Chatbot Evaluador de Agentes
"""

from evaluador_agentes import (
    EvaluadorChatbot, 
    Personalidad, 
    Canal, 
    ClienteSimulado,
    Evaluador,
    AdaptadorCanal
)
import json


def test_adaptador_canal():
    """Prueba el adaptador de canal"""
    print("=" * 60)
    print("TEST: Adaptador de Canal")
    print("=" * 60)
    
    mensaje = "Hola, ¿cómo estás?"
    
    for canal in Canal:
        mensaje_adaptado = AdaptadorCanal.adaptar_mensaje(mensaje, canal)
        print(f"\n{canal.value.upper()}:")
        print(f"  {mensaje_adaptado}")
    
    print("\n✓ Test de adaptador de canal completado\n")


def test_cliente_simulado():
    """Prueba la simulación de cliente"""
    print("=" * 60)
    print("TEST: Cliente Simulado")
    print("=" * 60)
    
    for personalidad in Personalidad:
        cliente = ClienteSimulado(
            personalidad, 
            Canal.CHAT, 
            "mi pedido no ha llegado"
        )
        mensaje = cliente.generar_mensaje_inicial()
        print(f"\n{personalidad.value.upper()}:")
        print(f"  {mensaje}")
    
    print("\n✓ Test de cliente simulado completado\n")


def test_evaluador():
    """Prueba el sistema de evaluación"""
    print("=" * 60)
    print("TEST: Sistema de Evaluación")
    print("=" * 60)
    
    evaluador = Evaluador()
    cliente = ClienteSimulado(Personalidad.ENOJADO, Canal.CHAT, "problema de prueba")
    
    # Simular diferentes tipos de respuestas
    respuestas = [
        ("Respuesta empática", "Lamento mucho su situación. Entiendo su frustración y voy a ayudarle inmediatamente."),
        ("Respuesta clara", "Para resolver esto, primero voy a verificar su pedido, luego contactaré al almacén y finalmente le daré una solución."),
        ("Respuesta orientada a solución", "Voy a procesar su reembolso ahora mismo y recibirá el dinero en 24-48 horas.")
    ]
    
    for nombre, respuesta in respuestas:
        puntaje = evaluador.evaluar_turno(respuesta, cliente)
        print(f"\n{nombre}:")
        print(f"  Puntaje: {puntaje:.1f}/100")
    
    puntajes = evaluador.obtener_puntaje_actual()
    print(f"\nPuntajes promedio:")
    print(f"  General: {puntajes['puntaje_general']:.1f}")
    print(f"  Empatía: {puntajes['empatia']:.1f}")
    print(f"  Claridad: {puntajes['claridad']:.1f}")
    print(f"  Resolución: {puntajes['resolucion']:.1f}")
    
    print("\n✓ Test de evaluación completado\n")


def test_chatbot_interactivo():
    """Prueba el chatbot de forma programática"""
    print("=" * 60)
    print("TEST: Chatbot Interactivo (Simulado)")
    print("=" * 60)
    
    chatbot = EvaluadorChatbot()
    
    # Test 1: Intentar responder sin iniciar test
    print("\n1. Intentar responder sin COMENZAR TEST:")
    respuesta = chatbot.procesar_comando("Hola")
    print(respuesta[:80] + "...")
    
    # Test 2: Iniciar test
    print("\n2. Iniciar test con COMENZAR TEST:")
    respuesta = chatbot.procesar_comando("COMENZAR TEST")
    print(respuesta[:200] + "...\n")
    
    # Test 3: Responder como agente
    print("3. Respuesta del agente:")
    respuesta = chatbot.procesar_comando(
        "Lamento mucho su situación. Entiendo completamente su frustración. "
        "Voy a revisar su caso inmediatamente y le daré una solución en los próximos minutos."
    )
    print(respuesta[:200] + "...\n")
    
    # Test 4: Ver puntaje actual
    print("4. Ver puntaje actual con /score_now:")
    respuesta = chatbot.procesar_comando("/score_now")
    print(respuesta[:300] + "...\n")
    
    # Test 5: Continuar con otra respuesta
    print("5. Otra respuesta del agente:")
    respuesta = chatbot.procesar_comando(
        "He verificado su pedido y veo que hubo un retraso en el almacén. "
        "Voy a enviárselo con envío express sin costo adicional. Llegará mañana."
    )
    print(respuesta[:200] + "...\n")
    
    # Test 6: Finalizar
    print("6. Finalizar test con /finalizar:")
    respuesta = chatbot.procesar_comando("/finalizar")
    print(respuesta[:400] + "...\n")
    
    print("✓ Test de chatbot interactivo completado\n")


def test_informe_json():
    """Prueba la generación de informe JSON"""
    print("=" * 60)
    print("TEST: Generación de Informe JSON")
    print("=" * 60)
    
    evaluador = Evaluador()
    cliente = ClienteSimulado(Personalidad.NEUTRAL, Canal.EMAIL, "consulta sobre facturación")
    
    # Simular algunos turnos
    respuestas = [
        "Buenos días, gracias por contactarnos. Voy a ayudarle con su consulta sobre facturación.",
        "Para resolver esto, necesito verificar algunos datos. ¿Puede proporcionarme su número de cuenta?",
        "Perfecto, he revisado su cuenta y veo el problema. Voy a generar una factura corregida."
    ]
    
    for respuesta in respuestas:
        evaluador.evaluar_turno(respuesta, cliente)
        evaluador.historial_dialogo.append({
            "turno": len(evaluador.historial_dialogo),
            "rol": "agente",
            "mensaje": respuesta
        })
    
    informe_json = evaluador.generar_informe_json(cliente)
    
    print("\nInforme JSON generado:")
    print(json.dumps(informe_json, indent=2, ensure_ascii=False)[:500] + "...\n")
    
    print("✓ Test de informe JSON completado\n")


def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "=" * 60)
    print("INICIANDO SUITE DE PRUEBAS")
    print("=" * 60 + "\n")
    
    try:
        test_adaptador_canal()
        test_cliente_simulado()
        test_evaluador()
        test_chatbot_interactivo()
        test_informe_json()
        
        print("=" * 60)
        print("✓ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("=" * 60 + "\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error en las pruebas: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
