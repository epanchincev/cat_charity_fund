from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import charity_project_validators
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud, donation_crud
from app.models import CharityProject
from app.schemas import (CharityProjectCreate, CharityProjectDB,
                         CharityProjectUpdate)
from app.services import investment_process

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
) -> List[CharityProjectDB]:
    """Возвращает список всех проектов."""
    projects = await charity_project_crud.get_multi(session)

    return projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """
    Только для суперюзеров.\n
    Создаёт благотворительный проект.
    """
    await charity_project_validators.check_name_duplicate(
        charity_project.name, session
    )
    new_project = CharityProject(**charity_project.dict(), invested_amount=0)
    not_fully_invested_donations = (
        await donation_crud.get_not_fully_invested_objects(session)
    )
    changed_objects = investment_process(new_project, not_fully_invested_donations)

    session.add_all(changed_objects)
    await session.commit()
    await session.refresh(new_project)

    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """
    Только для суперюзеров.\n
    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы средства,
    его можно только закрыть.
    """
    project = await charity_project_validators.check_project_exists(
        project_id, session
    )
    charity_project_validators.check_invested_in_project(project)
    project = await charity_project_crud.remove(project, session)

    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """
    Только для суперюзеров.\n
    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной.
    """
    project = await charity_project_validators.check_project_exists(
        project_id, session
    )
    charity_project_validators.check_project_is_open(project)

    if project_in.name:
        await charity_project_validators.check_name_duplicate(
            project_in.name, session
        )

    if project_in.full_amount:
        charity_project_validators.check_new_amount(
            project_in.full_amount, project
        )

    project = await charity_project_crud.update(
        project, project_in, session
    )

    return project
