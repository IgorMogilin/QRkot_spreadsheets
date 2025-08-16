from fastapi import APIRouter

from app.api.endpoints import (
    charityproject_router,
    donations_router,
    user_router,
    google_router,
)

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(
    charityproject_router,
    prefix='/charity_project',
    tags=['CharityProject'],
)
main_router.include_router(
    donations_router,
    prefix='/donation',
    tags=['Donation'],
)
main_router.include_router(
    google_router,
    prefix='/google',
    tags=['Google'],
)
