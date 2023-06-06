from typing import List, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


class CRUDBase:

    def __init__(self, model) -> None:
        self.model = model

    async def get_multi(
            self,
            session: AsyncSession
    ) -> List[Union[Donation, CharityProject]]:
        """Получить все объекты модели"""
        db_objs = await session.execute(select(self.model))

        return db_objs.scalars().all()

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ) -> Union[Donation, CharityProject]:
        """Обновление обьекта модели по схеме pydantic"""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ) -> Union[Donation, CharityProject]:
        """Удаление объекта модели"""
        await session.delete(db_obj)
        await session.commit()

        return db_obj

    async def get_open_multi(
        self,
        session: AsyncSession
    ) -> List[Union[Donation, CharityProject]]:
        """Получить все открытые объекты модели"""
        open_objects = await session.execute(
            select(self.model).where(
                self.model.fully_invested.is_(False)
            ).order_by(self.model.create_date)
        )

        return open_objects.scalars().all()
