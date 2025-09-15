"""Обработчики для работы с задачами в админском боте"""

import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from src.database.db import db
from src.database.models import Task, User
from src.handlers.task_create import new_task_conversation
from .constants import (
    TASK_LIST_MESSAGE,
    ADMIN_TASK_LIST_ITEM,
    ADMIN_TASK_DETAIL_MESSAGE,
    ASSIGN_TASK,
    EDIT_TASK,
    DELETE_TASK,
    SHOW_TASK_DETAILS,
    TASK_STATUSES
)

logger = logging.getLogger(__name__)

async def tasks_list_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /tasks_list"""
    try:
        tasks = db.get_all(Task)
        
        # Подсчет статистики
        total_count = len(tasks)
        in_progress_count = len([t for t in tasks if t.status == 'in_progress'])
        not_started_count = len([t for t in tasks if t.status == 'not_started'])
        completed_count = len([t for t in tasks if t.status == 'completed'])
        
        # Формирование списка задач
        tasks_list = []
        for task in tasks:
            assignee = db.get(User, task.assignee_id) if task.assignee_id else None
            tasks_list.append(ADMIN_TASK_LIST_ITEM.format(
                title=task.title,
                assignee=assignee.full_name if assignee else "Не назначен",
                status=TASK_STATUSES.get(task.status, task.status),
                deadline=task.due_date.strftime("%d.%m.%Y %H:%M") if task.due_date else "Не указан",
                client=task.client.name if task.client else "Не указан",
                project=task.project.name if task.project else "Не указан"
            ))
        
        # Отправка сообщения
        await update.message.reply_text(
            TASK_LIST_MESSAGE.format(
                tasks_list="\n".join(tasks_list),
                total_count=total_count,
                in_progress_count=in_progress_count,
                not_started_count=not_started_count,
                completed_count=completed_count
            ),
            parse_mode='MarkdownV2'
        )
    except Exception as e:
        logger.error(f"Ошибка при получении списка задач: {e}")
        await update.message.reply_text(
            "Произошла ошибка при получении списка задач. Пожалуйста, попробуйте позже."
        )

async def assign_task_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /assign_task"""
    # Будет реализовано позже
    await update.message.reply_text(
        "Функционал назначения задач находится в разработке..."
    )

async def edit_task_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /edit_task"""
    # Будет реализовано позже
    await update.message.reply_text(
        "Функционал редактирования задач находится в разработке..."
    )

async def delete_task_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /delete_task"""
    # Будет реализовано позже
    await update.message.reply_text(
        "Функционал удаления задач находится в разработке..."
    )

async def task_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик callback-запросов для задач"""
    query = update.callback_query
    await query.answer()
    
    # Обработка различных callback-действий будет добавлена позже

def setup_task_handlers(application: Application) -> None:
    """Настройка обработчиков для работы с задачами"""
    # Добавление обработчика создания задач
    application.add_handler(new_task_conversation)
    
    # Добавление обработчиков команд
    application.add_handler(CommandHandler("tasks_list", tasks_list_command))
    application.add_handler(CommandHandler("assign_task", assign_task_command))
    application.add_handler(CommandHandler("edit_task", edit_task_command))
    application.add_handler(CommandHandler("delete_task", delete_task_command))
    
    # Добавление обработчиков callback-запросов для задач
    application.add_handler(
        CallbackQueryHandler(
            task_callback_handler,
            pattern=f"^({ASSIGN_TASK}|{EDIT_TASK}|{DELETE_TASK}|{SHOW_TASK_DETAILS}).*"
        )
    )