from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field
from pydantic.types import PositiveInt

from app.core.constants import MAX_LEN_NAME_FIELD


class CharityProjectBase(BaseModel):
    """Базовая модель схемы благотворительного проекта"""

    name: Optional[str] = Field(None, min_length=1, max_length=MAX_LEN_NAME_FIELD)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:

        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    """Модель схемы благотворительного проекта из БД"""

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:

        orm_mode = True


class CharityProjectCreate(CharityProjectBase):
    """Модель схемы благотворительного проекта для создания"""

    name: str = Field(..., min_length=1, max_length=MAX_LEN_NAME_FIELD)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    """Модель схемы благотворительного проекта для обновления"""
    pass
