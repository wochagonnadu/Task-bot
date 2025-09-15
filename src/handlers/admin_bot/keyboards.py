from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from .constants import (
    # Кнопки главного меню
    BUTTON_TASKS,
    BUTTON_CLIENTS,
    BUTTON_PROJECTS,
    BUTTON_EMPLOYEES,
    BUTTON_NEW_TASK,
    BUTTON_REPORTS,
    # Callback data
    CALLBACK_TASKS_ALL,
    CALLBACK_TASKS_ACTIVE,
    CALLBACK_TASKS_COMPLETED,
    CALLBACK_TASKS_NOT_STARTED,
    CALLBACK_CLIENT_PREFIX,
    CALLBACK_CLIENT_ADD,
    CALLBACK_PROJECT_PREFIX,
    CALLBACK_PROJECT_ADD,
    CALLBACK_EMPLOYEE_PREFIX,
    CALLBACK_EMPLOYEE_ADD,
    CALLBACK_REPORT_WEEK,
    CALLBACK_REPORT_MONTH,
    CALLBACK_REPORT_QUARTER,
    CALLBACK_REPORT_YEAR,
    REPORT_PERIODS
)

def get_admin_keyboard() -> ReplyKeyboardMarkup:
    """Создает основную клавиатуру админа"""
    keyboard = [
        [BUTTON_TASKS, BUTTON_CLIENTS],
        [BUTTON_PROJECTS, BUTTON_EMPLOYEES],
        [BUTTON_NEW_TASK],
        [BUTTON_REPORTS]
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )

async def get_tasks_keyboard() -> InlineKeyboardMarkup:
    """Создает inline клавиатуру для раздела задач"""
    keyboard = [
        [
            InlineKeyboardButton("📋 Все задачи", callback_data=CALLBACK_TASKS_ALL),
            InlineKeyboardButton("🔄 Активные", callback_data=CALLBACK_TASKS_ACTIVE)
        ],
        [
            InlineKeyboardButton("✅ Завершенные", callback_data=CALLBACK_TASKS_COMPLETED),
            InlineKeyboardButton("⭕️ Не начатые", callback_data=CALLBACK_TASKS_NOT_STARTED)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def get_clients_keyboard(clients: list) -> InlineKeyboardMarkup:
    """Создает inline клавиатуру со списком клиентов"""
    keyboard = []
    
    # Добавляем кнопку для каждого клиента
    for client in clients:
        keyboard.append([
            InlineKeyboardButton(
                f"👥 {client.name}",
                callback_data=f"{CALLBACK_CLIENT_PREFIX}{client.id}"
            )
        ])
    
    # Добавляем кнопку создания нового клиента
    keyboard.append([
        InlineKeyboardButton(
            "➕ Добавить клиента",
            callback_data=CALLBACK_CLIENT_ADD
        )
    ])
    
    return InlineKeyboardMarkup(keyboard)

async def get_projects_keyboard(projects: list) -> InlineKeyboardMarkup:
    """Создает inline клавиатуру со списком проектов"""
    keyboard = []
    
    # Добавляем кнопку для каждого проекта
    for project in projects:
        keyboard.append([
            InlineKeyboardButton(
                f"📊 {project.name}",
                callback_data=f"{CALLBACK_PROJECT_PREFIX}{project.id}"
            )
        ])
    
    # Добавляем кнопку создания нового проекта
    keyboard.append([
        InlineKeyboardButton(
            "➕ Добавить проект",
            callback_data=CALLBACK_PROJECT_ADD
        )
    ])
    
    return InlineKeyboardMarkup(keyboard)

async def get_employees_keyboard(employees: list) -> InlineKeyboardMarkup:
    """Создает inline клавиатуру со списком сотрудников"""
    keyboard = []
    
    # Добавляем кнопку для каждого сотрудника
    for employee in employees:
        keyboard.append([
            InlineKeyboardButton(
                f"👤 {employee.full_name}",
                callback_data=f"{CALLBACK_EMPLOYEE_PREFIX}{employee.id}"
            )
        ])
    
    # Добавляем кнопку добавления сотрудника
    keyboard.append([
        InlineKeyboardButton(
            "➕ Добавить сотрудника",
            callback_data=CALLBACK_EMPLOYEE_ADD
        )
    ])
    
    return InlineKeyboardMarkup(keyboard)

async def get_reports_keyboard() -> InlineKeyboardMarkup:
    """Создает inline клавиатуру для выбора периода отчета"""
    keyboard = [
        [
            InlineKeyboardButton(
                REPORT_PERIODS['week'],
                callback_data=CALLBACK_REPORT_WEEK
            ),
            InlineKeyboardButton(
                REPORT_PERIODS['month'],
                callback_data=CALLBACK_REPORT_MONTH
            )
        ],
        [
            InlineKeyboardButton(
                REPORT_PERIODS['quarter'],
                callback_data=CALLBACK_REPORT_QUARTER
            ),
            InlineKeyboardButton(
                REPORT_PERIODS['year'],
                callback_data=CALLBACK_REPORT_YEAR
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)