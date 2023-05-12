from random import choice

from aiogram import Dispatcher, types
from config import ADMINS
from filters.is_group_chat_filter import IsGroupChat


def register_global_handler(dispatcher: Dispatcher):
    dispatcher.register_message_handler(echo_handler, IsGroupChat())


async def echo_handler(message: types.Message):
    if (
        message.text.startswith('game')
        and message.from_user.id in ADMINS
    ):
        emoji = '🎲', '🎯', '🏀', '⚽', '🎰', '🎳'
        random_emoji = choice(emoji)
        await message.reply_dice(random_emoji)
        return

    if message.text.isnumeric():
        input_number = str(int(message.text) ** 2)
        await message.reply(input_number)
        return

    await message.reply(message.text)
