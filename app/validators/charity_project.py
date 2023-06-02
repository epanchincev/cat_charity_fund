from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (CLOSED_PROJECT_UPDATE_ERROR,
                                INVESTED_RPOJECT_DELETION_ERROR,
                                NEW_AMOUNT_LESS_EXISTS_ERROR,
                                PROJECT_EXISTS_ERROR, PROJECT_NOT_FOUND_ERROR)
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


class CharityProjectValidator:
    """Валидатор благотворительного проекта"""

    @staticmethod
    async def check_name_duplicate(
            project_name: str,
            session: AsyncSession,
    ) -> None:
        room_id = await charity_project_crud.get_project_id_by_name(
            project_name, session,
        )
        if room_id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=PROJECT_EXISTS_ERROR,
            )

    @staticmethod
    async def check_project_exists(
        charity_project_id: int,
        session: AsyncSession,
    ) -> CharityProject:
        """Проверяет существование проекта и возвращает его"""
        project = await charity_project_crud.get(
            charity_project_id, session
        )

        if not project:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=PROJECT_NOT_FOUND_ERROR,
            )

        return project

    @staticmethod
    def check_invested_in_project(
        charity_project: CharityProject,
    ) -> None:
        """Проверяет внесены ли средства в проект"""
        if charity_project.invested_amount > 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=INVESTED_RPOJECT_DELETION_ERROR
            )

    @staticmethod
    def check_project_is_open(
        charity_project: CharityProject,
    ) -> None:
        """Проверяет открыт ли проект"""
        if charity_project.fully_invested:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=CLOSED_PROJECT_UPDATE_ERROR,
            )

    @staticmethod
    def check_new_amount(
        new_amount: int,
        charity_project: CharityProject,
    ) -> None:
        """Проверяет валидность новой суммы"""
        if new_amount < charity_project.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=NEW_AMOUNT_LESS_EXISTS_ERROR,
            )
