"""Обработчики для работы с проектами в админском боте"""

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
from src.database.models import Project, Client
from .constants import PROJECT_LIST_MESSAGE
from .keyboards import get_projects_keyboard, get_clients_keyboard

logger = logging.getLogger(__name__)

# Состояния диалога создания проекта
SELECT_CLIENT = 1
ENTER_PROJECT_NAME = 2
ENTER_PROJECT_DESCRIPTION = 3

async def projects_list_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /projects_list"""
    try:
        projects = db.get_all(Project)
        
        if not projects:
            await update.message.reply_text(
                "📝 Список проектов пуст. Используйте /new_project для создания проекта."
            )
            return

        # Формирование списка проектов
        projects_list = []
        active_count = 0
        completed_count = 0
        
        for project in projects:
            if project.status == 'active':
                active_count += 1
            elif project.status == 'completed':
                completed_count += 1
                
            client_name = project.client.name if project.client else "Без клиента"
            
            projects_list.append(
                f"📂 *{project.name}*\n"
                f"🏢 Клиент: {client_name}\n"
                f"📊 Статус: {project.status}\n"
            )

        # Отправка сообщения
        await update.message.reply_text(
            PROJECT_LIST_MESSAGE.format(
                projects_list="\n".join(projects_list),
                total_count=len(projects),
                active_count=active_count,
                completed_count=completed_count
            ),
            parse_mode='MarkdownV2'
        )
    except Exception as e:
        logger.error(f"Ошибка при получении списка проектов: {e}")
        await update.message.reply_text(
            "Произошла ошибка при получении списка проектов. Пожалуйста, попробуйте позже."
        )

async def new_project_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало диалога создания нового проекта"""
    clients = db.get_all(Client)
    
    if not clients:
        await update.message.reply_text(
            "❌ Необходимо сначала создать хотя бы одного клиента.\n"
            "Используйте /new_client для создания клиента."
        )
        return ConversationHandler.END
    
    await update.message.reply_text(
        "Выберите клиента для нового проекта:",
        reply_markup=get_clients_keyboard(clients, "select_client_for_project")
    )
    return SELECT_CLIENT

async def client_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора клиента"""
    query = update.callback_query
    await query.answer()
    
    client_id = int(query.data.split('_')[-1])
    context.user_data['client_id'] = client_id
    
    await query.message.edit_text(
        "Введите название нового проекта:"
    )
    return ENTER_PROJECT_NAME

async def enter_project_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка ввода названия проекта"""
    context.user_data['project_name'] = update.message.text
    await update.message.reply_text(
        "Введите описание проекта:\n"
        "(или отправьте /skip чтобы пропустить)"
    )
    return ENTER_PROJECT_DESCRIPTION

async def skip_project_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Пропуск ввода описания"""
    return await save_project(update, context, description=None)

async def enter_project_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка ввода описания"""
    return await save_project(update, context, description=update.message.text)

async def save_project(update: Update, context: ContextTypes.DEFAULT_TYPE, description: str = None) -> int:
    """Сохранение нового проекта"""
    try:
        project = db.create(Project,
            name=context.user_data['project_name'],
            description=description,
            client_id=context.user_data['client_id'],
            status='active'
        )
        
        client = db.get(Client, context.user_data['client_id'])
        await update.message.reply_text(
            f"✅ Проект \"{project.name}\" успешно создан для клиента \"{client.name}\"!",
            reply_markup=get_projects_keyboard(db.get_all(Project), "select_project")
        )
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Ошибка при создании проекта: {e}")
        await update.message.reply_text(
            "Произошла ошибка при создании проекта. Пожалуйста, попробуйте позже."
        )
        return ConversationHandler.END

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена создания проекта"""
    await update.message.reply_text(
        "❌ Создание проекта отменено."
    )
    return ConversationHandler.END

def setup_project_handlers(application: Application) -> None:
    """Настройка обработчиков для работы с проектами"""
    # Обработчик списка проектов
    application.add_handler(CommandHandler("projects_list", projects_list_command))
    
    # Обработчик создания нового проекта
    new_project_handler = ConversationHandler(
        entry_points=[CommandHandler("new_project", new_project_command)],
        states={
            SELECT_CLIENT: [
                CallbackQueryHandler(client_selected, pattern=r"^select_client_for_project_\d+$")
            ],
            ENTER_PROJECT_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_project_name)
            ],
            ENTER_PROJECT_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_project_description),
                CommandHandler("skip", skip_project_description)
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel_command)]
    )
    application.add_handler(new_project_handler)
    
    # Обработчики callback-запросов для проектов
    application.add_handler(
        CallbackQueryHandler(
            projects_list_command,
            pattern=r"^show_project_\d+$"
        )
    )