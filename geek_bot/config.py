from aiogram import Bot, Dispatcher
from decouple import config, Csv

API_TOKEN = config('TOKEN')
ADMINS = config('ADMINS', cast=Csv(post_process=tuple, cast=int))

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)