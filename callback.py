from telebot.types import Message, CallbackQuery

import step_functions
from bot import bot, queries, MAX_HOTELS, MAX_PHOTO
from markup import change_month_callback, date_choice_callback, calendar_days_markup
from datetime import datetime, date


def date_parse(callback_data: str, mode='query') -> str:
    callback_list = callback_data.split(':')
    if mode == 'print':
        res_string = '{day:02d}.{month:02d}.{year}'.format(
            year=int(callback_list[1]),
            month=int(callback_list[2]),
            day=int(callback_list[3])
        )
    else:
        res_string = '{year}-{month:02d}-{day:02d}'.format(
            year=int(callback_list[1]),
            month=int(callback_list[2]),
            day=int(callback_list[3])
        )

    return res_string


def callback_to_date(callback_data: str) -> date:
    callback_list = callback_data.split(':')
    result = date(int(callback_list[1]), int(callback_list[2]), int(callback_list[3]))

    return result


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'date_choice')
def calendar_callback(call: CallbackQuery) -> None:
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=callback_to_date(call.data).strftime('%d.%m.%Y')
    )
    callback_date = callback_to_date(call.data)
    if queries[call.message.chat.id].checkin_date is None:
        if callback_date >= date.today():
            queries[call.message.chat.id].checkin_date = callback_date
            step_functions.next_step(call.message, 'checkin_date')
        else:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text='Дата заезда не должна быть меньше текущей даты! Попробуем еще раз:'
            )
            step_functions.get_date(call.message, 'Выберите дату заезда:')
    else:
        if callback_date > queries[call.message.chat.id].checkin_date:
            queries[call.message.chat.id].checkout_date = callback_date
            step_functions.next_step(call.message, 'checkout_date')
        else:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text='Дата выезда должна быть больше даты заезда! Попробуем еще раз:'
            )
            step_functions.get_date(call.message, 'Выберите дату выезда:')


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'change_month')
def change_month(call: CallbackQuery) -> None:
    callback_data: dict = change_month_callback.parse(callback_data=call.data)
    year, month = int(callback_data['year']), int(callback_data['month'])
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.id,
        reply_markup=calendar_days_markup(year=year, month=month)
    )
