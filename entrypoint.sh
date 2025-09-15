#!/bin/sh
set -e

echo "\ud83d\udd04 Применяем миграции базы данных..."
alembic upgrade head

echo "\ud83d\udd04 Ждём доступности базы данных..."
/wait-for-db.sh "$DB_HOST" "$DB_PORT"

echo "\u25b6\ufe0f Запуск приложения..."
exec python src/main.py