"""Константы для форматирования сообщений"""

# Статусы задач
TASK_STATUSES = {
    'not_started': '⭕️ Не начата',
    'in_progress': '🔄 В работе',
    'completed': '✅ Завершена'
}

# Форматы сообщений
HELP_MESSAGE = """
🤖 *Task Bot \\- Система управления задачами*\n
*Доступные команды:*
/new\\_task \\- Создать новую задачу
/my\\_tasks \\- Показать список моих задач

*Вы получите уведомления:\\:*
\\- Утром \\(09:30\\) \\- список задач на день
\\- Вечером \\(17:30\\) \\- напоминание о завершении учета
"""

MY_TASKS_MESSAGE = """
📋 *Ваши задачи*:

{tasks_list}

Всего задач: {total_count}
"""

TASK_LIST_ITEM = """
🔹 *{title}*
⏱ Статус: {status}
⚡️ Срок: {deadline}
👤 Клиент: {client}
📂 Проект: {project}
"""

TASK_DETAIL_MESSAGE = """
📌 *Задача №{task_id}: {title}*

📝 *Описание:*
_{description}_

ℹ️ *Информация:*
• Статус: {status}
• Создана: {created_at}
• Срок: {deadline}
• Клиент: {client}
• Проект: {project}
"""

# Callback data для управления задачами
START_TASK = "start_task_{task_id}"
COMPLETE_TASK = "complete_task_{task_id}"