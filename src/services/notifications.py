import os
import logging
import re
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram import Bot
from src.database.db import db
from src.database.models import User, Task

# Telegram Bot instance для user_bot
user_bot = None

# Настройка логирования
logger = logging.getLogger(__name__)

# Загружаем время уведомлений из .env
WORK_START_TIME = os.getenv("WORK_START_TIME", "09:30")
WORK_END_TIME = os.getenv("WORK_END_TIME", "17:30")

def init_notifications(bot_instance: Bot):
    """Инициализация глобального bot instance для уведомлений"""
    global user_bot
    user_bot = bot_instance

def escape_markdown(text: str) -> str:
    """
    Экранирует специальные символы для MarkdownV2
    """
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f"\\{char}")
    return text

async def send_task_assignment_notification(task_id: int):
    """Отправляет мгновенное уведомление исполнителю о назначении задачи"""
    if not user_bot:
        logger.error("User bot not initialized for notifications")
        return
        
    try:
        # Получаем задачу
        task = await db.get(Task, task_id)
        if not task or not task.assignee_id or task.creator_id == task.assignee_id:
            return

        # Получаем исполнителя
        assignee = await db.get(User, task.assignee_id)
        if not assignee or not assignee.telegram_id:
            return

        # Экранируем специальные символы в заголовке задачи
        task_title = escape_markdown(task.title)
        due_date = escape_markdown(task.due_date.strftime('%d.%m.%Y'))
        
        message_text = (
            "📋 Вам назначена новая задача\\!\n"
            f"🔹 *Задача*: {task_title}\n"
            f"📅 *Срок*: {due_date}"
        )

        await user_bot.send_message(
            chat_id=assignee.telegram_id,
            text=message_text,
            parse_mode="MarkdownV2"
        )
        logger.info(f"Уведомление о назначении задачи отправлено пользователю {assignee.id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления о назначении задачи: {e}")

async def send_task_notifications(bot: Bot):
    """Отправляет пользователям уведомления о задачах со статусами 'not_started' и 'in_progress'."""
    users = await db.get_all(User)  # Получаем всех пользователей

    for user in users:
        if not user.telegram_id:
            continue  # Пропускаем пользователей без Telegram ID

        # Получаем задачи пользователя
        tasks = await db.get_all(
            Task,
            assignee_id=user.id,
            status=["not_started", "in_progress"]
        )

        if not tasks:
            continue  # У пользователя нет задач для напоминания

        # Формируем список задач для уведомления
        task_list = "\n".join(
            [f"📌 {task.title} (до {task.due_date.strftime('%d.%m.%Y')})" for task in tasks]
        )

        message = f"📢 У вас есть задачи в работе:\n\n{task_list}"

        try:
            await bot.send_message(
                chat_id=user.telegram_id,
                text=message
            )
            logger.info(f"Уведомление отправлено пользователю {user.id}")
        except Exception as e:
            logger.error(f"Ошибка при отправке уведомления {user.id}: {e}")

def start_scheduler(bot):
    """Запускает планировщик уведомлений"""
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")  # Указываем МСК

    # Планируем отправку уведомлений
    hour_start, minute_start = map(int, WORK_START_TIME.split(":"))
    hour_end, minute_end = map(int, WORK_END_TIME.split(":"))

    scheduler.add_job(
        send_task_notifications,
        trigger=CronTrigger(hour=hour_start, minute=minute_start),
        args=[bot],
        id="morning_notifications",
        replace_existing=True,
    )

    scheduler.add_job(
        send_task_notifications,
        trigger=CronTrigger(hour=hour_end, minute=minute_end),
        args=[bot],
        id="evening_notifications",
        replace_existing=True,
    )

    scheduler.start()
    print("✅ Планировщик уведомлений запущен")
