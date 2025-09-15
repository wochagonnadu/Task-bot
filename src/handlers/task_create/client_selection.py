"""
Обработчики для выбора клиента при создании задачи
"""
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram.helpers import escape_markdown

from src.database.models import User, Client
from src.database.db import db
from .constants import (
    SELECT_CLIENT,
    SELECT_PROJECT,
    MSG_SELECT_CLIENT,
    CALLBACK_NEW_CLIENT,
    CALLBACK_SELECT_CLIENT
)
from .keyboards import create_client_keyboard

async def start_client_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Начало процесса создания задачи - выбор клиента
    """
    try:
        user = await db.get_by_field(User, 'telegram_id', update.effective_user.id)
        if not user:
            await update.message.reply_text(
                "Для создания задач необходимо сначала зарегистрироваться. "
                "Используйте команду /start"
            )
            return ConversationHandler.END

        if update.effective_chat.type in ["group", "supergroup"]:
            await update.message.reply_text(
                "Давайте создадим новую задачу.\n"
                "Чтобы не засорять групповой чат, давайте продолжим в личных сообщениях.\n"
                "Напишите мне в личку команду /new_task"
            )
            return ConversationHandler.END

        # Получаем список клиентов и преобразуем их в словари
        clients = await db.get_all(Client)
        clients_data = [client.to_dict() for client in clients]
        reply_markup = create_client_keyboard(clients_data)
        
        await update.message.reply_text(MSG_SELECT_CLIENT, reply_markup=reply_markup)
        return SELECT_CLIENT
        
    except Exception as e:
        await update.message.reply_text(f"Ошибка при начале создания задачи: {str(e)}")
        return ConversationHandler.END

async def client_selection_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработка выбора клиента через инлайн-кнопку
    """
    query = update.callback_query
    await query.answer()
    
    try:
        client_id = int(query.data.replace(CALLBACK_SELECT_CLIENT, ""))
        client = await db.get(Client, client_id)
        
        if not client:
            await query.message.reply_text("Ошибка: клиент не найден")
            return ConversationHandler.END
        
        context.user_data['selected_client_id'] = client_id
        context.user_data['selected_client_name'] = client.name
        
        # Переходим к выбору проекта
        from .project_selection import show_projects  # Импорт здесь во избежание циклических зависимостей
        return await show_projects(update, context)
        
    except Exception as e:
        await query.message.reply_text(f"Ошибка при выборе клиента: {str(e)}")
        return ConversationHandler.END

async def new_client_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработка нажатия кнопки создания нового клиента
    """
    query = update.callback_query
    await query.answer()
    
    await query.message.reply_text(
        "Пожалуйста, введите название нового клиента:"
    )
    return SELECT_CLIENT

async def create_new_client(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Создание нового клиента из текстового сообщения
    """
    try:
        client_name = escape_markdown(update.message.text, version=2)
        
        # Создаем нового клиента
        new_client = await db.create(Client, name=client_name)
        
        context.user_data['selected_client_id'] = new_client.id
        context.user_data['selected_client_name'] = client_name
        
        # Переходим к выбору проекта
        from .project_selection import show_projects  # Импорт здесь во избежание циклических зависимостей
        return await show_projects(update, context)
    except Exception as e:
        await update.message.reply_text(f"Ошибка при создании клиента: {str(e)}")
        return ConversationHandler.END