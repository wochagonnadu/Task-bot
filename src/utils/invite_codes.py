"""
Утилиты для работы с инвайт-кодами
"""
import random
import string
import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple

from src.database.db import db
from src.database.models import User, Invitation

logger = logging.getLogger(__name__)

async def generate_invite_code() -> Tuple[str, datetime]:
    """
    Генерирует случайный 6-значный код и дату его истечения
    
    Returns:
        Tuple[str, datetime]: Кортеж из кода и даты истечения
    """
    # Генерируем код из 6 цифр
    while True:
        code = ''.join(random.choices(string.digits, k=6))
        # Проверяем, что такой код еще не существует
        existing_code = await db.get_by_field(Invitation, 'code', code)
        if not existing_code:
            break
    # Код действует 24 часа
    expires_at = datetime.utcnow() + timedelta(days=1)
    return code, expires_at

async def save_invite_code(code: str, expires_at: datetime) -> None:
    """
    Сохраняет сгенерированный код в базе данных
    
    Args:
        code (str): Сгенерированный код
        expires_at (datetime): Дата истечения кода
    """
    try:
        # Создаем приглашение
        await db.create(Invitation, code=code, expires_at=expires_at)
    except Exception as e:
        logger.error(f"Ошибка при сохранении кода: {e}", exc_info=True)
        raise Exception(f"Ошибка при сохранении кода: {e}")

async def validate_invite_code(code: str, telegram_id: int) -> Optional[User]:
    """
    Проверяет валидность инвайт-кода и создает пользователя
    
    Args:
        code (str): Код для проверки
        telegram_id (int): Telegram ID пользователя

    Returns:
        Optional[User]: Объект пользователя если код валиден, иначе None
    """
    try:
        # Проверяем, существует ли уже пользователь
        existing_user = await db.get_by_field(User, 'telegram_id', telegram_id)
        if existing_user:
            logger.warning(f"Пользователь с telegram_id={telegram_id} уже существует")
            return None
            
        # Ищем код в базе
        invitation = await db.get_by_field(Invitation, 'code', code)
        
        if not invitation:
            logger.warning(f"Код {code} не найден")
            return None
            
        # Проверяем срок действия
        if invitation.expires_at < datetime.utcnow():
            logger.warning(f"Код {code} истек")
            return None
            
        if invitation.is_used:
            logger.warning(f"Код {code} уже использован")
            return None
            
        # Создаем нового пользователя
        user = await db.create(User, 
            telegram_id=telegram_id,
            role='user'
        )
        logger.info(f"Создан новый пользователь: telegram_id={telegram_id}")
        
        # Отмечаем код как использованный
        invitation.is_used = True
        await db.update(Invitation, invitation.id, is_used=True)
        logger.info(f"Код {code} помечен как использованный")
        
        return user
        
    except Exception as e:
        logger.error(f"Ошибка при проверке кода: {e}", exc_info=True)
        raise Exception(f"Ошибка при проверке кода: {e}")

def is_code_expired(expires_at: datetime) -> bool:
    """
    Проверяет, истек ли срок действия кода
    
    Args:
        expires_at (datetime): Дата истечения кода

    Returns:
        bool: True если код истек, False если еще действителен
    """
    return expires_at < datetime.utcnow()