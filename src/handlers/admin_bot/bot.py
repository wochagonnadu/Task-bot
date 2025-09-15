"""Основной модуль админского бота"""

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters
)

from .base_handlers import (
    start_handler,
    help_handler,
    button_handler,
    handle_unknown
)
from src.middleware.auth import (
    handle_master_key_input, 
    handle_master_key_button,
    ENTER_MASTER_KEY,
    CALLBACK_ENTER_MASTER_KEY
)
from .callback_handlers import (
    handle_tasks_callback,
    handle_clients_callback,
    handle_client_name_input,
    handle_projects_callback,
    handle_project_name_input,
    handle_employees_callback,
    handle_reports_callback,
    ENTER_CLIENT_NAME,
    ENTER_PROJECT_NAME
)
from .constants import (
    BUTTON_TASKS,
    BUTTON_CLIENTS,
    BUTTON_PROJECTS,
    BUTTON_EMPLOYEES,
    BUTTON_NEW_TASK,
    BUTTON_REPORTS,
    # Callback patterns
    CALLBACK_TASKS_ALL,
    CALLBACK_TASKS_ACTIVE,
    CALLBACK_TASKS_COMPLETED,
    CALLBACK_TASKS_NOT_STARTED,
    CALLBACK_CLIENT_PREFIX,
    CALLBACK_PROJECT_PREFIX,
    CALLBACK_EMPLOYEE_PREFIX,
    CALLBACK_EMPLOYEE_ADD,
    # Отчеты
    CALLBACK_REPORT_WEEK,
    CALLBACK_REPORT_MONTH,
    CALLBACK_REPORT_QUARTER,
    CALLBACK_REPORT_YEAR
)
from src.utils.decorators import require_auth
from src.handlers.task_create import new_task_conversation

def setup_admin_bot(application: Application) -> None:
    """
    Настройка обработчиков для админского бота
    
    Args:
        application: Объект приложения telegram.ext.Application
    """
    # Добавляем обработчик для ввода мастер-ключа
    application.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("start", require_auth(bot_type='admin')(start_handler)),
            CallbackQueryHandler(handle_master_key_button, pattern=f"^{CALLBACK_ENTER_MASTER_KEY}$")
        ],
        states={
            ENTER_MASTER_KEY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    handle_master_key_input
                )
            ]
        },
        fallbacks=[],
        name="admin_auth",
        persistent=False
    ))
    application.add_handler(CommandHandler(
        "help",
        require_auth(bot_type='admin')(help_handler)
    ))
    application.add_handler(new_task_conversation)

    # Обработчик кнопок главного меню с проверкой прав
    application.add_handler(MessageHandler(
        filters.TEXT & 
        filters.Regex(f"^({BUTTON_TASKS}|{BUTTON_CLIENTS}|{BUTTON_PROJECTS}|"
                     f"{BUTTON_EMPLOYEES}|{BUTTON_NEW_TASK}|{BUTTON_REPORTS})$"),
        require_auth(bot_type='admin')(button_handler)
    ))

    # Обработчики callback-запросов с проверкой прав
    
    # Задачи
    application.add_handler(CallbackQueryHandler(
        require_auth(bot_type='admin')(handle_tasks_callback),
        pattern=f"^({CALLBACK_TASKS_ALL}|{CALLBACK_TASKS_ACTIVE}|"
                f"{CALLBACK_TASKS_COMPLETED}|{CALLBACK_TASKS_NOT_STARTED})$"
    ))

    # Клиенты
    client_conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                require_auth(bot_type='admin')(handle_clients_callback),
                pattern=rf"^({CALLBACK_CLIENT_PREFIX}[0-9]+|client_add)$"
            )
        ],
        states={
            ENTER_CLIENT_NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    require_auth(bot_type='admin')(handle_client_name_input)
                )
            ]
        },
        fallbacks=[],
        name="client_conversation",
        persistent=False,
        allow_reentry=True,
        per_message=False
    )
    application.add_handler(client_conv_handler)

    # Проекты
    project_conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                require_auth(bot_type='admin')(handle_projects_callback),
                pattern=rf"^({CALLBACK_PROJECT_PREFIX}[0-9]+|project_add)$"
            )
        ],
        states={
            ENTER_PROJECT_NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    require_auth(bot_type='admin')(handle_project_name_input)
                )
            ]
        },
        fallbacks=[],
        name="project_conversation",
        persistent=False,
        allow_reentry=True,
        per_message=False
    )
    application.add_handler(project_conv_handler)

    # Сотрудники
    application.add_handler(CallbackQueryHandler(
        require_auth(bot_type='admin')(handle_employees_callback),
        pattern=f"^({CALLBACK_EMPLOYEE_PREFIX}[0-9]+|{CALLBACK_EMPLOYEE_ADD})$"
    ))

    # Отчеты
    application.add_handler(CallbackQueryHandler(
        require_auth(bot_type='admin')(handle_reports_callback),
        pattern=f"^(report_(week|month|quarter|year))$"
    ))

    # Обработчик неизвестных команд
    application.add_handler(MessageHandler(
        filters.COMMAND,
        require_auth(bot_type='admin')(handle_unknown)
    ))

class AdminBot:
    """Класс для управления админским ботом"""

    def __init__(self, token: str):
        """
        Инициализация бота
        
        Args:
            token (str): Токен бота от BotFather
        """
        self.application = Application.builder().token(token).build()
        setup_admin_bot(self.application)
