from typing import List, Dict, Tuple
from itertools import product
from typing import List, Dict, Tuple

# Importar tus módulos y clases

import classes as cl


def utilidad_plan(
    planta_NCT: cl.NCT,
    planta_ZF: cl.ZF,
    plan: List[int],
    dict_precios_transaccion: Dict[Tuple[str, str, str], float],
):
    """
    Calcula la utilidad agregada para un plan de producción y precios de transacción dados.

    :param planta_NCT: Instancia de la clase NCT, que representa la planta de NCT.
    :param planta_ZF: Instancia de la clase ZF, que representa la planta de ZF.
    :param plan: Lista de enteros que representa el plan de producción (0 o 1).
    :param dict_precios_transaccion: Diccionario con los precios de transacción.
    :return: La utilidad agregada.
    """
    ejecutor = cl.EjecutorPlan(plan, planta_NCT, planta_ZF, dict_precios_transaccion)
    ejecutor.ejecutar()

    utilidad_NCT = ejecutor.planta_NCT.libro_contable.calcular_utilidad_operacional(
        0.35
    )

    utilidad_ZF = ejecutor.planta_ZF.libro_contable.calcular_utilidad_operacional(0.2)

    utilidad_agregada = utilidad_NCT + utilidad_ZF

    return utilidad_agregada


#####--------------- Loop de Busqueda ----------------------


def encontrar_mejor_plan(NCT: cl.NCT, ZF: cl.ZF, dict_precios_transaccion, plan_base):
    """
    Encuentra el mejor plan de decisiones que maximice la utilidad agregada.

    Args:
        planta_NCT: Objeto que representa la planta NCT.
        planta_ZF: Objeto que representa la planta ZF.
        dict_precios_transaccion: Diccionario con los precios de transacción.
        plan_base: Lista base que define el número de decisiones posibles.

    Returns:
        tuple: Mejor plan encontrado y la utilidad agregada correspondiente.
    """
    # Define el rango de planes posibles. Aquí suponemos que cada elemento del plan puede ser 0 o 1.
    num_decisiones = len(plan_base)  # El número de decisiones en el plan base
    todos_los_planes = list(product([0, 1], repeat=num_decisiones))

    # Variable para almacenar el mejor plan y su utilidad
    mejor_plan = None
    max_utilidad_agregada = float("-inf")

    # Iterar sobre todos los planes posibles
    for plan_actual in todos_los_planes:
        # Evaluar la utilidad agregada para el plan actual
        utilidad_agregada = utilidad_plan(
            planta_NCT=NCT,
            planta_ZF=ZF,
            plan=list(plan_actual),
            dict_precios_transaccion=dict_precios_transaccion,
        )

        # Comparar y actualizar el mejor plan si se encuentra una mayor utilidad
        if utilidad_agregada > max_utilidad_agregada:
            max_utilidad_agregada = utilidad_agregada
            mejor_plan = plan_actual

    # Retorna el mejor plan y la utilidad agregada correspondiente
    return {"mejor_plan": mejor_plan, "max_utilidad_agregada": max_utilidad_agregada}
