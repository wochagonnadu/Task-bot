"""
Модуль клавиатур для создания задач
"""
from .basic import (
    create_description_keyboard,
    create_confirmation_keyboard
)
from .datetime import (
    create_date_keyboard,
    create_time_keyboard
)
from .executor import create_executor_keyboard
from .client_project import (
    create_client_keyboard,
    create_project_keyboard
)

__all__ = [
    'create_description_keyboard',
    'create_confirmation_keyboard',
    'create_date_keyboard',
    'create_time_keyboard',
    'create_executor_keyboard',
    'create_client_keyboard',
    'create_project_keyboard'
]