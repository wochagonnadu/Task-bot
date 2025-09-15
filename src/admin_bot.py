"""Модуль админского бота"""
import logging
from telegram.ext import Application

logger = logging.getLogger(__name__)

class AdminBot:
    """Класс для управления админским ботом"""

    def __init__(self, token: str):
        """
        Инициализация бота
        
        Args:
            token (str): Токен бота от BotFather
        """
        from src.handlers.admin_bot.bot import setup_admin_bot
        self.application = Application.builder().token(token).build()
        setup_admin_bot(self.application)

__all__ = ['AdminBot']