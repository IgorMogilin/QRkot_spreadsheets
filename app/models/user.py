from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """Модель пользователя системы.

    Наследует стандартные поля из SQLAlchemyBaseUserTable:
    - id: int - первичный ключ
    - email: str - email пользователя (уникальный)
    - hashed_password: str - хеш пароля
    - is_active: bool - флаг активности
    - is_superuser: bool - флаг суперпользователя
    - is_verified: bool - флаг верификации
    """
    pass
