"""
Модуль обработчиков callback-запросов для административного бота.
Экспортирует все обработчики для использования в других модулях.
"""

from .tasks import handle_tasks_callback
from .clients import (
    handle_clients_callback,
    handle_client_name_input,
    ENTER_CLIENT_NAME
)
from .projects import (
    handle_projects_callback,
    handle_project_name_input,
    ENTER_PROJECT_NAME
)
from .employees import handle_employees_callback
from .reports import handle_reports_callback
from .utils import format_tasks_list, sort_tasks

__all__ = [
    # Task handlers
    'handle_tasks_callback',
    
    # Client handlers
    'handle_clients_callback',
    'handle_client_name_input',
    'ENTER_CLIENT_NAME',
    
    # Project handlers
    'handle_projects_callback',
    'handle_project_name_input',
    'ENTER_PROJECT_NAME',
    
    # Employee handlers
    'handle_employees_callback',
    
    # Report handlers
    'handle_reports_callback',
    
    # Utilities
    'format_tasks_list',
    'sort_tasks'
]