from http import HTTPStatus
from typing import Optional, List

from fastapi import HTTPException

from app.core.error_message import ErrorMessage
from app.core.exceptions import SpreadsheetDataTooLargeError
from app.core.constants import (
    GOOGLE_SPREADSHEET_HEADERS,
    GOOGLE_SPREADSHEET_CREATE_JSON
)
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


async def validate_spreadsheet_update(update_func, *args, **kwargs):
    """Проверяет успешность обновления Google таблицы."""
    try:
        await update_func(*args, **kwargs)
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=ErrorMessage.GOOGLE_SPREADSHEET_UPDATE_ERROR
        )


def validate_spreadsheet_data_fits(values: List[List]):
    """Проверяет, что данные поместятся в Google таблицу."""
    total_rows = len(values) + 1
    total_cols = len(GOOGLE_SPREADSHEET_HEADERS)
    grid_props = (
        GOOGLE_SPREADSHEET_CREATE_JSON['sheets'][0]
        ['properties']['gridProperties']
    )
    max_rows = grid_props['rowCount']
    max_cols = grid_props['columnCount']
    if total_rows > max_rows:
        raise SpreadsheetDataTooLargeError(
            f"Данные не помещаются в таблицу: строк > {max_rows}"
        )
    if total_cols > max_cols:
        raise SpreadsheetDataTooLargeError(
            f"Данные не помещаются в таблицу: колонок > {max_cols}"
        )
