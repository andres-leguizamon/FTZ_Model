from typing import List, Dict, Tuple


from accounting_templates import plantillas_contables_1
from utils import cargar_plantillas_cuentas
import classes as cl


# Ruta de la plantilla contable
ruta = r"C:\Users\andre\OneDrive\Documentos\Repositories\MIT_Tax_Avoidance\FTZ_Model\directorio_cuentas.xlsx"

# Cargar la plantilla contable
plantilla_1 = cargar_plantillas_cuentas(ruta)


### Diccionario precios:
dict_precios_2 = {
    # Combinaciones de "MKT" como vendedor
    ("MKT", "ZF", "materia_prima"): 5,
    ("MKT", "NCT", "materia_prima"): 5,
    # Combinaciones de "MKT" como comprador
    ("NCT", "MKT", "bien_final"): 7,
    ("ZF", "MKT", "bien_final"): 7,
    # Combinaciones de "NCT" como vendedor
    ("NCT", "ZF", "materia_prima"): 3,
    ("NCT", "ZF", "bien_intermedio"): 5,
    ("NCT", "ZF", "bien_final"): 6,
    ("NCT", "NCT", "materia_prima"): 20,
    ("NCT", "NCT", "bien_intermedio"): 80,
    ("NCT", "NCT", "bien_final"): 100,
    # Combinaciones de "ZF" como vendedor
    ("ZF", "NCT", "materia_prima"): 2,
    ("ZF", "NCT", "bien_intermedio"): 4,
    ("ZF", "NCT", "bien_final"): 6,
    ("ZF", "ZF", "materia_prima"): 20,
    ("ZF", "ZF", "bien_intermedio"): 80,
    ("ZF", "ZF", "bien_final"): 100,
}

### Instanciar Agentes de NCT y ZF
planta_NCT = cl.NCT("NCT", plantilla_1, plantillas_contables_1)
planta_ZF = cl.ZF("ZF", plantilla_1, plantillas_contables_1)

plan = [0, 1, 1]

ejecutor = cl.EjecutorPlan(plan, planta_NCT, planta_ZF, dict_precios_2)
ejecutor.ejecutar()


u1 = planta_NCT.generar_estado_resultados()

u2 = planta_ZF.generar_estado_resultados()


W = (
    planta_NCT.calcular_utilidad_operacional()
    + planta_ZF.calcular_utilidad_operacional()
)

print(u1, u2, "Utilidad Agregada", "|", W)
