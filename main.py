import telebot
from telebot.types import InputMediaPhoto
import lowprice
import hotels_api_requests
from telebot import formatting
from telebot.callback_data import CallbackData
import time
import json
from typing import Optional
from markup import yes_no_markup, destination_markup
from lowprice import lowprice_command
from commands import LowPrice


MAX_HOTELS = 10
MAX_PHOTO = 10


class QueryContainer:

    def __init__(self):
        self.destination_id: Optional[str] = None
        self.hotels = list()
        self.hotel_count: int = MAX_HOTELS
        self.show_photo: bool = False
        self.photo_count: int = MAX_PHOTO


TOKEN = '5178171548:AAGudbH7zz4sJpE6UNW1e2DX5ALUhy6ZS9w'
bot = telebot.TeleBot(TOKEN)
query_container = QueryContainer()


@bot.message_handler(commands=['lowprice'])
def low_price(message):
    bot.send_message(message.chat.id, 'Введите город для поиска')
    bot.register_next_step_handler(message, get_destination)


@bot.message_handler(content_types='text')
def answer(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id, 'Такая команда мне не понятна...')


def get_destination(message):
    destinations = hotels_api_requests.get_destinations()
    markup = destination_markup(destinations)
    bot.send_message(
        message.chat.id, f'Что из этого Вы имели ввиду?:',
        reply_markup=markup,
    )


def show_photo(message):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'О-оу! Тут нужно вводить цифру.')
        bot.register_next_step_handler(message, show_photo)
        return
    elif (int(message.text) < 1) or (int(message.text) > MAX_HOTELS):
        bot.send_message(message.chat.id, f'Количество должно быть от 1 до {MAX_HOTELS}')
        bot.register_next_step_handler(message, show_photo)
        return

    query_container.hotel_count = int(message.text)
    markup = yes_no_markup()
    bot.send_message(message.chat.id, 'Показать фото отелей?', reply_markup=markup)


def print_hotels(message) -> None:
    hotels = lowprice.hotel_attrs(query_container.hotel_count)

    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'О-оу! Тут нужно вводить цифру.')
        bot.register_next_step_handler(message, print_hotels)
        return
    elif (int(message.text) < 1) or (int(message.text) > MAX_HOTELS):
        bot.send_message(message.chat.id, f'Количество должно быть от 1 до {MAX_PHOTO}')
        bot.register_next_step_handler(message, print_hotels)
        return

    query_container.photo_count = int(message.text)
    with open('photo_634418464.json', 'r') as file:
        data = json.load(file)
    media = list()

    for photo in lowprice.formatted_photo_data(data, limit=query_container.photo_count):
        media.append(InputMediaPhoto(photo, 'Hotel'))
    for i_hotel in hotels:
        bot.send_message(message.chat.id, i_hotel, parse_mode='HTML')
        bot.send_media_group(message.chat.id, media)


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'destination')
def callback(call: telebot.types.CallbackQuery):

    bot.answer_callback_query(callback_query_id=call.id, text='Выполнено')
    time.sleep(0.4)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=f'Сколько отелей показать? Не больше {MAX_HOTELS}'
    )

    query_container.destination_id = call.data.split(':')[1]
    bot.register_next_step_handler(call.message, show_photo)


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'photo')
def callback(call: telebot.types.CallbackQuery):
    bot.answer_callback_query(callback_query_id=call.id, text='Выполнено')
    if call.data.split(':')[1] == 'yes':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=f'Сколько фотографий показать? Не больше {MAX_PHOTO}'
        )

        query_container.show_photo = True
        query_container.photo_count = call.data.split(':')[1]
        bot.register_next_step_handler(call.message, print_hotels)
    elif call.data.split(':')[1] == 'no':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=f'Вот отели, которые я нашел:'
        )
        hotels = lowprice.hotel_attrs(query_container.hotel_count)
        for i_hotel in hotels:
            bot.send_message(call.message.chat.id, i_hotel, parse_mode='HTML')


bot.infinity_polling()
