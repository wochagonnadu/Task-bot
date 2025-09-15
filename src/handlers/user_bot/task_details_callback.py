"""Обработчик callback-запросов для просмотра деталей задачи"""

import logging
from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes

from src.database.db import db, get_session
from src.database.models import Task, User
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.utils.helpers import format_datetime
from .constants import TASK_DETAIL_MESSAGE, TASK_STATUSES
from .keyboards import create_task_control_keyboard
from .task_list import my_tasks

logger = logging.getLogger(__name__)

async def view_task_details(query: CallbackQuery, task: Task) -> None:
    """Показывает детали задачи"""
    try:
        message_text = TASK_DETAIL_MESSAGE.format(
            task_id=task.id,
            title=task.title,
            description=task.description or "Нет описания",
            status=TASK_STATUSES.get(task.status, task.status),
            created_at=format_datetime(task.created_at),
            deadline=format_datetime(task.due_date) if task.due_date else "Не указан",
            client=task.client.name if task.client else "Не указан",
            project=task.project.name if task.project else "Не указан"
        )
        keyboard = create_task_control_keyboard(task)
        
        await query.message.edit_text(
            message_text,
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Ошибка при отображении деталей задачи: {e}", exc_info=True)
        await query.message.edit_text(
            "❌ Произошла ошибка при отображении деталей задачи."
        )

async def get_task_and_check_access(query: CallbackQuery, task_id: int) -> tuple[Task, User] | None:
    """Получает задачу с загруженными связями и проверяет доступ пользователя"""
    try:
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload

        async with get_session() as session:
            # Получаем задачу со всеми связями
            stmt = (select(Task)
                   .options(
                       selectinload(Task.client),
                       selectinload(Task.project)
                   )
                   .where(Task.id == task_id))
            result = await session.execute(stmt)
            task = result.scalar_one_or_none()

        user = await db.get_by_field(User, 'telegram_id', query.from_user.id)

        if not task:
            await query.message.reply_text("❌ Задача не найдена.")
            return None

        if not user:
            await query.message.reply_text("❌ Пользователь не найден.")
            return None

        if task.assignee_id != user.id:
            await query.message.reply_text("❌ У вас нет доступа к этой задаче.")
            return None

        return task, user
    except Exception as e:
        logger.error(f"Ошибка при проверке доступа к задаче: {e}", exc_info=True)
        await query.message.reply_text(
            "❌ Произошла ошибка при проверке доступа к задаче."
        )
        return None