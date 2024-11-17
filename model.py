#! Script para realizar la calculadora

from typing import List, Dict, Optional
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
        self.tariff = tariff
        self.insumos = insumos if insumos is not None else {}


class BienGravado(Good):
    """
    Clase para bienes gravados.
    """

    def __init__(
        self,
        name: str,
        price: float,
        iva_rate: float,
        tariff: float,
        insumos: Dict[str, float] = None,
    ):
        super().__init__(name, price, tariff, insumos)
        self.iva_rate = iva_rate
        self.status_iva = "gravado"


class BienExento(Good):
    """
    Clase para bienes exentos.
    """

    def __init__(
        self,
        name: str,
        price: float,
        tariff: float,
        insumos: Dict[str, float] = None,
    ):
        super().__init__(name, price, tariff, insumos)
        self.iva_rate = 0  # Un bien exento tiene tasa de IVA 0%
        self.status_iva = "exento"


class BienExcluido(Good):
    """
    Clase para bienes excluidos.
    """

    def __init__(
        self,
        name: str,
        price: float,
        insumos: Dict[str, float] = None,
    ):
        super().__init__(name, price, tariff=0, insumos=insumos)
        self.iva_rate = 0  # Un bien excluido no está gravado con IVA
        self.status_iva = "excluido"


# ---------------------- Clase Inventario -------------------------


class Lote:
    def __init__(self, good: Good, quantity: float, unit_cost: float):
        self.good = good
        self.quantity = quantity
        self.unit_cost = unit_cost


class Inventory:
    def __init__(self):
        # Diccionario para almacenar listas de lotes por bien
        self.lotes = {}

        # Diccionario para almacenar el método de costeo por bien
        self.costing_methods = {}

    def set_costing_method(self, good_name: str, method: str):
        if method not in ["FIFO", "LIFO", "WeightedAverage"]:
            raise ValueError(
                "Método de costeo inválido. Debe ser 'FIFO', 'LIFO' o 'WeightedAverage'."
            )
        self.costing_methods[good_name] = method

    def add_lote(self, good: Good, quantity: float, unit_cost: float):
        if good.name not in self.lotes:
            self.lotes[good.name] = []

        # Agregar un nuevo lote al inventario
        self.lotes[good.name].append(Lote(good, quantity, unit_cost))

    def remove_lote(self, good_name: str, quantity: float):
        if good_name not in self.lotes or not self.lotes[good_name]:
            raise ValueError(
                f"No hay suficiente inventario de {good_name} para retirar."
            )

        method = self.costing_methods.get(good_name, "FIFO")
        total_cost = 0.0
        quantity_to_remove = quantity

        if method == "FIFO":
            while quantity_to_remove > 0 and self.lotes[good_name]:
                first_lote = self.lotes[good_name][0]
                if first_lote.quantity <= quantity_to_remove:
                    total_cost += first_lote.quantity * first_lote.unit_cost
                    quantity_to_remove -= first_lote.quantity
                    self.lotes[good_name].pop(0)
                else:
                    total_cost += quantity_to_remove * first_lote.unit_cost
                    first_lote.quantity -= quantity_to_remove
                    quantity_to_remove = 0

        elif method == "LIFO":
            while quantity_to_remove > 0 and self.lotes[good_name]:
                last_lote = self.lotes[good_name][-1]
                if last_lote.quantity <= quantity_to_remove:
                    total_cost += last_lote.quantity * last_lote.unit_cost
                    quantity_to_remove -= last_lote.quantity
                    self.lotes[good_name].pop()
                else:
                    total_cost += quantity_to_remove * last_lote.unit_cost
                    last_lote.quantity -= quantity_to_remove
                    quantity_to_remove = 0

        elif method == "WeightedAverage":
            total_quantity = sum(lote.quantity for lote in self.lotes[good_name])
            if total_quantity < quantity:
                raise ValueError(
                    f"No hay suficiente inventario de {good_name} para retirar."
                )

            average_cost = (
                sum(lote.quantity * lote.unit_cost for lote in self.lotes[good_name])
                / total_quantity
            )
            total_cost = quantity * average_cost
            self._reduce_inventory(good_name, quantity)

        return total_cost

    def _reduce_inventory(self, good_name: str, quantity: float):
        """Método auxiliar para reducir el inventario sin calcular costos."""
        quantity_to_remove = quantity
        while quantity_to_remove > 0 and self.lotes[good_name]:
            first_lote = self.lotes[good_name][0]
            if first_lote.quantity <= quantity_to_remove:
                quantity_to_remove -= first_lote.quantity
                self.lotes[good_name].pop(0)
            else:
                first_lote.quantity -= quantity_to_remove
                quantity_to_remove = 0

    def get_total_quantity(self, good_name: str) -> float:
        return sum(lote.quantity for lote in self.lotes.get(good_name, []))


# ---------------------- Clase Agent ------------------------------


class Agent(ABC):
    """
    Clase base abstracta para las empresas.
    """

    def __init__(
        self,
        nombre: str,
        plantillas_cuentas: Dict,
        bienes_vendidos: List,
        bienes_producidos: List,
    ):
        """
        Inicializa una nueva instancia de Agent.

        :param nombre: El nombre del agente.
        :param plantillas_cuentas: Un diccionario que contiene las plantillas de cuentas
                                   que se usarán para crear instancias de Account para el agente.

        :param bienes_vendidos: Una lista de bienes vendidos por el agente.
        :param bienes_producidos: Una lista de bienes producidos por el agente.

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

        self.bienes_vendidos = bienes_vendidos if bienes_vendidos else []
        self.bienes_producidos = bienes_producidos if bienes_producidos else []

        # Inicializar el inventario
        self.inventory = Inventory()

    def set_costing_method_for_good(self, good_name: str, method: str):
        """
        Establece el método de costeo para un bien específico en el inventario.

        :param good_name: El nombre del bien para el cual se debe establecer el método de costeo.
        :param method: El método de costeo a establecer. Debe ser 'FIFO', 'LIFO' o 'WeightedAverage'.
        :raises ValueError: Si el método de costeo proporcionado no es válido.
        """
        self.inventory.set_costing_method(good_name, method)

    def purchase_good(self, good: Good, quantity: float, unit_cost: float):
        """
        Compra un bien y lo agrega al inventario como un nuevo lote.

        :param good: El bien a comprar.
        :param quantity: La cantidad comprada.
        :param unit_cost: El costo unitario del bien.
        """
        # Registrar la compra en las cuentas contables si es necesario
        # ...

        # Agregar al inventario como un nuevo lote
        self.inventory.add_lote(good, quantity, unit_cost)

    def sell_good(self, good_name: str, quantity: float, selling_price: float):
        """
        Vende una cantidad específica de un bien, actualiza el inventario y calcula el costo de los bienes vendidos.

        :param good_name: El nombre del bien a vender.
        :param quantity: La cantidad a vender.
        :param selling_price: El precio de venta por unidad.
        """
        # Calcular el costo de los bienes vendidos según el método de costeo
        cost_of_goods_sold = self.inventory.remove_lote(good_name, quantity)

        # Registrar la venta en las cuentas contables si es necesario
        # ...

        # Retornar o almacenar el costo de los bienes vendidos si es necesario
        return cost_of_goods_sold

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

    def generar_directorio_insumos(self) -> Dict:
        """
        Genera un diccionario con los bienes y sus insumos.

        :return: Un diccionario donde la clave es el nombre del bien y el valor es la lista de insumos.
        """
        directorio_insumos = {}
        for bien in self.bienes_vendidos:
            bien_name = bien.name
            directorio_insumos[bien_name] = bien.insumos
        return directorio_insumos


# Subclase para empresas ZF
class ZF(Agent):
    def get_type(self) -> str:
        return "ZF"


# Subclase para empresas NCT
class NCT(Agent):
    def get_type(self) -> str:
        return "NCT"


# ---------------------- Clase Transaction ------------------------------
class Transaction:
    """
    Clase para manejar transacciones entre agentes
    """

    def __init__(
        self,
        seller: Agent,
        buyer: Agent,
        good: Good,
        amount: float,
        temporal_export: int,
        national_VAT: int = 0,
        iva_status_transaccion: str = "gravado",
    ):
        """
        Inicializa una nueva transacci n.

        :param seller: El agente que vende el bien.
        :param buyer: El agente que compra el bien.
        :param good: El bien que se est  transaccionando.
        :param amount: La cantidad de bienes que se est n transaccionando.
        :param temporal_export: Si la transacci n es de exportaci n temporal (0 o 1).
        :param national_VAT: Si nacionalizaria el IVA usando VAN  (0 o 1).
        :param iva_status_transaccion: El estado de IVA de la transacci n ("gravado", "exento", "excluido").
        :raises ValueError: Si el valor de 'temporal_export' o 'national_VAT' no es 0 o 1.
        """
        self.seller = seller
        self.buyer = buyer
        self.good = good
        self.amount = amount
        self.temporal_export = temporal_export
        if self.temporal_export not in [0, 1]:
            raise ValueError("El valor de 'temporal_export' debe ser 0 o 1.")
        else:
            self.temporal_export = bool(self.temporal_export)

        self.national_VAT = national_VAT
        if self.national_VAT not in [0, 1]:
            raise ValueError("El valor de 'national_VAT' debe ser 0 o 1.")
        else:
            self.national_VAT = bool(self.national_VAT)

        self.iva_status_transaccion = iva_status_transaccion


### --------------------- Clase Production ------------------------------


class Production:
    """
    Clase para manejar operaciones de produccion
    """

    def __init__(
        self,
        producer: Agent,
        good: Good,
        amount_good: float,
        inputs: Dict[str, float],
    ):
        """
        Inicializa una nueva operaci n de producci n.

        :param producer: El agente que produce el bien.
        :param good: El bien que se est  produciendo.
        :param amount_good: La cantidad del bien que se va a producir.
        :param inputs: Un diccionario con los insumos necesarios para producir el bien.
                        Las claves son los nombres de los insumos y los valores son las cantidades requeridas.
        """
