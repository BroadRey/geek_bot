from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from decouple import Csv, config
from typing import Tuple

API_TOKEN: str = config('TOKEN')
ADMINS: Tuple[int] = config('ADMINS', cast=Csv(post_process=tuple, cast=int))

bot: Bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dispatcher: Dispatcher = Dispatcher(
    bot,
    storage=storage
)
