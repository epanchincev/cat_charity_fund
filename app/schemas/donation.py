from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.types import PositiveInt


class DonationBase(BaseModel):
    """Базовая модель схемы пожертвования"""

    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    """Модель схемы для создания пожертваования"""

    pass


class DonationDB(DonationBase):
    """Модель схемы пожертвования из БД"""

    id: int
    user_id: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]
    invested_amount: int

    class Config:

        orm_mode = True
