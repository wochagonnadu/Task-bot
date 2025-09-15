"""Обработчики callback-запросов для раздела задач"""

from telegram import Update
from telegram.ext import ContextTypes

from src.database.db import db
from src.database.models import Task
from ..keyboards import get_tasks_keyboard
from ..constants import (
    CALLBACK_TASKS_ALL,
    CALLBACK_TASKS_ACTIVE,
    CALLBACK_TASKS_COMPLETED,
    CALLBACK_TASKS_NOT_STARTED,
    TASK_STATS_MESSAGE,
    TASK_FILTER_NAMES,
    TASK_FILTER_EMOJI,
    TASK_STATUS_FILTERS
)
from .utils import format_tasks_list, get_tasks_statistics, format_assignees_stats

async def handle_tasks_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик callback-запросов для раздела задач

    Args:
        update: Объект обновления Telegram
        context: Контекст Telegram бота

    Обрабатывает следующие callback-запросы:
    - CALLBACK_TASKS_ALL: отображение всех задач
    - CALLBACK_TASKS_ACTIVE: отображение активных задач
    - CALLBACK_TASKS_COMPLETED: отображение завершенных задач
    - CALLBACK_TASKS_NOT_STARTED: отображение не начатых задач
    """
    query = update.callback_query
    await query.answer()
    
    try:
        # Получаем клавиатуру для дальнейшей фильтрации
        keyboard = await get_tasks_keyboard()

        # Получаем задачи в зависимости от фильтра
        filter_type = query.data
        status = TASK_STATUS_FILTERS.get(filter_type)
        
        if status:
            tasks = await db.get_all(Task, status=status)
        else:
            tasks = await db.get_all(Task)

        # Получаем статистику
        stats = await get_tasks_statistics(tasks)
        
        # Форматируем сообщение
        message = TASK_STATS_MESSAGE.format(
            filter_emoji=TASK_FILTER_EMOJI[filter_type],
            filter_name=TASK_FILTER_NAMES[filter_type],
            total_count=stats['total_count'],
            assignees_stats=format_assignees_stats(stats['assignees_stats'])
        )

        # Обновляем сообщение
        await query.message.edit_text(
            text=message,
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
    except Exception as e:
        await query.message.edit_text(f"❌ Ошибка при получении задач: {e}")