from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    ensure_project_active,
    validate_no_investments,
    verify_project_exists,
    validate_full_amount,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import CRUDCharityProject
from app.models import Donation, User, CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investments import fund_project


router = APIRouter()
crud = CRUDCharityProject(CharityProject)


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
    summary="Получить все проекты"
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Получить список всех благотворительных проектов."""
    return await crud.get_all_projects(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    summary="Создать новый проект",
    dependencies=[Depends(current_superuser)]
)
async def create_new_project(
    project_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser)
):
    """
    Создать новый благотворительный проект.
    Автоматически распределяет доступные пожертвования.
    Только для суперпользователей.
    """

    new_project = await crud.create_project(
        session,
        project_in,
        do_commit=False
    )
    result = await session.execute(
        select(Donation)
        .where(Donation.fully_invested.is_(False))
        .order_by(Donation.create_date)
    )
    open_donations = result.scalars().all()
    changed_objs = fund_project(target=new_project, sources=open_donations)
    for obj in changed_objs:
        session.add(obj)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    summary="Обновить проект",
    dependencies=[Depends(current_superuser)]
)
async def partially_update_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser)
):
    """
    Обновить информацию о проекте.
    Проверяет возможность изменения.
    Только для суперпользователей.
    """

    db_project = await crud.get_project_by_id(session, project_id)
    verify_project_exists(db_project)
    ensure_project_active(db_project)
    validate_full_amount(
        project_in.full_amount, db_project.invested_amount
    )

    project = await crud.update_project(session, db_project, project_in)
    if project.full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.utcnow()
        await session.commit()
        await session.refresh(project)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    summary="Удалить проект",
    dependencies=[Depends(current_superuser)]
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser)
):
    """
    Удалить проект.
    Проверяет возможность удаления.
    Только для суперпользователей.
    """

    project = await crud.get_project_by_id(session, project_id)
    verify_project_exists(project)
    validate_no_investments(project)
    return await crud.delete_project(session, project)
