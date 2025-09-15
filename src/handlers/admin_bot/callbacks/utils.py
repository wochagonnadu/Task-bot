"""Общие утилиты для callback-обработчиков"""

from datetime import datetime
from typing import List, Optional, Dict
from sqlalchemy import and_, select

from src.database.db import db
from src.database.models import Task, User
from ..constants import EMPLOYEE_TASK_ITEM, DATE_FORMAT


def format_tasks_list(tasks: List[Task]) -> str:
    """
    Форматирует список задач для отображения

    Args:
        tasks: Список объектов Task для форматирования

    Returns:
        str: Отформатированный текст со списком задач
    """
    if not tasks:
        return "Нет задач для отображения"
    
    result = []
    for task in tasks:
        status_emoji = {
            'not_started': '⭕️',
            'in_progress': '🔄',
            'completed': '✅'
        }.get(task.status, '❓')

        # Получаем информацию об исполнителе
        assignee = db.get(User, task.assignee_id) if task.assignee_id else None
        assignee_name = assignee.full_name if assignee else "Не назначен"
        
        # Формируем строку с информацией о задаче
        task_info = (
            f"{status_emoji} {task.title}\n"
            f"ID: {task.id}\n"
            f"Исполнитель: {assignee_name}\n"
        )

        # Добавляем срок, если он указан
        if task.due_date:
            task_info += f"Срок: {task.due_date.strftime('%d.%m.%Y')}\n"

        # Добавляем клиента и проект, если они указаны
        if task.client:
            task_info += f"Клиент: {task.client.name}\n"
        if task.project:
            task_info += f"Проект: {task.project.name}\n"
        
        result.append(task_info)
    
    return "\n".join(result)


def sort_tasks(tasks: List[Task]) -> List[Task]:
    """
    Сортирует задачи по дате и статусу

    Args:
        tasks: Список задач для сортировки

    Returns:
        List[Task]: Отсортированный список задач
    """
    return sorted(
        tasks,
        key=lambda x: (
            x.due_date or datetime.max,  # None даты в конец
            # Порядок статусов: в работе -> не начато
            {'in_progress': 0, 'not_started': 1}.get(x.status, 2)
        )
    )

async def get_tasks_statistics(tasks: List[Task]) -> dict:
    """
    Получает статистику по задачам

    Args:
        tasks: Список задач для анализа

    Returns:
        dict: Словарь со статистикой {
            'total_count': int,
            'assignees_stats': {
                user_id: {
                    'name': str,
                    'count': int
                }
            }
        }
    """
    assignees_stats = {}
    
    for task in tasks:
        if task.assignee_id:
            if task.assignee_id not in assignees_stats:
                # Получаем информацию об исполнителе из БД
                assignee = await db.get(User, task.assignee_id)
                if not assignee:
                    continue
                    
                assignees_stats[task.assignee_id] = {
                    'name': assignee.full_name,
                    'count': 0
                }
            assignees_stats[task.assignee_id]['count'] += 1

    return {
        'total_count': len(tasks),
        'assignees_stats': assignees_stats
    }

def format_assignees_stats(assignees_stats: dict) -> str:
    """
    Форматирует статистику по исполнителям

    Args:
        assignees_stats: Словарь со статистикой по исполнителям

    Returns:
        str: Отформатированная строка статистики
    """
    if not assignees_stats:
        return "Нет назначенных исполнителей"
        
    # Сортируем по количеству задач (по убыванию)
    sorted_stats = sorted(
        assignees_stats.values(),
        key=lambda x: x['count'],
        reverse=True
    )
    
    return "\n".join(
        f"• {stat['name']}: {stat['count']} задач"
        for stat in sorted_stats
    )

async def get_employee_active_tasks(employee_id: int) -> List[Task]:
    """
    Получает активные задачи сотрудника (в работе и не начатые)
    
    Args:
        employee_id: ID сотрудника
        
    Returns:
        List[Task]: Список активных задач
    """
    # Используем специальный метод для получения задач со связанными данными
    tasks = await db.get_tasks_with_relations(employee_id, only_active=True)
    
    # Сортируем по дате
    return sorted(
        tasks,
        key=lambda x: x.due_date or datetime.max
    )

def format_employee_tasks(tasks: List[Task]) -> Dict[str, any]:
    """
    Форматирует список задач сотрудника и собирает статистику
    
    Args:
        tasks: Список задач для форматирования
        
    Returns:
        dict: {
            'tasks_list': str,
            'total_tasks': int,
            'in_progress_tasks': int,
            'not_started_tasks': int,
            'nearest_deadline': str
        }
    """
    # Подсчет статистики
    stats = {
        'total_tasks': len(tasks),
        'in_progress_tasks': len([t for t in tasks if t.status == 'in_progress']),
        'not_started_tasks': len([t for t in tasks if t.status == 'not_started']),
        'nearest_deadline': 'Нет'
    }
    
    # Находим ближайший дедлайн
    active_tasks = [t for t in tasks if t.due_date]
    if active_tasks:
        nearest = min(active_tasks, key=lambda x: x.due_date)
        stats['nearest_deadline'] = nearest.due_date.strftime(DATE_FORMAT)
    
    # Форматируем список задач
    tasks_list = []
    for task in tasks:
        status_emoji = '🔄' if task.status == 'in_progress' else '⭕️'
        deadline = task.due_date.strftime(DATE_FORMAT) if task.due_date else 'Не указан'
        
        tasks_list.append(EMPLOYEE_TASK_ITEM.format(
            status_emoji=status_emoji,
            title=task.title,
            deadline=deadline,
            client=task.client.name if task.client else 'Не указан',
            project=task.project.name if task.project else 'Не указан'
        ))
    
    stats['tasks_list'] = '\n'.join(tasks_list) if tasks_list else 'Нет активных задач'
    return stats