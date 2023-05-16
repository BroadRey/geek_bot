import csv
import os

import filters.filters as handler_filters
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import ADMINS


def register_form_handlers(dispatcher: Dispatcher):
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
        process_choosing_mentor_id,
        state=MentorRegistrator.choosing_mentor_id,
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
    choosing_mentor_id = State()
    choosing_mentor_name = State()
    choosing_mentor_course = State()
    choosing_mentor_age = State()
    choosing_mentor_group = State()


async def mentor_registration_command_handler(msg: types.Message):
    if int(msg.from_user.id) not in ADMINS:
        return

    await msg.answer(text="Введите ID ментора:")
    await MentorRegistrator.choosing_mentor_id.set()


async def cancel_command_handler(msg: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.finish()
        await msg.answer("Добавление ментора прервано!")


async def process_choosing_mentor_id(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = msg.text

    await MentorRegistrator.next()
    await msg.answer(text="Введите имя ментора:")


async def process_choosing_mentor_name(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text

    await MentorRegistrator.next()
    await msg.answer(text="Введите имя направление ментора:")


async def process_choosing_mentor_course(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['course'] = msg.text

    await MentorRegistrator.next()
    await msg.answer(text="Введите возраст ментора:")


async def process_choosing_mentor_age(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = msg.text

    await MentorRegistrator.next()
    await msg.answer(text="Введите группу ментора:")


async def process_choosing_mentor_group(msg: types.Message, state: FSMContext):
    proxy_data = {}
    async with state.proxy() as data:
        proxy_data = data.as_dict()
    await state.finish()

    with open(f'{os.path.dirname(__file__)}/../form_data/fsmAdminMentor.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([
            proxy_data['id'],
            proxy_data['name'],
            proxy_data['course'],
            proxy_data['age'],
            msg.text],
        )