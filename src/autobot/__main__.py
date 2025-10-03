"""Punto de entrada del paquete para ejecutar la demo integrada."""

from __future__ import annotations

from .demo import ejecutar_demo


def main() -> None:
    """Imprime en consola el resultado de la demo."""

    print(ejecutar_demo())


if __name__ == "__main__":  # pragma: no cover - compatibilidad con `python -m`
    main()
