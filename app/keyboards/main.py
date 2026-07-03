import urllib.parse

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CopyTextButton
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
        InlineKeyboardButton(
            text="📋 Скопировать ссылку",
            copy_text=CopyTextButton(text=link),
        ),
        InlineKeyboardButton(text="📤 Поделиться ссылкой", url=share_url),
    )
    builder.adjust(1)
    return builder.as_markup()


def get_reveal_keyboard(admin_message_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="👤 Узнать отправителя",
            callback_data=f"reveal_sender:{admin_message_id}",
        ),
    )
    return builder.as_markup()
