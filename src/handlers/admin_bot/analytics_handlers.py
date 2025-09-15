"""Обработчики для аналитики в админском боте"""

import logging
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from src.database.db import db
from src.database.models import Task, User, Client, Project
from .keyboards import get_tasks_keyboard  # Исправили имя импортируемой функции

logger = logging.getLogger(__name__)

async def analytics_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /analytics - показывает общую статистику"""
    try:
        # Получаем все задачи
        tasks = db.get_all(Task)
        users = db.get_all(User)
        clients = db.get_all(Client)
        projects = db.get_all(Project)

        # Расчет статистики по задачам
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.status == 'completed'])
        in_progress_tasks = len([t for t in tasks if t.status == 'in_progress'])
        not_started_tasks = len([t for t in tasks if t.status == 'not_started'])

        # Статистика по срокам
        overdue_tasks = len([t for t in tasks if t.due_date and t.due_date < datetime.now() and t.status != 'completed'])
        
        # Статистика по пользователям
        total_users = len(users)
        users_with_tasks = len(set(task.assignee_id for task in tasks if task.assignee_id))
        
        # Статистика по клиентам и проектам
        total_clients = len(clients)
        total_projects = len(projects)
        active_projects = len([p for p in projects if p.status == 'active'])

        # Формируем сообщение
        analytics_text = (
            "📊 *Общая статистика*\n\n"
            
            "*Задачи:*\n"
            f"• Всего: {total_tasks}\n"
            f"• Завершено: {completed_tasks}\n"
            f"• В работе: {in_progress_tasks}\n"
            f"• Не начато: {not_started_tasks}\n"
            f"• Просрочено: {overdue_tasks}\n\n"
            
            "*Пользователи:*\n"
            f"• Всего пользователей: {total_users}\n"
            f"• С активными задачами: {users_with_tasks}\n\n"
            
            "*Клиенты и проекты:*\n"
            f"• Клиентов: {total_clients}\n"
            f"• Всего проектов: {total_projects}\n"
            f"• Активных проектов: {active_projects}\n\n"
            
            "*Эффективность:*\n"
            f"• Процент выполнения: {(completed_tasks/total_tasks*100):.1f}%\n"
            f"• Средняя нагрузка: {(total_tasks/users_with_tasks):.1f} задач/человек\n"
        ).replace(".", "\\.")  # Экранируем точки для MarkdownV2

        # Получаем клавиатуру для фильтрации задач
        keyboard = await get_tasks_keyboard()

        await update.message.reply_text(
            analytics_text,
            parse_mode='MarkdownV2',
            reply_markup=keyboard
        )

    except Exception as e:
        logger.error(f"Ошибка при получении аналитики: {e}")
        await update.message.reply_text(
            "Произошла ошибка при получении аналитики. Пожалуйста, попробуйте позже."
        )

async def task_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /task_stats - показывает статистику по задачам"""
    try:
        now = datetime.now()
        last_month = now - timedelta(days=30)
        tasks = db.get_all(Task)

        # Статистика по последнему месяцу
        recent_tasks = [t for t in tasks if t.created_at >= last_month]
        completed_recent = len([t for t in recent_tasks if t.status == 'completed'])
        
        # Среднее время выполнения
        completed_tasks = [t for t in tasks if t.status == 'completed']
        avg_completion_time = 0
        if completed_tasks:
            completion_times = [(t.updated_at - t.created_at).days for t in completed_tasks]
            avg_completion_time = sum(completion_times) / len(completion_times)

        stats_text = (
            "📈 *Статистика по задачам*\n\n"
            
            "*За последние 30 дней:*\n"
            f"• Новых задач: {len(recent_tasks)}\n"
            f"• Завершено: {completed_recent}\n"
            f"• Эффективность: {(completed_recent/len(recent_tasks)*100):.1f}%\n\n"
            
            "*Общая статистика:*\n"
            f"• Среднее время выполнения: {avg_completion_time:.1f} дней\n"
        ).replace(".", "\\.")  # Экранируем точки для MarkdownV2

        # Получаем клавиатуру для фильтрации задач
        keyboard = await get_tasks_keyboard()

        await update.message.reply_text(
            stats_text,
            parse_mode='MarkdownV2',
            reply_markup=keyboard
        )

    except Exception as e:
        logger.error(f"Ошибка при получении статистики задач: {e}")
        await update.message.reply_text(
            "Произошла ошибка при получении статистики. Пожалуйста, попробуйте позже."
        )

def setup_analytics_handlers(application: Application) -> None:
    """Настройка обработчиков для аналитики"""
    application.add_handler(CommandHandler("analytics", analytics_command))
    application.add_handler(CommandHandler("task_stats", task_stats_command))