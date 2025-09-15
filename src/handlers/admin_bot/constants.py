# Константы для админского бота

# Текст для кнопок главного меню
BUTTON_TASKS = "📋 Задачи"
BUTTON_CLIENTS = "👥 Клиенты"
BUTTON_PROJECTS = "📊 Проекты" 
BUTTON_EMPLOYEES = "👤 Сотрудники"
BUTTON_NEW_TASK = "➕ Новая задача"
BUTTON_REPORTS = "📈 Отчеты"

# Заголовки разделов (для inline keyboard)
TASKS_MENU_MESSAGE = "Выберите категорию задач:"
CLIENTS_MENU_MESSAGE = "Выберите действие:"
PROJECTS_MENU_MESSAGE = "Всего проектов:"
EMPLOYEES_MENU_MESSAGE = "Ваши пчелки:"
REPORTS_MENU_MESSAGE = "Выберите период отчета:"

# Callback data для inline кнопок
# Задачи
CALLBACK_TASKS_ALL = "tasks_all"
CALLBACK_TASKS_ACTIVE = "tasks_active"
CALLBACK_TASKS_COMPLETED = "tasks_completed"
CALLBACK_TASKS_NOT_STARTED = "tasks_not_started"

# Клиенты
CALLBACK_CLIENT_PREFIX = "client_"
CALLBACK_CLIENT_ADD = "client_add"

# Проекты
CALLBACK_PROJECT_PREFIX = "project_"
CALLBACK_PROJECT_ADD = "project_add"

# Сотрудники
CALLBACK_EMPLOYEE_PREFIX = "employee_"
CALLBACK_EMPLOYEE_ADD = "employee_add"

# Отчеты
CALLBACK_REPORT_WEEK = "report_week"
CALLBACK_REPORT_MONTH = "report_month"
CALLBACK_REPORT_QUARTER = "report_quarter"
CALLBACK_REPORT_YEAR = "report_year"

# Периоды отчетов
REPORT_PERIODS = {
    'week': '📊 За неделю',
    'month': '📈 За месяц',
    'quarter': '📋 За квартал',
    'year': '📅 За год'
}

# Основные сообщения
WELCOME_MESSAGE = "Добро пожаловать в панель администратора!"
HELP_MESSAGE = """Доступные команды:
/start - Запустить бота
/help - Показать это сообщение
/new_task - Создать новую задачу"""

# Статусы задач
TASK_STATUSES = {
    'not_started': '⭕️ Не начата',
    'in_progress': '🔄 В работе',
    'completed': '✅ Завершена'
}

# Сообщения для задач
TASK_LIST_MESSAGE = """
📋 *Список задач*

{tasks_list}

*Статистика:*
• Всего задач: {total_count}
• В работе: {in_progress_count}
• Не начато: {not_started_count}
• Завершено: {completed_count}
"""

ADMIN_TASK_LIST_ITEM = """
*{title}*
👤 Исполнитель: {assignee}
📊 Статус: {status}
⏰ Срок: {deadline}
🏢 Клиент: {client}
📂 Проект: {project}
"""

ADMIN_TASK_DETAIL_MESSAGE = """
📋 *Детали задачи*

*{title}*
ID: {id}
👤 Исполнитель: {assignee}
📊 Статус: {status}
⏰ Срок: {deadline}
🏢 Клиент: {client}
📂 Проект: {project}

📝 Описание:
{description}
"""

# Действия с задачами
ASSIGN_TASK = "assign_task"
EDIT_TASK = "edit_task"
DELETE_TASK = "delete_task"
SHOW_TASK_DETAILS = "show_task"

# Сообщения для отчетов
CLIENT_LIST_MESSAGE = """
👥 *Список клиентов*

{clients_list}

*Всего клиентов:* {total_count}
*Активных проектов:* {active_projects_count}
"""

PROJECT_LIST_MESSAGE = """
📊 *Список проектов*

{projects_list}

*Всего проектов:* {total_count}
*Активных:* {active_count}
*Завершенных:* {completed_count}
"""

# Сообщения статистики задач
TASK_STATS_MESSAGE = """
{filter_emoji} *{filter_name} задачи*

*Всего задач:* {total_count}

👥 *По исполнителям:*
{assignees_stats}
"""

# Названия фильтров задач
TASK_FILTER_NAMES = {
    'tasks_all': 'Все',
    'tasks_active': 'Активные',
    'tasks_completed': 'Завершенные',
    'tasks_not_started': 'Не начатые'
}

# Эмодзи для фильтров задач
TASK_FILTER_EMOJI = {
    'tasks_all': '📋',
    'tasks_active': '🔄',
    'tasks_completed': '✅',
    'tasks_not_started': '⭕️'
}

# Фильтры статусов задач
TASK_STATUS_FILTERS = {
    'tasks_all': None,  # Все задачи
    'tasks_active': 'in_progress',
    'tasks_completed': 'completed',
    'tasks_not_started': 'not_started'
}

# Сообщения для задач сотрудника
EMPLOYEE_TASKS_MESSAGE = """
👤 *Задачи сотрудника {employee_name}*

{tasks_list}

📊 *Статистика:*
• Всего активных задач: {total_tasks}
• В работе: {in_progress_tasks}
• Не начато: {not_started_tasks}

⏰ *Ближайший дедлайн:* {nearest_deadline}
"""

EMPLOYEE_TASK_ITEM = """
{status_emoji} *{title}*
⏰ Срок: {deadline}
🏢 Клиент: {client}
📂 Проект: {project}
"""

# Формат даты для дедлайнов
DATE_FORMAT = "%d.%m.%Y"