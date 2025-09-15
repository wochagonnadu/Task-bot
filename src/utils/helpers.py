from datetime import datetime, time, timedelta
from typing import Optional, Tuple
from src.config import get_config

# Получаем конфигурацию
config = get_config()

def is_work_time(current_time: Optional[time] = None) -> bool:
    """
    Проверяет, является ли текущее время рабочим
    """
    if current_time is None:
        current_time = datetime.now().time()
    return config.work_start_time <= current_time <= config.work_end_time

def get_effective_work_time(start_time: datetime, end_time: datetime) -> int:
    """
    Рассчитывает эффективное рабочее время в минутах между двумя датами
    Учитывает только время в рабочие часы
    """
    if start_time > end_time:
        return 0

    total_minutes = 0
    current = start_time

    while current < end_time:
        if is_work_time(current.time()):
            total_minutes += 1
        current += timedelta(minutes=1)

    return total_minutes

def format_datetime(dt: datetime) -> str:
    """
    Форматирует дату и время согласно настройкам
    """
    return dt.strftime(config.datetime_format)

def format_date(dt: datetime) -> str:
    """
    Форматирует только дату согласно настройкам
    """
    return dt.strftime(config.date_format)

def format_time(dt: datetime) -> str:
    """
    Форматирует только время согласно настройкам
    """
    return dt.strftime(config.time_format)

def parse_datetime(datetime_str: str) -> Optional[datetime]:
    """
    Парсит строку даты и времени в datetime объект
    Поддерживает форматы:
    - DD.MM.YYYY HH:MM
    - YYYY-MM-DD HH:MM
    """
    formats = [
        "%d.%m.%Y %H:%M",  # формат из клавиатуры
        "%Y-%m-%d %H:%M",  # формат из конфига
    ]
    
    for date_format in formats:
        try:
            return datetime.strptime(datetime_str, date_format)
        except ValueError:
            continue
    
    return None

def format_duration(minutes: int) -> str:
    """
    Форматирует продолжительность из минут в читаемый формат
    Пример: 122 -> "2ч 2м"
    """
    hours = minutes // 60
    remaining_minutes = minutes % 60
    
    if hours > 0 and remaining_minutes > 0:
        return f"{hours}ч {remaining_minutes}м"
    elif hours > 0:
        return f"{hours}ч"
    else:
        return f"{minutes}м"

def get_status_emoji(status: str) -> str:
    """
    Возвращает эмодзи для статуса задачи
    """
    status_emoji = {
        'not_started': '🆕',
        'in_progress': '▶️',
        'completed': '✅',
        'postponed': '⏳'
    }
    return status_emoji.get(status, '❓')

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Обрезает текст до указанной длины, добавляя многоточие
    """
    if len_text := len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
