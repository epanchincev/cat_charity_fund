from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import EXCLUDED_DONATION_FIELD_FOR_USERS
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import User
from app.schemas import DonationCreate, DonationDB
from app.services import add_donation_to_db


router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
) -> List[DonationDB]:
    """
    Только для суперюзеров.\n
    Возвращает список всех пожертвований.
    """
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude=EXCLUDED_DONATION_FIELD_FOR_USERS,
)
async def create_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> DonationDB:
    """Сделать пожертвование."""
    new_donation = await add_donation_to_db(donation, user, session)

    return new_donation


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude=EXCLUDED_DONATION_FIELD_FOR_USERS,
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> List[DonationDB]:
    """
    Вернуть список пожертвований пользователя, выполняющего запрос.
    """
    return await donation_crud.get_by_user(user.id, session)
