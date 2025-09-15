import os
import sys
import logging
import asyncio
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv # Добавляем загрузку переменных окружения

# Создаем директорию для логов
os.makedirs('logs', exist_ok=True)

# Отключаем логи от httpx
logging.getLogger("httpx").setLevel(logging.WARNING)

# Настраиваем ротацию логов
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
max_bytes = 10 * 1024 * 1024  # 10 MB

handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=max_bytes,
    backupCount=5
)
handler.setFormatter(logging.Formatter(log_format))

logging.basicConfig(
    format=log_format,
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        handler
    ]
)

# Принудительная загрузка переменных окружения из .env


# Загружаем рабочее время из переменных окружения
WORK_START_TIME = os.getenv("WORK_START_TIME", "09:30")
WORK_END_TIME = os.getenv("WORK_END_TIME", "17:30")

print(f"✅ WORK_START_TIME: {WORK_START_TIME}")
print(f"✅ WORK_END_TIME: {WORK_END_TIME}")

# Настраиваем путь к корневой директории проекта
src_dir = str(Path(__file__).resolve().parent.parent)
if src_dir not in sys.path:
    sys.path.append(src_dir)

from src.config import get_config
from src.admin_bot import AdminBot
from src.user_bot import UserBot
from src.database.db import init_db
from src.services.notifications import start_scheduler, send_task_notifications
logger = logging.getLogger(__name__)

class BotRunner:
    """Класс для управления запуском ботов"""

    def __init__(self):
        """Инициализация менеджера ботов"""
        self.config = get_config()
        self.admin_bot = None
        self.user_bot = None
        self._running = False
        self._stop_event = asyncio.Event()
        self._polling_ready = asyncio.Event()

    async def _start_polling(self, bot_name, updater):
        """Запускает polling для бота и устанавливает флаг готовности"""
        try:
            await updater.start_polling()
            logger.info(f"{bot_name} polling запущен успешно")
        except Exception as e:
            logger.error(f"Ошибка при запуске {bot_name} polling: {e}")
            raise

    async def init_bots(self):
        """Инициализация и запуск ботов"""
        try:
            # Инициализация базы данных
            logger.info("Инициализация базы данных...")
            await init_db()

            # Исправление sequence 'users_id_seq' (если требуется)
            from src.database.db import db
            await db.fix_users_sequence()

            # Инициализация ботов
            logger.info("Инициализация ботов...")
            self.admin_bot = AdminBot(self.config.admin_bot_token)
            self.user_bot = UserBot(self.config.user_bot_token)

            # Инициализация приложений
            logger.info("Инициализация приложений...")
            await self.admin_bot.application.initialize()
            await self.user_bot.application.initialize()

            # Запуск приложений
            logger.info("Запуск приложений...")
            await self.admin_bot.application.start()
            await self.user_bot.application.start()

            # Инициализация и запуск уведомлений
            logger.info("Запуск сервиса уведомлений...")
            from src.services.notifications import init_notifications
            init_notifications(self.user_bot.application.bot)
            start_scheduler(self.user_bot.application.bot)

            # Запуск polling
            logger.info("Запуск polling...")
            self._running = True
            
            polling_tasks = [
                self._start_polling("AdminBot", self.admin_bot.application.updater),
                self._start_polling("UserBot", self.user_bot.application.updater)
            ]
            
            # Запускаем задачи polling и ждем их инициализации
            await asyncio.gather(*polling_tasks)
            
            # Устанавливаем флаг готовности polling
            self._polling_ready.set()
            
            # Ждем сигнала остановки
            await self._stop_event.wait()

        except asyncio.CancelledError:
            logger.info("Получен сигнал остановки")
        except Exception as e:
            logger.error(f"Критическая ошибка: {e}", exc_info=True)
            raise
        finally:
            if self._polling_ready.is_set():
                await self.stop_bots()

    async def stop_bots(self):
        """Остановка ботов и фоновых задач"""
        if not self._running:
            return

        logger.info("Останавливаем боты...")
        self._running = False
        self._stop_event.set()

        # Остановка ботов
        if self.admin_bot and self.admin_bot.application.running:
            try:
                await self.admin_bot.application.stop()
            except Exception as e:
                logger.error(f"Ошибка при остановке admin_bot: {e}")

        if self.user_bot and self.user_bot.application.running:
            try:
                await self.user_bot.application.stop()
            except Exception as e:
                logger.error(f"Ошибка при остановке user_bot: {e}")

        # Отмена всех оставшихся задач
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        for task in tasks:
            task.cancel()

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

        logger.info("Боты остановлены")

    async def run(self):
        """Запуск ботов"""
        logger.info("Запуск BotRunner...")
        try:
            await self.init_bots()
        except KeyboardInterrupt:
            logger.info("Получен сигнал остановки (KeyboardInterrupt)")
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}", exc_info=True)
        finally:
            if self._running:
                await self.stop_bots()

def main():
    """Точка входа"""
    runner = BotRunner()

    try:
        asyncio.run(runner.run())
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}", exc_info=True)

if __name__ == "__main__":
    main()
