"""Обработчики для работы с клиентами в админском боте"""

import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)

from src.database.db import db
from src.database.models import Client
from .constants import CLIENT_LIST_MESSAGE
from .keyboards import get_clients_keyboard

logger = logging.getLogger(__name__)

# Состояния диалога создания клиента
ENTER_CLIENT_NAME = 1

async def clients_list_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /clients_list"""
    try:
        clients = db.get_all(Client)
        
        if not clients:
            await update.message.reply_text(
                "📝 Список клиентов пуст. Используйте /new_client для добавления клиента."
            )
            return

        # Формирование списка клиентов
        clients_list = []
        active_projects_count = 0
        for client in clients:
            projects_count = len(client.projects)
            active_projects = len([p for p in client.projects if p.status == 'active'])
            active_projects_count += active_projects
            
            clients_list.append(
                f"🏢 *{client.name}*\n"
                f"📂 Проектов: {projects_count} \\(активных: {active_projects}\\)\n"
            )

        # Отправка сообщения
        await update.message.reply_text(
            CLIENT_LIST_MESSAGE.format(
                clients_list="\n".join(clients_list),
                total_count=len(clients),
                active_projects_count=active_projects_count
            ),
            parse_mode='MarkdownV2'
        )
    except Exception as e:
        logger.error(f"Ошибка при получении списка клиентов: {e}")
        await update.message.reply_text(
            "Произошла ошибка при получении списка клиентов. Пожалуйста, попробуйте позже."
        )

async def new_client_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало диалога создания нового клиента"""
    await update.message.reply_text(
        "Введите название нового клиента:",
        reply_markup=None  # Убираем клавиатуру на время ввода
    )
    return ENTER_CLIENT_NAME

async def enter_client_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка ввода названия клиента"""
    context.user_data['client_name'] = update.message.text
    return await save_client(update, context)

async def save_client(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сохранение нового клиента"""
    try:
        client = db.create(Client,
            name=context.user_data['client_name']
        )
        
        await update.message.reply_text(
            f"✅ Клиент \"{client.name}\" успешно создан!",
            reply_markup=get_clients_keyboard(db.get_all(Client), "select_client")
        )
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Ошибка при создании клиента: {e}")
        await update.message.reply_text(
            "Произошла ошибка при создании клиента. Пожалуйста, попробуйте позже."
        )
        return ConversationHandler.END

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена создания клиента"""
    await update.message.reply_text(
        "❌ Создание клиента отменено."
    )
    return ConversationHandler.END

def setup_client_handlers(application: Application) -> None:
    """Настройка обработчиков для работы с клиентами"""
    # Обработчик списка клиентов
    application.add_handler(CommandHandler("clients_list", clients_list_command))
    
    # Обработчик создания нового клиента
    new_client_handler = ConversationHandler(
        entry_points=[CommandHandler("new_client", new_client_command)],
        states={
            ENTER_CLIENT_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_client_name)
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel_command)]
    )
    application.add_handler(new_client_handler)
