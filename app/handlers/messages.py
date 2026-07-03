import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.config import config
from app.states import MessageState

router = Router()
logger = logging.getLogger(__name__)


@router.message(MessageState.waiting_for_message)
async def handle_anonymous_message(message: Message, state: FSMContext):
    data = await state.get_data()
    recipient_id = data.get("recipient_id")

    if not recipient_id:
        await message.answer("❌ Ошибка: получатель не найден. Попробуйте снова.")
        await state.clear()
        return

    try:
        await message.bot.send_message(
            chat_id=recipient_id,
            text=f"📩 Новое анонимное сообщение\n\n{message.text}",
        )

        sender = message.from_user
        sender_username = f"@{sender.username}" if sender.username else "отсутствует"
        sender_name = sender.first_name or ""
        if sender.last_name:
            sender_name += f" {sender.last_name}"

        recipient_name = "неизвестно"
        recipient_username = "отсутствует"
        try:
            recipient_chat = await message.bot.get_chat(recipient_id)
            recipient_name = recipient_chat.first_name or "неизвестно"
            if recipient_chat.last_name:
                recipient_name += f" {recipient_chat.last_name}"
            recipient_username = (
                f"@{recipient_chat.username}"
                if recipient_chat.username
                else "отсутствует"
            )
        except Exception as e:
            logger.error(f"Failed to get recipient info: {e}")

        log_text = (
            f"📋 Лог нового сообщения\n\n"
            f"Получатель:\n"
            f"ID: {recipient_id}\n"
            f"Username: {recipient_username}\n"
            f"Имя: {recipient_name}\n\n"
            f"Текст:\n{message.text}\n\n"
            f"Отправитель:\n"
            f"ID: {sender.id}\n"
            f"Username: {sender_username}\n"
            f"Имя: {sender_name}"
        )

        await message.bot.send_message(
            chat_id=config.LOG_RECEIVER_ID,
            text=log_text,
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
