# import
import os

from aiogram.utils.executor import start_polling

# from import
from create_bot import dp
from handlers import main


async def register_handlers():
    main.register_handler_main(dp)


async def on_startup(dp):
    await register_handlers()
    print("Bot Online")


async def on_shutdown(dp):
    print("Bot Offline")


def start_bot():
    start_polling(
        dispatcher=dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=False,
    )
