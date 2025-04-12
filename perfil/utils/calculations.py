from datetime import datetime
from typing import List, Tuple

from extrato.models import Valores


def calcula_total(obj: List[object], campo: str = 'valor') -> int:
    """Calcula a soma total de um campo especificado em uma lista de objetos.

    Args:
        obj (List[object]): A lista de objetos.
        campo (str): O campo a ser somado.

    Retorna: int: A soma total do campo especificado. """

    total = 0
    for item in obj:
        total += getattr(item, campo)
    return total


def calcula_equilibrio_financeiro() -> Tuple[float, float]:
    """Calcula o equilíbrio financeiro determinando o percentual de despesas
    essenciais e não essenciais.

    Retorna:
        percentual_gastos_essenciais (float):
        A porcentagem de despesas essenciais.

        percentual_gastos_nao_essenciais (float):
        O percentual de despesas não essenciais.
    """

    gastos_essenciais = Valores.objects.filter(
        data__month=datetime.now().month
    ).filter(tipo='S').filter(categoria__essencial=True)

    gastos_nao_essenciais = Valores.objects.filter(
        data__month=datetime.now().month
    ).filter(tipo='S').filter(categoria__essencial=False)

    gastos_essenciais = calcula_total(gastos_essenciais)
    gastos_nao_essenciais = calcula_total(gastos_nao_essenciais)
    total = gastos_essenciais + gastos_nao_essenciais

    try:
        percentual_gastos_essenciais = (gastos_essenciais * 100) / total
        percentual_gastos_nao_essenciais = (gastos_nao_essenciais * 100)/total
        return percentual_gastos_essenciais, percentual_gastos_nao_essenciais
    except ZeroDivisionError:
        return 0, 0
