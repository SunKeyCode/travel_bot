import sqlite3 as sq
import os

from telebot.types import Message
from loader import QueryContainer
from utils.format import format_history
from typing import List
from datetime import datetime, timedelta


def get_path() -> str:
    directory = 'database'
    file = 'tet_bot.db'
    db_path = os.path.join(directory, file)

    return db_path


def check_user_settings(message: Message):
    with sq.connect('database/tet_bot.db') as connect:
        cursor = connect.cursor()

        cursor.execute(f'SELECT user_id FROM settings WHERE user_id == {int(message.chat.id)}')
        result = cursor.fetchall()

        if not result:
            cursor.execute(f'INSERT INTO settings (user_id) VALUES ({int(message.chat.id)})')


def check_sql_tables() -> None:
    with sq.connect('database/tet_bot.db') as con:
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

    with sq.connect('database/tet_bot.db') as sql_connect:
        cursor = sql_connect.cursor()
        cursor.execute(
            'INSERT INTO queries (user_id, command, date, time, params, result) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, command, date, time, params.__repr__(), result)
        )


def read_history(message: Message, depth: int) -> List:

    date_filter = (datetime.now().date() - timedelta(depth)).strftime('%Y-%m-%d')

    with sq.connect('database/tet_bot.db') as sql_connect:  # сделать через модуль os?
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


if __name__ == '__main__':
    print(get_path())
