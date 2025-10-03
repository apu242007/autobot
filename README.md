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
source .venv/bin/activate
pip install -e .
black src tests
pytest
```

