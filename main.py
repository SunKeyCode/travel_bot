import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import lowprice
import hotels_api_requests
from telebot import formatting
from telebot.callback_data import CallbackData, CallbackDataFilter
import time


MAX_HOTELS = 10
MAX_PHOTO = 10


city_callback = CallbackData('destination_id', prefix='city')
TOKEN = '5178171548:AAGudbH7zz4sJpE6UNW1e2DX5ALUhy6ZS9w'
bot = telebot.TeleBot(TOKEN)


def gen_markup():
    markup = InlineKeyboardMarkup()
    # markup.row_width = 2)
    return markup


def show_hotels(message):
    hotels = lowprice.hotel_attrs()
    for i_hotel in hotels:
        bot.send_message(message.chat.id, i_hotel, parse_mode='HTML')


def get_city(message):
    city = message.text
    print(message)

    destinations = hotels_api_requests.get_destinations()
    markup = gen_markup()
    for i_dest in destinations:
        markup.add(InlineKeyboardButton(
            f'{i_dest["name"]}, {i_dest["caption"]}',
            callback_data=city_callback.new(destination_id=i_dest['destinationId']))
            )
    bot.send_message(
        message.chat.id, f'По запросу {city} мы нашли такие варианты:',
        reply_markup=markup,
        )


@bot.message_handler(commands=['lowprice'])
def low_price(message):
    bot.send_message(message.chat.id, 'Введите город для поиска')
    bot.register_next_step_handler(message, get_city)


@bot.message_handler(content_types='text')
def answer(message: telebot.types.Message) -> None:
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет! Я будущий чат бот турагенства.')


@bot.callback_query_handler(func=None)
def callback(call: telebot.types.CallbackQuery):
    callback_data: dict = city_callback.parse(callback_data=call.data)
    if callback_data['@'] == 'city':
        # bot.send_message(call.message.chat.id, callback_data['destination_id'])
        bot.answer_callback_query(callback_query_id=call.id, text='Выполнено')
        # bot.edit_message_text(
        #     chat_id=call.message.chat.id,
        #     message_id=call.message.id,
        #     text='Ищем отели...'
        # )
        time.sleep(0.5)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=f'Сколько отелей показать? Не больше {MAX_HOTELS}'
            )
        # bot.send_message(call.message.chat.id, f'Сколько отелей показать? Не больше {MAX_HOTELS}')
        bot.register_next_step_handler(call.message, show_hotels)


bot.infinity_polling()
