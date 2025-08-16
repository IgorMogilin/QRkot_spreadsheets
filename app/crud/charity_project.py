from typing import Optional
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
)
from .base import CRUDBase


class CRUDCharityProject(CRUDBase):
    """
    CRUD операции для благотворительных проектов с дополнительными проверками.
    """

    async def get_project_by_id(
            self,
            session: AsyncSession,
            project_id: int
    ) -> Optional[CharityProject]:
        """Получить проект по ID"""
        return await self.get(project_id, session)

    async def get_project_id_by_name(
            self,
            session: AsyncSession,
            name: str
    ) -> Optional[int]:
        """Получить ID проекта по имени"""
        result = await session.execute(
            select(CharityProject.id).where(CharityProject.name == name)
        )
        return result.scalar_one_or_none()

    async def create_project(
            self,
            session: AsyncSession,
            project_in: CharityProjectCreate,
            do_commit: bool,
    ) -> CharityProject:
        """Создать проект"""
        await self._check_name_unique(session, project_in.name)
        return await super().create(project_in, session)

    async def get_all_projects(
            self,
            session: AsyncSession
    ) -> list[CharityProject]:
        """Получить все проекты"""
        return await self.get_multi(session)

    async def update_project(
            self,
            session: AsyncSession,
            db_project: CharityProject,
            project_in: CharityProjectUpdate
    ) -> CharityProject:
        """Обновить проект"""
        if project_in.name and project_in.name != db_project.name:
            await self._check_name_unique(session, project_in.name)
        return await super().update(db_project, project_in, session)

    async def delete_project(
            self,
            session: AsyncSession,
            db_project: CharityProject
    ) -> CharityProject:
        """Удалить проект"""
        return await super().remove(db_project, session)

    async def _check_name_unique(
            self,
            session: AsyncSession,
            name: str
    ) -> None:
        """Проверка уникальности имени проекта"""
        if await self.get_project_id_by_name(session, name):
            raise HTTPException(
                status_code=400,
                detail="Проект с таким именем уже существует!"
            )


crud_charityproject = CRUDCharityProject(CharityProject)
