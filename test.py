from accounting_templates import plantillas_contables_1, dict_precios_1

from classes import Agent, NCT, ZF, Good, Transaccion, LibroContable, Account

from utils import cargar_plantillas_cuentas


# prueba


# TODO Usar pathlib
ruta = r"C:\Users\andre\OneDrive\Documentos\Repositories\MIT_Tax_Avoidance\FTZ_Model\directorio_cuentas.xlsx"

plantilla_1 = cargar_plantillas_cuentas(
    ruta
)  ### Generar plantilla para las cuentas basada en el PUC


# Inicializar agentes
comprador = NCT(
    nombre="Empresa NCT",
    plantillas_cuentas=plantilla_1,
    plantillas_transacciones=plantillas_contables_1,
)
vendedor = ZF(
    nombre="Empresa ZF",
    plantillas_cuentas=plantilla_1,
    plantillas_transacciones=plantillas_contables_1,
)

# Crear un bien
bien_mp = Good(name="Acero", price=100)
bien_mp.tipo_bien = "materia prima"

# Crear una transacción
transaccion = Transaccion(
    vendedor=vendedor,
    comprador=comprador,
    bien=bien_mp,
    dict_precios_transaccion=dict_precios_1,
)

# Registrar la compra
transaccion.registrar_compra()
