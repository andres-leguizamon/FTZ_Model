### Plantillas para realizar cuentas contables

"""

precio_unitario: Precio unitario del bien o servicio sin incluir impuestos.

cantidad: Número de unidades vendidas o compradas.

precio_total: precio_unitario * cantidad.

monto_iva: Impuesto calculado sobre el precio_total.

precio_con_iva: precio_total + monto_iva.

costo_unitario: Costo unitario de producción o compra.

costo_total: costo_unitario * cantidad.

costo_indirecto: Costos indirectos asociados (si aplica).

valor_total: Monto total de la transacción (puede ser igual a precio_con_iva o precio_total dependiendo del contexto).


"""

accounting_templates_1 = {
    "venta_mercancia_producida": {
        "debe": [
            (
                1105,
                "precio_con_iva",
            ),  # Efectivo o bancos aumenta por el precio total con IVA
            (
                6120,
                "costo_total",
            ),  # Costo de ventas aumenta por el costo total de producción
        ],
        "haber": [
            (4120, "precio_total"),  # Ingresos por ventas aumenta por el precio sin IVA
            (2408, "monto_iva"),  # IVA por pagar aumenta por el monto del IVA
            (
                1430,
                "costo_total",
            ),  # Inventario de productos terminados disminuye por el costo total
        ],
    },
    "venta_mercancia_producida_exenta": {
        "debe": [
            (
                1105,
                "precio_total",
            ),  # Efectivo o bancos aumenta por el precio total (exento de IVA)
            (
                6120,
                "costo_total",
            ),  # Costo de ventas aumenta por el costo total de producción
        ],
        "haber": [
            (4120, "precio_total"),  # Ingresos por ventas aumenta por el precio total
            (
                1430,
                "costo_total",
            ),  # Inventario de productos terminados disminuye por el costo total
        ],
    },
    "venta_mercancia_no_producida": {
        "debe": [
            (
                1105,
                "precio_con_iva",
            ),  # Efectivo o bancos aumenta por el precio total con IVA
            (
                6135,
                "costo_total",
            ),  # Costo de ventas aumenta por el costo total de la mercancía
        ],
        "haber": [
            (4135, "precio_total"),  # Ingresos por ventas aumenta por el precio sin IVA
            (2408, "monto_iva"),  # IVA por pagar aumenta por el monto del IVA
            (
                1435,
                "costo_total",
            ),  # Inventario de mercancía disminuye por el costo total
        ],
    },
    "venta_mercancia_no_producida_exenta": {
        "debe": [
            (
                1105,
                "precio_total",
            ),  # Efectivo o bancos aumenta por el precio total (exento de IVA)
            (
                6135,
                "costo_total",
            ),  # Costo de ventas aumenta por el costo total de la mercancía
        ],
        "haber": [
            (4135, "precio_total"),  # Ingresos por ventas aumenta por el precio total
            (
                1435,
                "costo_total",
            ),  # Inventario de mercancía disminuye por el costo total
        ],
    },
    "compra_materia_prima": {
        "debe": [
            (
                1405,
                "precio_total",
            ),  # Inventario de materia prima aumenta por el precio de compra sin IVA
            (2408, "monto_iva"),  # IVA por cobrar aumenta por el monto del IVA
        ],
        "haber": [
            (
                1105,
                "precio_con_iva",
            ),  # Efectivo o bancos disminuye por el total con IVA
        ],
    },
    "compra_materia_prima_sin_iva": {
        "debe": [
            (
                1405,
                "precio_total",
            ),  # Inventario de materia prima aumenta por el precio de compra
        ],
        "haber": [
            (
                1105,
                "precio_total",
            ),  # Efectivo o bancos disminuye por el precio de compra
        ],
    },
    "proceso_produccion": {
        "debe": [
            (
                1430,
                "costo_total",
            ),  # Inventario de productos terminados aumenta por el costo total de producción
        ],
        "haber": [
            (
                1405,
                "costo_total_materiales",
            ),  # Inventario de materia prima disminuye por el costo de los materiales utilizados
            (73, "costo_indirecto"),  # Costos indirectos reconocidos
        ],
    },
    "compra_bien_final_comercializable": {
        "debe": [
            (
                1435,
                "precio_total",
            ),  # Inventario de mercancía aumenta por el precio de compra sin IVA
            (2408, "monto_iva"),  # IVA por cobrar aumenta por el monto del IVA
        ],
        "haber": [
            (
                1105,
                "precio_con_iva",
            ),  # Efectivo o bancos disminuye por el total con IVA
        ],
    },
}
