from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import donation_crud
from app.models import CharityProject
from app.schemas import CharityProjectCreate
from app.services.utils import calculate_invested_amount


async def add_project_to_db(
    project_in: CharityProjectCreate,
    session: AsyncSession,
) -> CharityProject:
    """Процесс добавления проекта в БД, с инвестированием"""
    project = CharityProject(**project_in.dict(), invested_amount=0)
    open_donations = await donation_crud.get_open_donations(session)

    for donation in open_donations:
        invested_amount = calculate_invested_amount(donation, project)
        project.investment(invested_amount)
        donation.investment(invested_amount)
        session.add(donation)

        if project.fully_invested:
            break

    session.add(project)
    await session.commit()
    await session.refresh(project)

    return project
