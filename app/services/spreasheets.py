from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.google_client import get_service
from app.core.constants import (
    GOOGLE_SPREADSHEET_HEADERS,
    GOOGLE_SPREADSHEET_CREATE_JSON,
    GOOGLE_PERMISSIONS_JSON,
    GOOGLE_SPREADSHEET_TITLE,
    DEFAULT_ROW_COUNT,
    DEFAULT_COLUMN_COUNT,
)
from app.models.charity_project import CharityProject
from app.core.exceptions import SpreadsheetDataTooLargeError


async def get_closed_projects(session: AsyncSession) -> List[List]:
    """Закрытые проекты, отсортированные по скорости сбора."""
    query = select(CharityProject).where(CharityProject.fully_invested)
    result = await session.execute(query)
    projects = result.scalars().all()
    data = []
    for p in projects:
        if p.create_date and p.close_date:
            days = (p.close_date - p.create_date).days
            data.append([
                p.id, p.name, p.description,
                p.full_amount, p.invested_amount,
                p.create_date.strftime('%Y-%m-%d'),
                p.close_date.strftime('%Y-%m-%d'),
                days
            ])
    return sorted(data, key=lambda x: x[-1])


async def create_spreadsheet() -> str:
    """Создание новой Google таблицы."""
    aiogoogle = await get_service()
    sheets_service = await aiogoogle.discover('sheets', 'v4')
    spreadsheet_json = {
        **GOOGLE_SPREADSHEET_CREATE_JSON,
        'properties': {
            **GOOGLE_SPREADSHEET_CREATE_JSON['properties'],
            'title': GOOGLE_SPREADSHEET_TITLE,
        },
    }
    spreadsheet = await aiogoogle.as_service_account(
        sheets_service.spreadsheets.create(json=spreadsheet_json)
    )
    return spreadsheet['spreadsheetId']


async def set_user_permissions(file_id: str):
    """Выдача прав доступа пользователю."""
    aiogoogle = await get_service()
    drive_service = await aiogoogle.discover('drive', 'v3')
    await aiogoogle.as_service_account(
        drive_service.permissions.create(
            fileId=file_id,
            json=GOOGLE_PERMISSIONS_JSON
        )
    )


async def update_spreadsheet_values(spreadsheet_id: str, values: List[List]):
    """Заполнение таблицы заголовками и данными."""
    aiogoogle = await get_service()
    sheets_service = await aiogoogle.discover('sheets', 'v4')
    total_rows = len(values) + 1
    total_cols = len(GOOGLE_SPREADSHEET_HEADERS)
    if total_rows > DEFAULT_ROW_COUNT:
        raise SpreadsheetDataTooLargeError(
            f"Данные не помещаются в таблицу: строк > {DEFAULT_ROW_COUNT}"
        )
    if total_cols > DEFAULT_COLUMN_COUNT:
        raise SpreadsheetDataTooLargeError(
            f"Данные не помещаются в таблицу: колонок > {DEFAULT_COLUMN_COUNT}"
        )
    last_col = chr(ord('A') + total_cols - 1)
    range_name = f"A1:{last_col}{total_rows}"
    await aiogoogle.as_service_account(
        sheets_service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            json={"values": [GOOGLE_SPREADSHEET_HEADERS] + values}
        )
    )