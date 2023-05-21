import sqlite3
from typing import Optional
from config import bot, ADMINS
from sqlite3 import Connection, Cursor, Error
from aiogram.dispatcher import FSMContext
from aiogram import types


conn: Optional[Connection] = None
cursor: Optional[Cursor] = None


async def sql_create_db_conection():
    try:
        global conn, cursor
        conn = sqlite3.connect('database/sqllite3.db')
        cursor = conn.cursor()
    except Error as e:
        for admin_id in ADMINS:
            await bot.send_message(
                admin_id,
                f'Ошибка создания БД:\n{e}')
        raise e


async def sql_create_table():
    await sql_create_db_conection()

    if not conn or not cursor:
        raise AttributeError

    try:
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS mentors (
                id INTEGER PRIMARY KEY,
                telegram_id INTEGER UNIQUE,
                name VARCHAR(50) NOT NULL,
                course_name VARCHAR(50) NOT NULL,
                age INTEGER CHECK (age BETWEEN 1 and 80) NOT NULL,
                group_name VARCHAR(10) NOT NULL
            );
            '''
        )
    except Error as e:
        for admin_id in ADMINS:
            await bot.send_message(
                admin_id,
                f'Ошибка создания таблицы БД:\n{e}')
        raise e


async def sql_insert_mentor(msg: types.Message, state: FSMContext):
    if not conn or not cursor:
        raise AttributeError

    async with state.proxy() as proxy_data:
        try:
            cursor.execute(
                '''
                INSERT INTO mentors (
                    telegram_id, name, course_name, age, group_name
                ) VALUES (
                    ?, ?, ?, ?, ?
                );
                ''',
                tuple(proxy_data.values())
            )

            conn.commit()
        except Error as e:
            await msg.reply(f'Ошибка вставки данных в БД:\n{e}')
            raise e


async def sql_select_all_mentors(msg: types.Message):
    if not conn or not cursor:
        raise AttributeError

    all_db_rows = None
    try:
        all_db_rows = cursor.execute(
            '''
            SELECT * FROM mentors
            '''
        ).fetchall()
    except Error as e:
        await msg.reply(f'Ошибка вставки данных в БД:\n{e}')
        raise e

    return all_db_rows


async def sql_delete_mentor(msg: types.Message, telegram_id: str):
    if not conn or not cursor:
        raise AttributeError

    try:
        cursor.execute(
            '''
            DELETE FROM mentors
            WHERE telegram_id = ?
            ''',
            (telegram_id,)
        )
        conn.commit()
        await msg.reply('Ментор успешно удален из БД!')
    except Error as e:
        await msg.reply(f'Ошибка удаления данных из БД:\n{e}')
        raise e
