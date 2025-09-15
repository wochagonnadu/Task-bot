"""Обработчики callback-запросов для раздела отчетов"""

from datetime import datetime, timedelta
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from src.services.excel import ExcelReportGenerator
from ..constants import (
    CALLBACK_REPORT_WEEK,
    CALLBACK_REPORT_MONTH,
    CALLBACK_REPORT_QUARTER,
    CALLBACK_REPORT_YEAR,
    REPORTS_MENU_MESSAGE,
    REPORT_PERIODS
)

logger = logging.getLogger(__name__)

async def handle_reports_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик callback-запросов для раздела отчетов

    Args:
        update: Объект обновления Telegram
        context: Контекст Telegram бота
    """
    query = update.callback_query
    await query.answer()
    
    if query.data in [CALLBACK_REPORT_WEEK, CALLBACK_REPORT_MONTH, CALLBACK_REPORT_QUARTER, CALLBACK_REPORT_YEAR]:
        await generate_report(update, context, query.data.split('_')[1])
    else:
        # Показываем меню выбора периода
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
        
        await query.message.edit_text(
            REPORTS_MENU_MESSAGE,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def generate_report(update: Update, context: ContextTypes.DEFAULT_TYPE, period: str) -> None:
    """
    Генерация и отправка отчета за выбранный период

    Args:
        update: Объект обновления Telegram
        context: Контекст Telegram бота
        period: Период (week/month/quarter/year)
    """
    query = update.callback_query
    
    try:
        # Сообщаем о начале генерации
        await query.message.edit_text(
            f"🔄 Генерация отчета {REPORT_PERIODS[period].lower()}..."
        )
        
        # Создаем генератор отчетов
        generator = ExcelReportGenerator()
        
        # Генерируем отчет
        file_data = await generator.generate_report(period)
        
        # Отправляем файл
        await query.message.reply_document(
            document=file_data,
            filename=f"report_{period}_{datetime.now().strftime('%Y%m%d')}.xlsx",
            caption=f"📊 Отчет {REPORT_PERIODS[period].lower()}"
        )
        
        # Восстанавливаем меню выбора периода
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
        
        await query.message.edit_text(
            REPORTS_MENU_MESSAGE,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
    except Exception as e:
        logger.error(f"Ошибка при генерации отчета: {e}", exc_info=True)
        await query.message.edit_text(
            "❌ Произошла ошибка при генерации отчета. Попробуйте позже."
        )