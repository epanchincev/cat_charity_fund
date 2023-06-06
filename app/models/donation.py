from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.financial_base import FinancialBase


class Donation(FinancialBase):
    """Модель пожертвования"""

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self) -> str:
        return ', '.join(('Пожертвование', super().__repr__()))
