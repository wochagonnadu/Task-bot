"""
Константы для модуля создания задач
"""

# Состояния диалога создания задачи
SELECT_CLIENT = 0   # Выбор клиента
SELECT_PROJECT = 1  # Выбор проекта
TITLE = 2          # Ввод названия
DESCRIPTION = 3    # Ввод описания
DUE_DATE = 4       # Выбор даты
SELECT_TIME = 5    # Выбор времени
SELECT_EXECUTOR = 6 # Выбор исполнителя задачи
CONFIRM = 7        # Подтверждение создания

# Callback данные для кнопок
CALLBACK_NEW_CLIENT = 'new_client'     # Создание нового клиента
CALLBACK_SELECT_CLIENT = 'sel_client:'  # Префикс для выбора клиента
CALLBACK_NEW_PROJECT = 'new_project'    # Создание нового проекта
CALLBACK_SELECT_PROJECT = 'sel_proj:'   # Префикс для выбора проекта

# Сообщения для пользователя
MSG_SELECT_CLIENT = "Выберите клиента или отправьте сообщение для создания нового:"
MSG_SELECT_PROJECT = "Выберите проект или отправьте сообщение для создания нового:"