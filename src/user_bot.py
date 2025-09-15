"""Модуль пользовательского бота"""

import logging
from telegram.ext import Application

logger = logging.getLogger(__name__)

class UserBot:
    """Класс для управления пользовательским ботом"""

    def __init__(self, token: str):
        """
        Инициализация бота
        
        Args:
            token (str): Токен бота от BotFather
        """
        from src.handlers.user_bot.bot import setup_user_bot
        self.application = Application.builder().token(token).build()
        setup_user_bot(self.application)