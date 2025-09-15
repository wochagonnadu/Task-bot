"""
Клавиатуры для выбора клиента и проекта
"""
from typing import List, Dict

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from ..constants import (
    CALLBACK_NEW_CLIENT,
    CALLBACK_SELECT_CLIENT,
    CALLBACK_NEW_PROJECT,
    CALLBACK_SELECT_PROJECT
)

def create_client_keyboard(clients: List[Dict[str, any]]) -> InlineKeyboardMarkup:
    """
    Создание клавиатуры со списком клиентов и кнопкой создания нового

    Args:
        clients: Список словарей с данными клиентов (id и name)

    Returns:
        InlineKeyboardMarkup: Клавиатура со списком клиентов
    """
    keyboard = []
    row = []
    
    # Добавляем клиентов по 2 в ряд
    for client in clients:
        btn = InlineKeyboardButton(
            f"👥 {client['name']}",
            callback_data=f"{CALLBACK_SELECT_CLIENT}{client['id']}"
        )
        row.append(btn)
        if len(row) == 2:
            keyboard.append(row)
            row = []
    
    if row:  # Добавляем оставшиеся кнопки
        keyboard.append(row)
    
    # Добавляем кнопки создания нового клиента и отмены
    keyboard.extend([
        [
            InlineKeyboardButton(
                "➕ Создать нового клиента",
                callback_data=CALLBACK_NEW_CLIENT
            )
        ],
        [
            InlineKeyboardButton(
                "❌ Отмена",
                callback_data="cancel_task"
            )
        ]
    ])
    
    return InlineKeyboardMarkup(keyboard)

def create_project_keyboard(projects: List[Dict[str, any]]) -> InlineKeyboardMarkup:
    """
    Создание клавиатуры со списком проектов и кнопкой создания нового

    Args:
        projects: Список словарей с данными проектов (id и name)

    Returns:
        InlineKeyboardMarkup: Клавиатура со списком проектов
    """
    keyboard = []
    row = []
    
    # Добавляем проекты по 2 в ряд
    for project in projects:
        btn = InlineKeyboardButton(
            f"📁 {project['name']}",
            callback_data=f"{CALLBACK_SELECT_PROJECT}{project['id']}"
        )
        row.append(btn)
        if len(row) == 2:
            keyboard.append(row)
            row = []
    
    if row:  # Добавляем оставшиеся кнопки
        keyboard.append(row)
    
    # Добавляем кнопки создания нового проекта и отмены
    keyboard.extend([
        [
            InlineKeyboardButton(
                "➕ Создать новый проект",
                callback_data=CALLBACK_NEW_PROJECT
            )
        ],
        [
            InlineKeyboardButton(
                "❌ Отмена",
                callback_data="cancel_task"
            )
        ]
    ])
    
    return InlineKeyboardMarkup(keyboard)