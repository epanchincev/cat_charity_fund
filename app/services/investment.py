from typing import List, Union

from app.models import CharityProject, Donation


def calculate_invested_amount(
    obj_in: Union[Donation, CharityProject],
    not_fully_invested_obj: Union[Donation, CharityProject],
) -> int:
    """Расчет размера доната"""
    if obj_in.amount_to_fully_invested >= not_fully_invested_obj.amount_to_fully_invested:
        return not_fully_invested_obj.amount_to_fully_invested

    return obj_in.amount_to_fully_invested


def investment_process(
    obj_in: Union[Donation, CharityProject],
    not_fully_invested_objs: List[Union[Donation, CharityProject]],
) -> List[Union[Donation, CharityProject]]:
    """Процесс инвестирования"""
    changed_objects = []

    for not_fully_invested_obj in not_fully_invested_objs:
        invested_amount = calculate_invested_amount(obj_in, not_fully_invested_obj)
        obj_in.investment(invested_amount)
        not_fully_invested_obj.investment(invested_amount)
        changed_objects.append(not_fully_invested_obj)

        if obj_in.fully_invested:
            break

    changed_objects.append(obj_in)

    return changed_objects
