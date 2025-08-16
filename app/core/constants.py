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

# Заголовки для Google таблицы отчёта
GOOGLE_SPREADSHEET_HEADERS = [
    "ID проекта", "Название", "Описание",
    "Требуемая сумма", "Собранная сумма",
    "Дата создания", "Дата закрытия",
    "Время сбора (дни)"
]