"""Обработчик для списка задач"""

import logging
from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes

from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from src.database.db import db, get_session
from src.database.models import User, Task
from src.utils.helpers import format_datetime
from .constants import (
    MY_TASKS_MESSAGE,
    TASK_LIST_ITEM,
    TASK_STATUSES
)
from .keyboards import create_tasks_keyboard, create_main_keyboard

logger = logging.getLogger(__name__)

async def get_user_tasks(user_id: int) -> list[Task]:
    """Получение активных и не начатых задач с загруженными связанными объектами"""
    try:
        tasks = await db.get_tasks_with_relations(
            user_id,
            only_active=True  # Получаем только активные и не начатые задачи
        )
        return tasks
    except Exception as e:
        logger.error(f"Ошибка при получении списка задач: {e}", exc_info=True)
        return []

async def format_task_list(tasks: list[Task]) -> tuple[str, int]:
    """Форматирование списка задач"""
    tasks_list = []
    for task in tasks:
        try:
            # Так как связанные объекты уже загружены, можно безопасно обращаться к ним
            client_name = task.client.name if task.client else "Не указан"
            project_name = task.project.name if task.project else "Не указан"
            
            task_text = TASK_LIST_ITEM.format(
                title=task.title,
                status=TASK_STATUSES.get(task.status, task.status),
                deadline=format_datetime(task.due_date) if task.due_date else "Не указан",
                client=client_name,
                project=project_name
            )
            tasks_list.append(task_text)
        except Exception as e:
            logger.error(f"Ошибка при форматировании задачи {task.id}: {e}", exc_info=True)
            continue
    
    return "\n".join(tasks_list), len(tasks)

async def update_task_message(query: CallbackQuery, user_id: int) -> None:
    """Обновляет сообщение со списком активных задач"""
    async with get_session() as session:
        try:
            # Получаем пользователя по telegram_id
            user = await session.execute(
                select(User).where(User.telegram_id == user_id)
            )
            user = user.scalar_one_or_none()
            if not user:
                await query.edit_message_text("❌ Пользователь не найден.")
                return

            # Получаем задачи для пользователя
            stmt = (
                select(Task)
                .where(
                    and_(
                        Task.assignee_id == user.id,
                        Task.status.in_(['not_started', 'in_progress'])
                    )
                )
                .options(
                    selectinload(Task.client),
                    selectinload(Task.project)
                )
            )
            result = await session.execute(stmt)
            tasks = list(result.scalars().all())

            if not tasks:
                await query.edit_message_text("📋 У вас нет активных задач.")
                return

            # Форматируем список
            tasks_list, total_count = await format_task_list(tasks)

            # Обновляем сообщение
            message_text = MY_TASKS_MESSAGE.format(
                tasks_list=tasks_list,
                total_count=total_count
            )
            await query.edit_message_text(
                message_text,
                reply_markup=create_tasks_keyboard(tasks),
                parse_mode='Markdown'
            )

        except Exception as e:
            logger.error(f"Ошибка при обновлении списка задач: {e}", exc_info=True)
            await query.edit_message_text("❌ Произошла ошибка при обновлении списка задач.")

async def my_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показать список задач пользователя"""
    try:
        # Получаем пользователя
        user = await db.get_by_field(User, 'telegram_id', update.effective_user.id)

        if not user:
            await update.message.reply_text(
                "❌ У вас нет доступа к этому боту.",
                reply_markup=create_main_keyboard()
            )
            return

        # Получаем только активные и не начатые задачи
        tasks = await get_user_tasks(user.id)

        if not tasks:
            await update.message.reply_text(
                "📋 У вас нет активных задач.",
                reply_markup=create_main_keyboard()
            )
            return

        # Форматируем список задач
        tasks_list, total_count = await format_task_list(tasks)

        # Формируем сообщение
        message_text = MY_TASKS_MESSAGE.format(
            tasks_list=tasks_list,
            total_count=total_count
        )

        # Создаем клавиатуру только с кнопками задач
        keyboard = create_tasks_keyboard(tasks)

        await update.message.reply_text(
            message_text,
            reply_markup=keyboard,
            parse_mode='Markdown'
        )

    except Exception as e:
        logger.error(f"Ошибка при получении списка задач: {e}", exc_info=True)
        await update.message.reply_text(
            "❌ Произошла ошибка при получении списка задач. Попробуйте позже.",
            reply_markup=create_main_keyboard()
        )