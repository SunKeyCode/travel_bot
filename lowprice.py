from telebot.types import Message, CallbackQuery
import step_functions
from bot import bot, query_container, queries, QueryContainer, MAX_HOTELS, MAX_PHOTO
from typing import Dict


def first_step(message: Message):
    bot.send_message(message.chat.id, 'Введите название города для поиска:')
    queries[message.chat.id]: Dict[QueryContainer] = QueryContainer(message.chat.id)
    bot.register_next_step_handler(message, step_functions.print_destinations)


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'destination')
def destination_callback(call: CallbackQuery):
    bot.answer_callback_query(callback_query_id=call.id, text='Выполнено')
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=f'Сколько отелей показать? Не больше {MAX_HOTELS}'
    )
    queries[call.message.chat.id].destination_id = call.data.split(':')[1]
    query_container.destination_id = call.data.split(':')[1]
    bot.register_next_step_handler(call.message, step_functions.show_photo)


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'photo')
def photo_callback(call: CallbackQuery):
    bot.answer_callback_query(callback_query_id=call.id, text='Выполнено')
    if call.data.split(':')[1] == 'yes':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=f'Сколько фотографий показать? Не больше {MAX_PHOTO}'
        )
        queries[call.message.chat.id].show_photo = True
        queries[call.message.chat.id].photo_count = call.data.split(':')[1]
        query_container.show_photo = True
        query_container.photo_count = call.data.split(':')[1]
        step_functions.print_hotels(message=call.message, no_photo=False)
    elif call.data.split(':')[1] == 'no':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=f'Вот отели, которые я нашел:'
        )
        step_functions.print_hotels(message=call.message, no_photo=True)
