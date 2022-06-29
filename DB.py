import sqlite3 as sq
from telebot.types import Message
from bot import QueryContainer
from datetime import datetime
from format import format_history
from typing import Dict, List
from datetime import datetime, timedelta


def check_settings_table(message: Message):
    with sq.connect('tet_bot.bd') as con:
        cursor = con.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS settings (
            user_id INTEGER PRIMARY KEY,
            locale TEXT DEFAULT 'en_US',
            currency TEXT DEFAULT 'USD'
            )"""
        )

        cursor.execute(f'SELECT user_id FROM settings WHERE user_id == {int(message.chat.id)}')
        result = cursor.fetchall()

        if not result:
            cursor.execute(f'INSERT INTO settings (user_id) VALUES ({int(message.chat.id)})')


def check_sql_tables() -> None:
    with sq.connect('tet_bot.bd') as con:
        cursor = con.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS settings (
            user_id INTEGER PRIMARY KEY UNIQUE,
            locale TEXT DEFAULT 'en_US',
            currency TEXT DEFAULT 'USD'
            )"""
        )

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


def write_history(query: QueryContainer):

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

    try:
        con = sq.connect('tet_bot.bd')
        cursor = con.cursor()
        cursor.execute(
            'INSERT INTO queries (user_id, command, date, time, params, result) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, command, date, time, params.__repr__(), result)
        )
        con.commit()
        cursor.close()
    except sq.Error as exc:
        print(exc)
    finally:
        if (con):
            con.close()


def get_history(message: Message, depth: int) -> List:
    try:
        date_filter = (datetime.now().date() - timedelta(depth)).strftime('%Y-%m-%d')

        sql_connect = sq.connect('tet_bot.bd')
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

        sql_connect.commit()
        cursor.close()

        return result
    except sq.Error as exc:
        print(exc)
    finally:
        if sql_connect:
            sql_connect.close()
