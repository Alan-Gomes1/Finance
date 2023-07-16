from typing import List


def calcula_total(obj: List[object], campo: str) -> int:
    """Calcula a soma total de um campo especificado em uma lista de objetos.

    Args:
        obj (List[object]): A lista de objetos.
        campo (str): O campo a ser somado.

    Retorna: int: A soma total do campo especificado. """

    total = 0
    for item in obj:
        total += getattr(item, campo)
    return total
