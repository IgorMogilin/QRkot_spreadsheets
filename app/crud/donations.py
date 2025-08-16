from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import DonationCreate
from app.services.investments import fund_project


class DonationCRUD(CRUDBase):
    """CRUD-операции для модели Donation с поддержкой инвестирования."""
    async def create_with_investment(
        self,
        session: AsyncSession,
        donation_in: DonationCreate,
        user: Optional[User] = None
    ) -> Donation:
        """
        Создать пожертвование, привязать пользователя (если передан)
        и выполнить автоматическое инвестирование.
        """

        data = donation_in.dict()
        if user:
            data["user_id"] = user.id

        donation = Donation(**data)
        session.add(donation)
        await session.commit()
        await session.refresh(donation)

        open_projects = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested.is_(False))
            .order_by(CharityProject.create_date)
        )
        projects = open_projects.scalars().all()
        updated_objects = fund_project(target=donation, sources=projects)
        for obj in updated_objects:
            session.add(obj)
        await session.commit()
        await session.refresh(donation)

        return donation

    async def get_by_user(
        self,
        session: AsyncSession,
        user: User
    ) -> List[Donation]:
        """
        Получить список пожертвований конкретного пользователя.
        """
        result = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return result.scalars().all()

    async def get_all(
        self,
        session: AsyncSession
    ) -> List[Donation]:
        """
        Получить список всех пожертвований.
        """
        result = await session.execute(
            select(Donation).order_by(Donation.create_date)
        )
        return result.scalars().all()

    async def get_uninvested(
        self,
        session: AsyncSession
    ) -> List[Donation]:
        """
        Получить пожертвования, которые ещё не распределены.
        """
        result = await session.execute(
            select(Donation)
            .where(Donation.fully_invested.is_(False))
            .order_by(Donation.create_date)
        )
        return result.scalars().all()


donation_crud = DonationCRUD(Donation)
