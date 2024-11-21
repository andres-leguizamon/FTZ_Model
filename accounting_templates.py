### Plantillas para realizar cuentas contables


"""
Parameter Definition




"""

dict_precios_1 = {
    # Combinaciones de "MKT" como vendedor
    ("MKT", "ZF", "materia prima"): 20,
    ("MKT", "NCT", "materia prima"): 20,
    # Combinaciones de "MKT" como comprador
    ("NCT", "MKT", "bien final"): 100,
    ("ZF", "MKT", "bien final"): 100,
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
            "debito": [("1405", "precio")],
            "credito": [("1105", "precio")],
        },
        "venta": {
            "debito": [("1105", "precio"), ("6135", "costo")],
            "credito": [("4135", "precio"), ("1405", "costo")],
        },
        "produccion": {
            "debito": [("71", "costo"), ("1410", "costo")],
            "credito": [("1405", "costo"), ("71", "costo")],
        },
    },
    "bien intermedio": {
        "compra": {
            "debito": [("1405", "precio")],
            "credito": [("1105", "precio")],
        },
        "venta": {
            "debito": [("1105", "precio"), ("6135", "costo")],
            "credito": [("4135", "precio"), ("1410", "costo")],
        },
        "produccion": {
            "debito": [("71", "costo"), ("1410", "costo")],
            "credito": [("1410", "costo"), ("71", "costo")],
        },
    },
    "bien final": {
        "compra": {
            "debito": [("1405", "precio")],
            "credito": [("1105", "precio")],
        },
        "venta": {
            "debito": [("1105", "precio"), ("6120", "costo")],
            "credito": [("4120", "precio"), ("1430", "costo")],
        },
    },
}
