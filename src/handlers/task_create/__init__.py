"""
Модуль создания новых задач
"""
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

from .constants import (
    SELECT_CLIENT,
    SELECT_PROJECT,
    TITLE,
    DESCRIPTION,
    DUE_DATE,
    SELECT_TIME,
    SELECT_EXECUTOR,
    CONFIRM
)
from .handlers import get_conversation_handlers
from .client_selection import start_client_selection

# Получаем states и fallbacks из handlers.py
states, fallbacks = get_conversation_handlers()

# Создаем ConversationHandler
new_task_conversation = ConversationHandler(
    entry_points=[
        CommandHandler("new_task", start_client_selection),
        MessageHandler(filters.Text(["➕ Новая задача"]), start_client_selection)
    ],
    states=states,
    fallbacks=fallbacks,
    name="new_task_conversation",
    persistent=False,
    allow_reentry=True,
    per_message=False
)