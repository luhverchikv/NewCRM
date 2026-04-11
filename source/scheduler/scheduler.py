"""Настройка APScheduler для автоматической рассылки сообщений.

Интеграция модуля APScheduler в проект NewCRM на основе архитектуры
проекта Cardio. Планировщик использует AsyncIOScheduler для выполнения
асинхронных задач в заданное время.
"""

import zoneinfo
from contextlib import suppress
from typing import TYPE_CHECKING

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from source.scheduler.jobs import send_daily_welcome_message

if TYPE_CHECKING:
    from aiogram import Bot

# Часовой пояс по умолчанию (Europe/Minsk)
DEFAULT_TIMEZONE = "Europe/Minsk"


def create_scheduler(bot: "Bot") -> AsyncIOScheduler:
    """Создает и настраивает экземпляр планировщика APScheduler.

    Регистрирует все запланированные задачи и запускает планировщик.
    Задачи выполняются в асинхронном режиме с использованием
    AsyncIOScheduler.

    Args:
        bot: Экземпляр Telegram-бота для передачи в задачи.

    Returns:
        Настроенный и запущенный экземпляр AsyncIOScheduler.
    """
    timezone = zoneinfo.ZoneInfo(DEFAULT_TIMEZONE)
    scheduler = AsyncIOScheduler(timezone=timezone)

    # ☀️ Ежедневное приветственное сообщение администраторам (09:00)
    scheduler.add_job(
        send_daily_welcome_message,
        CronTrigger(hour=9, minute=0),
        args=[bot],
        id="daily_welcome_message",
        replace_existing=True,
    )

    # Запуск планировщика
    scheduler.start()
    return scheduler


def shutdown_scheduler(scheduler: AsyncIOScheduler) -> None:
    """Останавливает планировщик APScheduler.

    Корректно завершает работу планировщика, ожидая завершения
    текущих задач.

    Args:
        scheduler: Экземпляр планировщика для остановки.
    """
    with suppress(Exception):
        scheduler.shutdown(wait=False)
