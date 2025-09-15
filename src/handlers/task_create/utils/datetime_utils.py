"""
Утилиты для работы с датой и временем
"""
from datetime import datetime, timedelta

def get_next_workdays(count=6):
    """
    Получение следующих count рабочих дней

    Args:
        count (int): Количество рабочих дней для получения

    Returns:
        list[datetime]: Список дат рабочих дней
    """
    workdays = []
    current_date = datetime.now()
    while len(workdays) < count:
        current_date += timedelta(days=1)
        # 5 = суббота, 6 = воскресенье
        if current_date.weekday() not in [5, 6]:
            workdays.append(current_date)
    return workdays