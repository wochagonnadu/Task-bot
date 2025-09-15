"""Основной модуль запуска пользовательского бота"""

import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters
)

from .base_handlers import start_command, help_command
from .task_list import my_tasks
from .task_view import view_task
from .callback_handler import handle_task_callback
from .message_handlers import handle_button_message
from src.handlers.task_create import new_task_conversation
from src.utils.error_handlers import common_error_handler
from src.utils.decorators import require_auth
from src.middleware.auth import (
    handle_invite_code_button,
    handle_invite_code_input,
    cancel_invite_code,
    ENTER_INVITE_CODE,
    CALLBACK_ENTER_CODE
)

logger = logging.getLogger(__name__)

def setup_user_bot(application: Application) -> None:
    """Настройка пользовательского бота"""
    logger.info("Настройка пользовательского бота...")

    # Группы обработчиков с приоритетами
    AUTH_GROUP = -1  # Самый высокий приоритет для авторизации
    CONVERSATION_GROUP = 0  # Приоритет для ConversationHandler
    COMMAND_GROUP = 1  # Приоритет для команд
    CALLBACK_GROUP = 2  # Приоритет для callback-запросов
    MESSAGE_GROUP = 3  # Самый низкий приоритет для текстовых сообщений

    # Добавление обработчика ввода инвайт-кода
    invite_code_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                handle_invite_code_button,
                pattern=f"^{CALLBACK_ENTER_CODE}$"
            )
        ],
        states={
            ENTER_INVITE_CODE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    handle_invite_code_input
                )
            ]
        },
        fallbacks=[
            CommandHandler("cancel", cancel_invite_code),
            CallbackQueryHandler(
                handle_invite_code_button,
                pattern=f"^{CALLBACK_ENTER_CODE}$"
            )
        ],
        name="invite_code_handler",
        persistent=False,
        allow_reentry=True,
        per_message=False
    )

    # Регистрация обработчиков по группам
    logger.info("Добавление обработчика инвайт-кодов...")
    application.add_handler(invite_code_handler, group=AUTH_GROUP)

    logger.info("Добавление обработчика создания задач...")
    application.add_handler(new_task_conversation, group=CONVERSATION_GROUP)

    # Команды
    logger.info("Добавление обработчиков команд...")
    command_handlers = [
        CommandHandler("start", require_auth(bot_type='user')(start_command)),
        CommandHandler("help", require_auth(bot_type='user')(help_command)),
        CommandHandler("my_tasks", require_auth(bot_type='user')(my_tasks)),
        CommandHandler("view_task", require_auth(bot_type='user')(view_task))
    ]
    for handler in command_handlers:
        application.add_handler(handler, group=COMMAND_GROUP)
        logger.info(f"Добавлен обработчик команды: {next(iter(handler.commands))}")

    # Callback-запросы для задач
    logger.info("Добавление обработчика callback-запросов для задач...")
    application.add_handler(
        CallbackQueryHandler(
            require_auth(bot_type='user')(handle_task_callback),
            pattern=r"^(my_tasks|(view|start|complete)_task_\d+)$"
        ),
        group=CALLBACK_GROUP
    )

    # Текстовые сообщения
    logger.info("Добавление обработчика текстовых сообщений...")
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            require_auth(bot_type='user')(handle_button_message)
        ),
        group=MESSAGE_GROUP
    )

    # Добавление обработчика ошибок
    application.add_error_handler(common_error_handler)
    logger.info("Настройка пользовательского бота завершена")