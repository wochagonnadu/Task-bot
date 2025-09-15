import asyncio
import sys
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Добавляем корневую директорию проекта в PYTHONPATH
root_path = str(Path(__file__).parent.parent.parent.parent)
if root_path not in sys.path:
    sys.path.append(root_path)

from src.config import get_config
from src.database.base import Base

# Import all models so that Alembic can detect them
from src.database.models.clients import Client, Project
from src.database.models.tasks import Task, TaskTime
from src.database.models.users import User
from src.database.models.reports import WorkReport
from src.database.models.invitations import Invitation

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

async def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    config = get_config()
    url = config.database_url  # Оставляем +asyncpg для асинхронного подключения
    context.configure(
        url=url,
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=Base.metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    """Запускаем асинхронные миграции."""

    config = get_config()
    url = config.database_url  # Сначала объявляем url

    alembic_config = context.config.get_section(context.config.config_ini_section)
    alembic_config["sqlalchemy.url"] = url  # Теперь url определён

    connectable = async_engine_from_config(
        alembic_config,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
