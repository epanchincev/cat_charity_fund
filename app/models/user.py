from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.base import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """Модель пользователя"""
    pass
