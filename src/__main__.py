import apykuma
import asyncio

from aiogram import Bot, Dispatcher

from src.handlers import main
from src.config import KUMA_TOKEN
from src.config import TOKEN


async def start_bot():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(main.router)

    if KUMA_TOKEN != "":
        await apykuma.start(url=KUMA_TOKEN, delay=10)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start_bot())
