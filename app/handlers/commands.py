from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from app.keyboards.main import get_main_keyboard
from app.utils.stats import get_all_time, get_today, get_this_week, get_this_month

router = Router()


@router.message(Command("share"))
async def share_command(message: Message):
    bot_username = (await message.bot.me()).username
    user_id = message.from_user.id
    link = f"https://t.me/{bot_username}?start={user_id}"

    await message.answer(
        f"🔗 Твоя ссылка для анонимных сообщений:\n\n"
        f"{link}\n\n"
        f"Размести её в описании профиля, чтобы тебе могли написать.",
        reply_markup=get_main_keyboard(bot_username, user_id),
        disable_web_page_preview=True,
    )


@router.message(Command("stats"))
async def stats_command(message: Message):
    total = get_all_time()
    today = get_today()
    week = get_this_week()
    month = get_this_month()

    await message.answer(
        f"📊 Статистика бота\n\n"
        f"Всего отправлено: {total}\n"
        f"За сегодня: {today}\n"
        f"За эту неделю: {week}\n"
        f"За этот месяц: {month}"
    )


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        f"🤖 Как это работает\n\n"
        f"1. Получи свою ссылку — напиши /share\n"
        f"2. Размести ссылку в описании профиля Instagram, TikTok, Telegram и т.д.\n"
        f"3. Люди переходят по ссылке и пишут тебе анонимные сообщения\n"
        f"4. Ты получаешь сообщение без информации об отправителе\n"
        f"5. Ты можешь ответить — и начать диалог, оставаясь анонимным\n\n"
        f"🔒 Твои данные в безопасности. Никто не узнает, кто написал сообщение, "
        f"если ты сам не решишь раскрыть себя.\n\n"
        f"Команды:\n"
        f"/share — получить свою ссылку\n"
        f"/stats — статистика бота\n"
        f"/help — это сообщение"
    )
