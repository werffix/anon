import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config import config
from app.handlers.start import router as start_router
from app.handlers.messages import router as message_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(message_router)

    logger.info("Bot started polling")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
