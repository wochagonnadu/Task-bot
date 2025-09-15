"""
Базовые клавиатуры для создания задачи
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_description_keyboard() -> InlineKeyboardMarkup:
    """
    Создание клавиатуры для этапа ввода описания задачи

    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопками пропуска и отмены
    """
    keyboard = [
        [InlineKeyboardButton("⏭ Пропустить", callback_data="skip_description")],
        [InlineKeyboardButton("❌ Отмена", callback_data="cancel_task")]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_confirmation_keyboard() -> InlineKeyboardMarkup:
    """
    Создание клавиатуры для подтверждения создания задачи

    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопками подтверждения/отмены
    """
    keyboard = [
        [
            InlineKeyboardButton("✅ Подтвердить", callback_data="confirm_task"),
            InlineKeyboardButton("❌ Отменить", callback_data="cancel_task")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_task_list_keyboard() -> InlineKeyboardMarkup:
    """
    Создание клавиатуры с кнопкой возврата к списку задач

    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопкой возврата к списку
    """
    keyboard = [
        [InlineKeyboardButton("📋 К списку задач", callback_data="my_tasks")]
    ]
    return InlineKeyboardMarkup(keyboard)