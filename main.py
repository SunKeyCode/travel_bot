import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import lowprice
from telebot import formatting


TOKEN = '5178171548:AAGudbH7zz4sJpE6UNW1e2DX5ALUhy6ZS9w'
bot = telebot.TeleBot(TOKEN)


def gen_markup():
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, input_field_placeholder='123')
    markup.row_width = 2
    # markup.add(InlineKeyboardButton(text, callback_data="cb_yes"), InlineKeyboardButton("No", callback_data="cb_no"))
    return markup


def get_city(message):
    city = message.text

    cities = lowprice.get_cities()
    markup = gen_markup()
    for i_city in cities:
        city_str = f'{i_city["name"]}\n {i_city["caption"]}'

        markup.add(KeyboardButton(city_str))
    bot.send_message(message.chat.id, f'Вы запросили информацию по городу {city}', reply_markup=markup)
    # markup = telebot.types.ReplyKeyboardRemove()
    # bot.send_message(message.from_user.id, "Done with Keyboard", reply_markup=markup)


@bot.message_handler(commands=['lowprice'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Введите город для поиска')
    bot.register_next_step_handler(message, get_city)


@bot.message_handler(content_types='text')
def answer(message: telebot.types.Message) -> None:
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет! Я будущий чат бот турагенства.')


bot.infinity_polling()

