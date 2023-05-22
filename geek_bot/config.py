from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from decouple import Csv, config

API_TOKEN = config('TOKEN')
ADMINS: tuple = config('ADMINS', cast=Csv(post_process=tuple, cast=int))

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dispatcher = Dispatcher(
    bot,
    storage=storage
)
