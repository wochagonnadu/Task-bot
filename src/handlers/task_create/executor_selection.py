"""
Модуль для работы с выбором исполнителя задачи
"""
from typing import List, Tuple
import logging

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from src.database.models import User
from src.database.db import db
from .constants import CONFIRM, SELECT_EXECUTOR
from .keyboards import create_executor_keyboard
from .task_confirmation import show_task_confirmation

logger = logging.getLogger(__name__)

async def get_available_executors() -> List[Tuple[int, str]]:
    """
    Получение списка доступных исполнителей из базы данных

    Returns:
        List[Tuple[int, str]]: Список кортежей (id, full_name) доступных исполнителей
    """
    logger.info("Получение списка доступных исполнителей")
    
    try:
        # Получаем всех пользователей из БД
        executors = await db.get_all(User)
        logger.info(f"Найдено {len(executors)} пользователей в базе данных")
        
        # Если список пустой, логируем это
        if not executors:
            logger.warning("В базе данных не найдено пользователей")
            return []
        
        # Сохраняем только необходимые данные
        result = [(user.id, (user.full_name or user.username or "Без имени")) 
                 for user in executors if user.id]
        logger.debug(f"Обработанные данные исполнителей: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Ошибка при получении списка исполнителей: {str(e)}", exc_info=True)
        return []

async def handle_executor_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработка этапа выбора исполнителя
    """
    # Получаем список доступных исполнителей
    logger.info("Запрос доступных исполнителей...")
    executors = await get_available_executors()
    logger.debug(f"Получен список исполнителей: {executors}")
    
    if not executors:
        logger.warning("Нет доступных исполнителей")
        message = (update.callback_query.message 
                  if update.callback_query 
                  else update.message)
        await message.reply_text("❌ Ошибка: нет доступных исполнителей")
        return ConversationHandler.END
    
    # Создаем список объектов для клавиатуры
    executors_data = [{"id": ex_id, "name": name} for ex_id, name in executors]
    logger.debug(f"Подготовлено {len(executors_data)} исполнителей для клавиатуры")
    
    # Создаем клавиатуру с исполнителями
    reply_markup = create_executor_keyboard(executors_data)
    
    message = (update.callback_query.message 
              if update.callback_query 
              else update.message)
    
    try:
        if update.callback_query:
            await message.edit_text(
                "👥 Выберите исполнителя задачи:",
                reply_markup=reply_markup
            )
        else:
            await message.reply_text(
                "👥 Выберите исполнителя задачи:",
                reply_markup=reply_markup
            )
        return SELECT_EXECUTOR
        
    except Exception as e:
        logger.error(f"Ошибка при отображении клавиатуры исполнителей: {str(e)}", 
                    exc_info=True)
        await message.reply_text("❌ Произошла ошибка при выборе исполнителя")
        return ConversationHandler.END

async def handle_executor_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработка выбора исполнителя через callback
    """
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    
    try:
        if callback_data == "cancel_executor":
            await query.message.edit_text("❌ Создание задачи отменено")
            return ConversationHandler.END
        
        # Извлекаем ID исполнителя из callback_data
        executor_id = int(callback_data.split('_')[2])
        
        # Получаем исполнителя из БД
        executor = await db.get(User, executor_id)
        if not executor:
            logger.warning(f"Исполнитель с ID {executor_id} не найден")
            await query.message.edit_text("⚠️ Ошибка: исполнитель не найден")
            return await handle_executor_selection(update, context)
            
        # Сохраняем ID исполнителя
        context.user_data['assignee_id'] = executor_id
        executor_name = executor.full_name or executor.username
        
        await query.message.edit_text(f"👤 Выбран исполнитель: {executor_name}")
        # Переходим к подтверждению
        return await show_task_confirmation(update, context)
            
    except Exception as e:
        logger.error(f"Ошибка при обработке выбора исполнителя: {str(e)}", 
                    exc_info=True)
        await query.message.edit_text("❌ Произошла ошибка при выборе исполнителя")
        return ConversationHandler.END