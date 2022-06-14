import telebot
from telebot.types import Message, CallbackQuery
from typing import Dict, List
import step_functions
from bot import bot, query_container, MAX_HOTELS, MAX_PHOTO


def first_step(message: Message):
    bot.send_message(message.chat.id, 'Введите город для поиска')
    bot.register_next_step_handler(message, step_functions.print_destinations)


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'destination')
def callback(call: CallbackQuery):
    bot.answer_callback_query(callback_query_id=call.id, text='Выполнено')
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=f'Сколько отелей показать? Не больше {MAX_HOTELS}'
    )
    query_container.destination_id = call.data.split(':')[1]
    bot.register_next_step_handler(call.message, step_functions.show_photo)


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'photo')
def callback(call: CallbackQuery):
    bot.answer_callback_query(callback_query_id=call.id, text='Выполнено')
    if call.data.split(':')[1] == 'yes':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=f'Сколько фотографий показать? Не больше {MAX_PHOTO}'
        )
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
