"""Обработчики для просмотра задач"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from src.database.db import db
from src.database.models import User, Task
from src.utils.helpers import format_datetime, truncate_text, get_status_emoji
from .constants import TASK_STATUSES
from .keyboards import create_main_keyboard

logger = logging.getLogger(__name__)

async def view_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показ детальной информации о задаче"""
    try:
        if not context.args:
            await update.message.reply_text(
                "❌ Не указан ID задачи.\n"
                "Используйте команду в формате: /view_task <ID задачи>",
                reply_markup=create_main_keyboard()
            )
            return

        task_id = int(context.args[0])
        task = db.get(Task, task_id)

        if not task:
            await update.message.reply_text(
                "❌ Задача с указанным ID не найдена.",
                reply_markup=create_main_keyboard()
            )
            return

        creator = db.get(User, task.creator_id)
        assignee = db.get(User, task.assignee_id) if task.assignee_id else None

        task_text = (
            f"*Информация о задаче:*\n\n"
            f"🆔 ID: `{task.id}`\n"
            f"📋 Название: {truncate_text(task.title)}\n"
        )
        if task.description:
            task_text += f"📝 Описание: {truncate_text(task.description)}\n"
        if task.deadline:
            task_text += f"⏰ Срок: {format_datetime(task.deadline)}\n"
        
        task_text += f"👤 Создатель: {creator.full_name}\n"
        if assignee:
            task_text += f"👥 Исполнитель: {assignee.full_name}\n"
        
        status_emoji = get_status_emoji(task.status)
        task_text += f"📊 Статус: {status_emoji} {task.status}\n"
        task_text += f"📅 Создано: {format_datetime(task.created_at)}\n"
        
        await update.message.reply_text(
            task_text,
            parse_mode='MarkdownV2',
            reply_markup=create_main_keyboard()
        )

    except ValueError:
        await update.message.reply_text(
            "❌ Некорректный ID задачи. ID должен быть числом.",
            reply_markup=create_main_keyboard()
        )
    except Exception as e:
        logger.error(f"Ошибка при просмотре задачи: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка при получении информации о задаче. Попробуйте позже.",
            reply_markup=create_main_keyboard()
        )