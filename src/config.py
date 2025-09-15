"""Конфигурация приложения"""
import os
from datetime import time
from dataclasses import dataclass
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

@dataclass
class Config:
    """Класс конфигурации"""
    admin_bot_token: str
    user_bot_token: str
    database_url: str
    work_start_time: time = time(9, 30)
    work_end_time: time = time(17, 30)
    datetime_format: str = "%Y-%m-%d %H:%M"  # Формат для парсинга даты и времени

def get_config() -> Config:
    """Получение конфигурации приложения"""
    admin_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    user_bot_token = os.getenv('USER_TELEGRAM_BOT_TOKEN')
    database_url = os.getenv('DATABASE_URL')  # Убираем хардкод localhost

    if not admin_bot_token:
        raise ValueError("❌ Не установлен TELEGRAM_BOT_TOKEN")
    if not user_bot_token:
        raise ValueError("❌ Не установлен USER_TELEGRAM_BOT_TOKEN")
    if not database_url:
        raise ValueError("❌ Не установлен DATABASE_URL")

    return Config(
        admin_bot_token=admin_bot_token,
        user_bot_token=user_bot_token,
        database_url=database_url
    )

# Статусы задач
TASK_STATUSES = {
    'not_started': 'Не начата',
    'in_progress': 'В работе',
    'completed': 'Завершена',
    'postponed': 'Отложена'
}

# Роли пользователей
USER_ROLES = {
    'admin': 'Администратор',
    'user': 'Пользователь'
}

# Настройки уведомлений для пользовательского бота
USER_BOT_NOTIFICATIONS = {
    'task_assigned': '👋 Вам назначена новая задача:\n{task_info}',
    'morning_tasks': '🌅 Доброе утро! Ваши задачи на сегодня:\n{tasks_list}',
    'evening_reminder': '🌆 Не забудьте завершить учет времени по сегодняшним задачам!',
    'deadline_reminder': '⚠️ Напоминание: срок выполнения задачи "{task_title}" истекает {due_date}',
}

WORK_START_TIME = os.getenv("WORK_START_TIME", "09:30")
WORK_END_TIME = os.getenv("WORK_END_TIME", "17:30")
