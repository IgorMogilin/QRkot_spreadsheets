from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, root_validator

from app.core.constants import (
    MAX_ANYSTR_LENGTH,
    MIN_ANYSTR_LENGTH,
    MINIMAL_MONEY_INVESTED,
)


class CharityProjectBase(BaseModel):
    """Базовая схема благотворительного проекта."""
    name: str = Field(
        ..., max_length=MAX_ANYSTR_LENGTH
    )
    description: str
    full_amount: PositiveInt

    class Config:
        min_anystr_length = MIN_ANYSTR_LENGTH


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания проекта. Наследует все поля базовой схемы."""
    pass


class CharityProjectUpdate(BaseModel):
    """Схема для обновления проекта (все поля опциональны)."""
    name: Optional[str] = Field(
        None, max_length=MAX_ANYSTR_LENGTH
    )
    description: Optional[str]
    full_amount: Optional[PositiveInt] = None

    @root_validator
    def check_at_least_one_field(cls, values):
        """Проверяет, что хотя бы одно поле предоставлено для обновления."""
        if not any(values.values()):
            raise ValueError(
                "Хотя бы одно поле должно быть предоставлено для обновления"
            )
        return values


class CharityProjectDB(CharityProjectBase):
    """Схема для отображения проекта из БД."""
    id: int
    invested_amount: int = MINIMAL_MONEY_INVESTED
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True
