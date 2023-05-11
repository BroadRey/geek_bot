from aiogram import Dispatcher, types
from config import dispatcher


def register_global_handler(dispatcher: Dispatcher):
    dispatcher.register_message_handler(echo_handler)


async def echo_handler(msg: types.Message):
    if msg.text.isnumeric():
        input_number = str(int(msg.text) ** 2)
        await msg.reply(input_number)
        return
    
    await msg.reply(msg.text)