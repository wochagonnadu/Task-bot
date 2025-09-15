"""
Обработчики для выбора даты и времени задачи
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from src.utils.helpers import parse_datetime
from .constants import DUE_DATE, SELECT_TIME, SELECT_EXECUTOR
from .keyboards import create_time_keyboard, create_executor_keyboard
from src.database.models import User
from src.database.db import db
from .utils import get_next_workdays

logger = logging.getLogger(__name__)

async def process_date_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработка выбора даты и переход к выбору времени
    """
    query = update.callback_query
    await query.answer()
    
    if query.data == "cancel_date":
        await query.message.reply_text("Создание задачи отменено")
        return ConversationHandler.END
        
    # Извлекаем дату из callback_data
    selected_date = query.data.replace("date_", "")
    context.user_data['selected_date'] = selected_date
    
    # Показываем клавиатуру выбора времени
    reply_markup = create_time_keyboard()
    await query.edit_message_text(
        "🕐 Выберите время выполнения задачи:",
        reply_markup=reply_markup
    )
    return SELECT_TIME

async def process_time_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработка выбора времени и переход к выбору исполнителя
    """
    query = update.callback_query
    await query.answer()
    
    try:
        if query.data == "cancel_time":
            await query.message.reply_text("Создание задачи отменено")
            return ConversationHandler.END
        
        # Извлекаем время из callback_data
        selected_time = query.data.replace("time_", "")
        
        # Комбинируем дату и время
        date_str = context.user_data['selected_date']
        time_str = selected_time
        due_date = parse_datetime(f"{date_str} {time_str}")
        context.user_data['task_due_date'] = due_date
        
        # Получаем всех пользователей
        executors = await db.get_all(User)
        
        if not executors:
            await query.message.reply_text("❌ Нет доступных исполнителей")
            return ConversationHandler.END

        # Преобразуем в формат для клавиатуры
        executors_data = [
            {
                "id": executor.id,
                "name": executor.full_name or executor.username or f"User {executor.telegram_id}"
            }
            for executor in executors
        ]
        
        reply_markup = create_executor_keyboard(executors_data)
        
        await query.edit_message_text(
            "👤 Выберите исполнителя задачи:",
            reply_markup=reply_markup
        )
        return SELECT_EXECUTOR
    
    except Exception as e:
        logger.error(f"Ошибка при выборе времени: {e}", exc_info=True)
        await query.message.reply_text(f"❌ Ошибка при выборе времени: {str(e)}")
        return ConversationHandler.END