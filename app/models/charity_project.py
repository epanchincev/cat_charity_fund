from sqlalchemy import Column, String, Text

from app.core.base import Base
from app.core.constants import MAX_LEN_NAME_FIELD
from app.models.mixins import DonationCharityMixin


class CharityProject(DonationCharityMixin, Base):
    """Модель благотворительного проекта"""

    name = Column(String(MAX_LEN_NAME_FIELD), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    @property
    def amount_to_close(self) -> int:
        """Сумма до закрытия"""
        return self.full_amount - self.invested_amount

    def __repr__(self) -> str:
        return f'id:{self.id} name:{self.name} full_amount: {self.full_amount}'
