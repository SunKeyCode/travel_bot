import sqlite3 as sq
import os

import logs.logs as log

from telebot.types import Message
from loader import QueryContainer
from utils.format import format_history
from typing import List, Callable
from functools import wraps
from datetime import datetime, timedelta


def get_path() -> str:
    directory = 'database'
    file = 'tet_bot.db'
    db_path = os.path.join(directory, file)

    return db_path


def db_track_exception(func: Callable) -> Callable:
    """Декоратор для отслеживания исключений связанных с базой данных"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sq.Error as exc:
            print(f'{datetime.now()} Ошибка базы данных в функции {__name__}.{func.__name__}:', exc)
            log.error_log(exc, 'Ошибка базы данных', f'{__name__}.{func.__name__}')
            raise sq.Error
    return wrapper


@db_track_exception
def check_user_settings(message: Message):
    with sq.connect(get_path()) as connect:
        cursor = connect.cursor()

        cursor.execute(f'SELECT user_id FROM settings WHERE user_id == {int(message.chat.id)}')
        result = cursor.fetchall()

        if not result:
            cursor.execute(f'INSERT INTO settings (user_id) VALUES ({int(message.chat.id)})')


@db_track_exception
def check_sql_tables() -> None:
    with sq.connect(get_path()) as con:
        cursor = con.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS settings (
            user_id INTEGER PRIMARY KEY UNIQUE,
            locale TEXT DEFAULT 'en_US',
            currency TEXT DEFAULT 'USD'
            )"""
        )

        print('Table "settings" -> OK')

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS queries (
            query_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            user_id INTEGER NOT NULL,
            command TEXT,
            date TEXT,
            time TEXT,
            params TEXT,
            result TEXT
            )"""
        )

        print('Table "queries" -> OK')


@db_track_exception
def write_history(query: QueryContainer) -> None:

    user_id = query.user
    command = query.command.value
    date = datetime.now().date().strftime('%Y-%m-%d')
    time = datetime.now().time().strftime('%H:%M')
    params = dict()
    destination_id = query.destination_id
    params['destination'] = query.destinations[destination_id]
    params['checkin'] = query.checkin_date
    params['checkout'] = query.checkout_date
    params['min_price'] = query.min_price
    params['max_price'] = query.max_price
    params['max_distance'] = query.max_distance

    result = list()
    for elem in query.hotels:
        result.append(format_history(elem, currency=query.currency))
    result = '\n\n'.join(result)

    with sq.connect(get_path()) as sql_connect:
        cursor = sql_connect.cursor()
        cursor.execute(
            'INSERT INTO queries (user_id, command, date, time, params, result) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, command, date, time, params.__repr__(), result)
        )


@db_track_exception
def read_history(message: Message, depth: int) -> List:

    date_filter = (datetime.now().date() - timedelta(depth)).strftime('%Y-%m-%d')

    with sq.connect(get_path()) as sql_connect:
        sql_connect.row_factory = sq.Row
        cursor = sql_connect.cursor()
        cursor.execute(
            f'SELECT command, date, time, params,result FROM queries WHERE user_id == {int(message.chat.id)} '
            f'AND date >= "{date_filter}"'
        )

        result = list()

        for elem in cursor:
            query = dict()
            query['command'] = elem['command']
            query['date'] = elem['date']
            query['time'] = elem['time']
            query['params'] = elem['params']
            query['result'] = elem['result']
            result.append(query)

    return result


@db_track_exception
def set_locale(message: Message, locale: str) -> None:
    with sq.connect(get_path()) as sql_connect:
        cursor = sql_connect.cursor()
        cursor.execute(
            f'UPDATE settings SET locale = "{locale}" WHERE user_id = {int(message.chat.id)}'
        )


@db_track_exception
def set_currency(message: Message, currency: str) -> None:
    with sq.connect(get_path()) as sql_connect:
        cursor = sql_connect.cursor()
        cursor.execute(
            f'UPDATE settings SET currency = "{currency}" WHERE user_id = {int(message.chat.id)}'
        )


@db_track_exception
def get_locale(message: Message) -> str:
    with sq.connect(get_path()) as sql_connect:
        cursor = sql_connect.cursor()
        cursor.execute(
            f'SELECT locale FROM settings WHERE user_id = {int(message.chat.id)}'
        )

        result = cursor.fetchone()

    return result[0]


@db_track_exception
def get_currency(message: Message) -> str:
    with sq.connect(get_path()) as sql_connect:
        cursor = sql_connect.cursor()
        cursor.execute(
            f'SELECT currency FROM settings WHERE user_id = {int(message.chat.id)}'
        )

        result = cursor.fetchone()

    return result[0]

# TODO добавить документацию
