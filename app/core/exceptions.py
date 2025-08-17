class SpreadsheetError(Exception):
    """Базовое исключение для ошибок Google таблиц."""
    pass


class SpreadsheetDataTooLargeError(SpreadsheetError):
    """Данные не помещаются в таблицу."""
    pass
