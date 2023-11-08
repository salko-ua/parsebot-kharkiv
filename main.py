from create_bot import bot, dp
from handlers import main

async def register_handlers():
    dp.include_router(main.router)

async def start_bot():
     await register_handlers()
     await bot.delete_webhook(drop_pending_updates=True)
     await dp.start_polling(bot)
     print("Bot Online")