import telebot
import lowprice
from telebot import formatting
from typing import Optional
from bot import bot


MAX_HOTELS = 10
MAX_PHOTO = 10


@bot.message_handler(commands=['lowprice'])
def low_price(message):
    lowprice.first_step(message)


@bot.message_handler(content_types='text')
def answer(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id, 'Такая команда мне не понятна...')


bot.infinity_polling()
