from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема для чтения данных пользователя.
    Наследует стандартные поля из BaseUser:
    - id: int - идентификатор пользователя
    - email: str - электронная почта
    - is_active: bool - статус активности
    - is_superuser: bool - статус суперпользователя
    - is_verified: bool - статус верификации
    """
    pass


class UserCreate(schemas.BaseUserCreate):
    """Схема для создания пользователя.
    Наследует стандартные поля:
    - email: str - электронная почта
    - password: str - пароль
    """
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для обновления данных пользователя.
    Наследует стандартные поля:
    - password: Optional[str] - пароль (опционально)
    - email: Optional[str] - почта (опционально)
    """
    pass
