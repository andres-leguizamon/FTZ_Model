#! Script para realizar la calculadora

from typing import List, Dict, Optional, Tuple
from abc import ABC, abstractmethod

from utils import cargar_plantillas_cuentas

from accounting_templates import (
    dict_precios_1,
    plantillas_contables_1,
    mapear_valor,
    obtener_precio_transaccion,
)
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


# -------------- Clase Libro Contable


class LibroContable:
    def __init__(self, plantillas_cuentas: Dict, plantillas_transacciones: Dict):
        self.plantillas_transacciones = plantillas_transacciones
        self.cuentas = {}

        for codigo, plantilla in plantillas_cuentas.items():
            cuenta_nombre = plantilla["cuenta"]
            codigo_tipo_cuenta = plantilla["codigo_tipo_cuenta"]
            # Creamos una nueva instancia de Account para cada cuenta del agente
            self.cuentas[codigo] = Account(name=cuenta_nombre, tipo=codigo_tipo_cuenta)

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
        return self.cuentas.get(int(account_code), None)

    def debitar_cuenta(self, cuenta_codigo: str, monto: float):
        """
        Debita una cuenta del agente.

        :param cuenta_codigo: Código de la cuenta a debitar.
        :param monto: Monto a debitar de la cuenta.
        """
        cuenta = self.get_account_by_code(cuenta_codigo)
        cuenta.registrar_transaccion(monto, 0)

    def acreditar_cuenta(self, cuenta_codigo: str, monto: float):
        """
        Acredita una cuenta del agente.

        :param cuenta_codigo: Código de la cuenta a acreditar.
        """
        cuenta = self.get_account_by_code(cuenta_codigo)
        cuenta.registrar_transaccion(0, monto)

    def calcular_utilidad_operacional(self, tasa_impuesto: float) -> str:
        """
        Calcula la utilidad operacional y genera un estado de resultados.

        :param tasa_impuesto: Tasa porcentual de impuesto (por ejemplo, 0.3 para 30%).
        :return: Estado de resultados en formato de texto.
        """
        total_ingresos = 0
        total_costos = 0

        for cuenta in self.cuentas.values():
            if cuenta.tipo == 4:
                # Las cuentas tipo 4 (Ingresos) aumentan con el haber
                saldo = cuenta.haber - cuenta.debe
                total_ingresos += saldo
            elif cuenta.tipo == 6:
                # Las cuentas tipo 6 (Costos) aumentan con el debe
                saldo = cuenta.debe - cuenta.haber
                total_costos += saldo

        utilidad_bruta = total_ingresos - total_costos
        impuesto = utilidad_bruta * tasa_impuesto
        utilidad_neta = utilidad_bruta - impuesto

        # Generar el estado de resultados
        estado_resultados = (
            f"Ingresos Totales: {total_ingresos}\n"
            f"Costos Totales: {total_costos}\n"
            f"Utilidad Bruta: {utilidad_bruta}\n"
            f"Impuesto ({tasa_impuesto * 100}%): {impuesto}\n"
            f"Utilidad Neta: {utilidad_neta}\n"
        )

        return estado_resultados


# -------------- Clase Agente ----------------


class Agent(ABC):
    """
    Clase base abstracta para los agentes.
    """

    def __init__(
        self,
        nombre: str,
        plantillas_cuentas: Dict,
        plantillas_transacciones: Dict,
    ):
        """
        Inicializa una nueva instancia de Agent.

        :param nombre: El nombre del agente.
        :param plantillas_cuentas: Un diccionario que contiene las plantillas de cuentas
                                   que se usarán para crear instancias de Account para el agente.
        """
        self.nombre = nombre
        self.type = self.get_type()  # Establece el tipo según la subclase
        # Crear el libro contable del agente
        self.libro_contable = LibroContable(
            plantillas_cuentas, plantillas_transacciones
        )

    @abstractmethod
    def get_type(self) -> str:
        """
        Método abstracto para obtener el tipo de empresa.
        Debe ser implementado por las subclases.
        """
        pass

    def __repr__(self):
        return f"{self.type} {self.nombre}"

    def __str__(self):
        return f"{self.type} {self.nombre}"


# Subclase para empresas ZF
class ZF(Agent):
    def get_type(self) -> str:
        return "ZF"


# Subclase para empresas NCT
class NCT(Agent):
    def get_type(self) -> str:
        return "NCT"


# ------------------------------------ Clase Flow --------------------------------------------


class Flow:
    def __init__(
        self, name: str, owner, precio_venta: float = 0, ultimo_costo: float = 0
    ):
        self.name = name
        self.owner = owner
        self.precio_venta = precio_venta
        self.ultimo_costo = ultimo_costo
        self.historial = []  # Lista vacía para el historial
        self.guardar_en_historial()  # Guarda el estado inicial en el historial

    def guardar_en_historial(self):
        estado = {
            "owner": self.owner,
            "precio_venta": self.precio_venta,
            "ultimo_costo": self.ultimo_costo,
        }
        self.historial.append(estado)

    def actualizar_precio_venta(self, nuevo_precio_venta: float):
        self.precio_venta = nuevo_precio_venta
        self.guardar_en_historial()

    def actualizar_ultimo_costo(self, nuevo_ultimo_costo: float):
        self.ultimo_costo = nuevo_ultimo_costo
        self.guardar_en_historial()

    def actualizar_owner(self, nuevo_owner):
        self.owner = nuevo_owner
        self.guardar_en_historial()


# ------------------------------------- Clase Transaccion ------------------------------------


class Transaccion:
    def __init__(
        self,
        vendedor: Agent,
        comprador: Agent,
        bien: Good,
        dict_precios_transaccion: Dict[Tuple[str, str, str], float],
    ):
        self.bien = bien
        self.vendedor = vendedor
        self.comprador = comprador
        self.dict_precios_transaccion = dict_precios_transaccion
        self.llave_dict_precios_transaccion = (
            vendedor.type,
            comprador.type,
            bien.tipo_bien,
        )

    def registrar_compra(self, precio: float) -> None:
        """
        Registra una compra de un bien por parte del comprador, actualizando sus cuentas contables.
        """
        comprador = self.comprador
        tipo_bien = self.bien.tipo_bien

        # Obtener la plantilla de compra para el tipo de bien
        plantilla = comprador.libro_contable.plantillas_transacciones.get(
            tipo_bien, {}
        ).get("compra", {})
        if not plantilla:
            raise ValueError(
                f"No se encontró una plantilla de compra para el tipo de bien '{tipo_bien}'"
            )

        # Actualizar las cuentas del comprador según la plantilla
        for cuenta_codigo, valor_key in plantilla.get("debito", []):
            comprador.libro_contable.debitar_cuenta(cuenta_codigo, precio)

        for cuenta_codigo, valor_key in plantilla.get("credito", []):
            comprador.libro_contable.acreditar_cuenta(cuenta_codigo, precio)

    def registrar_venta(self, precio: float, costo: float) -> None:
        """
        Registra una venta de un bien por parte del vendedor, actualizando sus cuentas contables.
        """
        vendedor = self.vendedor
        tipo_bien = self.bien.tipo_bien

        # Obtener la plantilla de venta para el tipo de bien
        plantilla = vendedor.libro_contable.plantillas_transacciones.get(
            tipo_bien, {}
        ).get("   venta", {})
        if not plantilla:
            raise ValueError(
                f"No se encontró una plantilla de venta para el tipo de bien '{tipo_bien}'"
            )

        # Procesar la plantilla, reemplazando 'precio' y 'costo' por los argumentos proporcionados
        debitos = []
        creditos = []

        for cuenta, variable in plantilla.get("debito", []):
            if variable == "precio":
                valor = precio
            elif variable == "costo":
                valor = costo
            else:
                raise ValueError(f"Variable desconocida '{variable}' en débito")
        debitos.append((cuenta, valor))

        for cuenta, variable in plantilla.get("credito", []):
            if variable == "precio":
                valor = precio
            elif variable == "costo":
                valor = costo
            else:
                raise ValueError(f"Variable desconocida '{variable}' en crédito")
        creditos.append((cuenta, valor))

        # Actualizar las cuentas contables del vendedor
        for cuenta, valor in debitos:
            vendedor.libro_contable.registrar_movimiento(cuenta, "debito", valor)

        for cuenta, valor in creditos:
            vendedor.libro_contable.registrar_movimiento(cuenta, "credito", valor)


# ------------------------------------ Clase Modelo  ------------------------------------
