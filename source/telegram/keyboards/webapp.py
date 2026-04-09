from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo


# URL вашего Mini App
MINI_APP_URL = "https://luhverchikv.github.io/mini_app"


def get_webapp_inline_kb() -> InlineKeyboardMarkup:
    """Inline клавиатура с кнопкой запуска Mini App."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Открыть Mini App",
                    web_app=WebAppInfo(url=MINI_APP_URL)
                )
            ]
        ]
    )


def get_webapp_reply_kb() -> ReplyKeyboardMarkup:
    """Reply клавиатура с кнопкой запуска Mini App."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🚀 Mini App",
                    web_app=WebAppInfo(url=MINI_APP_URL)
                )
            ]
        ],
        resize_keyboard=True
    )
