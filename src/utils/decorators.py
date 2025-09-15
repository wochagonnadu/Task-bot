"""Декораторы для обработчиков ботов"""

import logging
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from src.middleware.auth import AuthMiddleware

logger = logging.getLogger(__name__)

def require_auth(bot_type: str = 'user'):
    """
    Декоратор для проверки авторизации пользователя
    
    Args:
        bot_type (str): Тип бота ('user' или 'admin')
        
    Returns:
        Callable: Обертка для хендлера
    """
    def decorator(handler):
        auth_middleware = AuthMiddleware(bot_type)
        
        @wraps(handler)
        async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            logger.info(
                f"Проверка авторизации для handler={handler.__name__}, "
                f"user_id={update.effective_user.id if update.effective_user else 'None'}, "
                f"bot_type={bot_type}"
            )
            
            # Пропускаем проверку для команды отмены
            if (update.message and 
                update.message.text and 
                update.message.text.startswith('/cancel')):
                return await handler(update, context, *args, **kwargs)
            
            # Проверяем авторизацию
            is_authorized = await auth_middleware(update, context)
            if not is_authorized:
                logger.warning(
                    f"Доступ запрещен: handler={handler.__name__}, "
                    f"user_id={update.effective_user.id if update.effective_user else 'None'}"
                )
                return None
                
            logger.info(
                f"Доступ разрешен: handler={handler.__name__}, "
                f"user_id={update.effective_user.id}"
            )
            return await handler(update, context, *args, **kwargs)
            
        return wrapped
    return decorator