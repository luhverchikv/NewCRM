from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def get_location_kb(locale: str = "ru") -> ReplyKeyboardMarkup:
    """Клавиатура с кнопкой отправки геолокации (Reply Keyboard)."""
    texts = {
        "ru": "📍 Отправить местоположение",
        "en": "📍 Send Location",
    }
    
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=texts.get(locale, texts["ru"]),
                    request_location=True,
                )
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
