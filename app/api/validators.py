from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (CLOSED_OBJECT_UPDATE_ERROR,
                                NEW_AMOUNT_LESS_EXISTS_ERROR,
                                OBJECT_INVESTED_DELETE_ERROR,
                                OBJECT_NOT_FOUND_ERROR, PROJECT_EXISTS_ERROR)
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject, FinancialBase


async def check_project_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Проверка уникальности имени в бд"""
    room_id = await charity_project_crud.get_project_id_by_name(
        project_name, session,
    )
    if room_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_EXISTS_ERROR,
        )


def existence_check(object: FinancialBase) -> None:
    """Проверяет существование объекта"""
    if not object:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=OBJECT_NOT_FOUND_ERROR.format(object.__class__.__name__),
        )


def investment_check(object: FinancialBase) -> None:
    """Проверяет вложена ли сумма у объекта"""
    if object.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=OBJECT_INVESTED_DELETE_ERROR,
        )


def opennes_check(object: FinancialBase) -> None:
    """Проверяет открыт ли объект"""
    if object.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CLOSED_OBJECT_UPDATE_ERROR,
        )


def check_poject_new_amount(
    new_amount: int,
    charity_project: CharityProject,
) -> None:
    """Проверяет валидность новой суммы для проекта"""
    if new_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NEW_AMOUNT_LESS_EXISTS_ERROR,
        )
