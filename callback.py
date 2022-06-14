from telebot.types import Message, CallbackQuery
from bot import bot, queries, MAX_HOTELS, MAX_PHOTO


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


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'date_choice')
def calendar_callback(call: CallbackQuery):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=date_parse(call.data, 'print')
    )

    if queries[call.message.chat.id].checkin_date is None:
        queries[call.message.chat.id].checkin_date = date_parse(call.data)
    else:
        queries[call.message.chat.id].checkout_date = date_parse(call.data)
    print(queries[call.message.chat.id])
    # bot.send_message(call.message.chat.id, call.data)
