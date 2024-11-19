class RuleEngine:
    """
    Motor de reglas para clasificar operaciones según el tipo de objeto y las reglas definidas.
    """

    def __init__(self):
        self.rules = {"Trade": [], "Production": []}

    def add_rule(self, obj_type: str, rule):
        """
        Agrega una nueva regla al motor para un tipo específico de objeto.

        :param obj_type: Tipo de objeto ("Trade" o "Production").
        :param rule: Función que representa una regla de clasificación.
        """
        if obj_type not in self.rules:
            raise ValueError(f"Tipo de objeto no soportado: {obj_type}")
        self.rules[obj_type].append(rule)

    def classify(self, obj, agent) -> str:
        """
        Clasifica una operación según las reglas del motor y el tipo de objeto.

        :param obj: Objeto a clasificar (Trade o Production).
        :param agent: Instancia del agente que participa en la operación.
        :return: Clasificación de la operación.
        """
        obj_type = type(obj).__name__
        if obj_type not in self.rules:
            return "Tipo de objeto no soportado"

        for rule in self.rules[obj_type]:
            classification = rule(obj, agent)
            if classification:
                return classification
        return "No clasificada"


# ------------------------ Reglas granulares


def is_good_produced(agent, good) -> bool:
    """
    Determina si un bien es producido por la empresa.
    """
    return good in agent.bienes_producidos


def is_good_sold(agent, good) -> bool:
    """
    Determina si un bien es vendido por la empresa.
    """
    return good in agent.bienes_vendidos


def rule_good_status(trade, agent) -> str:
    """
    Determina el status de un bien en una transacción respecto a la empresa.

    :param trade: Objeto Trade representando la transacción.
    :param agent: Instancia del agente.
    :return: Estado del bien ('materia prima', 'intermedio', 'final', etc.) o 'independiente'.
    """
    good = trade.good
    return agent.get_good_status(good)


def classify_good(agent, good) -> str:
    """
    Clasifica un bien como producido, no producido o independiente.
    """
    if is_good_produced(agent, good):
        return "producido"

    elif is_good_sold(agent, good) and is_good_final(agent, good):
        return "no producido"
    return "independiente"


# Reglas para Trade
def rule_determine_role(trade, agent) -> str:
    """
    Determina el rol del agente en una transacción: vendedor, comprador, o no involucrado.

    :param trade: Objeto Trade representando la transacción.
    :param agent: Instancia del agente.
    :return: Rol del agente ('vendedor', 'comprador', 'no involucrado').
    """
    if trade.seller == agent:
        return "vendedor"
    elif trade.buyer == agent:
        return "comprador"
    return "no involucrado"


def rule_good_produced(trade, agent) -> str:
    """
    Clasifica si el bien en la transacción es producido y la operación es de venta.
    """
    role = rule_determine_role(trade, agent)
    if role == "vendedor":
        good = trade.good
        if classify_good(agent, good) == "producido":
            return "ingreso por venta de mercancía producida"
    return None


def rule_good_not_produced(trade, agent) -> str:
    """
    Clasifica si el bien en la transacción es no producido y la operación es de venta.
    """
    role = rule_determine_role(trade, agent)
    if role == "vendedor":
        good = trade.good
        if classify_good(agent, good) == "no producido":
            return "ingreso por venta de mercancía no producida"
    return None
