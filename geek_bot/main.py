import logging

from aiogram.utils import executor
from config import dispatcher
from general_chats_logics.handlers import command_handlers as general_handlers
from group_admin_logics.handlers import command_handlers as group_handlers, callbacks
from private_chat_logics.handlers import forms_handlers

if __name__ == '__main__':
    forms_handlers.register_form_handlers(dispatcher)
    general_handlers.register_command_handlers(dispatcher)
    group_handlers.register_command_handlers(dispatcher)
    callbacks.register_callbacks_handlers(dispatcher)

    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dispatcher, skip_updates=True)