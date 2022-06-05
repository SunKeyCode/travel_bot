import telebot
import lowprice
from telebot import formatting
from typing import Optional
from bot import bot


MAX_HOTELS = 10
MAX_PHOTO = 10


class QueryContainer:

    def __init__(self):
        self.destination_id: Optional[str] = None
        self.hotels = list()
        self.hotel_count: int = MAX_HOTELS
        self.show_photo: bool = False
        self.photo_count: int = MAX_PHOTO

    def __str__(self):
        return '{destination_id}{hotels}{hotel_count}{show_photo}{photo_count}'.format(
            destination_id=self.destination_id,
            hotels=self.hotels,
            hotel_count=self.hotel_count,
            show_photo=self.show_photo,
            photo_count=self.photo_count
        )


query_container = QueryContainer()


@bot.message_handler(commands=['lowprice'])
def low_price(message):
    lowprice.first_step(message)


@bot.message_handler(content_types='text')
def answer(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id, 'Такая команда мне не понятна...')


bot.infinity_polling()
