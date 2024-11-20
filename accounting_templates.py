### Plantillas para realizar cuentas contables

from typing import Dict, Tuple
from classes import Flow

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


def mapear_valor(variable: str, flow: Flow):
    """
    Mapea el valor de una variable dada en el flujo de caja a su valor real.

    :param variable: El nombre de la variable a mapear (precio o costo).
    :param flow: El flujo de caja actual.
    :return: El valor mapeado de la variable (None si no se reconoce la variable).
    """
    if variable == "precio":
        return flow.precio_venta
    elif variable == "costo":
        return flow.ultimo_costo
    else:
        return None  # O puedes lanzar una excepción si la variable no es reconocida


def obtener_precio_transaccion(
    key: Tuple[str, str, str],
    dict_precios_transaccion: Dict[Tuple[str, str, str], float],
) -> float:
    """
    Determina el precio de transaccion segun el diccionario de precios
    el parametro key es
    """
    # Clave para acceder al diccionario de precios
    if key in dict_precios_transaccion:
        precio = dict_precios_transaccion[key]
    return precio
