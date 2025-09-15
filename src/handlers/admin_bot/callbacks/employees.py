"""Обработчики callback-запросов для раздела сотрудников"""

import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from src.database.db import db
from src.database.models import User
from src.utils.invite_codes import generate_invite_code, save_invite_code
from ..constants import (
    CALLBACK_EMPLOYEE_PREFIX,
    CALLBACK_EMPLOYEE_ADD,
    EMPLOYEE_TASKS_MESSAGE,
    EMPLOYEES_MENU_MESSAGE
)
from .utils import get_employee_active_tasks, format_employee_tasks
from ..keyboards import get_employees_keyboard

logger = logging.getLogger(__name__)

async def handle_employees_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик callback-запросов для раздела сотрудников

    Args:
        update: Объект обновления Telegram
        context: Контекст Telegram бота

    Обрабатывает следующие callback-запросы:
    - CALLBACK_EMPLOYEE_ADD: запрос на добавление нового сотрудника
    - CALLBACK_EMPLOYEE_PREFIX: просмотр задач сотрудника
    """
    query = update.callback_query
    await query.answer()
    
    try:
        if query.data == CALLBACK_EMPLOYEE_ADD:
            # Генерируем новый код приглашения
            code, expires_at = await generate_invite_code()
            
            # Сохраняем код в базе
            await save_invite_code(code, expires_at)
            
            # Форматируем дату истечения и экранируем спецсимволы
            formatted_date = expires_at.strftime('%d\\.%m\\.%Y %H:%M')
            
            # Форматируем сообщение с кодом
            bot_username = "@pc\\_user\\_task\\_bot"
            message = (
                "🎫 *Новый код приглашения*\n\n"
                f"Код: `{code}`\n"
                f"Действует до: {formatted_date}\n\n"
                "Перейдите в бота: \n\n"
                f"{bot_username}\n\n"
                "и введите код для добавления" 
            )

            await query.message.edit_text(
                message,
                parse_mode='MarkdownV2'
            )
        
        elif query.data == "back_to_employees":
            # Получаем список всех сотрудников
            employees = await db.get_all(User)
            # Отправляем сообщение со списком
            await query.message.edit_text(
                EMPLOYEES_MENU_MESSAGE,
            )
        
        elif query.data == EMPLOYEE_TASKS_MESSAGE:
            # Получаем список всех сотрудников
            employees = await db.get_all(User)
            # Создаем клавиатуру со списком
            keyboard = await get_employees_keyboard(employees)
            # Отправляем сообщение со списком
            await query.message.edit_text(
                EMPLOYEES_MENU_MESSAGE,
            )
        
        elif query.data.startswith(CALLBACK_EMPLOYEE_PREFIX):
            # Получаем ID сотрудника из callback data
            employee_id = int(query.data.split('_')[-1])
            
            # Получаем информацию о сотруднике
            users = await db.get_all(User)
            employee = next(
                (user for user in users if user.id == employee_id),
                None
            )
            if not employee:
                await query.message.edit_text("❌ Сотрудник не найден")
                return
            
            # Получаем активные задачи сотрудника
            tasks = await get_employee_active_tasks(employee_id)
            
            # Форматируем список задач и получаем статистику
            stats = format_employee_tasks(tasks)
            
            # Экранируем специальные символы для Markdown
            employee_name = employee.full_name.replace('.', '\\.').replace('-', '\\-').replace('_', '\\_')
            tasks_list = stats['tasks_list'].replace('.', '\\.').replace('-', '\\-').replace('_', '\\_')
            nearest_deadline = stats['nearest_deadline'].replace('.', '\\.').replace('-', '\\-').replace('_', '\\_')
            
            # Создаем сообщение
            message = EMPLOYEE_TASKS_MESSAGE.format(
                employee_name=employee_name,
                tasks_list=tasks_list,
                total_tasks=stats['total_tasks'],
                in_progress_tasks=stats['in_progress_tasks'],
                not_started_tasks=stats['not_started_tasks'],
                nearest_deadline=nearest_deadline
            )

            await query.message.edit_text(
                text=message,
                parse_mode='MarkdownV2',
            )
            
    except Exception as e:
        logger.error(f"Ошибка при обработке callback сотрудника: {e}")
        await query.message.edit_text(
            "❌ Произошла ошибка при получении информации о сотруднике"
        )