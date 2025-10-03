# Guía de Uso - Chatbot Evaluador de Agentes

## 🚀 Inicio Rápido

### Modo 1: Demo Automática
Para ver una demostración completa del sistema:

```bash
python3 demo.py
```

Este script ejecuta un escenario completo mostrando:
- Inicialización del test
- Respuestas del cliente simulado
- Evaluación en tiempo real
- Informe final completo

### Modo 2: Interactivo
Para practicar como agente:

```bash
python3 evaluador_agentes.py
```

Luego, escriba sus comandos:
```
> COMENZAR TEST
```

## 📚 Comandos Disponibles

| Comando | Descripción | Cuándo usar |
|---------|-------------|-------------|
| `COMENZAR TEST` | Inicia una nueva evaluación | Al inicio o después de finalizar una prueba |
| `/score_now` | Muestra puntaje actual | Durante la prueba para monitorear progreso |
| `/finalizar` | Termina la prueba | Cuando desee finalizar y ver el informe |
| `salir` | Sale del programa | Para cerrar la aplicación |

## 💡 Consejos para Mejorar Puntajes

### Empatía (35%)
- ✅ Reconocer las emociones del cliente explícitamente
- ✅ Usar frases como "Entiendo su frustración", "Lamento la situación"
- ✅ Validar los sentimientos del cliente
- ❌ Evitar respuestas frías o técnicas sin empatía

**Ejemplo:**
```
❌ "Su pedido está en proceso"
✅ "Lamento mucho el retraso. Entiendo lo frustrante que debe ser esperar su pedido. Voy a resolverlo inmediatamente."
```

### Claridad (30%)
- ✅ Usar lenguaje simple y directo
- ✅ Estructurar respuestas con pasos (primero, segundo, luego)
- ✅ Mantener mensajes entre 10-50 palabras
- ❌ Evitar jerga técnica excesiva
- ❌ No ser ni muy breve ni muy extenso

**Ejemplo:**
```
❌ "Vamos a implementar un proceso de gestión para ejecutar la resolución"
✅ "Voy a hacer tres cosas: verificar su pedido, contactar al almacén y darle una solución en 30 minutos."
```

### Resolución (35%)
- ✅ Ofrecer soluciones concretas
- ✅ Especificar acciones y plazos
- ✅ Hacer preguntas de clarificación al inicio
- ✅ Proponer alternativas cuando sea necesario
- ❌ No dar respuestas vagas

**Ejemplo:**
```
❌ "Vamos a ver qué podemos hacer"
✅ "Voy a procesar su reembolso ahora mismo. Recibirá el dinero en 24-48 horas y le enviaré confirmación por email."
```

## 🎭 Adaptación por Personalidad

### Cliente Enojado 😤
- Reconocer su frustración inmediatamente
- Ofrecer disculpas sinceras
- Dar soluciones rápidas y concretas
- Evitar excusas o justificaciones

### Cliente Ansioso 😰
- Transmitir calma y seguridad
- Explicar el proceso paso a paso
- Confirmar que todo estará bien
- Dar plazos específicos

### Cliente Neutral 😐
- Ser eficiente y directo
- Proporcionar información clara
- Enfocarse en la solución
- No sobre-explicar

### Cliente Confundido 🤔
- Usar lenguaje muy simple
- Explicar paso a paso
- Ofrecer múltiples formas de ayuda (tutorial, guía, etc.)
- Confirmar comprensión

### Cliente Impaciente ⏰
- Ser muy conciso
- Ofrecer soluciones rápidas
- Especificar tiempos exactos
- No dar rodeos

## 📱 Adaptación por Canal

### WhatsApp
- Mensajes cortos
- Uso de emojis apropiados
- Tono informal pero profesional

### Email
- Estructura formal (saludo, cuerpo, despedida)
- Más detallado
- Tono profesional

### Chat
- Semi-informal
- Mensajes de longitud media
- Directo al punto

### Teléfono
- Conversacional
- Más expresivo
- Mencionar tono de voz

## 📊 Interpretación de Puntajes

| Puntaje | Clasificación | Significado |
|---------|---------------|-------------|
| 90-100 | Excelente ⭐⭐⭐⭐⭐ | Desempeño sobresaliente |
| 75-89 | Muy Bueno ⭐⭐⭐⭐ | Buen desempeño, pequeñas mejoras posibles |
| 60-74 | Bueno ⭐⭐⭐ | Desempeño aceptable, áreas de mejora identificadas |
| 45-59 | Regular ⭐⭐ | Necesita trabajo en varios aspectos |
| 0-44 | Necesita Mejora ⭐ | Requiere capacitación significativa |

## 📈 Métricas del Cliente

### Satisfacción (0-100)
- Mide qué tan contento está el cliente con la atención
- Aumenta con buenas respuestas
- Disminuye con respuestas inadecuadas

### Paciencia (0-100)
- Mide cuánto aguantará el cliente antes de irse
- Se agota con el tiempo y malas respuestas
- Se recupera con respuestas excelentes

## 🔄 Ejemplo de Sesión Completa

```
> COMENZAR TEST

[Sistema muestra cliente enojado vía WhatsApp con problema de envío]

> Lamento muchísimo esta situación. Entiendo perfectamente su frustración 
  por la demora. Voy a revisar su pedido ahora mismo y le daré una solución 
  inmediata.

[Cliente responde positivamente]

> He verificado que hay un retraso en el almacén. Voy a hacer dos cosas: 
  1) Envío express sin costo, llegará mañana. 2) 20% de descuento en su 
  próxima compra. ¿Le parece bien?

[Cliente acepta]

> Perfecto. Le enviaré el número de rastreo en 15 minutos a su email. 
  ¿Hay algo más en lo que pueda ayudarle hoy?

[Cliente finaliza satisfecho]

> /finalizar

[Sistema muestra informe completo con puntajes altos]
```

## 🧪 Pruebas Automatizadas

Para verificar que el sistema funciona correctamente:

```bash
python3 test_evaluador.py
```

Esto ejecuta una suite completa de pruebas que valida:
- Adaptación de canales
- Generación de personalidades
- Sistema de evaluación
- Flujo completo de conversación
- Generación de informes

## 📁 Archivos Generados

Cada evaluación genera un archivo JSON con el formato:
```
evaluacion_YYYYMMDD_HHMMSS.json
```

Este archivo contiene:
- Configuración de la prueba
- Métricas detalladas
- Historial completo del diálogo
- Puntajes por turno
- Estado final del cliente

## 🎯 Casos de Uso

### 1. Capacitación de Agentes
Use el sistema para que agentes practiquen diferentes escenarios antes de atender clientes reales.

### 2. Evaluación de Desempeño
Genere escenarios estándar para evaluar a diferentes agentes de manera consistente.

### 3. Desarrollo de Habilidades
Identifique áreas de mejora específicas para cada agente basándose en los puntajes.

### 4. Quality Assurance
Compare el desempeño de agentes a lo largo del tiempo usando los informes JSON.

## ❓ Solución de Problemas

### El programa no inicia
```bash
# Verificar versión de Python
python3 --version  # Debe ser 3.6 o superior

# Verificar que el archivo es ejecutable
chmod +x evaluador_agentes.py
```

### No se generan archivos JSON
- Los archivos se guardan en el directorio actual
- Verificar permisos de escritura en el directorio
- Asegurarse de finalizar la prueba con `/finalizar`

### Las respuestas del cliente no tienen sentido
- Esto es normal, el cliente es simulado y puede responder de forma inesperada
- Use `/finalizar` para terminar la prueba actual
- Inicie una nueva prueba con `COMENZAR TEST`

## 📞 Soporte

Para reportar problemas o sugerir mejoras, abra un issue en GitHub:
https://github.com/apu242007/autobot/issues
