import logging

from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.states import MessageState
from app.keyboards.main import get_main_keyboard

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start_command(message: Message, command: CommandObject, state: FSMContext):
    if command.args:
        try:
            recipient_id = int(command.args)
        except ValueError:
            await message.answer("❌ Неверная ссылка.")
            return

        if message.from_user.id == recipient_id:
            await message.answer("❌ Нельзя отправить сообщение самому себе.")
            return

        await state.update_data(recipient_id=recipient_id)
        await state.set_state(MessageState.waiting_for_message)
        await message.answer("📨 Отправьте ваше сообщение:")
        return

    bot_username = (await message.bot.me()).username
    user_id = message.from_user.id
    link = f"https://t.me/{bot_username}?start={user_id}"

    await message.answer(
        f"Начни получать анонимные вопросы прямо сейчас 👀\n\n"
        f"🔗 Ссылка для получения анонимных вопросов:\n\n"
        f"{link}\n\n"
        f"Размести эту ссылку ☝️ в описании профиля, чтобы тебе могли написать.",
        reply_markup=get_main_keyboard(bot_username, user_id),
        disable_web_page_preview=True,
    )


@router.callback_query(F.data.startswith("copy_link:"))
async def copy_link_callback(callback: CallbackQuery):
    try:
        user_id = int(callback.data.split(":", 1)[1])
        bot_username = (await callback.bot.me()).username
        link = f"https://t.me/{bot_username}?start={user_id}"

        await callback.message.answer(
            f"🔗 Ваша ссылка:\n\n{link}\n\n"
            f"Нажмите и удерживайте сообщение, чтобы скопировать."
        )
    except Exception as e:
        logger.error(f"Error in copy_link callback: {e}")
    finally:
        await callback.answer()
