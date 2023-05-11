from aiogram import Bot, Dispatcher
from decouple import config

API_TOKEN = config('TOKEN')

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)