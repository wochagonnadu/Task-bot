"""Обработчики текстовых сообщений от кнопок Reply клавиатуры"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from .task_list import my_tasks
from .base_handlers import help_command
from .keyboards import create_main_keyboard

logger = logging.getLogger(__name__)

async def handle_button_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений от кнопок"""
    message_text = update.message.text
    
    try:
        if message_text == "📋 Мои задачи":
            await my_tasks(update, context)
            
        # Убираем обработку "➕ Новая задача", так как теперь это обрабатывается через ConversationHandler
            
        elif message_text == "❔ Помощь":
            await help_command(update, context)
            
    except Exception as e:
        logger.error(f"Ошибка при обработке кнопки: {e}", exc_info=True)
        await update.message.reply_text(
            "❌ Произошла ошибка при обработке команды. Попробуйте позже.",
            reply_markup=create_main_keyboard()
        )