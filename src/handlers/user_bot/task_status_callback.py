"""Обработчик статусов задач"""

import logging
from telegram import CallbackQuery

from src.database.db import db, get_session
from src.database.models import Task
from .constants import TASK_STATUSES
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

logger = logging.getLogger(__name__)

async def handle_start_task(query: CallbackQuery, task: Task) -> None:
    """Обработка начала работы над задачей"""
    try:
        if task.status != 'not_started':
            await query.edit_message_text(
                f"❌ Невозможно начать задачу в статусе {TASK_STATUSES[task.status]}"
            )
            return

        # Обновляем статус задачи
        await db.update(Task, task.id, status="in_progress")
        
        # После обновления получаем свежую задачу со связями
        async with get_session() as session:
            stmt = (select(Task)
                   .where(Task.id == task.id)
                   .options(selectinload(Task.client),
                           selectinload(Task.project)))
            result = await session.execute(stmt)
            updated_task = result.scalar_one_or_none()
            
            if not updated_task:
                await query.edit_message_text("❌ Задача не найдена.")
                return

            # Отправляем подтверждение
            from src.handlers.task_create.keyboards.basic import create_task_list_keyboard
            await query.edit_message_text(
                f"✅ Задача «{updated_task.title}» начата\n"
                f"Клиент: {updated_task.client.name if updated_task.client else 'Не указан'}\n"
                f"Проект: {updated_task.project.name if updated_task.project else 'Не указан'}",
                reply_markup=create_task_list_keyboard()
            )

    except Exception as e:
        logger.error(f"Ошибка при начале работы над задачей: {e}", exc_info=True)
        await query.edit_message_text("❌ Произошла ошибка. Попробуйте позже.")

async def handle_complete_task(query: CallbackQuery, task: Task) -> None:
    """Обработка завершения задачи"""
    try:
        if task.status != 'in_progress':
            await query.edit_message_text(
                f"❌ Можно завершить только задачу в статусе {TASK_STATUSES['in_progress']}"
            )
            return

        # Обновляем статус задачи
        await db.update(Task, task.id, status="completed")
        
        # После обновления получаем свежую задачу со связями
        async with get_session() as session:
            stmt = (select(Task)
                   .where(Task.id == task.id)
                   .options(selectinload(Task.client),
                           selectinload(Task.project)))
            result = await session.execute(stmt)
            updated_task = result.scalar_one_or_none()
            
            if not updated_task:
                await query.edit_message_text("❌ Задача не найдена.")
                return

            # Отправляем подтверждение
            from src.handlers.task_create.keyboards.basic import create_task_list_keyboard
            await query.edit_message_text(
                f"✅ Задача «{updated_task.title}» завершена\n"
                f"Клиент: {updated_task.client.name if updated_task.client else 'Не указан'}\n"
                f"Проект: {updated_task.project.name if updated_task.project else 'Не указан'}",
                reply_markup=create_task_list_keyboard()
            )

    except Exception as e:
        logger.error(f"Ошибка при завершении задачи: {e}", exc_info=True)
        await query.edit_message_text("❌ Произошла ошибка. Попробуйте позже.")