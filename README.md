# Task Bot

Task-bot — это комплексная система управления задачами, построенная на базе Telegram. Она использует архитектуру с несколькими ботами (для администратора и для пользователя), чтобы обеспечить бесшовное создание, назначение и отслеживание задач между администраторами, исполнителями и клиентами.

## О проекте

### Проблема
Организациям часто требуется более быстрый и доступный способ управления задачами, проектами и клиентами, чем предоставляют традиционные системы. Цель состоит в том, чтобы перенести эти рабочие процессы непосредственно в интерфейс мессенджера.

### Решение
Этот проект представляет собой решение на базе Telegram, которое обеспечивает:
- Быстрое создание и назначение задач.
- Обновление статуса от исполнителей в реальном времени.
- Управление клиентами и проектами.
- Административный надзор с помощью отчетов и аналитики.

## Ключевые возможности

### Бот для администратора
- **Управление задачами**: Создание, определение деталей, установка сроков и назначение задач.
- **Управление проектами**: Создание и управление проектами, а также их привязка к клиентам.
- **Управление клиентами**: Регистрация и управление информацией о клиентах.
- **Управление пользователями**: Контроль доступа к системе через систему приглашений.
- **Аналитика**: Создание отчетов и просмотр аналитики по проектам и задачам.
- **Экспорт данных**: Экспорт отчетов в Excel.

### Бот для пользователя (исполнителя)
- **Уведомления о задачах**: Мгновенные уведомления о новых задачах.
- **Список задач**: Просмотр всех назначенных задач.
- **Обновление статуса**: Обновление статуса задачи (например, "в работе", "выполнена").
- **Детали задачи**: Доступ ко всей информации, связанной с задачей.

## Галерея

### Безопасность и доступ
<table>
  <tr>
    <td><img src="./assets/images/security_invitation_code.PNG" alt="Пример кода приглашения" width="50%"></td>
    <td><img src="./assets/images/security_first_access_manager.PNG" alt="Запрос доступа от менеджера" width="50%"></td>
  </tr>
  <tr>
    <td align="center">1. Пользователь вводит код приглашения.</td>
    <td align="center">2. Бот запрашивает подтверждение у администратора.</td>
  </tr>
  <tr>
    <td><img src="./assets/images/security_first_access_manager_approved.PNG" alt="Доступ разрешен" width="50%"></td>
    <td><img src="./assets/images/access_denied.PNG" alt="Доступ запрещен" width="50%"></td>
  </tr>
  <tr>
    <td align="center">3. Администратор одобряет доступ.</td>
    <td align="center">Пример сообщения об отказе в доступе.</td>
  </tr>
</table>

### Пример интерфейса
<img src="./assets/images/actions_example.PNG" alt="Пример меню с действиями" width="50%">
*Пример инлайн-меню для управления задачами.*

### Демонстрация работы
- [Демонстрация работы менеджера (видео)](./assets/images/start_demo_manager.MP4)
- [Демонстрация работы исполнителя (видео)](./assets/images/start_demo_worker.MP4)

*Примечание: GitHub не отображает видео `.MP4` напрямую. Для лучшего опыта рекомендуется загрузить их на видеохостинг.*

## Как добавлять медиа (скриншоты и видео)

По вашему запросу, вот инструкция по встраиванию медиа в этот README.

### Скриншоты
Чтобы добавить изображение, поместите файл в репозиторий (например, в новую папку `assets/images`) и используйте следующий синтаксис Markdown:
```markdown
![Альт-текст для вашего изображения](./assets/images/screenshot.png)
```

### Видео
Markdown на GitHub не поддерживает прямое встраивание видео. Лучший подход — связать изображение с вашим видео, размещенным на платформе вроде YouTube:
```markdown
[![Смотреть демо видео](./assets/images/video_thumbnail.png)](https://www.youtube.com/watch?v=your_video_id)
```

## Технологический стек

- **Ядро**: Python
- **База данных**: SQLAlchemy (ORM), Alembic (миграции)
- **Telegram API**: `python-telegram-bot`
- **Окружение**: Docker, Docker Compose

## Архитектура

Система использует архитектуру с несколькими ботами с четким разделением ответственности, следуя нескольким ключевым шаблонам проектирования.

### Архитектура с несколькими ботами
```mermaid
graph TB
    Admin[Бот администратора] --> DB[(База данных)]
    User[Бот пользователя] --> DB
    DB --> Models[Модели базы данных]
    Models --> Tasks[Задачи]
    Models --> Clients[Клиенты]
    Models --> Users[Пользователи]
    Models --> Reports[Отчеты]
    Models --> Invitations[Приглашения]
```

### Конечный автомат для создания задач
Создание задачи следует управляемому, пошаговому шаблону конечного автомата.
```mermaid
graph LR
    Start[Начало] --> Client[Выбор клиента]
    Client --> Project[Выбор проекта]
    Project --> Details[Детали задачи]
    Details --> DateTime[Выбор даты и времени]
    DateTime --> Executor[Выбор исполнителя]
    Executor --> Confirm[Подтверждение задачи]
```

### Процесс аутентификации
```mermaid
graph TD
    Request[Входящий запрос] --> Auth[Промежуточное ПО аутентификации]
    Auth --> Check{Проверка аутентификации}
    Check -->|Успешно| Handler[Обработчик]
    Check -->|Неудачно| Reject[Отклонить запрос]
    Auth --> MasterKey[Проверка мастер-ключа]
    Auth --> Invitation[Проверка приглашения]
```

## Схема Базы Данных
```mermaid
erDiagram
    users {
        bigint telegram_id PK
        varchar username
        varchar full_name
        varchar role
    }

    clients {
        int id PK
        varchar name
    }

    projects {
        int id PK
        int client_id FK
        varchar name
        text description
        varchar status
    }

    tasks {
        int id PK
        int creator_id FK
        int assignee_id FK
        int client_id FK
        int project_id FK
        varchar title
        varchar status
        datetime due_date
    }

    task_times {
        int id PK
        int task_id FK
        int user_id FK
        date work_date
        time start_time
        time end_time
    }

    invitations {
        int id PK
        varchar code
        bool is_used
    }

    users ||--o{ tasks : "creates"
    users ||--o{ tasks : "is assigned"
    users ||--o{ task_times : "logs time"
    clients ||--o{ projects : "has"
    clients ||--o{ tasks : "has"
    projects ||--o{ tasks : "contains"
    tasks ||--o{ task_times : "has"
```

## Установка и настройка

### 1. Docker (рекомендуемый способ)
Этот метод автоматически настраивает базу данных и приложение.

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/wochagonnadu/Task-bot.git
    cd Task-bot
    ```

2.  **Создайте файл `.env`** в корневом каталоге и добавьте токены ваших ботов:
    ```env
    # Токены ботов
    TELEGRAM_BOT_TOKEN=
    USER_TELEGRAM_BOT_TOKEN=

    # Master Key
    MASTER_KEY=

    DB_HOST=
    DB_PORT=
    DB_NAME=
    DB_USER=
    DB_PASSWORD=

    # Database URL
    DATABASE_URL=

    # Work Hours Configuration (optional)
    WORK_START_TIME=09:30
    WORK_END_TIME=17:30
    ```

3.  **Запустите с помощью Docker Compose:**
    ```bash
    docker-compose up -d
    ```
    Миграции базы данных будут применены автоматически при первом запуске.

### 2. Ручная установка

1.  **Клонируйте репозиторий** и перейдите в каталог проекта.

2.  **Создайте виртуальное окружение** и установите зависимости:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Linux/macOS
    # или
    venv\Scripts\activate  # Для Windows
    pip install -r requirements.txt
    ```

3.  **Создайте файл `.env`**, как описано выше, а также добавьте URL для подключения к базе данных:
    ```env
    DATABASE_URL=postgresql+asyncpg://user:password@host:port/dbname?ssl=disable
    ```

4.  **Примените миграции базы данных:**
    ```bash
    alembic upgrade head
    ```

5.  **Запустите приложение:**
    ```bash
    python src/main.py
    ```

## Использование
После запуска ботов вы можете взаимодействовать с ними с помощью команд `/start` и `/help`, которые проведут вас по доступным интерактивным меню.

## Лицензия

Этот проект лицензирован под лицензией MIT. Подробности смотрите в файле [LICENSE](LICENSE).