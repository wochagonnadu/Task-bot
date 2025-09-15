"""
Утилиты для форматирования сообщений при создании задачи
"""
from datetime import datetime
from src.database.models import User

def escape_markdown(text: str) -> str:
    """
    Экранирование специальных символов для MarkdownV2
    """
    if not text:
        return ""
    chars_to_escape = ['.', '-', '!', '*', '[', ']', '(', ')', '~', '>', '#', '+', '=', '|', '{', '}']
    text_str = str(text)
    for char in chars_to_escape:
        text_str = text_str.replace(char, f"\\{char}")
    return text_str

def format_task_details(
    title: str,
    description: str = "",
    due_date: datetime = None,
    executor: User = None,
    client_name: str = None,
    project_name: str = None
) -> str:
    """
    Форматирование деталей задачи для отображения
    
    Args:
        title: Название задачи
        description: Описание задачи
        due_date: Срок выполнения
        executor: Объект исполнителя
        client_name: Название клиента
        project_name: Название проекта
    """
    details = [
        "*Подтвердите создание задачи:*\n"
    ]
    
    if client_name:
        details.append(f"🏢 *Клиент:* {escape_markdown(client_name)}")
    
    if project_name:
        details.append(f"📁 *Проект:* {escape_markdown(project_name)}")
    
    details.append(f"📋 *Название:* {escape_markdown(title)}")
    
    if description:
        details.append(f"📝 *Описание:* {escape_markdown(description)}")
    
    if due_date:
        details.append(f"⏰ *Срок:* {escape_markdown(due_date.strftime('%d.%m.%Y %H:%M'))}")
    
    executor_text = "Не назначен"
    if executor:
        executor_text = executor.full_name or executor.username
    details.append(f"👤 *Исполнитель:* {escape_markdown(executor_text)}")
    
    return "\n".join(details)

def format_task_success(task_id: int, task_details: dict) -> str:
    """
    Форматирование сообщения об успешном создании задачи
    """
    success_text = [
        f"✅ *Задача успешно создана\\!*\n",
        f"🆔 ID: `{task_id}`",
        f"📋 *Название:* {escape_markdown(task_details['title'])}"
    ]
    
    if task_details.get('executor_name'):
        success_text.append(f"👤 *Исполнитель:* {escape_markdown(task_details['executor_name'])}")
    else:
        success_text.append("👤 *Исполнитель:* Не назначен")
    
    if task_details.get('due_date'):
        success_text.append(f"⏰ *Срок:* {escape_markdown(task_details['due_date'].strftime('%d.%m.%Y %H:%M'))}")
    
    success_text.append(f"📊 *Статус:* Не начата")
    
    return "\n".join(success_text)