"""
Клавиатуры для выбора исполнителя задачи
"""
from typing import List, Dict
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_executor_keyboard(executors: List[Dict[str, any]]) -> InlineKeyboardMarkup:
    """
    Создание клавиатуры с исполнителями и кнопкой 'Отмена'

    Args:
        executors: Список словарей с данными исполнителей {id: int, name: str}

    Returns:
        InlineKeyboardMarkup: Клавиатура с исполнителями
    """
    keyboard = []
    row = []
    
    # Добавляем исполнителей по 2 в ряд
    for executor in executors:
        btn = InlineKeyboardButton(
            f"👤 {executor['name']}",
            callback_data=f"select_executor_{executor['id']}"
        )
        row.append(btn)
        if len(row) == 2:
            keyboard.append(row)
            row = []
    
    if row:  # Добавляем оставшиеся кнопки
        keyboard.append(row)
    
    # Добавляем кнопку отмены
    keyboard.append([
        InlineKeyboardButton(
            "❌ Отмена",
            callback_data="cancel_executor"
        )
    ])
    
    return InlineKeyboardMarkup(keyboard)