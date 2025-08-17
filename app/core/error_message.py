class ErrorMessage:
    PROJECT_NOT_FOUND = "Проект не найден"
    CLOSED_PROJECT_EDIT = "Нельзя редактировать закрытый проект"
    INVESTED_AMOUNT_GREATER_THAN_FULL_AMOUNT = (
        "Новая требуемая сумма не может быть меньше уже инвестированной"
    )
    INVESTED_PROJECT_DELETE = (
        "Нельзя удалить проект, в который уже были инвестированы средства"
    )
    NOT_UNIQUE_PROJECT_NAME = "Проект с таким именем уже существует"
    NOT_CLOSED_PROJECT = "Закрытых проектов не найдено"
    GOOGLE_SPREADSHEET_UPDATE_ERROR = "Ошибка при заполнении таблицы данными"
