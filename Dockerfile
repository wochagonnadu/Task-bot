# Используем стабильный образ Python 3.11
FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    libmagic1 \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Moscow

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем скрипты и делаем их исполняемыми
COPY wait-for-db.sh /wait-for-db.sh
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /wait-for-db.sh
RUN chmod +x /app/entrypoint.sh

# Копируем весь код приложения
COPY . .

# Создаём папку для логов
RUN mkdir -p logs

# Запуск приложения
ENTRYPOINT ["/app/entrypoint.sh"]