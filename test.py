from accounting_templates import plantillas_contables_1, dict_precios_1

from classes import Agent, NCT, ZF, Good, Transaccion, LibroContable, Account

from utils import cargar_plantillas_cuentas


# prueba


# TODO Usar pathlib
ruta = r"C:\Users\andre\OneDrive\Documentos\Repositories\MIT_Tax_Avoidance\FTZ_Model\directorio_cuentas.xlsx"

plantilla_1 = cargar_plantillas_cuentas(
    ruta
)  ### Generar plantilla para las cuentas basada en el PUC


# Crear las plantas

planta_NCT = NCT(
    nombre="Empresa NCT",
    plantillas_cuentas=plantilla_1,
    plantillas_transacciones=plantillas_contables_1,
)
planta_ZF = ZF(
    nombre="Empresa ZF",
    plantillas_cuentas=plantilla_1,
    plantillas_transacciones=plantillas_contables_1,
)

# Crear los bienes
bien_mp = Good(name="materia prima")
bien_mp.tipo_bien = "materia prima"

bien_intermedio = Good(name="intermedio")
bien_intermedio.tipo_bien = "intermedio"

bien_final = Good(name="final")
bien_final.tipo_bien = "final"


### Loop de Busqueda


def ejecutar_plan(
    decision_1: int, decision_2: int, decision_3: int, planta_1: ZF, planta_2: NCT
):
    # Verificar si los números son 1 o 0
    if all(decision in [0, 1] for decision in [decision_1, decision_2, decision_3]):
        # Convertir a booleanos
        decision_1 = bool(decision_1)
        decision_2 = bool(decision_2)
        decision_3 = bool(decision_3)
        return decision_1, decision_2, decision_3
    else:
        raise ValueError("Los números deben ser 0 o 1.")
