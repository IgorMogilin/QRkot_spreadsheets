from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.google_client import get_service
from app.core.constants import GOOGLE_SPREADSHEET_HEADERS
from app.models.charity_project import CharityProject


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


async def create_spreadsheet(title: str = "Отчёт по закрытым проектам") -> str:
    """Создание новой Google таблицы."""
    async for aiogoogle in get_service():
        sheets_service = await aiogoogle.discover('sheets', 'v4')
        spreadsheet = await aiogoogle.as_service_account(
            sheets_service.spreadsheets.create(
                json={
                    "properties": {"title": title},
                    "sheets": [{"properties": {"title": "Закрытые проекты"}}]
                }
            )
        )
        return spreadsheet['spreadsheetId']


async def set_user_permissions(file_id: str, user_email: str):
    """Выдача прав доступа пользователю."""
    async for aiogoogle in get_service():
        drive_service = await aiogoogle.discover('drive', 'v3')
        await aiogoogle.as_service_account(
            drive_service.permissions.create(
                fileId=file_id,
                json={
                    "type": "user",
                    "role": "writer",
                    "emailAddress": user_email
                }
            )
        )


async def update_spreadsheet_values(spreadsheet_id: str, values: List[List]):
    """Заполнение таблицы заголовками и данными."""
    async for aiogoogle in get_service():
        sheets_service = await aiogoogle.discover('sheets', 'v4')
        await aiogoogle.as_service_account(
            sheets_service.spreadsheets.values.update(
                spreadsheetId=spreadsheet_id,
                range="A1",
                valueInputOption="RAW",
                json={"values": [GOOGLE_SPREADSHEET_HEADERS] + values}
            )
        )