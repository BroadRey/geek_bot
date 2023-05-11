import emoji
from aiogram import types, Dispatcher
from config import bot


def register_callbacks_handlers(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(next_quiz_handler, text='next')

async def next_quiz_handler(call: types.CallbackQuery):
    question = 'Сколько тебе лет?'
    answers = [
        emoji.emojize(':keycap_1: 35+'),
        emoji.emojize(':keycap_2: 19-34'),
        emoji.emojize(':keycap_3: 1-18'),
    ]

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answers,
        is_anonymous=True,
    )