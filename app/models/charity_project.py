from sqlalchemy import Column, String, Text

from .base import BaseProjectModel
from app.core.constants import MAX_LENGTH_NAME_PROJECT


class CharityProject(BaseProjectModel):
    """Модель благотворительного проекта."""
    name = Column(
        String(MAX_LENGTH_NAME_PROJECT), nullable=False, unique=True
    )
    description = Column(
        Text, nullable=False
    )
