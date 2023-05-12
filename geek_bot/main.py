import logging
from config import dispatcher, ADMINS
from aiogram.utils import executor
from handlers import (command_handlers,
                      callbacks,
                      global_handlers,
                      )


if __name__ == '__main__':
    command_handlers.register_command_handlers(dispatcher)
    callbacks.register_callbacks_handlers(dispatcher)
    global_handlers.register_global_handler(dispatcher)

    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dispatcher, skip_updates=True)