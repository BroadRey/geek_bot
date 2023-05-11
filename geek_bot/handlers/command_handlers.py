import emoji
from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from config import dispatcher


def register_command_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start_command_handler, commands=['start'])
    dispatcher.register_message_handler(quiz_command_handler, commands=['quiz'])
    dispatcher.register_message_handler(mem_command_handler, commands=['mem'])
    

async def start_command_handler(msg: types.Message):
    await msg.reply(emoji.emojize('Я - бот! :robot:\n'
                                  'Будем знакомы!'), )


async def quiz_command_handler(msg: types.Message):
    inline_markup = InlineKeyboardMarkup()
    in_button_1 = InlineKeyboardButton(
        'Следующий вопрос', callback_data='next')
    inline_markup.insert(in_button_1)

    question = 'Как твои дела?'
    answers = [
        emoji.emojize(':keycap_1: Отлично!'),
        emoji.emojize(':keycap_2: Нормально.'),
        emoji.emojize(':keycap_3: Ужасно'),
    ]

    await msg.answer_poll(
        question=question,
        options=answers,
        correct_option_id=0,
        is_anonymous=True,
        type='quiz',
        reply_markup=inline_markup)
    

async def mem_command_handler(msg: types.Message):
    photo = InputFile('./pic/mems/mem.jpg')
    await msg.reply_photo(
        photo=photo,
    )