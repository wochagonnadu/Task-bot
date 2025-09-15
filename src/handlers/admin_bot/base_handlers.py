from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.database.db import db
from src.database.models import Client, User, Project

from .constants import (
    WELCOME_MESSAGE,
    HELP_MESSAGE,
    BUTTON_TASKS,
    BUTTON_CLIENTS,
    BUTTON_PROJECTS,
    BUTTON_EMPLOYEES,
    BUTTON_NEW_TASK,
    BUTTON_REPORTS,
    TASKS_MENU_MESSAGE,
    CLIENTS_MENU_MESSAGE,
    PROJECTS_MENU_MESSAGE,
    EMPLOYEES_MENU_MESSAGE,
    REPORTS_MENU_MESSAGE
)
from .keyboards import (
    get_admin_keyboard,
    get_tasks_keyboard,
    get_clients_keyboard,
    get_projects_keyboard,
    get_employees_keyboard,
    get_reports_keyboard
)

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    if context.user_data.get('db_user'):  # Only show keyboard if user is authenticated
        await update.message.reply_text(
            text="Выберите действие:",
            reply_markup=get_admin_keyboard()
        )

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    await update.message.reply_text(HELP_MESSAGE)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки главного меню"""
    if not update.message or not update.message.text:
        return

    text = update.message.text

    try:
        if text == BUTTON_TASKS:
            # Показываем подменю задач с inline кнопками
            keyboard = await get_tasks_keyboard()
            await update.message.reply_text(
                TASKS_MENU_MESSAGE,
                reply_markup=keyboard
            )
        
        elif text == BUTTON_CLIENTS:
            # Получаем реальных клиентов из БД
            clients = await db.get_all(Client)
            msg = f"{CLIENTS_MENU_MESSAGE}\nВсего клиентов: {len(clients)}"
            keyboard = await get_clients_keyboard(clients)
            await update.message.reply_text(
                msg,
                reply_markup=keyboard
            )
        
        elif text == BUTTON_PROJECTS:
            # Получаем реальные проекты из БД
            projects = await db.get_all(Project)
            msg = f"{PROJECTS_MENU_MESSAGE} {len(projects)}"
            keyboard = await get_projects_keyboard(projects)
            await update.message.reply_text(
                msg,
                reply_markup=keyboard
            )
        
        elif text == BUTTON_EMPLOYEES:
            # Получаем реальных сотрудников из БД
            employees = await db.get_all(User)
            keyboard = await get_employees_keyboard(employees)
            await update.message.reply_text(
                EMPLOYEES_MENU_MESSAGE,
                reply_markup=keyboard
            )
        
        elif text == BUTTON_NEW_TASK:
            # Запускаем команду создания новой задачи
            await update.message.reply_text("/new_task")
        
        elif text == BUTTON_REPORTS:
            # Показываем подменю отчетов с inline кнопками
            keyboard = await get_reports_keyboard()
            await update.message.reply_text(
                REPORTS_MENU_MESSAGE,
                reply_markup=keyboard
            )
            
    except Exception as e:
        await update.message.reply_text(
            f"Произошла ошибка при обработке команды: {str(e)}"
        )

async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик неизвестных команд"""
    await update.message.reply_text(
        "Извините, я не понимаю эту команду. Используйте /help для просмотра доступных команд."
    )
