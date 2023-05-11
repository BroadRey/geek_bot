import emoji
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from decouple import config

API_TOKEN = config('TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(msg: types.Message):
    await msg.reply(emoji.emojize('Я - бот! :robot:\n'
                                  'Будем знакомы!'), )


@dp.message_handler(commands=['quiz'])
async def generate_quiz_command(msg: types.Message):
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


@dp.callback_query_handler(text='next')
async def next_quiz_command(call: types.CallbackQuery):
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


@dp.message_handler(commands=['mem'])
async def send_mem_command(msg: types.Message):
    photo = InputFile('./pic/mem.jpg')
    await msg.reply_photo(
        photo=photo,
    )


@dp.message_handler()
async def echo(msg: types.Message):
    if msg.text.isnumeric():
        input_number = str(int(msg.text) ** 2)
        await msg.reply(input_number)
        return
    
    await msg.reply(msg.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)