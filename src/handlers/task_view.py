import logging
from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler
)

from src.database.models import Task, User
from src.database.db import db
from src.utils.helpers import format_datetime, get_status_emoji, truncate_text

logger = logging.getLogger(__name__)

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Показ списка активных задач
    """
    try:
        is_group = update.effective_chat.type in ["group", "supergroup"]
        user = db.get_by_field(User, 'telegram_id', update.effective_user.id)
        
        if not user:
            await update.message.reply_text(
                "Для просмотра задач необходимо сначала зарегистрироваться. "
                "Используйте команду /start"
            )
            return

        if is_group:
            tasks = db.get_all(Task, status='not_started')
        else:
            # В личном чате показываем только задачи пользователя
            tasks = db.get_all(Task, creator_id=user.id, status='not_started')
        
        if not tasks:
            await update.message.reply_text(
                "Активных задач нет." if is_group else "У вас нет активных задач."
            )
            return
        
        tasks_text = "*Список активных задач:*\n\n" if is_group else "*Ваши активные задачи:*\n\n"
        for task in tasks:
            status_emoji = get_status_emoji(task.status)
            tasks_text += f"{status_emoji} ID: `{task.id}` \\- {truncate_text(task.title)}\n"
            if task.description:
                tasks_text += f"📝 {truncate_text(task.description, max_length=50)}\n"
            if task.due_date:
                tasks_text += f"⏰ Срок: {format_datetime(task.due_date)}\n"
            tasks_text += "\n"
        
        await update.message.reply_text(tasks_text, parse_mode='MarkdownV2')
        
    except Exception as e:
        logger.error(f"Ошибка при получении списка задач: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка при получении списка задач. Попробуйте позже."
        )

async def view_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Показ детальной информации о задаче
    """
    try:
        # Проверяем, передан ли ID задачи
        if not context.args:
            await update.message.reply_text(
                "❌ Не указан ID задачи.\n"
                "Используйте команду в формате: /view_task <ID задачи>"
            )
            return

        task_id = int(context.args[0])
        task = db.get_by_id(Task, task_id)

        if not task:
            await update.message.reply_text(
                "❌ Задача с указанным ID не найдена."
            )
            return

        # Получаем информацию о создателе и исполнителе
        creator = db.get_by_id(User, task.creator_id)
        assignee = db.get_by_id(User, task.assignee_id) if task.assignee_id else None

        # Формируем детальное представление задачи
        task_text = (
            f"*Информация о задаче:*\n\n"
            f"🆔 ID: `{task.id}`\n"
            f"📋 Название: {truncate_text(task.title)}\n"
        )
        if task.description:
            task_text += f"📝 Описание: {truncate_text(task.description)}\n"
        if task.due_date:
            task_text += f"⏰ Срок: {format_datetime(task.due_date)}\n"
        
        task_text += f"👤 Создатель: {creator.full_name}\n"
        if assignee:
            task_text += f"👥 Исполнитель: {assignee.full_name}\n"
        
        status_emoji = get_status_emoji(task.status)
        task_text += f"📊 Статус: {status_emoji} {task.status}\n"
        task_text += f"📅 Создано: {format_datetime(task.created_at)}\n"
        
        await update.message.reply_text(task_text, parse_mode='MarkdownV2')

    except ValueError:
        await update.message.reply_text(
            "❌ Некорректный ID задачи. ID должен быть числом."
        )
    except Exception as e:
        logger.error(f"Ошибка при просмотре задачи: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка при получении информации о задаче. Попробуйте позже."
        )

async def my_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Показ задач текущего пользователя
    """
    try:
        user = db.get_by_field(User, 'telegram_id', update.effective_user.id)
        if not user:
            await update.message.reply_text(
                "Для просмотра задач необходимо сначала зарегистрироваться. "
                "Используйте команду /start"
            )
            return

        # Получаем задачи, где пользователь является создателем или исполнителем
        created_tasks = db.get_all(Task, creator_id=user.id)
        assigned_tasks = db.get_all(Task, assignee_id=user.id)

        if not created_tasks and not assigned_tasks:
            await update.message.reply_text("У вас нет активных задач.")
            return

        tasks_text = "*Ваши задачи:*\n\n"
        
        if created_tasks:
            tasks_text += "*Созданные вами:*\n"
            for task in created_tasks:
                status_emoji = get_status_emoji(task.status)
                tasks_text += f"{status_emoji} ID: `{task.id}` \\- {truncate_text(task.title)}\n"
                if task.due_date:
                    tasks_text += f"⏰ Срок: {format_datetime(task.due_date)}\n"
                tasks_text += "\n"

        if assigned_tasks:
            tasks_text += "\n*Назначенные вам:*\n"
            for task in assigned_tasks:
                status_emoji = get_status_emoji(task.status)
                tasks_text += f"{status_emoji} ID: `{task.id}` \\- {truncate_text(task.title)}\n"
                if task.due_date:
                    tasks_text += f"⏰ Срок: {format_datetime(task.due_date)}\n"
                tasks_text += "\n"

        await update.message.reply_text(tasks_text, parse_mode='MarkdownV2')

    except Exception as e:
        logger.error(f"Ошибка при получении списка задач пользователя: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка при получении списка задач. Попробуйте позже."
        )

# Создание обработчиков команд просмотра
view_task_handler = CommandHandler('view_task', view_task)
my_tasks_handler = CommandHandler('my_tasks', my_tasks)