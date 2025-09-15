"""
Обработчики callback-запросов для диалога создания задачи
"""
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from .constants import (
    SELECT_TIME,
    SELECT_EXECUTOR,
    CALLBACK_NEW_CLIENT,
    CALLBACK_NEW_PROJECT,
    CALLBACK_SELECT_CLIENT,
    CALLBACK_SELECT_PROJECT
)
from .keyboards import create_time_keyboard
from .executor_selection import handle_executor_selection
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

async def handle_date_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора даты"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "cancel_date":
        await query.edit_message_text("❌ Создание задачи отменено.")
        return ConversationHandler.END
        
    selected_date = query.data.replace("date_", "")
    context.user_data['selected_date'] = selected_date
    
    reply_markup = create_time_keyboard()
    await query.edit_message_text(
        f"📅 Выбрана дата: {selected_date}\n\n🕐 Теперь выберите время:",
        reply_markup=reply_markup
    )
    return SELECT_TIME

async def handle_time_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора времени"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "cancel_time":
        await query.edit_message_text("❌ Создание задачи отменено.")
        return ConversationHandler.END
        
    selected_time = query.data.replace("time_", "")
    context.user_data['task_due_date'] = f"{context.user_data['selected_date']} {selected_time}"
    
    # Переходим к выбору исполнителя
    return await handle_executor_selection(update, context)

# Экспортируем обработчики
__all__ = [
    'handle_date_selection',
    'handle_time_selection',
    'client_selection_callback',
    'new_client_callback',
    'create_new_client',
    'project_selection_callback',
    'new_project_callback',
    'create_new_project'
]