"""Модуль планировщика задач APScheduler.

Предоставляет функциональность для автоматической рассылки сообщений
по расписанию в Telegram-боте.
"""

from source.scheduler.jobs import send_daily_welcome_message
from source.scheduler.scheduler import create_scheduler, shutdown_scheduler

__all__ = [
    "create_scheduler",
    "shutdown_scheduler",
    "send_daily_welcome_message",
]
