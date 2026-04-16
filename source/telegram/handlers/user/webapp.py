from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from dishka.integrations.aiogram import inject as aiogram_inject
from dishka import FromDishka

from source.telegram.keyboards import get_webapp_inline_kb, get_webapp_reply_kb
from source.utils import I18n

webapp_router = Router(name=__name__)


@webapp_router.message(Command("mini_app"))
@aiogram_inject
async def open_mini_app(
    message: Message,
    i18n: FromDishka[I18n],
) -> None:
    """Команда для открытия Mini App."""
    user_id = message.from_user.id
    text = await i18n(user_id, "mini_app_welcome")

    await message.answer(
        text=text,
        reply_markup=get_webapp_inline_kb()
    )
