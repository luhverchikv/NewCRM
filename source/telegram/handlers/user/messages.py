from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from dishka import FromDishka
from dishka.integrations.aiogram import inject as aiogram_inject

from source.services import UserService
from source.utils import I18n

user_messages_router = Router(name=__name__)


@user_messages_router.message(F.location)
@aiogram_inject
async def handle_location(
    message: Message,  # <-- location получаем из message.location
    user_service: FromDishka[UserService],
    i18n: FromDishka[I18n],
) -> None:
    """Обработка полученной геолокации."""
    user_id = message.from_user.id
    lat = message.location.latitude      # <-- так достаём широту
    lon = message.location.longitude     # <-- так достаём долготу

    # Сохраняем в БД (опционально)
    #await user_service.update_location(user_id, lat, lon)

    # Формируем Google Maps ссылку
    maps_url = f"https://www.google.com/maps?q={lat},{lon}"

    text = await i18n(
        user_id,
        "location_received",
        lat=lat,
        lon=lon,
        maps_url=maps_url,
    )
    await message.answer(text)


@user_messages_router.message(F.text, StateFilter(None))
async def echo(message: Message) -> None:
    await message.answer(message.text)
