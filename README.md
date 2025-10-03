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
# Si no puedes instalar en modo editable (por ejemplo, sin conexión),
# usa `python run_demo.py` para lanzar la simulación directamente.
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

# Alternativa sin instalación previa (añade automáticamente ``src`` al PYTHONPATH)
python run_demo.py

# Servidor web estático con interfaz HTML
python serve_demo.py  # abre http://127.0.0.1:8000 en el navegador
```

El comando imprime en consola la información del escenario seleccionado, la
conversación de ejemplo y el informe final generado por el motor de evaluación.

