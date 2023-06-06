from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.financial_base import FinancialBase


class Donation(FinancialBase):
    """Модель пожертвования"""

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    @property
    def balance_of_invested_amount(self) -> int:
        """Остаток инвестируемого"""
        return self.full_amount - self.invested_amount
