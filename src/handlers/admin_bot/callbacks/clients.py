"""Обработчики callback-запросов для раздела клиентов"""

import re
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram.helpers import escape_markdown

from src.database.db import db
from src.database.models import Client, Task, User
from ..keyboards import get_clients_keyboard
from ..constants import (
    CALLBACK_CLIENT_PREFIX,
    CALLBACK_CLIENT_ADD
)
from .utils import sort_tasks

# Состояния обработки
ENTER_CLIENT_NAME = 1

async def handle_clients_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик callback-запросов для раздела клиентов

    Args:
        update: Объект обновления Telegram
        context: Контекст Telegram бота

    Returns:
        int: Следующее состояние разговора или ConversationHandler.END

    Обрабатывает следующие callback-запросы:
    - CALLBACK_CLIENT_ADD: запрос на добавление нового клиента
    - CALLBACK_CLIENT_PREFIX: просмотр информации о клиенте
    """
    query = update.callback_query
    await query.answer()
    
    if query.data == CALLBACK_CLIENT_ADD:
        # Запрашиваем имя нового клиента
        await query.message.edit_text(
            "Пожалуйста, введите название нового клиента:",
        )
        return ENTER_CLIENT_NAME
    
    elif query.data.startswith(CALLBACK_CLIENT_PREFIX):
        client_id = int(query.data.replace(CALLBACK_CLIENT_PREFIX, ""))
        client = await db.get(Client, client_id)
        
        if client:
            # Получаем только активные задачи для этого клиента
            active_tasks = await db.get_all(
                Task,
                client_id=client_id,
                status=['in_progress', 'not_started']
            )
            
            # Сортируем задачи
            sorted_tasks = sort_tasks(active_tasks)
            
            # Формируем заголовок
            header = (
                f"🏢 *Клиент:* {escape_markdown(client.name, version=2)}\n"
                f"📋 Всего задач: {len(sorted_tasks)}\n\n"
                f"*Список задач:*\n"
            )
            
            # Формируем список задач
            tasks_list = []
            for task in sorted_tasks:
                # Получаем исполнителя
                assignee = await db.get(User, task.assignee_id) if task.assignee_id else None
                assignee_name = assignee.full_name if assignee else "Не назначен"
                
                # Формируем строку задачи
                status_emoji = {'not_started': '⭕️', 'in_progress': '🔄'}.get(task.status, '❓')
                task_str = (
                    f"{status_emoji} *{escape_markdown(task.title, version=2)}*\n"
                    f"👤 {escape_markdown(assignee_name, version=2)}\n"
                )
                if task.due_date:
                    formatted_date = re.sub(r'([.!])', r'\\\1', task.due_date.strftime('%d.%m.%Y'))
                    task_str += f"📅 {formatted_date}\n"
                
                tasks_list.append(task_str)
            
            # Если задач нет, добавляем сообщение
            if not tasks_list:
                tasks_list = ["У клиента пока нет задач"]
            
            # Объединяем всё вместе
            message = header + "\n".join(tasks_list)
            
            await query.message.edit_text(
                text=message,
                parse_mode='MarkdownV2'
            )
        else:
            await query.message.edit_text("❌ Клиент не найден")
    
    return ConversationHandler.END

async def handle_client_name_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработка ввода имени нового клиента

    Args:
        update: Объект обновления Telegram
        context: Контекст Telegram бота

    Returns:
        int: Следующее состояние разговора (всегда ConversationHandler.END)
    """
    try:
        # Создаем нового клиента
        client_name = update.message.text
        new_client = await db.create(Client, name=client_name)
        if new_client:
            # Обновляем список клиентов
            clients = await db.get_all(Client)
            keyboard = await get_clients_keyboard(clients)
            
            await update.message.reply_text(
                f"✅ Клиент \"{client_name}\" успешно создан!\n\nСписок клиентов:",
                reply_markup=keyboard
            )
            
        return ConversationHandler.END
        
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при создании клиента: {str(e)}")
        return ConversationHandler.END