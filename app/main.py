from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_title,
    description=settings.description,
)

app.include_router(main_router)


@app.on_event('startup')
async def startup() -> None:
    """Действия при запуске"""
    pass
