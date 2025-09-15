"""
DEPRECATED: Этот модуль сохранен для обратной совместимости.
Используйте прямые импорты из callbacks.* вместо этого модуля.
"""

from .callbacks import (
    # Task handlers
    handle_tasks_callback,
    
    # Client handlers
    handle_clients_callback,
    handle_client_name_input,
    ENTER_CLIENT_NAME,
    
    # Project handlers
    handle_projects_callback,
    handle_project_name_input,
    ENTER_PROJECT_NAME,
    
    # Employee handlers
    handle_employees_callback,
    
    # Report handlers
    handle_reports_callback,
    
    # Utilities
    format_tasks_list,
    sort_tasks
)

__all__ = [
    'handle_tasks_callback',
    'handle_clients_callback',
    'handle_client_name_input',
    'ENTER_CLIENT_NAME',
    'handle_projects_callback',
    'handle_project_name_input',
    'ENTER_PROJECT_NAME',
    'handle_employees_callback',
    'handle_reports_callback',
    'format_tasks_list',
    'sort_tasks'
]