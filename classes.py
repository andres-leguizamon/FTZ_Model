#! Script para realizar la calculadora

from typing import List, Dict, Optional, Tuple
from abc import ABC, abstractmethod

from utils import cargar_plantillas_cuentas


### Ensayo

# TODO Usar pathlib
ruta = r"C:\Users\andre\OneDrive\Documentos\Repositories\MIT_Tax_Avoidance\FTZ_Model\directorio_cuentas.xlsx"

plantilla_1 = cargar_plantillas_cuentas(
    ruta
)  ### Generar plantilla para las cuentas basada en el PUC


class Account:
    """
    Clase para generar las cuentas y registrarlas
    """

    def __init__(self, name: str, tipo: int):
        self.historial = {}  # Diccionario vacío para el historial
        self.contador_transacciones = 0  # Contador de transacciones
        self.name = name
        self.tipo = tipo

    def registrar_transaccion(self, debe=0, haber=0) -> None:
        if not isinstance(debe, (int, float)) or not isinstance(haber, (int, float)):
            raise ValueError("Los valores de 'debe' y 'haber' deben ser números.")

        # Aumenta el contador de transacciones
        self.contador_transacciones += 1

        # Crea un registro de la transacción
        transaccion = {"debe": debe, "haber": haber}

        # Añade la transacción al historial
        self.historial[self.contador_transacciones] = transaccion

    def mostrar_historial(self) -> None:
        return self.historial

    def calcular_totales(self) -> Dict:
        total_debe = sum(transaccion["debe"] for transaccion in self.historial.values())
        total_haber = sum(
            transaccion["haber"] for transaccion in self.historial.values()
        )
        neto = total_haber - total_debe
        totales_cuenta = {}

        if neto > 0:
            saldo = {"haber": neto}
        elif neto < 0:
            saldo = {"debe": -neto}
        else:
            saldo = "Saldo neto: 0 (Debe y Haber son iguales)"

        totales_cuenta = {"Debe": total_debe, "Haber": total_haber, "Neto": saldo}

        return totales_cuenta

    def saldo_neto(self) -> Dict:
        total_debe = sum(transaccion["debe"] for transaccion in self.historial.values())
        total_haber = sum(
            transaccion["haber"] for transaccion in self.historial.values()
        )
        neto = total_haber - total_debe

        if neto > 0:
            saldo = {"haber": neto}
        elif neto < 0:
            saldo = {"debe": -neto}
        else:
            saldo = {"debe": 0, "haber": 0}

        return saldo


### Prueba

inventarios = Account("inventarios", 1)

inventarios.registrar_transaccion(100, 0)

inventarios.registrar_transaccion(0, 50)

inventarios.calcular_totales()


### ---------------------- Clase Good ------------------------------


class Good(ABC):
    """
    Clase abstracta base para los bienes.
    Permite añadir precio, tarifa del IVA, arancel e insumos necesarios para producir el bien.
    """

    def __init__(
        self,
        name: str,
        price: float,
        tariff: float,
        insumos: Dict[str, float] = None,
    ):
        """
        Inicializa un nuevo bien.

        :param name: Nombre del bien.
        :param price: Precio base del bien.
        :param tariff: Arancel aplicado al bien (en porcentaje).
        :param insumos: Diccionario de insumos necesarios para producir el bien.
                        Las claves son los nombres de otros bienes y los valores son las cantidades requeridas.
        """
        self.name = name
        self.price = price
        self.insumos = insumos if insumos is not None else {}
        self.tipo_bien = None  # "materia prima", "intermedio", "final"

    def asignar_tipo_bien(self, bienes_dict, usados_como_insumo):
        """
        Asigna el tipo de bien basado en sus insumos y si es insumo de otros bienes.

        :param bienes_dict: Diccionario de todos los bienes {nombre: objeto bien}.
        :param usados_como_insumo: Diccionario {nombre_bien: [bienes_que_lo_usan]}.
        """
        tiene_insumos = len(self.insumos) > 0
        es_insumo = self.name in usados_como_insumo

        if tiene_insumos and es_insumo:
            self.tipo_bien = "intermedio"
        elif not tiene_insumos and es_insumo:
            self.tipo_bien = "materia prima"
        elif tiene_insumos and not es_insumo:
            self.tipo_bien = "final"
        else:
            self.tipo_bien = "independiente"  # No tiene insumos y no es insumo de nadie

    def __repr__(self):
        return f"{self.name} ({self.tipo_bien})"


# -------------- Clase Agente ----------------


class Agent(ABC):
    """
    Clase base abstracta para las empresas.
    """

    def __init__(
        self,
        nombre: str,
        plantillas_cuentas: Dict,
    ):
        """
        Inicializa una nueva instancia de Agent.

        :param nombre: El nombre del agente.
        :param plantillas_cuentas: Un diccionario que contiene las plantillas de cuentas
                                   que se usarán para crear instancias de Account para el agente.

        :param bienes_vendidos: Una lista de bienes vendidos por el agente.
        :param bienes_producidos: Una lista de bienes producidos por el agente.
        :param status_bienes: Un diccionario que contiene el status de todos los bienes del modelo para el agente,
                              donde las claves son los posibles status y los valores son listas bienes
        """

        self.nombre = nombre
        self.cuentas = {}
        self.type = self.get_type()  # Establece el tipo según la subclase

        # Inicializar las cuentas contables del agente
        for codigo, plantilla in plantillas_cuentas.items():
            cuenta_nombre = plantilla["cuenta"]
            codigo_tipo_cuenta = plantilla["codigo_tipo_cuenta"]
            # Creamos una nueva instancia de Account para cada cuenta del agente
            self.cuentas[codigo] = Account(name=cuenta_nombre, tipo=codigo_tipo_cuenta)

    def registrar_transaccion(
        self,
        es_venta: bool,
        cuenta_debito_codigo: str,
        cuenta_credito_codigo: str,
        precio: float,
    ):
        """
        Registra una transacción contable en las cuentas del agente.

        :param otro_agente: El agente con quien se realiza la transacción.
        :param bien: El bien que se transacciona.
        :param es_venta: True si es una venta, False si es una compra.
        :param cuenta_debito_codigo: Código de la cuenta a debitar.
        :param cuenta_credito_codigo: Código de la cuenta a acreditar.
        :param precio: Precio al cual se realiza la transacción.
        """
        cuenta_debito = self.get_account_by_code(cuenta_debito_codigo)
        cuenta_credito = self.get_account_by_code(cuenta_credito_codigo)

        if cuenta_debito is None or cuenta_credito is None:
            raise ValueError("Código de cuenta no válido.")

        if es_venta:
            # Registro en las cuentas del vendedor
            cuenta_debito.registrar_transaccion(debe=precio, haber=0)
            cuenta_credito.registrar_transaccion(debe=0, haber=precio)
        else:
            # Registro en las cuentas del comprador
            cuenta_debito.registrar_transaccion(debe=precio, haber=0)
            cuenta_credito.registrar_transaccion(debe=0, haber=precio)

    def producir_bien(
        self,
        bien_producido: Good,
        insumo_utilizado: Good,
        cuenta_debito_codigo: str,
        cuenta_credito_codigo: str,
        costo_produccion: float,
    ):
        """
        Registra el proceso de producción en las cuentas del agente.

        :param bien_producido: El bien que se produce.
        :param insumo_utilizado: El insumo utilizado en la producción.
        :param cuenta_debito_codigo: Código de la cuenta a debitar.
        :param cuenta_credito_codigo: Código de la cuenta a acreditar.
        :param costo_produccion: Costo de producción del bien.
        """
        cuenta_debito = self.get_account_by_code(cuenta_debito_codigo)
        cuenta_credito = self.get_account_by_code(cuenta_credito_codigo)

        if bien_producido is None or insumo_utilizado is None:
            raise ValueError("Bien o insumo no válido.")

        if insumo_utilizado not in bien_producido.insumos:
            raise ValueError("El insumo utilizado no es un insumo del bien producido.")

        if cuenta_debito is None or cuenta_credito is None:
            raise ValueError("Código de cuenta no válido.")

        # Registrar salida del insumo
        cuenta_credito.registrar_transaccion(debe=0, haber=costo_produccion)

        # Registrar entrada del bien producido
        cuenta_debito.registrar_transaccion(debe=costo_produccion, haber=0)

    @abstractmethod
    def get_type(self) -> str:
        """
        Método abstracto para obtener el tipo de empresa.
        Debe ser implementado por las subclases.
        """
        pass

    def get_account_by_name(self, account_name: str) -> Optional["Account"]:
        """
        Obtiene una cuenta por su nombre.

        :param account_name: El nombre de la cuenta a buscar.
        :return: La cuenta encontrada o None si no existe.
        """
        for cuenta in self.cuentas.values():
            if cuenta.name == account_name:
                return cuenta
        return None

    def get_account_by_code(self, account_code: str) -> Optional["Account"]:
        """
        Obtiene una cuenta por su código.

        :param account_code: El código de la cuenta a buscar.
        :return: La cuenta encontrada o None si no existe.
        """
        return self.cuentas.get(account_code, None)


# Subclase para empresas ZF
class ZF(Agent):
    def get_type(self) -> str:
        return "ZF"


# Subclase para empresas NCT
class NCT(Agent):
    def get_type(self) -> str:
        return "NCT"


# ------------------------------------ Clase Modelo  ------------------------------------


class Modelo:
    """Clase para representar el modelo de bienes y empresas."""

    def __init__(
        self,
        lista_bienes: List[Good],
        lista_agentes: List[Agent],
        precios_transaccion: Dict[Tuple[str, str, str], float],
    ):
        self.lista_bienes = lista_bienes
        self.lista_agentes = lista_agentes
        self.precios_transaccion = (
            precios_transaccion  # Diccionario para parametrizar precios
        )

    def obtener_precio_transaccion(
        self, bien: Good, vendedor: Agent, comprador: Agent
    ) -> float:
        """
        Determina el precio de transacción del bien según los parámetros definidos en precios_transaccion.

        :param bien: Objeto Good que se va a transaccionar.
        :param vendedor: Agente que vende el bien.
        :param comprador: Agente que compra el bien.
        :return: Precio ajustado del bien.
        """
        # Clave para acceder al diccionario de precios
        key = (vendedor.type, comprador.type, bien.tipo_bien)
        if key in self.precios_transaccion:
            precio = self.precios_transaccion[key]
        else:
            # Si no se encuentra una regla específica, usar el precio base del bien
            precio = bien.price
        return precio

    def realizar_trade(self, vendedor: Agent, comprador: Agent, bien: Good):
        """
        Realiza una transacción de venta de un bien entre dos agentes y actualiza sus cuentas.

        :param vendedor: Agente que vende el bien.
        :param comprador: Agente que compra el bien.
        :param bien: El bien que se transacciona.
        """
        # Obtener el precio ajustado de la transacción
        precio = self.obtener_precio_transaccion(bien, vendedor, comprador)

        # Determinar las cuentas a afectar según el tipo de bien
        # Debes ajustar estos códigos de cuenta según tus plantillas
        cuentas_config = {
            "materia prima": {
                "venta": {"debito": "1105", "credito": "4135"},
                "compra": {"debito": "1435", "credito": "2205"},
            },
            "intermedio": {
                "venta": {"debito": "1106", "credito": "4140"},
                "compra": {"debito": "1436", "credito": "2206"},
            },
            "final": {
                "venta": {"debito": "1107", "credito": "4145"},
                "compra": {"debito": "1437", "credito": "2207"},
            },
        }

        tipo_bien = bien.tipo_bien
        cuentas_vendedor = cuentas_config[tipo_bien]["venta"]
        cuentas_comprador = cuentas_config[tipo_bien]["compra"]

        # Registrar la transacción en las cuentas del vendedor
        vendedor.registrar_transaccion(
            otro_agente=comprador,
            bien=bien,
            es_venta=True,
            cuenta_debito_codigo=cuentas_vendedor["debito"],
            cuenta_credito_codigo=cuentas_vendedor["credito"],
            precio=precio,
        )

        # Registrar la transacción en las cuentas del comprador
        comprador.registrar_transaccion(
            otro_agente=vendedor,
            bien=bien,
            es_venta=False,
            cuenta_debito_codigo=cuentas_comprador["debito"],
            cuenta_credito_codigo=cuentas_comprador["credito"],
            precio=precio,
        )

    def realizar_produccion(
        self, agente: Agent, bien_producido: Good, insumo_utilizado: Good
    ):
        """
        Realiza el proceso de producción de un bien y actualiza las cuentas del agente.

        :param agente: El agente que realiza la producción.
        :param bien_producido: El bien que se produce.
        :param insumo_utilizado: El insumo utilizado en la producción.
        """
        # Determinar el costo de producción (puedes ajustar esta lógica)
        costo_produccion = (
            insumo_utilizado.price
        )  # Suponemos que el costo es el precio del insumo

        # Determinar las cuentas a afectar según el tipo de producción
        # Debes ajustar estos códigos de cuenta según tus plantillas
        cuentas_produccion = {
            ("materia prima", "intermedio"): {
                "debito": "1436",  # Inventario de producto intermedio
                "credito": "1435",  # Inventario de materia prima
            },
            ("intermedio", "final"): {
                "debito": "1437",  # Inventario de producto final
                "credito": "1436",  # Inventario de producto intermedio
            },
        }

        tipo_produccion = (insumo_utilizado.tipo_bien, bien_producido.tipo_bien)
        if tipo_produccion in cuentas_produccion:
            cuentas = cuentas_produccion[tipo_produccion]
            cuenta_debito_codigo = cuentas["debito"]
            cuenta_credito_codigo = cuentas["credito"]
        else:
            raise ValueError("Tipo de producción no soportado")

        # Registrar la producción en las cuentas del agente
        agente.producir_bien(
            bien_producido=bien_producido,
            insumo_utilizado=insumo_utilizado,
            cuenta_debito_codigo=cuenta_debito_codigo,
            cuenta_credito_codigo=cuenta_credito_codigo,
            costo_produccion=costo_produccion,
        )
