from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    """CRUD операции для благотворительных проектов"""

    @staticmethod
    async def get_project_id_by_name(
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """Получить id проекта по имени"""
        project_exists = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )

        return project_exists.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
