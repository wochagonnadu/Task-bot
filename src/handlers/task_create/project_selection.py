"""
Обработчики для выбора проекта при создании задачи
"""
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram.helpers import escape_markdown

from src.database.models import Project
from src.database.db import db
from .constants import (
    SELECT_PROJECT,
    TITLE,
    MSG_SELECT_PROJECT,
    CALLBACK_NEW_PROJECT,
    CALLBACK_SELECT_PROJECT
)
from .keyboards import create_project_keyboard

async def show_projects(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Отображение списка проектов для выбранного клиента
    """
    client_id = context.user_data.get('selected_client_id')
    if not client_id:
        await update.message.reply_text("Ошибка: клиент не выбран")
        return ConversationHandler.END

    try:
        # Получаем проекты для выбранного клиента и преобразуем их в словари
        projects = await db.get_all(Project, client_id=client_id)
        print(f"Found projects for client {client_id}: {projects}")  # Debug log
        
        if not projects:
            # Если проектов нет, создаем клавиатуру только с кнопкой создания
            projects_data = []
        else:
            projects_data = [project.to_dict() for project in projects]
            print(f"Projects data: {projects_data}")  # Debug log
            
        reply_markup = create_project_keyboard(projects_data)

        message_text = (MSG_SELECT_PROJECT if projects_data
                       else "У клиента нет проектов. Создайте новый проект:")

        # Определяем, откуда пришел запрос (сообщение или callback)
        if update.callback_query:
            await update.callback_query.edit_message_text(
                message_text,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                message_text,
                reply_markup=reply_markup
            )
        return SELECT_PROJECT
    except Exception as e:
        error_msg = f"Ошибка при получении списка проектов: {str(e)}"
        print(f"Error in show_projects: {error_msg}")  # Debug log
        await (update.callback_query or update).message.reply_text(error_msg)
        return ConversationHandler.END

async def project_selection_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработка выбора проекта через инлайн-кнопку
    """
    query = update.callback_query
    await query.answer()
    
    try:
        project_id = int(query.data.replace(CALLBACK_SELECT_PROJECT, ""))
        project = await db.get(Project, project_id)
        
        if not project:
            await query.message.reply_text("Ошибка: проект не найден")
            return ConversationHandler.END
        
        context.user_data['selected_project_id'] = project_id
        context.user_data['selected_project_name'] = project.name
        
        # Переходим к вводу названия задачи
        from .task_details import create_title_keyboard
        reply_markup = create_title_keyboard()
        await query.message.reply_text(
            "Отлично! Теперь введите название задачи:",
            reply_markup=reply_markup
        )
        return TITLE
    except Exception as e:
        await query.message.reply_text(f"Ошибка при выборе проекта: {str(e)}")
        return ConversationHandler.END

async def new_project_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработка нажатия кнопки создания нового проекта
    """
    query = update.callback_query
    await query.answer()
    
    await query.message.reply_text(
        "Пожалуйста, введите название нового проекта:"
    )
    return SELECT_PROJECT

async def create_new_project(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Создание нового проекта из текстового сообщения
    """
    try:
        project_name = escape_markdown(update.message.text, version=2)
        client_id = context.user_data.get('selected_client_id')
        
        if not client_id:
            await update.message.reply_text("Ошибка: клиент не выбран")
            return ConversationHandler.END
        
        # Создаем новый проект
        new_project = await db.create(Project, name=project_name, client_id=client_id)
        
        context.user_data['selected_project_id'] = new_project.id
        context.user_data['selected_project_name'] = project_name
        
        # Переходим к вводу названия задачи
        from .task_details import create_title_keyboard
        reply_markup = create_title_keyboard()
        await update.message.reply_text(
            "Отлично! Теперь введите название задачи:",
            reply_markup=reply_markup
        )
        return TITLE
    except Exception as e:
        await update.message.reply_text(f"Ошибка при создании проекта: {str(e)}")
        return ConversationHandler.END