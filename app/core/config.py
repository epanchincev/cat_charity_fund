from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """Настройки приложения"""

    app_title: str = 'Кошачий благотворительный фонд'
    description: str = 'Сервис для поддержки котиков!'
    database_url: str = 'sqlite+aiosqlite:///./cat_charity_fund.db'
    secret: str = 'secretkeyasfas'
    first_superuser_email: Optional[EmailStr] = 'admin@admin.ru'
    first_superuser_password: Optional[str] = 'StrongPassword'

    class Config:
        env_file = '.env'


settings = Settings()
