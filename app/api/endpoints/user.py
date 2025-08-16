from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from app.core.user import (
    auth_backend,
    fastapi_users,
    current_user,
)
from app.core.constants import (
    AUTH_ROUTER_PREFIX,
    AUTH_ROUTER_TAGS,
    REGISTER_ROUTER_PREFIX,
    USER_DELETE_ENDPOINT_NAME,
    USER_ROUTER_PREFIX,
    USER_ROUTER_TAGS
)
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=AUTH_ROUTER_PREFIX,
    tags=AUTH_ROUTER_TAGS,
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=REGISTER_ROUTER_PREFIX,
    tags=AUTH_ROUTER_TAGS,
)

users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
users_router.routes = [
    route for route in users_router.routes
    if route.name != USER_DELETE_ENDPOINT_NAME
]
router.include_router(
    users_router,
    prefix=USER_ROUTER_PREFIX,
    tags=USER_ROUTER_TAGS,
)


@router.get("/users/me", response_model=UserRead, tags=["users"])
async def read_users_me(user=Depends(current_user)):
    """Текущий пользователь."""
    return user


@router.delete(
    '/users/{id}',
    tags=['users'],
    deprecated=True
)
def delete_user(id: str):
    """Удаление не поддерживается."""
    raise HTTPException(
        status_code=HTTPStatus.METHOD_NOT_ALLOWED,
        detail="Удаление пользователей запрещено!"
    )
