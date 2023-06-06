from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class FinancialBase(Base):
    """Общие поля и методы для проектов и пожертвований."""

    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    close_date = Column(DateTime, default=None)

    __table_args__ = (
        CheckConstraint('full_amount > 0', name='full_amount_is_positive'),
        CheckConstraint(
            'invested_amount <= full_amount',
            name='full_amount_greater_then_invested_amount',
        ),
    )

    def __repr__(self) -> str:
        return f'id: {self.id}'

    @property
    def amount_to_fully_invested(self) -> int:
        """Сумма до закрытия"""
        return self.full_amount - self.invested_amount

    def _close(self) -> None:
        """Закрытие объекта"""
        self.close_date = datetime.now()
        self.fully_invested = True

    def investment(self, investment_amount: int) -> None:
        self.invested_amount += investment_amount

        if self.invested_amount == self.full_amount:
            self._close()
