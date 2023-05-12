import logging

from aiogram.utils import executor
from config import dispatcher
from handlers import callbacks, command_handlers, global_handlers

if __name__ == '__main__':
    command_handlers.register_command_handlers(dispatcher)
    callbacks.register_callbacks_handlers(dispatcher)
    global_handlers.register_global_handler(dispatcher)

    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dispatcher, skip_updates=True)