"""Функции задач планировщика.

Содержит функции-обработчики, которые выполняются по расписанию.
Каждая функция принимает экземпляр бота в качестве первого аргумента.
"""

from datetime import datetime, timezone
import zoneinfo




    # ... rest of code




from aiogram import Bot
from loguru import logger

from source.config import settings

DEFAULT_TIMEZONE = "Europe/Minsk"

async def send_daily_welcome_message(bot: Bot) -> None:
    """Отправляет приветственное сообщение администраторам.

    Выполняется ежедневно в 09:00. Отправляет сообщение всем
    администраторам из конфигурации с текущей датой.

    Args:
        bot: Экземпляр Telegram-бота для отправки сообщений.
    """
    tz = zoneinfo.ZoneInfo(DEFAULT_TIMEZONE)
    now = datetime.now(tz)
    today = now.strftime("%d.%m.%Y")
    try:
        
        welcome_text = (
            f"☀️ <b>Доброе утро!</b>\n\n"
            f"📅 Дата: {today}\n"
            f"🤖 Бот успешно работает.\n\n"
            f"Хорошего рабочего дня!"
        )

        for admin_id in settings.tg.admin_ids:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=welcome_text,
                    parse_mode="HTML",
                )
                logger.info(f"Приветственное сообщение отправлено админу {admin_id}")
            except Exception as e:
                logger.error(f"Ошибка отправки сообщения админу {admin_id}: {e}")

    except Exception:
        logger.exception("Критическая ошибка при отправке приветственного сообщения")
