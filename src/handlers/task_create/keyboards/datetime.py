"""
Клавиатуры для выбора даты и времени задачи
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from ..utils import get_next_workdays

def create_date_keyboard() -> InlineKeyboardMarkup:
    """
    Создание клавиатуры с датами для выбора срока задачи

    Returns:
        InlineKeyboardMarkup: Клавиатура с датами
    """
    keyboard = []
    workdays = get_next_workdays()
    
    # Форматируем даты для отображения и callback_data
    row = []
    for date in workdays:
        display_date = date.strftime("%d.%m")
        callback_date = date.strftime("%d.%m.%Y")
        btn = InlineKeyboardButton(
            f"📅 {display_date}",
            callback_data=f"date_{callback_date}"
        )
        row.append(btn)
        if len(row) == 2:  # По 2 кнопки в ряду
            keyboard.append(row)
            row = []
    
    if row:  # Добавляем оставшиеся кнопки
        keyboard.append(row)
        
    # Добавляем кнопку отмены
    keyboard.append([InlineKeyboardButton("❌ Отмена", callback_data="cancel_date")])
    return InlineKeyboardMarkup(keyboard)

def create_time_keyboard() -> InlineKeyboardMarkup:
    """
    Создание клавиатуры со временем для выбора срока задачи

    Returns:
        InlineKeyboardMarkup: Клавиатура со временем
    """
    keyboard = []
    row = []
    
    for hour in range(10, 19):
        time_str = f"{hour}:00"
        btn = InlineKeyboardButton(
            f"🕐 {time_str}",
            callback_data=f"time_{time_str}"
        )
        row.append(btn)
        if len(row) == 2:  # По 2 кнопки в ряду
            keyboard.append(row)
            row = []
            
    if row:  # Добавляем оставшиеся кнопки
        keyboard.append(row)
    
    # Добавляем кнопку отмены
    keyboard.append([InlineKeyboardButton("❌ Отмена", callback_data="cancel_time")])
    return InlineKeyboardMarkup(keyboard)