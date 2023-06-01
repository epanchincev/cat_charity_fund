from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import Donation, User
from app.schemas import DonationCreate
from app.services.utils import calculate_invested_amount


async def add_donation_to_db(
    donation_in: DonationCreate,
    user: User,
    session: AsyncSession,
) -> Donation:
    """Процесс добавления пожертвования в БД, с инвестированием"""
    donation = Donation(**donation_in.dict(), user_id=user.id, invested_amount=0)
    open_projects = await charity_project_crud.get_open_projects(session)

    for project in open_projects:
        invested_amount = calculate_invested_amount(donation, project)
        project.investment(invested_amount)
        donation.investment(invested_amount)
        session.add(project)

        if donation.fully_invested:
            break

    session.add(donation)
    await session.commit()
    await session.refresh(donation)

    return donation
