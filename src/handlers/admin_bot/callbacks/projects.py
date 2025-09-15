"""Обработчики callback-запросов для раздела проектов"""

import re
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram.helpers import escape_markdown

from src.database.db import db
from src.database.models import Client, Project, Task, User
from ..keyboards import get_projects_keyboard
from ..constants import (
    CALLBACK_PROJECT_PREFIX,
    CALLBACK_PROJECT_ADD
)
from .utils import sort_tasks

# Состояния обработки
ENTER_PROJECT_NAME = 2

async def handle_projects_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик callback-запросов для раздела проектов

    Args:
        update: Объект обновления Telegram
        context: Контекст Telegram бота

    Returns:
        int: Следующее состояние разговора или ConversationHandler.END

    Обрабатывает следующие callback-запросы:
    - CALLBACK_PROJECT_ADD: запрос на добавление нового проекта
    - CALLBACK_PROJECT_PREFIX: просмотр информации о проекте
    """
    query = update.callback_query
    await query.answer()
    
    if query.data == CALLBACK_PROJECT_ADD:
        await query.message.edit_text(
            "Пожалуйста, введите название нового проекта:"
        )
        return ENTER_PROJECT_NAME
    
    elif query.data.startswith(CALLBACK_PROJECT_PREFIX):
        project_id = int(query.data.replace(CALLBACK_PROJECT_PREFIX, ""))
        project = await db.get(Project, project_id)
        
        if project:
            # Получаем клиента проекта
            client = await db.get(Client, project.client_id) if project.client_id else None

            # Получаем только активные задачи для этого проекта
            active_tasks = await db.get_all(
                Task,
                project_id=project_id,
                status=['in_progress', 'not_started']
            )
            
            # Сортируем задачи
            sorted_tasks = sort_tasks(active_tasks)
            
            # Формируем заголовок
            header = (
                f"📊 *Проект:* {escape_markdown(project.name, version=2)}\n"
                f"🏢 *Клиент:* {escape_markdown(client.name, version=2) if client else 'Не указан'}\n"
                f"📋 Активных задач: {len(sorted_tasks)}\n\n"
                f"*Список задач:*\n"
            )
            
            # Формируем список задач
            tasks_list = []
            for task in sorted_tasks:
                # Получаем исполнителя через ID
                assignee = await db.get(User, task.assignee_id) if task.assignee_id else None
                assignee_name = assignee.full_name if assignee else "Не назначен"
                
                # Формируем строку задачи
                status_emoji = {'not_started': '⭕️', 'in_progress': '🔄'}.get(task.status, '❓')
                task_str = (
                    f"{status_emoji} *{escape_markdown(task.title, version=2)}*\n"
                    f"👤 {escape_markdown(assignee_name, version=2)}\n"
                )
                if task.due_date:
                    formatted_date = task.due_date.strftime('%d.%m.%Y')
                    task_str += f"📅 {formatted_date}\n"
                
                tasks_list.append(task_str)
            
            # Если задач нет, добавляем сообщение
            if not tasks_list:
                tasks_list = ["_У проекта пока нет активных задач_"]
            
            # Объединяем всё вместе
            message = header + "\n\n".join(tasks_list)
            
            await query.message.edit_text(
                text=message,
                parse_mode='MarkdownV2'
            )
        else:
            await query.message.edit_text("❌ Проект не найден")
    
    return ConversationHandler.END

async def handle_project_name_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработка ввода имени нового проекта

    Args:
        update: Объект обновления Telegram
        context: Контекст Telegram бота

    Returns:
        int: Следующее состояние разговора (всегда ConversationHandler.END)
    """
    try:
        # Создаем новый проект
        project_name = update.message.text
        new_project = await db.create(Project, name=project_name)
        if new_project:
            # Обновляем список проектов
            projects = await db.get_all(Project)
            keyboard = await get_projects_keyboard(projects)
            
            await update.message.reply_text(
                f"✅ Проект \"{project_name}\" успешно создан!\n\nСписок проектов:",
                reply_markup=keyboard
            )
            
        return ConversationHandler.END
        
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при создании проекта: {str(e)}")
        return ConversationHandler.END