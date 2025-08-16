from typing import List
from pydantic import BaseModel


class ProjectData(BaseModel):
    """Схема данных проекта для отчёта."""
    id: int
    name: str
    description: str
    full_amount: int
    invested_amount: int
    create_date: str
    close_date: str
    collection_time_days: int


class GoogleReportResponse(BaseModel):
    """Схема ответа при создании Google отчёта."""
    message: str
    spreadsheet_id: str
    spreadsheet_url: str
    projects_count: int
    projects: List[ProjectData]
