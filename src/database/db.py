"""База данных Task Bot"""

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager
from typing import TypeVar, Type, Optional, List, Any, AsyncGenerator
from src.database.base import Base
import logging

from src.config import get_config

# Настройка логгера
logger = logging.getLogger(__name__)

# Получение конфигурации
config = get_config()

# Создание типа для моделей
ModelType = TypeVar("ModelType", bound=Base)

# Создание асинхронного движка базы данных
engine = create_async_engine(
    config.database_url,
    echo=False,  # Отключаем echo для уменьшения шума в логах
    pool_pre_ping=True  # Проверка соединения перед использованием
)

# Создание асинхронной фабрики сессий
AsyncSessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронный контекстный менеджер для работы с сессией БД"""
    session = AsyncSessionFactory()
    try:
        yield session
    finally:
        await session.close()

async def init_db() -> None:
    """Инициализация базы данных: создание всех таблиц"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("База данных успешно инициализирована")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при инициализации базы данных: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка при инициализации БД: {e}", exc_info=True)
        raise

class DatabaseManager:
    """Асинхронный менеджер для работы с базой данных"""
    
    async def create(self, model: Type[ModelType], **kwargs: Any) -> ModelType:
        """Создание новой записи в БД"""
        async with get_session() as session:
            try:
                item = model(**kwargs)
                session.add(item)
                await session.flush()
                await session.commit()
                return item
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Ошибка при создании записи: {e}", exc_info=True)
                raise

    async def get_session(self):
        """Возвращает асинхронную сессию"""
        async with get_session() as session:
            yield session  # Правильный вызов с созданием сессии
    
    async def get(self, model: Type[ModelType], id: int) -> Optional[ModelType]:
        """Получение записи по ID"""
        async with get_session() as session:
            try:
                return await session.get(model, id)
            except SQLAlchemyError as e:
                logger.error(f"Ошибка при получении записи по ID: {e}", exc_info=True)
                raise

    async def fix_users_sequence(self):
        """Исправление sequence 'users_id_seq' после ручного добавления ID"""
        async with get_session() as session:
            try:
                stmt = text(
                    "SELECT setval('users_id_seq', COALESCE((SELECT MAX(id) FROM users)::BIGINT, 1), true);"
                )
                await session.execute(stmt)
                await session.commit()
                logger.info("Последовательность 'users_id_seq' успешно обновлена")
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Ошибка при обновлении 'users_id_seq': {e}", exc_info=True)
                raise

    async def get_by_field(self, model: Type[ModelType], field: str, value: Any) -> Optional[ModelType]:
        """Получение записи по произвольному полю"""
        async with get_session() as session:
            try:
                stmt = select(model).where(getattr(model, field) == value)
                result = await session.execute(stmt)
                return result.scalar_one_or_none()
            except SQLAlchemyError as e:
                logger.error(f"Ошибка при получении записи по полю: {e}", exc_info=True)
                raise

    async def get_all(self, model: Type[ModelType], **filters: Any) -> List[ModelType]:
        """Получение всех записей с опциональными фильтрами"""
        async with get_session() as session:
            try:
                stmt = select(model)
                for field, value in filters.items():
                    if isinstance(value, list):
                        stmt = stmt.where(getattr(model, field).in_(value))
                    else:
                        stmt = stmt.where(getattr(model, field) == value)
                result = await session.execute(stmt)
                return list(result.scalars().all())
            except SQLAlchemyError as e:
                logger.error(f"Ошибка при получении списка записей: {e}", exc_info=True)
                raise

    async def get_tasks_with_relations(self, user_id: int, only_active: bool = False) -> List["Task"]:
        """Получение задач с предварительной загрузкой связанных объектов"""
        from src.database.models import Task  # Импорт здесь во избежание циклических зависимостей
        async with get_session() as session:
            try:
                stmt = (
                    select(Task)
                    .options(
                        selectinload(Task.client),
                        selectinload(Task.project)
                    )
                    .where(Task.assignee_id == user_id)
                )
                
                if only_active:
                    stmt = stmt.where(Task.status.in_(['not_started', 'in_progress']))
                
                result = await session.execute(stmt)
                return list(result.scalars().all())
            except SQLAlchemyError as e:
                logger.error(f"Ошибка при получении задач: {e}", exc_info=True)
                raise

    async def update(self, model: Type[ModelType], id: int, **kwargs: Any) -> Optional[ModelType]:
        """Обновление существующей записи"""
        async with get_session() as session:
            try:
                stmt = select(model).where(model.id == id)
                result = await session.execute(stmt)
                item = result.scalar_one_or_none()
                
                if item:
                    for key, value in kwargs.items():
                        setattr(item, key, value)
                    await session.commit()
                return item
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Ошибка при обновлении записи: {e}", exc_info=True)
                raise

    async def delete(self, model: Type[ModelType], id: int) -> bool:
        """Удаление записи по ID"""
        async with get_session() as session:
            try:
                stmt = select(model).where(model.id == id)
                result = await session.execute(stmt)
                item = result.scalar_one_or_none()
                
                if item:
                    await session.delete(item)
                    await session.commit()
                    return True
                return False
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Ошибка при удалении записи: {e}", exc_info=True)
                raise

    async def exists(self, model: Type[ModelType], **filters: Any) -> bool:
        """Проверка существования записи с заданными фильтрами"""
        async with get_session() as session:
            try:
                stmt = select(1).select_from(model)
                for field, value in filters.items():
                    stmt = stmt.where(getattr(model, field) == value)
                result = await session.execute(stmt)
                return result.scalar_one_or_none() is not None
            except SQLAlchemyError as e:
                logger.error(f"Ошибка при проверке существования записи: {e}", exc_info=True)
                raise

# Создание экземпляра менеджера БД для использования в других модулях
db = DatabaseManager()
