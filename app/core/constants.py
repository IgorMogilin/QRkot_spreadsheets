from app.core.config import settings

MAX_LENGTH_NAME_PROJECT = 100
DEFAULT_INVESTED_AMOUNT = 0
AUTH_ROUTER_PREFIX = '/auth/jwt'
REGISTER_ROUTER_PREFIX = '/auth'
USER_ROUTER_PREFIX = '/users'
AUTH_ROUTER_TAGS = ['auth']
USER_ROUTER_TAGS = ['users']
USER_DELETE_ENDPOINT_NAME = 'users:delete_user'
MIN_ANYSTR_LENGTH = 1
MAX_ANYSTR_LENGTH = 100
MINIMAL_MONEY_INVESTED = 0
URL_PREFIX_GOOGLEDRIVE = 'https://docs.google.com/spreadsheets/d/'
REPORT_IS_OK = 'Отчёт успешно создан'
GOOGLE_SPREADSHEET_HEADERS = [
    "ID проекта", "Название", "Описание",
    "Требуемая сумма", "Собранная сумма",
    "Дата создания", "Дата закрытия",
    "Время сбора (дни)"
]
DEFAULT_LOCALIZE = 'ru_RU'
DEFAULT_ROW_COUNT = 100
DEFAULT_COLUMN_COUNT = 100
DEFAULT_SHEET_ID = 0
GOOGLE_SPREADSHEET_CREATE_JSON = {
    'properties': {
        'title': '{title}',
        'locale': DEFAULT_LOCALIZE
    },
    'sheets': [
        {
            'properties': {
                'sheetType': 'GRID',
                'sheetId': DEFAULT_SHEET_ID,
                'title': 'Закрытые проекты',
                'gridProperties': {
                    'rowCount': DEFAULT_ROW_COUNT,
                    'columnCount': DEFAULT_COLUMN_COUNT,
                },
            }
        }
    ],
}
GOOGLE_PERMISSIONS_JSON = {
    "type": "user",
    "role": "writer",
    "emailAddress": settings.email
}