"""
Инициализация пользовательского бота
"""

from .bot import setup_user_bot
from .base_handlers import start_command, help_command
from .task_list import my_tasks
from .task_view import view_task

__all__ = [
    'setup_user_bot',
    'start_command',
    'help_command',
    'my_tasks',
    'view_task'
]