"""Функции создания клавиатур для пользовательского бота"""

from typing import List
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from src.database.models import Task
from .constants import (
    START_TASK,
    COMPLETE_TASK
)

def create_main_keyboard() -> ReplyKeyboardMarkup:
    """Создает основную клавиатуру с командами"""
    keyboard = [
        [KeyboardButton("📋 Мои задачи"),
         KeyboardButton("➕ Новая задача")],
        [KeyboardButton("❔ Помощь")]
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

def create_tasks_keyboard(tasks: List[Task]) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру со списком задач, где каждая строка состоит из двух кнопок:
      1. Название задачи (сокращенное до 30 символов)
      2. Кнопка действия ("▶️ Начать" или "✅ Завершить" в зависимости от статуса)
    
    Args:
        tasks: Список объектов Task
    """
    keyboard = []
    
    for task in tasks:
        # Форматируем название задачи с ограничением в 30 символов и добавляем эмодзи в зависимости от статуса
        status_emoji = "🔄" if task.status == "in_progress" else "⭕️"
        task_name = f"{status_emoji} {task.title[:30]}{'...' if len(task.title) > 30 else ''}"
        
        # Определяем текст и callback для кнопки действия
        if task.status == 'not_started':
            action_text = "▶️ Начать"
            action_callback = START_TASK.format(task_id=task.id)
        else:  # in_progress
            action_text = "✅ Завершить"
            action_callback = COMPLETE_TASK.format(task_id=task.id)
        
        # Добавляем строку с двумя кнопками: название задачи и кнопка действия
        keyboard.append([
            InlineKeyboardButton(task_name, callback_data=f"view_task_{task.id}"),
            InlineKeyboardButton(action_text, callback_data=action_callback)
        ])
    
    return InlineKeyboardMarkup(keyboard)

def create_task_control_keyboard(task: Task) -> InlineKeyboardMarkup:
    """Создает клавиатуру с кнопками управления задачей"""
    keyboard = []
    
    if task.status == 'not_started':
        keyboard.append([
            InlineKeyboardButton(
                "▶️ Начать работу",
                callback_data=START_TASK.format(task_id=task.id)
            )
        ])
    elif task.status == 'in_progress':
        keyboard.append([
            InlineKeyboardButton(
                "✅ Завершить задачу",
                callback_data=COMPLETE_TASK.format(task_id=task.id)
            )
        ])
    
    # Кнопка возврата к списку всегда присутствует
    keyboard.append([
        InlineKeyboardButton(
            "📋 К списку задач",
            callback_data="my_tasks"
        )
    ])
    
    return InlineKeyboardMarkup(keyboard)