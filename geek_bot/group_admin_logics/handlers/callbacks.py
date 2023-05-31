import emoji
from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot


def register_callbacks_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(
        next_1_callback_handler,
        text='next_1'
    )
    dispatcher.register_callback_query_handler(
        next_2_callback_handler,
        text='next_2'
    )
    dispatcher.register_callback_query_handler(
        next_3_callback_handler,
        text='next_3'
    )


async def next_1_callback_handler(callback: types.CallbackQuery) -> None:
    await bot.edit_message_reply_markup(
        callback.message.chat.id,
        callback.message.message_id,
        reply_markup=InlineKeyboardMarkup()
    )

    inline_markup = InlineKeyboardMarkup()
    next_button = InlineKeyboardButton(
        'Следующий вопрос',
        callback_data='next_2'
    )
    inline_markup.add(next_button)

    question = 'Сколько тебе лет?'
    answers = [
        emoji.emojize(':keycap_1: 35+'),
        emoji.emojize(':keycap_2: 19-34'),
        emoji.emojize(':keycap_3: 1-18'),
    ]

    await bot.send_poll(
        chat_id=callback.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=True,
        reply_markup=inline_markup
    )


async def next_2_callback_handler(callback: types.CallbackQuery) -> None:
    await bot.edit_message_reply_markup(
        callback.message.chat.id,
        callback.message.message_id,
        reply_markup=InlineKeyboardMarkup()
    )

    inline_markup = InlineKeyboardMarkup()
    next_button = InlineKeyboardButton(
        'Следующий вопрос',
        callback_data='next_3'
    )
    inline_markup.add(next_button)

    question = 'Как называется лучший язык программирования?'
    answers = [
        emoji.emojize(':keycap_1: Python'),
        emoji.emojize(':keycap_2: Java'),
        emoji.emojize(':keycap_3: JavaScript'),
        emoji.emojize(':keycap_3: Golang')
    ]

    await bot.send_poll(
        chat_id=callback.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=True,
        type='quiz',
        correct_option_id=0,
        reply_markup=inline_markup
    )


async def next_3_callback_handler(callback: types.CallbackQuery) -> None:
    await bot.edit_message_reply_markup(
        callback.message.chat.id,
        callback.message.message_id,
        reply_markup=InlineKeyboardMarkup()
    )

    question = 'Как называется худший язык программирования?'
    answers = [
        emoji.emojize(':keycap_3: JavaScript'),
        emoji.emojize(':keycap_1: Python'),
        emoji.emojize(':keycap_2: Java'),
        emoji.emojize(':keycap_3: Golang'),
    ]

    await bot.send_poll(
        chat_id=callback.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=True,
        type='quiz',
        correct_option_id=0
    )