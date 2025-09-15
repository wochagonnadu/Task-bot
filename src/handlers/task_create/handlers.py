"""
Основной модуль с настройкой диалога создания задачи
"""
from typing import Dict, List, Union, Tuple

from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
    BaseHandler,
    ContextTypes
)

from .constants import (
    SELECT_CLIENT,
    SELECT_PROJECT,
    TITLE,
    DESCRIPTION,
    DUE_DATE,
    SELECT_TIME,
    SELECT_EXECUTOR,
    CONFIRM,
    CALLBACK_NEW_CLIENT,
    CALLBACK_NEW_PROJECT,
    CALLBACK_SELECT_CLIENT,
    CALLBACK_SELECT_PROJECT
)

from .client_selection import (
    client_selection_callback,
    new_client_callback,
    create_new_client
)
from .project_selection import (
    project_selection_callback,
    new_project_callback,
    create_new_project
)
from .task_details import (
    task_title,
    task_description,
    skip_description_callback
)
from .datetime_selection import (
    process_date_selection,
    process_time_selection
)
from .executor_selection import handle_executor_callback
from .task_confirmation import create_task

async def cancel_task_creation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена создания задачи"""
    context.user_data.clear()
    
    if update.message:
        await update.message.reply_text(
            "Создание задачи отменено. Используйте /new_task для начала заново."
        )
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            "Создание задачи отменено. Используйте /new_task для начала заново."
        )

    return ConversationHandler.END

def get_conversation_handlers() -> Tuple[Dict, List[BaseHandler]]:
    """
    Создание и настройка обработчиков для диалога создания задачи
    """
    states = {
        SELECT_CLIENT: [
            CallbackQueryHandler(
                client_selection_callback,
                pattern=rf"^{CALLBACK_SELECT_CLIENT}\d+$"
            ),
            CallbackQueryHandler(
                new_client_callback,
                pattern=f"^{CALLBACK_NEW_CLIENT}$"
            ),
            CallbackQueryHandler(
                cancel_task_creation,
                pattern="^cancel_task$"
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, create_new_client)
        ],
        
        SELECT_PROJECT: [
            CallbackQueryHandler(
                project_selection_callback,
                pattern=rf"^{CALLBACK_SELECT_PROJECT}\d+$"
            ),
            CallbackQueryHandler(
                new_project_callback,
                pattern=f"^{CALLBACK_NEW_PROJECT}$"
            ),
            CallbackQueryHandler(
                cancel_task_creation,
                pattern="^cancel_task$"
            ),
            MessageHandler(filters.TEXT & ~filters.COMMAND, create_new_project)
        ],
        
        TITLE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, task_title),
            CallbackQueryHandler(cancel_task_creation, pattern="^cancel_task$")
        ],
        
        DESCRIPTION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, task_description),
            CallbackQueryHandler(skip_description_callback, pattern="^skip_description$"),
            CallbackQueryHandler(cancel_task_creation, pattern="^cancel_task$")
        ],
        
        DUE_DATE: [
            CallbackQueryHandler(process_date_selection)
        ],
        
        SELECT_TIME: [
            CallbackQueryHandler(process_time_selection)
        ],
        
        SELECT_EXECUTOR: [
            CallbackQueryHandler(handle_executor_callback)
        ],
        
        CONFIRM: [
            CallbackQueryHandler(create_task)
        ]
    }
    
    # Добавление fallbacks для отмены и обработки таймаутов
    fallbacks = [
        CommandHandler('cancel', cancel_task_creation),
        MessageHandler(filters.COMMAND, cancel_task_creation),  # Отмена при любой другой команде
        MessageHandler(filters.ALL, lambda u, c: ConversationHandler.END)  # Защита от неожиданных сообщений
    ]
    
    return states, fallbacks