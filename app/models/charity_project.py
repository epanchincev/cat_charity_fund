from sqlalchemy import Column, String, Text

from app.core.constants import MAX_LEN_NAME_FIELD
from app.models.financial_base import FinancialBase


class CharityProject(FinancialBase):
    """Модель благотворительного проекта"""

    name = Column(String(MAX_LEN_NAME_FIELD), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return ('Благотворительный проект, ' +
                super().__repr__() + f', наименование: {self.name}')

    @property
    def amount_to_close(self) -> int:
        """Сумма до закрытия"""
        return self.full_amount - self.invested_amount
