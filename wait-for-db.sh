#!/bin/sh
set -e

host="$1"
port="$2"

shift 2

until nc -z "$host" "$port"; do
  echo "\ud83d\udd04 Ожидание доступности базы данных: $host:$port..."
  sleep 1
done

echo "\u2705 БД доступна!"
