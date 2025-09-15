"""
Модуль для обработки ошибок
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def common_error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Общий обработчик ошибок для всех ботов
    
    Args:
        update (Update): Объект обновления от Telegram
        context (ContextTypes.DEFAULT_TYPE): Контекст бота
    """
    logger.error(f"Update {update} caused error {context.error}")
    try:
        if update and update.effective_message:
            await update.message.reply_text(
                "Произошла ошибка при выполнении команды. Пожалуйста, попробуйте позже."
            )
    except Exception as e:
        logger.error(f"Ошибка в обработчике ошибок: {e}")