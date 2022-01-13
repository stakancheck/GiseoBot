from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from decouple import config

# attach bot telegram api
BOT_API = config('BOT_API')

# choose type of storage
storage = MemoryStorage()

# create object bot
bot = Bot(BOT_API)

# create dispatcher bot
dp = Dispatcher(bot, storage=storage)

