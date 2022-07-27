from telebot.types import CallbackQuery

import step_functions
import keyboards.inline.inline_markup as inline_markup
import database.DB as DB

from loader import bot, queries, Steps
from config_data import config
from datetime import date


def callback_to_date(callback_data: str) -> date:
    callback_list = callback_data.split(':')
    result = date(int(callback_list[1]), int(callback_list[2]), int(callback_list[3]))
    return result


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'date_choice')
def calendar_callback(call: CallbackQuery) -> None:
    """Получение даты из календаря"""
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text='✅ ' + callback_to_date(call.data).strftime('%d.%m.%Y')
    )
    callback_date = callback_to_date(call.data)
    if queries[call.message.chat.id].checkin_date is None:
        if callback_date >= date.today():
            queries[call.message.chat.id].checkin_date = callback_date
            step_functions.next_step(call.message, Steps.checkin_date)
        else:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text='❌ Дата заезда не должна быть меньше текущей даты! Попробуем еще раз:'
            )
            step_functions.get_date(call.message, 'Выберите дату заезда 📅:')
    else:
        if callback_date > queries[call.message.chat.id].checkin_date:
            queries[call.message.chat.id].checkout_date = callback_date
            step_functions.next_step(call.message, Steps.checkout_date)
        else:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text='❌ Дата выезда должна быть больше даты заезда! Попробуем еще раз:'
            )
            step_functions.get_date(
                message=call.message,
                text='Выберите дату выезда 📅:',
                limit_date=queries[call.message.chat.id].checkin_date
            )


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'change_month')
def change_month(call: CallbackQuery) -> None:
    """Функция для выбора следующего/предыдущего месяца в календаре"""
    callback_data: dict = inline_markup.change_month_callback.parse(callback_data=call.data)
    year, month = int(callback_data['year']), int(callback_data['month'])

    if queries[call.message.chat.id].checkin_date:
        limit_date = queries[call.message.chat.id].checkin_date
    else:
        limit_date = date.today()

    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.id,
        reply_markup=inline_markup.calendar_days_markup(year=year, month=month, limit_date=limit_date)
    )


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'destination')
def destination_callback(call: CallbackQuery):
    """Получение destination"""
    bot.answer_callback_query(callback_query_id=call.id, text='Выполнено')
    destination_id = call.data.split(':')[1]
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text='✅ ' + queries[call.message.chat.id].destinations[destination_id]
    )
    queries[call.message.chat.id].destination_id = destination_id
    step_functions.next_step(call.message, Steps.destination)


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'photo')
def photo_callback(call: CallbackQuery):
    """Показывать фотографии или нет"""
    if call.data.split(':')[1] == 'yes':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=f'Сколько фотографий показать? Не больше {config.MAX_PHOTO}'
        )
        queries[call.message.chat.id].show_photo = True
        queries[call.message.chat.id].photo_count = call.data.split(':')[1]
        bot.register_next_step_handler(call.message, step_functions.print_hotels)
    elif call.data.split(':')[1] == 'no':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=f'Ищем отели... ⌛'
        )
        step_functions.print_hotels(message=call.message)


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'settings')
def settings_callback(call: CallbackQuery):
    """Навигация по меню настроек бота (команды settings)"""
    submenu = call.data.split(':')[1]
    data = call.data.split(':')[2]

    if submenu == 'main':
        if data == 'locale':
            current = DB.get_locale(call.message)
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                reply_markup=inline_markup.settings_markup(mode='locale', current=current))
        elif data == 'currency':
            current = DB.get_currency(call.message)
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                reply_markup=inline_markup.settings_markup(mode='currency', current=current))
        elif data == 'exit':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text='Настройка завершена.'

            )

    elif submenu == 'locale':
        if data == 'exit':
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                reply_markup=inline_markup.settings_markup(mode='main'))
        else:
            if DB.get_locale(call.message) != data:
                DB.set_locale(call.message, data)
                bot.edit_message_reply_markup(
                    chat_id=call.message.chat.id,
                    message_id=call.message.id,
                    reply_markup=inline_markup.settings_markup(mode='locale', current=data))
            else:
                bot.answer_callback_query(callback_query_id=call.id, text='Значение уже установлено!', cache_time=2)

    elif submenu == 'currency':
        if data == 'exit':
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                reply_markup=inline_markup.settings_markup(mode='main'))
        else:
            if DB.get_currency(call.message) != data:
                DB.set_currency(call.message, data)
                bot.edit_message_reply_markup(
                    chat_id=call.message.chat.id,
                    message_id=call.message.id,
                    reply_markup=inline_markup.settings_markup(mode='currency', current=data))
            else:
                bot.answer_callback_query(callback_query_id=call.id, text='Значение уже установлено!', cache_time=2)
