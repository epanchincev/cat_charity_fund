from typing import List

from app.models import FinancialBase


def investment_process(
    target: FinancialBase,
    sources: List[FinancialBase],
) -> List[FinancialBase]:
    """Процесс инвестирования"""
    changed_objects = []

    for source in sources:
        invested_amount = min(
            target.amount_to_fully_invested,
            source.amount_to_fully_invested,
        )
        target.investment(invested_amount)
        source.investment(invested_amount)
        changed_objects.append(source)

        if target.fully_invested:
            break

    changed_objects.append(target)

    return changed_objects
