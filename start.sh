#!/bin/bash
# Script de inicio rápido para el Chatbot Evaluador de Agentes

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          CHATBOT EVALUADOR DE AGENTES - INICIO               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Seleccione una opción:"
echo ""
echo "  1) Modo Interactivo (chatbot completo)"
echo "  2) Demo Automática (ver ejemplo)"
echo "  3) Ejecutar Tests (verificar funcionamiento)"
echo "  4) Ejemplos Programáticos (integración)"
echo "  5) Salir"
echo ""
read -p "Opción [1-5]: " opcion

case $opcion in
    1)
        echo ""
        echo "Iniciando modo interactivo..."
        echo "----------------------------------------"
        python3 evaluador_agentes.py
        ;;
    2)
        echo ""
        echo "Ejecutando demo..."
        echo "----------------------------------------"
        python3 demo.py
        ;;
    3)
        echo ""
        echo "Ejecutando tests..."
        echo "----------------------------------------"
        python3 test_evaluador.py
        ;;
    4)
        echo ""
        echo "Mostrando ejemplos programáticos..."
        echo "----------------------------------------"
        python3 ejemplos_programaticos.py
        ;;
    5)
        echo "¡Hasta luego!"
        exit 0
        ;;
    *)
        echo "Opción inválida. Use: ./start.sh"
        exit 1
        ;;
esac
