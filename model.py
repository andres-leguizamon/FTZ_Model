from classes import (
    Good,
    BienExcluido,
    BienExento,
    BienGravado,
    Agent,
    Transaction,
    Inventory,
    Lote,
)
from typing import Dict, List, Tuple
import json
import os
from utils import cargar_plantillas_cuentas


class Model:
    def __init__(self, lista_bienes: List[Good]):
        self.lista_bienes = lista_bienes

    def clasificar_bienes(self):
        """
        Clasifica los bienes en materias primas, bienes intermedios y bienes finales.
        """
        bienes_dict = {bien.name: bien for bien in self.lista_bienes}

        # Diccionario para saber en qué bienes es usado cada bien
        usados_como_insumo = {}

        # Construimos el diccionario de usados_como_insumo
        for bien in self.lista_bienes:
            for insumo_name in bien.insumos:
                # Validación: Asegurarnos de que el insumo exista en bienes_dict
                if insumo_name not in bienes_dict:
                    raise ValueError(
                        f"Insumo '{insumo_name}' no encontrado en la lista de bienes."
                    )
                if insumo_name not in usados_como_insumo:
                    usados_como_insumo[insumo_name] = []
                usados_como_insumo[insumo_name].append(bien.name)

        # Asignamos el tipo de bien a cada bien
        for bien in self.lista_bienes:
            bien.asignar_tipo_bien(bienes_dict, usados_como_insumo)
