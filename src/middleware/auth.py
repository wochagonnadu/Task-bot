"""
Middleware для аутентификации пользователей
"""
from typing import Optional, Dict, Any
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from sqlalchemy import select
import logging

from src.database.db import db
from src.database.models import User
from src.utils.invite_codes import validate_invite_code

logger = logging.getLogger(__name__)

import os

# Состояния для ConversationHandler
ENTER_INVITE_CODE = 1
ENTER_MASTER_KEY = 2

# Callback data для кнопок
CALLBACK_ENTER_CODE = "enter_invite_code"
CALLBACK_ENTER_MASTER_KEY = "enter_master_key"

# Мастер-ключ из переменной окружения
MASTER_KEY = os.getenv("MASTER_KEY")

class AuthMiddleware:
    """Middleware для проверки авторизации пользователей"""
    
    def __init__(self, bot_type: str = 'user'):
        """
        Инициализация middleware
        
        Args:
            bot_type: Тип бота ('user' или 'admin')
        """
        self.bot_type = bot_type
    
    async def __call__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Проверяет права доступа пользователя
        
        Args:
            update: Объект обновления
            context: Контекст бота
            
        Returns:
            bool: True если доступ разрешен, False если нет
        """
        if not update.effective_user:
            return False
            
        user_id = update.effective_user.id
        
        # Проверка в БД
        user = await self.get_user(user_id)
        if not user:
            if update.message:
                if self.bot_type == 'admin':
                    # Send welcome message first
                    if update.message.text == "/start":
                        from src.handlers.admin_bot.constants import WELCOME_MESSAGE
                        await update.message.reply_text(WELCOME_MESSAGE)
                        
                    keyboard = InlineKeyboardMarkup([[
                        InlineKeyboardButton("🔑 Ввести мастер-ключ", callback_data=CALLBACK_ENTER_MASTER_KEY)
                    ]])
                    await update.message.reply_text(
                        "⛔️ Доступ запрещен. Требуется ввести мастер-ключ.",
                        reply_markup=keyboard
                    )
                    return ENTER_MASTER_KEY
                else:
                    # Создаем клавиатуру с кнопкой для ввода кода
                    keyboard = InlineKeyboardMarkup([[
                        InlineKeyboardButton("🔑 Ввести код", callback_data=CALLBACK_ENTER_CODE)
                    ]])
                    
                    await update.message.reply_text(
                        "⛔️ Доступ запрещен. Обратитесь к администратору для получения доступа.",
                        reply_markup=keyboard
                    )
            return False
            
        # Проверка доступа к admin_bot
        if self.bot_type == 'admin' and user.role != 'admin':
            if update.message:
                await update.message.reply_text(
                    "⛔️ У вас нет прав для использования админ-бота"
                )
            return False
            
        # Сохраняем объект пользователя в контексте
        context.user_data['db_user'] = user
        return True

    async def get_user(self, telegram_id: int) -> Optional[User]:
        """
        Получение пользователя из БД
        
        Args:
            telegram_id: Telegram ID пользователя
            
        Returns:
            Optional[User]: Объект пользователя или None
        """
        await db.fix_users_sequence()  # Исправляем автоинкремент перед запросом пользователя
        stmt = select(User).where(User.telegram_id == telegram_id)
        async for session in db.get_session():
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            return user

async def handle_invite_code_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик нажатия кнопки 'Ввести код'"""
    query = update.callback_query
    logger.info(f"Получен callback для ввода кода: data={query.data}")
    
    await query.answer()
    
    await query.message.edit_text(
        "Введите код приглашения:",
        reply_markup=None
    )
    return ENTER_INVITE_CODE

async def handle_invite_code_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик ввода кода приглашения"""
    if not update.message or not update.message.text:
        return ConversationHandler.END
        
    code = update.message.text.strip()
    telegram_id = update.effective_user.id
    logger.info(f"Получен код приглашения от пользователя {telegram_id}: {code}")
    
    try:
        # Проверяем код
        user = await validate_invite_code(code, telegram_id)
        
        if user:
            # Код верный, обновляем данные пользователя
            user.username = update.effective_user.username
            user.full_name = update.effective_user.full_name
            await db.update(User, user.id, 
                role='user',
                username=update.effective_user.username,
                full_name=update.effective_user.full_name
            )
            logger.info(f"Пользователь {telegram_id} успешно активирован")
            
            await update.message.reply_text(
                "✅ Код принят! Теперь у вас есть доступ к боту.\n"
                "Используйте /start для начала работы."
            )
        else:
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("🔄 Попробовать снова", callback_data=CALLBACK_ENTER_CODE)
            ]])
            logger.warning(f"Неверный код от пользователя {telegram_id}: {code}")
            
            await update.message.reply_text(
                "❌ Неверный код или срок его действия истек.",
                reply_markup=keyboard
            )
            
    except Exception as e:
        logger.error(f"Ошибка при проверке кода: {e}", exc_info=True)
        await update.message.reply_text(
            "❌ Произошла ошибка при проверке кода. Попробуйте позже."
        )
    
    return ConversationHandler.END

async def cancel_invite_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена ввода кода"""
    await update.message.reply_text(
        "Ввод кода отменен. Используйте /start для новой попытки."
    )
    return ConversationHandler.END

async def handle_master_key_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик нажатия кнопки 'Ввести мастер-ключ'"""
    query = update.callback_query
    logger.info(f"Получен callback для ввода мастер-ключа: data={query.data}")
    
    await query.answer()
    await query.message.edit_text(
        "Введите мастер-ключ:",
        reply_markup=None
    )
    return ENTER_MASTER_KEY

async def handle_master_key_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик ввода мастер-ключа для админского бота"""
    if not update.message or not update.message.text or not MASTER_KEY:
        return ConversationHandler.END
        
    key = update.message.text.strip()
    telegram_id = update.effective_user.id
    
    try:
        if key == MASTER_KEY:
            # Проверяем существует ли уже пользователь
            user = await AuthMiddleware().get_user(telegram_id)
            if user:
                # Обновляем роль существующего пользователя
                await db.update(User, user.id, role='admin')
            else:
                # Создаем нового пользователя с правами админа
                async for session in db.get_session():
                    user = User(
                        telegram_id=telegram_id,
                        username=update.effective_user.username,
                        full_name=update.effective_user.full_name,
                        role='admin'
                    )
                    session.add(user)
                    await session.commit()
                
            logger.info(f"Администратор {telegram_id} успешно активирован")
            
            await update.message.reply_text(
                "✅ Мастер-ключ принят! Теперь у вас есть доступ к админ-боту.\n"
                "Используйте /start для начала работы."
            )
        else:
            logger.warning(f"Неверный мастер-ключ от пользователя {telegram_id}")
            await update.message.reply_text(
                "❌ Неверный мастер-ключ. Попробуйте еще раз:"
            )
            return ENTER_MASTER_KEY
            
    except Exception as e:
        logger.error(f"Ошибка при проверке мастер-ключа: {e}", exc_info=True)
        await update.message.reply_text(
            "❌ Произошла ошибка при проверке ключа. Попробуйте позже."
        )
    
    return ConversationHandler.END
