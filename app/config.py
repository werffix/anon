import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    LOG_RECEIVER_ID: int = int(os.getenv("LOG_RECEIVER_ID", "0"))


config = Config()
