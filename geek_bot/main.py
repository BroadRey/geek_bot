import logging

from aiogram.utils import executor
from config import dispatcher
from database.db import sql_create_db_conection, sql_create_table
from general_chats_logics.handlers import command_handlers as general_handlers
from group_admin_logics.handlers import callbacks
from group_admin_logics.handlers import command_handlers as group_handlers
from private_chat_logics.handlers import (forms_handlers,
                                          command_handlers as private_handlers)


async def on_startup(dp):
    await sql_create_table()

if __name__ == '__main__':
    forms_handlers.register_form_handlers(dispatcher)
    general_handlers.register_command_handlers(dispatcher)
    group_handlers.register_command_handlers(dispatcher)
    private_handlers.register_command_handlers(dispatcher)
    callbacks.register_callbacks_handlers(dispatcher)

    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dispatcher,
                           skip_updates=True,
                           on_startup=on_startup)
