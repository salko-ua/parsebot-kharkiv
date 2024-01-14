from create_bot import bot, dp
from handlers import main
import apykuma
from config import KUMA_TOKEN


async def register_handlers():
    dp.include_router(main.router)


async def start_bot():
    await register_handlers()
    await bot.delete_webhook(drop_pending_updates=True)
    print("Bot Online")
    if KUMA_TOKEN != "":
        await apykuma.start(url=KUMA_TOKEN, delay=10)
    await dp.start_polling(bot)
