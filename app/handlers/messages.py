import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.config import config
from app.states import MessageState
from app.utils.message_map import add_mapping, get_mapping
from app.utils.admin_log import store_reveal, get_reveal, remove_reveal
from app.keyboards.main import get_reveal_keyboard

router = Router()
logger = logging.getLogger(__name__)


def _format_sender(user) -> dict:
    username = f"@{user.username}" if user.username else "отсутствует"
    name = user.first_name or ""
    if user.last_name:
        name += f" {user.last_name}"
    return {"id": user.id, "username": username, "name": name}


async def _fetch_recipient_info(bot, recipient_id: int) -> dict:
    try:
        chat = await bot.get_chat(recipient_id)
        username = f"@{chat.username}" if chat.username else "отсутствует"
        name = chat.first_name or "неизвестно"
        if chat.last_name:
            name += f" {chat.last_name}"
        return {"id": recipient_id, "username": username, "name": name}
    except Exception as e:
        logger.error(f"Failed to get recipient info: {e}")
        return {"id": recipient_id, "username": "отсутствует", "name": "неизвестно"}


def _build_full_log(label: str, text: str, sender: dict, recipient: dict) -> str:
    return (
        f"{label}\n\n"
        f"Текст:\n{text}\n\n"
        f"Получатель:\n"
        f"ID: {recipient['id']}\n"
        f"Username: {recipient['username']}\n"
        f"Имя: {recipient['name']}\n\n"
        f"Отправитель:\n"
        f"ID: {sender['id']}\n"
        f"Username: {sender['username']}\n"
        f"Имя: {sender['name']}"
    )


@router.message(MessageState.waiting_for_message)
async def handle_anonymous_message(message: Message, state: FSMContext):
    data = await state.get_data()
    recipient_id = data.get("recipient_id")

    if not recipient_id:
        await message.answer("❌ Ошибка: получатель не найден. Попробуйте снова.")
        await state.clear()
        return

    try:
        sent = await message.bot.send_message(
            chat_id=recipient_id,
            text=(
                f"📩 Новое анонимное сообщение\n\n"
                f"{message.text}\n\n"
                f"💬 Ответь на это сообщение, чтобы написать в ответ."
            ),
        )

        add_mapping(recipient_id, sent.message_id, message.from_user.id)

        sender_info = _format_sender(message.from_user)
        recipient_info = await _fetch_recipient_info(message.bot, recipient_id)

        log_preview = f"📋 Новое анонимное сообщение\n\nТекст:\n{message.text}"

        admin_msg = await message.bot.send_message(
            chat_id=config.LOG_RECEIVER_ID,
            text=log_preview,
        )

        store_reveal(
            admin_msg.message_id,
            sender_info,
            recipient_info,
            message.text,
        )

        await message.bot.edit_message_reply_markup(
            chat_id=config.LOG_RECEIVER_ID,
            message_id=admin_msg.message_id,
            reply_markup=get_reveal_keyboard(admin_msg.message_id),
        )

        await message.answer("✅ Сообщение успешно отправлено.")
    except Exception as e:
        logger.error(f"Error sending anonymous message: {e}")
        await message.answer(
            "❌ Не удалось отправить сообщение. "
            "Возможно, пользователь заблокировал бота или не начал диалог."
        )
    finally:
        await state.clear()


@router.message(F.reply_to_message, F.text)
async def handle_reply(message: Message):
    replied = message.reply_to_message
    key = (message.chat.id, replied.message_id)
    other_party_id = get_mapping(*key)

    if other_party_id is None:
        return

    try:
        sent = await message.bot.send_message(
            chat_id=other_party_id,
            text=(
                f"💬 Новый ответ\n\n"
                f"{message.text}\n\n"
                f"💬 Ответь на это сообщение, чтобы написать в ответ."
            ),
        )

        add_mapping(other_party_id, sent.message_id, message.from_user.id)

        sender_info = _format_sender(message.from_user)
        recipient_info = await _fetch_recipient_info(message.bot, other_party_id)

        log_preview = f"📋 Новый ответ в цепочке\n\nТекст:\n{message.text}"

        admin_msg = await message.bot.send_message(
            chat_id=config.LOG_RECEIVER_ID,
            text=log_preview,
        )

        store_reveal(
            admin_msg.message_id,
            sender_info,
            recipient_info,
            message.text,
        )

        await message.bot.edit_message_reply_markup(
            chat_id=config.LOG_RECEIVER_ID,
            message_id=admin_msg.message_id,
            reply_markup=get_reveal_keyboard(admin_msg.message_id),
        )

        await message.answer("✅ Ответ отправлен.")
    except Exception as e:
        logger.error(f"Error forwarding reply: {e}")
        await message.answer(
            "❌ Не удалось отправить ответ. "
            "Возможно, пользователь заблокировал бота или не начал диалог."
        )


@router.callback_query(F.data.startswith("reveal_sender:"))
async def reveal_sender_callback(callback: CallbackQuery):
    try:
        admin_message_id = int(callback.data.split(":", 1)[1])
        entry = get_reveal(admin_message_id)

        if entry is None:
            await callback.answer("Информация уже раскрыта или устарела.", show_alert=True)
            return

        full_text = _build_full_log(
            "📋 Лог нового сообщения",
            entry["text"],
            entry["sender"],
            entry["recipient"],
        )

        await callback.message.edit_text(text=full_text)
        remove_reveal(admin_message_id)
        await callback.answer("Информация об отправителе раскрыта.", show_alert=False)
    except Exception as e:
        logger.error(f"Error in reveal_sender callback: {e}")
        await callback.answer("Произошла ошибка.", show_alert=True)
