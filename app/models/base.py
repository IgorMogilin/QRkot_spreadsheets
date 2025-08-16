from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, CheckConstraint

from app.core.db import Base
from app.core.constants import DEFAULT_INVESTED_AMOUNT


class BaseProjectModel(Base):
    """Абстрактная базовая модель для проектов и пожертвований."""

    __abstract__ = True

    __table_args__ = (
        CheckConstraint('full_amount > 0', name='positive_full_amount'),
        CheckConstraint(
            'invested_amount <= full_amount',
            name='invested_within_limit'
        ),
    )

    full_amount = Column(
        Integer, nullable=False
    )
    invested_amount = Column(
        Integer, default=DEFAULT_INVESTED_AMOUNT
    )
    fully_invested = Column(
        Boolean, default=False
    )
    create_date = Column(
        DateTime, default=datetime.now
    )
    close_date = Column(
        DateTime, nullable=True
    )