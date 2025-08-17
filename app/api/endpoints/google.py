from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_closed_projects_exist, 
    validate_spreadsheet_update
)
from app.core.constants import URL_PREFIX_GOOGLEDRIVE
from app.core.db import get_async_session
from app.services.spreasheets import (
    get_closed_projects,
    create_spreadsheet,
    update_spreadsheet_values
)

router = APIRouter()


@router.post('/')
async def create_google_report(
    session: AsyncSession = Depends(get_async_session)
):
    """Создать отчёт в Google таблице с закрытыми проектами."""
    projects = await get_closed_projects(session)
    check_closed_projects_exist(projects)
    spreadsheet_id = await create_spreadsheet()
    await validate_spreadsheet_update(
        update_spreadsheet_values,
        spreadsheet_id,
        projects
    )
    return {
        "spreadsheet_url": f"{URL_PREFIX_GOOGLEDRIVE}{spreadsheet_id}"
    }
