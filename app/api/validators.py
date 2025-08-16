from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException

from app.core.error_message import ErrorMessage
from app.models import CharityProject


def verify_project_exists(project: Optional[CharityProject]):
    """Проверяет существование проекта."""
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ErrorMessage.PROJECT_NOT_FOUND
        )


def ensure_project_active(project: CharityProject):
    """Проверяет, что проект не закрыт."""
    if project.close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMessage.CLOSED_PROJECT_EDIT
        )


def validate_full_amount(
    new_amount: Optional[int],
    invested_amount: int
):
    """Проверяет корректность суммы."""
    if new_amount is not None and new_amount < invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMessage.INVESTED_AMOUNT_GREATER_THAN_FULL_AMOUNT
        )


def validate_no_investments(project: CharityProject):
    """Проверяет отсутствие инвестиций."""
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMessage.INVESTED_PROJECT_DELETE
        )


def check_closed_projects_exist(projects: list):
    """Проверяет существование закрытых проектов."""
    if not projects:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ErrorMessage.NOT_CLOSED_PROJECT
        )
