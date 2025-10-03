codex/add-documentation-for-chatbot-evaluation-system-176ypa
# Autobot

Sistema modular para simular clientes con personalidades complejas y evaluar el
comportamiento de agentes de atención en la industria de la construcción.

## Estructura principal

- `src/autobot/models.py`: Modelos basados en dataclasses para escenarios, mensajes y
  resultados de evaluación.
- `src/autobot/personalities.py`: Perfiles psicológicos detallados.
- `src/autobot/scenarios.py`: Biblioteca de escenarios realistas.
- `src/autobot/context.py`: Gestor de contexto multi-turno con almacenamiento en
  memoria.
- `src/autobot/evaluation.py`: Motor de evaluación con rúbrica configurable.
- `src/autobot/commands.py`: Sistema de comandos para iniciar y finalizar
  simulaciones.

## Instalación y pruebas

```bash
python -m venv .venv
# En Linux/macOS
source .venv/bin/activate
# En Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
pip install -e .
black src tests
pytest
```

## Ejecución de la demo

Tras instalar las dependencias puedes ejecutar una simulación básica sin
configuración adicional con:

```bash
# Linux/macOS/Windows
python -m autobot.demo

# Alternativa: ejecutar la demo directamente como módulo del paquete
python -m autobot
```

El comando imprime en consola la información del escenario seleccionado, la
conversación de ejemplo y el informe final generado por el motor de evaluación.

=======
# Autobot - Chatbot Evaluador de Agentes

Sistema de evaluación de agentes de servicio al cliente mediante simulación de clientes con diferentes personalidades y canales de comunicación.

## 🎯 Características

- **Simulación de clientes realista**: Personalidades variadas (enojado, ansioso, neutral, confundido, impaciente)
- **Múltiples canales**: WhatsApp, Email, Chat en vivo, Teléfono
- **Evaluación integral**: Mide empatía, claridad y capacidad de resolución
- **Diálogos multi-turno**: Mantiene contexto y adapta el comportamiento según las respuestas del agente
- **Role prompting**: Tono realista adaptado al canal y personalidad
- **Informes detallados**: Narrativos y JSON con métricas cuantitativas

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/apu242007/autobot.git
cd autobot

# No se requieren dependencias externas - usa solo la biblioteca estándar de Python
```

## 📋 Requisitos

- Python 3.6 o superior

## 💻 Uso

### Inicio Rápido con Script

```bash
./start.sh
```

El script mostrará un menú con las siguientes opciones:
1. Modo Interactivo (chatbot completo)
2. Demo Automática (ver ejemplo)
3. Ejecutar Tests (verificar funcionamiento)
4. Ejemplos Programáticos (integración)

### Modo Interactivo Directo

```bash
python3 evaluador_agentes.py
```

### Comandos Disponibles

- `COMENZAR TEST` - Inicia una nueva evaluación con cliente y canal aleatorios
- `/score_now` - Muestra el puntaje actual sin finalizar la prueba
- `/finalizar` - Termina la prueba y genera el informe completo
- `salir` - Sale del programa

### Ejemplo de Sesión

```
> COMENZAR TEST

╔══════════════════════════════════════════════════════════════╗
║                    EVALUACIÓN INICIADA                        ║
╚══════════════════════════════════════════════════════════════╝

📋 INFORMACIÓN DE LA PRUEBA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Canal:        WHATSAPP
Personalidad: ENOJADO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 CLIENTE (vía whatsapp):
¡Estoy HARTO! mi pedido no ha llegado después de una semana ¡Quiero una solución YA! 😤

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Su respuesta (como agente):

> Lamento mucho la situación. Entiendo su frustración. Voy a revisar inmediatamente 
  el estado de su pedido y le daré una solución concreta en los próximos minutos.

👤 CLIENTE:
Bueno, eso suena mejor. ¿Y cuándo se resolverá? 😊

🎯 Su respuesta (como agente):

> /finalizar

[Se muestra el informe completo con puntajes y análisis]
```

## 📊 Sistema de Evaluación

### Criterios de Evaluación

1. **Empatía (35%)**: Capacidad de comprender y responder a las emociones del cliente
2. **Claridad (30%)**: Comunicación clara y fácil de entender
3. **Resolución (35%)**: Efectividad en resolver el problema del cliente

### Escalas de Puntaje

- **90-100**: Excelente ⭐⭐⭐⭐⭐
- **75-89**: Muy Bueno ⭐⭐⭐⭐
- **60-74**: Bueno ⭐⭐⭐
- **45-59**: Regular ⭐⭐
- **0-44**: Necesita Mejora ⭐

## 🎭 Personalidades de Clientes

- **Enojado**: Molesto, exigente, requiere validación emocional
- **Ansioso**: Preocupado, necesita tranquilidad y confirmación
- **Neutral**: Objetivo, directo, busca eficiencia
- **Confundido**: Desorientado, necesita explicaciones claras y simples
- **Impaciente**: Con prisa, busca soluciones rápidas

## 📱 Canales de Comunicación

- **WhatsApp**: Informal, mensajes cortos, emojis
- **Email**: Formal, estructura completa
- **Chat**: Semi-formal, directo
- **Teléfono**: Conversacional, expresivo

## 📄 Informes Generados

El sistema genera dos tipos de informes:

1. **Informe Narrativo**: Análisis detallado con recomendaciones
2. **Informe JSON**: Datos estructurados con métricas (`evaluacion_YYYYMMDD_HHMMSS.json`)

### Estructura del JSON

```json
{
  "fecha_evaluacion": "2024-01-01T10:00:00",
  "configuracion_prueba": {
    "canal": "whatsapp",
    "personalidad": "enojado",
    "problema": "..."
  },
  "metricas": {
    "puntaje_general": 85.5,
    "numero_turnos": 4,
    "criterios": {
      "empatia": { "puntaje": 90.0, "peso": 0.35 },
      "claridad": { "puntaje": 80.0, "peso": 0.30 },
      "resolucion": { "puntaje": 87.0, "peso": 0.35 }
    }
  },
  "estado_cliente": {
    "satisfaccion": 75,
    "paciencia": 80
  },
  "historial": [...],
  "puntajes_por_turno": [...]
}
```

## 🛠️ Uso Programático

```python
from evaluador_agentes import EvaluadorChatbot, Personalidad, Canal

# Crear instancia del evaluador
chatbot = EvaluadorChatbot()

# Iniciar una prueba
respuesta = chatbot.procesar_comando("COMENZAR TEST")
print(respuesta)

# Procesar respuestas del agente
respuesta = chatbot.procesar_comando("Buenos días, ¿en qué puedo ayudarle?")
print(respuesta)

# Ver puntaje actual
respuesta = chatbot.procesar_comando("/score_now")
print(respuesta)

# Finalizar y obtener informe
respuesta = chatbot.procesar_comando("/finalizar")
print(respuesta)
```

## 🔍 Arquitectura

El sistema está compuesto por varios módulos:

- `Personalidad`: Enum de personalidades de clientes
- `Canal`: Enum de canales de comunicación
- `RubricaEvaluacion`: Define criterios y pesos de evaluación
- `AdaptadorCanal`: Adapta mensajes al estilo del canal
- `ClienteSimulado`: Simula comportamiento del cliente
- `Evaluador`: Evalúa respuestas del agente
- `EvaluadorChatbot`: Orquesta el flujo de la evaluación

## 📝 Licencia

Este proyecto está bajo la Licencia Apache 2.0. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📧 Contacto

Para preguntas o sugerencias, por favor abre un issue en GitHub.
main
