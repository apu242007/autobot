"""Colección de escenarios realistas utilizados en las simulaciones."""

from __future__ import annotations

from typing import List

from .models import EscenarioObra


ESCENARIOS_OBRA: List[EscenarioObra] = [
    EscenarioObra(
        id="ESC-001",
        titulo="Retraso en entrega de materiales críticos",
        descripcion=(
            "El cliente es supervisor de obra en un proyecto petrolero. Hace 5 días "
            "ordenó 200 bolsas de cemento especial para fundaciones críticas."
            " La entrega prometida en 72 horas no se cumplió, la obra está paralizada"
            " y hay operarios inactivos mientras la gerencia presiona por avances."
            " Código de pedido: #CM-2024-8847."
        ),
        complejidad="alta",
        area="logistica",
        palabras_clave=[
            "cemento",
            "obra paralizada",
            "entrega",
            "72 horas",
            "Vaca Muerta",
        ],
        solucion_esperada=(
            "1. Pedir disculpas genuinas\n"
            "2. Verificar estado del pedido con el código\n"
            "3. Ofrecer envío express sin costo adicional\n"
            "4. Proveer tracking en tiempo real\n"
            "5. Compensación: descuento o materiales extra\n"
            "6. Asignar responsable con contacto directo\n"
            "7. Comprometer fecha y hora de entrega en 24 horas"
        ),
        tiempo_estimado_resolucion=8,
    ),
    EscenarioObra(
        id="ESC-002",
        titulo="Material defectuoso instalado - riesgo de obra",
        descripcion=(
            "Un contratista recibió perfiles de acero instalados en un 40 %. Un"
            " inspector detectó espesor menor al especificado, con riesgo"
            " estructural y potenciales acciones legales. Lote: ACERO-L0445."
        ),
        complejidad="alta",
        area="calidad",
        palabras_clave=[
            "acero",
            "defectuoso",
            "inspección",
            "norma IRAM",
            "acciones legales",
        ],
        solucion_esperada=(
            "1. Reconocer la gravedad del problema\n"
            "2. Enviar ingeniero auditor en 24 horas\n"
            "3. Retirar material defectuoso sin costo\n"
            "4. Reemplazar por material certificado\n"
            "5. Cubrir desmontaje y reinstalación\n"
            "6. Emitir carta de garantía técnica\n"
            "7. Auditar lotes del mismo proveedor\n"
            "8. Ofrecer compensación económica"
        ),
        tiempo_estimado_resolucion=12,
    ),
    EscenarioObra(
        id="ESC-003",
        titulo="Error en facturación - cobro duplicado",
        descripcion=(
            "Una constructora detectó el cobro duplicado de un pedido de"
            " cerámicos por $850.000 ARS. Pagaron ambas facturas por error"
            " administrativo y necesitan reintegro urgente para afrontar"
            " pagos de nómina."
        ),
        complejidad="media",
        area="administracion",
        palabras_clave=[
            "facturación",
            "duplicado",
            "reintegro",
            "transferencia",
        ],
        solucion_esperada=(
            "1. Validar facturas reportadas\n"
            "2. Confirmar error y disculparse\n"
            "3. Iniciar devolución inmediata por transferencia\n"
            "4. Plazo máximo de 48 horas hábiles\n"
            "5. Enviar comprobante de transferencia\n"
            "6. Compartir contacto de administración\n"
            "7. Ofrecer bono o descuento compensatorio"
        ),
        tiempo_estimado_resolucion=6,
    ),
    EscenarioObra(
        id="ESC-004",
        titulo="Cambio de especificaciones técnicas post-pedido",
        descripcion=(
            "El cliente solicitó aberturas de aluminio y el arquitecto cambió"
            " el proyecto a vidrios DVH cuando la producción ya había"
            " comenzado. Requiere conocer opciones, demoras y costos"
            " asociados para el pedido #AB-2024-1102."
        ),
        complejidad="baja",
        area="ventas",
        palabras_clave=[
            "aberturas",
            "modificación",
            "DVH",
            "producción",
        ],
        solucion_esperada=(
            "1. Mostrar empatía por cambios de proyecto\n"
            "2. Verificar estado de fabricación\n"
            "3. Explicar opciones según avance\n"
            "4. Enviar cotización en menos de 4 horas\n"
            "5. Facilitar proceso sin trabas\n"
            "6. Confirmar nueva fecha de entrega"
        ),
        tiempo_estimado_resolucion=5,
    ),
]
