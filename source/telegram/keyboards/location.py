from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_location_kb(locale: str = "ru") -> InlineKeyboardMarkup:
    """Клавиатура с кнопкой отправки геолокации."""
    texts = {
        "ru": "📍 Отправить местоположение",
        "en": "📍 Send Location",
    }
    
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=texts.get(locale, texts["ru"]),
                    request_location=True,
                )
            ],
        ],
    )