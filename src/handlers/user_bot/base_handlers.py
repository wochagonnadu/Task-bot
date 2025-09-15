"""Базовые обработчики команд пользовательского бота"""

import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from src.database.db import db
from src.database.models import User
from .constants import HELP_MESSAGE
from .keyboards import create_main_keyboard
from src.middleware.auth import CALLBACK_ENTER_CODE

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    if not update.message:
        return
        
    user = update.effective_user
    try:
        # Проверяем существование пользователя
        existing_user = await db.get_by_field(User, 'telegram_id', user.id)

        if existing_user:
            # Для существующего пользователя показываем обычное приветствие
            main_keyboard = create_main_keyboard()
            await update.message.reply_text(
                "С возвращением в Task Bot!\n\n"
                "Используйте /help для просмотра доступных команд.",
                reply_markup=main_keyboard
            )
        else:
            # Для нового пользователя показываем сообщение с кнопкой ввода кода
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("🔑 Ввести код", callback_data=CALLBACK_ENTER_CODE)
            ]])
            
            await update.message.reply_text(
                "👋 Добро пожаловать в Task Bot!\n\n"
                "⛔️ Для доступа к боту необходим код приглашения.\n"
                "Получите код у администратора и нажмите кнопку ниже.",
                reply_markup=keyboard
            )
            
    except Exception as e:
        logger.error(f"Ошибка при обработке команды /start: {e}", exc_info=True)
        await update.message.reply_text(
            "❌ Произошла ошибка. Пожалуйста, попробуйте позже."
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    if not update.message:
        return
        
    try:
        main_keyboard = create_main_keyboard()
        await update.message.reply_text(
            HELP_MESSAGE,
            parse_mode='MarkdownV2',
            reply_markup=main_keyboard
        )
    except Exception as e:
        logger.error(f"Ошибка при обработке команды /help: {e}", exc_info=True)
        await update.message.reply_text(
            "❌ Произошла ошибка. Пожалуйста, попробуйте позже."
        )