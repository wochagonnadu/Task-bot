"""Основной обработчик callback-запросов"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from .task_details_callback import view_task_details, get_task_and_check_access
from .task_status_callback import handle_start_task, handle_complete_task

logger = logging.getLogger(__name__)

async def handle_task_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик callback-запросов для управления задачами"""
    if not update.callback_query:
        return
        
    query = update.callback_query
    await query.answer()  # Отвечаем на callback-запрос

    try:
        data = query.data
        logger.info(f"Получен callback с данными: {data}")
        
        if data == "my_tasks":  # Вернуться к списку задач
            from .task_list import update_task_message
            await update_task_message(query, update.effective_user.id)
            return

        # Разбираем callback_data и получаем задачу
        try:
            action, task_id = data.split('_task_')
            logger.info(f"Разбор callback: action={action}, task_id={task_id}")
            
            if not task_id.isdigit():
                logger.warning(f"Некорректный ID задачи: {task_id}")
                await query.message.reply_text("❌ Некорректный ID задачи.")
                return

            # Получаем задачу и проверяем доступ
            result = await get_task_and_check_access(query, int(task_id))
            if result is None:
                return

            task, user = result

            # Обрабатываем действие
            if action == "view":
                await view_task_details(query, task)
            elif action == "start":
                await handle_start_task(query, task)
            elif action == "complete":
                await handle_complete_task(query, task)
            else:
                logger.warning(f"Неизвестное действие: {action}")
                await query.message.reply_text("❌ Неизвестное действие.")

        except ValueError:
            logger.error(f"Ошибка при разборе callback данных: {data}")
            await query.message.reply_text("❌ Некорректный формат callback данных.")
            return

    except Exception as e:
        logger.error(f"Ошибка при обработке callback-запроса: {e}", exc_info=True)
        await query.message.reply_text(
            "❌ Произошла ошибка при выполнении действия. Попробуйте позже."
        )