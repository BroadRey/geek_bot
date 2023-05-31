from sqlite3 import IntegrityError
import filters.filters as handler_filters
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import ADMINS
from database import db


def register_form_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        mentor_registration_command_handler,
        handler_filters.IsPrivateChat(),
        commands=['mentor_registration']
    )
    dispatcher.register_message_handler(
        cancel_command_handler,
        state='*',
        commands=['cancel']
    )

    dispatcher.register_message_handler(
        process_choosing_mentor_telegram_id,
        state=MentorRegistrator.choosing_mentor_telegram_id,
    )

    dispatcher.register_message_handler(
        process_choosing_mentor_name,
        state=MentorRegistrator.choosing_mentor_name,
    )

    dispatcher.register_message_handler(
        process_choosing_mentor_course,
        state=MentorRegistrator.choosing_mentor_course,
    )

    dispatcher.register_message_handler(
        process_choosing_mentor_age,
        state=MentorRegistrator.choosing_mentor_age,
    )

    dispatcher.register_message_handler(
        process_choosing_mentor_group,
        state=MentorRegistrator.choosing_mentor_group,
    )


class MentorRegistrator(StatesGroup):
    choosing_mentor_telegram_id = State()
    choosing_mentor_name = State()
    choosing_mentor_course = State()
    choosing_mentor_age = State()
    choosing_mentor_group = State()


async def cancel_command_handler(msg: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state:
        await state.finish()
        await msg.answer("Добавление ментора прервано!")


async def mentor_registration_command_handler(msg: types.Message) -> None:
    if int(msg.from_user.id) not in ADMINS:
        return

    await msg.answer(text="Введите Telegram ID ментора:")
    await MentorRegistrator.choosing_mentor_telegram_id.set()


async def process_choosing_mentor_telegram_id(msg: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['telegram_id'] = msg.text

    await msg.answer(text="Введите имя ментора:")
    await MentorRegistrator.next()


async def process_choosing_mentor_name(msg: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = msg.text

    await msg.answer(text="Введите имя направление ментора:")
    await MentorRegistrator.next()


async def process_choosing_mentor_course(msg: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['course'] = msg.text

    await msg.answer(text="Введите возраст ментора:")
    await MentorRegistrator.next()


async def process_choosing_mentor_age(msg: types.Message, state: FSMContext) -> None:
    if not msg.text.isdigit():
        await msg.reply('Возраст должен быть целым числом!')
        return

    if not (1 <= int(msg.text) < 80):
        await msg.reply('Возраст должен быть в диапазоне [1; 80)')
        return

    async with state.proxy() as data:
        data['age'] = msg.text

    await msg.answer(text="Введите группу ментора:")
    await MentorRegistrator.next()


async def process_choosing_mentor_group(msg: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['group'] = msg.text

    try:
        await db.sql_insert_mentor(msg, state)
        await msg.answer('Ментор успешно добавлен в БД!')
    except IntegrityError:
        await msg.answer('Ментор с такими данными уже есть в БД!')
    finally:
        await state.finish()