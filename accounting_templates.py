### Plantillas para realizar cuentas contables

"""
Parameter Definition




"""

dict_precios_1 = {
    # Combinaciones de "NCT" como vendedor
    ("NCT", "ZF", "materia prima"): 20,
    ("NCT", "ZF", "intermedio"): 80,
    ("NCT", "ZF", "final"): 100,
    ("NCT", "NCT", "materia prima"): 20,
    ("NCT", "NCT", "intermedio"): 80,
    ("NCT", "NCT", "final"): 100,
    # Combinaciones de "ZF" como vendedor
    ("ZF", "NCT", "materia prima"): 20,
    ("ZF", "NCT", "intermedio"): 80,
    ("ZF", "NCT", "final"): 90,
    ("ZF", "ZF", "materia prima"): 20,
    ("ZF", "ZF", "intermedio"): 80,
    ("ZF", "ZF", "final"): 100,
}


plantillas_contables_1 = {
    "materia prima": {
        "compra": {
            "debito": [("1405", "precio_mp")],
            "credito": [("1105", "precio_mp")],
        },
        "venta": {
            "debito": [("1105", "precio_mp"), ("6135", "costo")],
            "credito": [("4135", "precio_mp"), ("1405", "costo")],
        },
        "produccion": {
            "debito": [("71", "precio_mp"), ("1410", "precio_mp")],
            "credito": [("1405", "precio_mp"), ("71", "precio_mp")],
        },
    },
    "bien intermedio": {
        "compra": {
            "debito": [("1405", "precio_bien_intermedio")],
            "credito": [("1105", "precio_bien_intermedio")],
        },
        "venta": {
            "debito": [("1105", "precio_bien_intermedio"), ("6135", "costo")],
            "credito": [("4135", "precio_bien_intermedio"), ("1410", "costo")],
        },
        "produccion": {
            "debito": [("71", "precio_mp"), ("1410", "precio_mp")],
            "credito": [("1410", "precio_mp"), ("71", "precio_mp")],
        },
    },
    "bien final": {
        "compra": {
            "debito": [("1405", "precio_bien")],
            "credito": [("1105", "precio_bien")],
        },
        "venta": {
            "debito": [("1105", "precio_bien_final"), ("6120", "costo")],
            "credito": [("4120", "precio_bien_final"), ("1430", "costo")],
        },
    },
}
