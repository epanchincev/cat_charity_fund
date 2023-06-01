from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker


class PreBase:
    """Поля и методы базового класса"""

    @declared_attr
    def __tablename__(cls) -> str:

        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine('sqlite+aiosqlite:///./fastapi.db')

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session() -> AsyncSession:
    """Корутина отдающая асинхронную сессию"""
    async with AsyncSessionLocal() as async_session:
        yield async_session
