"""
Обработчики для ввода основных деталей задачи
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram.helpers import escape_markdown

from .constants import TITLE, DESCRIPTION, DUE_DATE
from .keyboards import create_description_keyboard, create_date_keyboard

def create_title_keyboard() -> InlineKeyboardMarkup:
    """
    Создание клавиатуры для этапа ввода названия задачи
    """
    keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data="cancel_task")]]
    return InlineKeyboardMarkup(keyboard)

async def task_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Сохранение названия задачи и запрос описания
    """
    context.user_data['task_title'] = update.message.text
    
    reply_markup = create_description_keyboard()
    await update.message.reply_text(
        "Отлично! Теперь введите описание задачи\n"
        "или нажмите кнопку «Пропустить»:",
        reply_markup=reply_markup
    )
    return DESCRIPTION

async def skip_description_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработка нажатия кнопки пропуска описания
    """
    query = update.callback_query
    await query.answer()
    
    context.user_data['task_description'] = ""
    reply_markup = create_date_keyboard()
    
    await query.edit_message_text(
        "📅 Выберите дату выполнения задачи:",
        reply_markup=reply_markup
    )
    return DUE_DATE

async def task_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Сохранение описания задачи и запрос срока выполнения
    """
    context.user_data['task_description'] = update.message.text
    reply_markup = create_date_keyboard()
    await update.message.reply_text(
        "📅 Выберите дату выполнения задачи:", 
        reply_markup=reply_markup
    )
    return DUE_DATE