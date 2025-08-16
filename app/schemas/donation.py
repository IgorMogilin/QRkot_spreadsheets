from datetime import datetime
from typing import Optional
from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    """Базовая схема для пожертвований."""
    full_amount: PositiveInt
    comment: Optional[str] = None


class DonationCreate(DonationBase):
    """Схема для создания пожертвования."""
    pass


class DonationDB(DonationBase):
    """Схема для отображения пожертвования."""
    id: int
    create_date: datetime

    class Config:
        """Конфигурация для работы с ORM."""
        orm_mode = True


class DonationAdminDB(DonationDB):
    """Схема для отображения пожертвования (администратор)."""
    id: int
    user_id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        """Конфигурация для работы с ORM."""
        orm_mode = True
