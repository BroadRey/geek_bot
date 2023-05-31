import time

import emoji
from aiogram import Dispatcher, filters as aiogram_filters, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from filters.filters import IsGroupChat


def register_command_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        start_command_handler,
        aiogram_filters.CommandStart()
    )

    dispatcher.register_message_handler(
        quiz_command_handler,
        commands=['quiz']
    )

    dispatcher.register_message_handler(
        mem_command_handler,
        commands=['mem']
    )

    dispatcher.register_message_handler(
        pin_command_handler,
        IsGroupChat(),
        commands=['pin'],
        commands_prefix='!/'
    )

    dispatcher.register_message_handler(
        dice_commad_handler,
        commands=['dice']
    )


async def start_command_handler(message: types.Message) -> None:
    await message.reply(emoji.emojize(
        'Я - бот! :robot:\n'
        'Будем знакомы!')
    )


async def quiz_command_handler(message: types.Message) -> None:
    inline_markup = InlineKeyboardMarkup()
    next_button = InlineKeyboardButton(
        text='Следующий вопрос',
        callback_data='next_1'
    )
    inline_markup.insert(next_button)

    question = 'Как твои дела?'
    answers = [
        emoji.emojize(':keycap_1: Отлично!'),
        emoji.emojize(':keycap_2: Нормально.'),
        emoji.emojize(':keycap_3: Ужасно'),
    ]

    await message.answer_poll(
        question=question,
        options=answers,
        correct_option_id=0,
        is_anonymous=True,
        type='quiz',
        reply_markup=inline_markup
    )


async def mem_command_handler(message: types.Message) -> None:
    photo = InputFile('./pic/mems/mem.jpg')
    await message.reply_photo(photo=photo)


async def pin_command_handler(message: types.Message) -> None:
    if not message.reply_to_message:
        return

    await message.reply_to_message.pin()


async def dice_commad_handler(message: types.Message) -> None:
    await message.reply(
        f'Хотите сыграть в {emoji.emojize(":game_die:")}?\n'
        'Давайте попробуем!\n'
        'Бросаю:'
    )

    bot_score = (await message.answer_dice(disable_notification=False)).dice.value

    await message.answer(
        f'{emoji.emojize(":face_with_monocle:")} '
        'Посмотрим, что выпадет у вас:'
    )

    user_score = (await message.answer_dice(disable_notification=False)).dice.value

    time.sleep(2)

    if bot_score > user_score:
        await message.answer(
            f'{emoji.emojize(":winking_face_with_tongue:")} '
            'Увы, удача не на вашей стороне!'
        )
    elif bot_score < user_score:
        await message.answer(
            f'{emoji.emojize(":partying_face:")} '
            'Вы сегодня везунчик! Победа за вами.'
        )
    else:
        await message.answer(
            f'{emoji.emojize(":thinking_face:")} '
            'Кто мог подумать - ничья!'
        )
