from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import BaseProjectModel


class Donation(BaseProjectModel):
    """Модель пожертвования в благотворительный проект."""
    user_id = Column(
        Integer, ForeignKey('user.id')
    )
    comment = Column(
        Text, nullable=True
    )
