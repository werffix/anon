import urllib.parse

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_keyboard(bot_username: str, user_id: int) -> InlineKeyboardMarkup:
    link = f"https://t.me/{bot_username}?start={user_id}"
    share_text = "Отправь мне анонимное сообщение"
    share_url = (
        f"https://t.me/share/url?url={urllib.parse.quote(link)}"
        f"&text={urllib.parse.quote(share_text)}"
    )

    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📋 Скопировать ссылку", callback_data=f"copy_link:{user_id}"),
        InlineKeyboardButton(text="📤 Поделиться ссылкой", url=share_url),
    )
    builder.adjust(1)
    return builder.as_markup()
