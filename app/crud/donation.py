from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation


class CRUDDonation(CRUDBase):
    """CRUD операции для пожертвований"""

    @staticmethod
    async def get_by_user(
        user_id: int,
        session: AsyncSession,
    ) -> List[Donation]:
        """Получить все пожертвования пользователя"""
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user_id,
            )
        )

        return donations.scalars().all()

    @staticmethod
    async def get_open_donations(
        session: AsyncSession,
    ) -> List[Donation]:
        """Получить все открытые пожертвования."""
        donations = await session.execute(
            select(Donation).where(
                Donation.fully_invested.is_(False)
            ).order_by(Donation.create_date)
        )

        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
