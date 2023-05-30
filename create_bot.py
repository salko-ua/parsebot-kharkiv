# from import
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from config import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
