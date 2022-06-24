from telebot.types import Message, CallbackQuery

import step_functions
from bot import bot, queries, Steps, MAX_HOTELS, MAX_PHOTO
from markup import change_month_callback, calendar_days_markup
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
            step_functions.get_date(call.message, 'Выберите дату выезда 📅:')


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'change_month')
def change_month(call: CallbackQuery) -> None:
    """Функция для выбора следующего/предыдущего месяца в календаре"""
    callback_data: dict = change_month_callback.parse(callback_data=call.data)
    year, month = int(callback_data['year']), int(callback_data['month'])
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.id,
        reply_markup=calendar_days_markup(year=year, month=month)
    )


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'destination')
def destination_callback(call: CallbackQuery):
    """Получение destination"""
    bot.answer_callback_query(callback_query_id=call.id, text='Выполнено')
    destination_id = call.data.split(':')[1]
    # bot.send_message(call.message.chat.id, '✅ ' + queries[call.message.chat.id].destinations[destination_id])
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
    bot.answer_callback_query(callback_query_id=call.id, text='Выполнено')
    if call.data.split(':')[1] == 'yes':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=f'Сколько фотографий показать? Не больше {MAX_PHOTO}'
        )
        queries[call.message.chat.id].show_photo = True
        queries[call.message.chat.id].photo_count = call.data.split(':')[1]
        bot.register_next_step_handler(call.message, step_functions.print_hotels)
        # step_functions.print_hotels(message=call.message, no_photo=False)
    elif call.data.split(':')[1] == 'no':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=f'Ищем отели... ⌛'
        )
        step_functions.print_hotels(message=call.message)
