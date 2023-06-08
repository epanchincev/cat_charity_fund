from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_poject_new_amount,
                                check_project_name_duplicate, existence_check,
                                investment_check, opennes_check)
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
    await check_project_name_duplicate(
        charity_project.name, session
    )
    new_project = CharityProject(**charity_project.dict())

    session.add_all(investment_process(
        new_project,
        await donation_crud.get_not_fully_invested_objects(session)
    ))
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
    project = await charity_project_crud.get(project_id, session)
    existence_check(project)
    investment_check(project)
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
    project = await charity_project_crud.get(project_id, session)

    existence_check(project)
    opennes_check(project)

    if project_in.name:
        await check_project_name_duplicate(
            project_in.name, session
        )

    if project_in.full_amount:
        check_poject_new_amount(
            project_in.full_amount, project
        )

    project = await charity_project_crud.update(
        project, project_in, session
    )

    return project
