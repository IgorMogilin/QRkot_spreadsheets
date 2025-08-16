from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donations import donation_crud
from app.models.user import User
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationAdminDB,
)

router = APIRouter()


@router.post(
    "/",
    response_model=DonationDB,
    status_code=status.HTTP_200_OK
)
async def create_donation(
    donation_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Создать пожертвование от текущего пользователя."""
    return await donation_crud.create_with_investment(
        session,
        donation_in,
        user
    )


@router.get(
    "/my",
    response_model=List[DonationDB]
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Получить список пожертвований текущего пользователя."""
    return await donation_crud.get_by_user(session, user)


@router.get(
    "/",
    response_model=List[DonationAdminDB],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Получить список всех пожертвований (только для суперпользователя)."""
    return await donation_crud.get_all(session)
