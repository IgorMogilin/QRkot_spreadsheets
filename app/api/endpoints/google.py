from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_closed_projects_exist
from app.core.constants import REPORT_IS_OK, URL_PREFIX_GOOGLEDRIVE
from app.core.db import get_async_session
from app.core.config import settings
from app.services.spreasheets import (
    get_closed_projects,
    create_spreadsheet,
    update_spreadsheet_values,
    set_user_permissions
)

router = APIRouter()


@router.post("/create-report")
async def create_google_report(
    session: AsyncSession = Depends(get_async_session)
):
    """Создать отчёт в Google таблице с закрытыми проектами."""
    projects = await get_closed_projects(session)
    check_closed_projects_exist(projects)
    spreadsheet_id = await create_spreadsheet()
    await update_spreadsheet_values(spreadsheet_id, projects)

    if settings.email:
        await set_user_permissions(spreadsheet_id, settings.email)

    return {
        "message": REPORT_IS_OK,
        "spreadsheet_id": spreadsheet_id,
        "spreadsheet_url": f"{URL_PREFIX_GOOGLEDRIVE}{spreadsheet_id}",
        "projects_count": len(projects)
    }
