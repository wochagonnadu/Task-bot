"""
Обработчики подтверждения и создания задачи
"""
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler

from src.database.models import Task, User
from src.database.db import db
from src.utils.helpers import parse_datetime

from .constants import CONFIRM
from .keyboards import create_confirmation_keyboard
from .utils.message_formatting import format_task_details, format_task_success

logger = logging.getLogger(__name__)

async def show_task_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показ подтверждения создания задачи"""
    try:
        # Проверяем наличие всех необходимых данных
        if not all(key in context.user_data for key in ['task_title', 'task_due_date']):
            message = update.callback_query.message if update.callback_query else update.message
            await message.reply_text("❌ Ошибка: недостаточно данных для создания задачи")
            return ConversationHandler.END

        # Получаем данные исполнителя если есть
        executor = None
        assignee_id = context.user_data.get('assignee_id')
        if assignee_id:
            executor = await db.get(User, assignee_id)

        # Получаем дату из контекста и обрабатываем её
        due_date = context.user_data['task_due_date']
        if isinstance(due_date, str):
            due_date = parse_datetime(due_date)
        
        # Форматируем сообщение с деталями задачи
        confirmation_text = format_task_details(
            title=context.user_data['task_title'],
            description=context.user_data.get('task_description', ''),
            due_date=due_date,
            executor=executor,
            client_name=context.user_data.get('selected_client_name'),
            project_name=context.user_data.get('selected_project_name')
        )
        
        reply_markup = create_confirmation_keyboard()
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                confirmation_text,
                reply_markup=reply_markup,
                parse_mode='MarkdownV2'
            )
        else:
            await update.message.reply_text(
                confirmation_text,
                reply_markup=reply_markup,
                parse_mode='MarkdownV2'
            )
        return CONFIRM

    except Exception as e:
        logger.error(f"Ошибка при отображении подтверждения: {e}", exc_info=True)
        message = update.callback_query.message if update.callback_query else update.message
        await message.reply_text("❌ Произошла ошибка. Попробуйте создать задачу заново.")
        return ConversationHandler.END

async def create_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Создание задачи в базе данных"""
    query = update.callback_query
    await query.answer()
    
    try:
        # Получаем пользователя-создателя
        user = await db.get_by_field(User, 'telegram_id', update.effective_user.id)
        
        if not user:
            await query.edit_message_text(
                "❌ Ошибка: пользователь не найден. Используйте команду /start"
            )
            return ConversationHandler.END

        # Получаем и обрабатываем дату
        due_date = context.user_data['task_due_date']
        if isinstance(due_date, str):
            due_date = parse_datetime(due_date)
        if not due_date:
            await query.edit_message_text("❌ Ошибка: некорректный формат даты")
            return ConversationHandler.END

        # Создаем задачу
        task = await db.create(
            Task,
            title=context.user_data['task_title'],
            description=context.user_data.get('task_description', ''),
            due_date=due_date,
            creator_id=user.id,
            assignee_id=context.user_data.get('assignee_id'),
            client_id=context.user_data.get('selected_client_id'),
            project_id=context.user_data.get('selected_project_id'),
            status='not_started'
        )
        
        # Получаем данные для сообщения об успехе
        task_details = {
            'title': task.title,
            'due_date': task.due_date
        }
        
        if task.assignee_id:
            executor = await db.get(User, task.assignee_id)
            if executor:
                task_details['executor_name'] = executor.full_name or executor.username
        
        # Отправляем уведомление через сервис уведомлений
        from src.services.notifications import send_task_assignment_notification
        await send_task_assignment_notification(task.id)

        # Форматируем сообщение об успехе
        success_text = format_task_success(task.id, task_details)
        
        from .keyboards.basic import create_task_list_keyboard
        await query.edit_message_text(
            success_text,
            parse_mode='MarkdownV2',
            )
        
    except Exception as e:
        logger.error(f"Ошибка при создании задачи: {e}", exc_info=True)
        await query.edit_message_text(
            "❌ Произошла ошибка при создании задачи. Попробуйте позже."
        )
    
    return ConversationHandler.END

async def cancel_task_creation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена создания задачи"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("❌ Создание задачи отменено.")
    return ConversationHandler.END
