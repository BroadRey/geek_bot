from sqlite3 import Error

from aiogram import Dispatcher, types
from database import db
from filters.filters import IsPrivateChat
from private_chat_logics.parsers.rezka_parser import parse_rezka


def register_command_handlers(dispatcher: Dispatcher) -> None:
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

    dispatcher.register_message_handler(
        films_command_handler,
        IsPrivateChat(),
        commands=['film']
    )


async def all_mentors_command_handler(msg: types.Message) -> None:
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


async def delete_mentor_command_handler(msg: types.Message) -> None:
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


async def films_command_handler(msg: types.Message) -> None:
    for film_data in parse_rezka():
        inline_markup = types.InlineKeyboardMarkup()
        inline_button = types.InlineKeyboardButton(
            "Кликни, чтобы посмотреть", url=film_data['url']
        )
        inline_markup.add(inline_button)

        await msg.answer_photo(
            film_data['img'],
            caption='Название:\n'
                    f'<a href="{film_data["url"]}">{film_data["title"]}</a>\n\n'
                    'Дата выхода:\n'
                    f'#year_{film_data["year"]}\n\n'
                    'Страна:\n'
                    f'#{film_data["country"]}\n\n'
                    'Жанр:\n'
                    f'#{film_data["genre"]}',
            reply_markup=inline_markup,
            parse_mode=types.ParseMode.HTML
        )
