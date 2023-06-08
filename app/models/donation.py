from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.financial_base import FinancialBase


class Donation(FinancialBase):
    """Модель пожертвования"""

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self) -> str:
        return '{}, user_id: {}, comment: {}'.format(
            super().__repr__(), self.user_id, self.comment
        )
