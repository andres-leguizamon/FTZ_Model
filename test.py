import itertools
from typing import List, Dict, Tuple

# Importar tus módulos y clases
from accounting_templates import dict_precios_1, plantillas_contables_1
from utils import cargar_plantillas_cuentas
import classes as cl


pan = cl.MateriaPrima("pan", 0)

# Ruta de la plantilla contable
ruta = r"C:\Users\andre\OneDrive\Documentos\Repositories\MIT_Tax_Avoidance\FTZ_Model\directorio_cuentas.xlsx"

# Cargar la plantilla contable
plantilla_1 = cargar_plantillas_cuentas(ruta)

# Definir el diccionario de precios de transacción (asegúrate de que esté definido correctamente)
dict_precios_transaccion = dict_precios_1  # Asumiendo que dict_precios_1 está definido


# Función para calcular la utilidad del plan
def utilidad_plan(
    plan: List[int], dict_precios_transaccion: Dict[Tuple[str, str, str], float]
):
    # Crear nuevas instancias de los agentes para cada iteración
    planta_ZF = cl.ZF("ZF", plantilla_1, plantillas_contables_1)
    planta_NCT = cl.NCT("NCT", plantilla_1, plantillas_contables_1)

    # Crear el ejecutor del plan y ejecutar el plan
    ejecutor = cl.EjecutorPlan(plan, planta_NCT, planta_ZF, dict_precios_transaccion)
    ejecutor.ejecutar()

    # Calcular la utilidad operacional de cada planta
    utilidad_NCT = ejecutor.planta_NCT.libro_contable.calcular_utilidad_operacional(
        0.35
    )
    utilidad_ZF = ejecutor.planta_ZF.libro_contable.calcular_utilidad_operacional(0.20)

    # Sumar las utilidades para obtener la utilidad total
    utilidad_total = utilidad_NCT + utilidad_ZF
    return utilidad_total


# Función para generar los estados financieros finales del plan
def contabilidad_final_plan(
    plan: List[int], dict_precios_transaccion: Dict[Tuple[str, str, str], float]
):
    # Crear nuevas instancias de los agentes
    planta_ZF = cl.ZF("ZF", plantilla_1, dict_precios_transaccion)
    planta_NCT = cl.NCT("NCT", plantilla_1, dict_precios_transaccion)

    # Ejecutar el plan
    ejecutor = cl.EjecutorPlan(plan, planta_NCT, planta_ZF, dict_precios_transaccion)
    ejecutor.ejecutar()

    # Generar los estados financieros de cada planta
    estado_NCT = ejecutor.planta_NCT.libro_contable.generar_estado_resultados()
    estado_ZF = ejecutor.planta_ZF.libro_contable.generar_estado_resultados()
    return estado_NCT, estado_ZF


# Variables para almacenar el mejor plan y la mayor utilidad
mejor_plan = None
mayor_utilidad = float("-inf")

# Generar todas las combinaciones posibles de planes (8 combinaciones)
for plan in itertools.product([0, 1], repeat=3):
    plan = list(plan)  # Convertir la tupla en lista
    utilidad = utilidad_plan(plan, dict_precios_transaccion)

    print(f"Plan: {plan}, Utilidad Total: {utilidad}")

    # Actualizar el mejor plan si se encuentra una mayor utilidad
    if utilidad > mayor_utilidad:
        mayor_utilidad = utilidad
        mejor_plan = plan

# Mostrar el mejor plan y su utilidad
print("\nEl mejor plan es:", mejor_plan)
print("Con una utilidad total de:", mayor_utilidad)

# Obtener y mostrar los estados financieros finales del mejor plan
estado_NCT, estado_ZF = contabilidad_final_plan(mejor_plan, dict_precios_transaccion)
print("\nEstado de Resultados de NCT:")
print(estado_NCT)
print("\nEstado de Resultados de ZF:")
print(estado_ZF)
