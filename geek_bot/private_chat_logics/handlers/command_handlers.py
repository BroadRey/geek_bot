from sqlite3 import Error

from aiogram import Dispatcher, types
from database import db
from filters.filters import IsPrivateChat


def register_command_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        all_mentors_command_handler,
        IsPrivateChat(),
        commands=['all_mentors']
    )

    dispatcher.register_message_handler(
        delete_mentor_command_handler,
        IsPrivateChat(),
        commands=['delete_mentor']
    )


async def all_mentors_command_handler(msg: types.Message):
    all_mentors_data = await db.sql_select_all_mentors(msg)

    if not all_mentors_data:
        await msg.reply('Список менторов пуст!')
        return

    all_mentors_names = []
    for _, telegram_id, name, _, _, group_name in all_mentors_data:
        if name in all_mentors_names:
            all_mentors_names.append(f'{telegram_id}. {name} ({group_name})')
            continue

        all_mentors_names.append(f'{telegram_id}. {name}')

    result = '\n'.join(all_mentors_names)
    await msg.reply(result)


async def delete_mentor_command_handler(msg: types.Message):
    msg_args = msg.text.split()

    command_format = (
        'Команду необходимо вводить в следующем формате:\n'
        '/delete_mentor <id> (int)'
    )
    if len(msg_args) != 2:
        await msg.reply(command_format)
        return

    user_id = msg_args[1]

    if not user_id.isdigit():
        await msg.reply(command_format)
        return

    try:
        await db.sql_delete_mentor(msg, user_id)
    except Error as e:
        await msg.reply(str(e))