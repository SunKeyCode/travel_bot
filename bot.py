import telebot
from typing import Optional


TOKEN = '5178171548:AAGudbH7zz4sJpE6UNW1e2DX5ALUhy6ZS9w'
bot = telebot.TeleBot(TOKEN)

MAX_HOTELS = 10
MAX_PHOTO = 10


queries = dict()


class QueryContainer:

    def __init__(self):
        self.destination_id: Optional[str] = None
        self.hotels = list()
        self.hotel_count: int = MAX_HOTELS
        self.show_photo: bool = False
        self.photo_count: int = MAX_PHOTO
        self.language = 'en_US'

    def __str__(self):
        return 'destination_id={destination_id}\nhotels={hotels}\nhotel_count={hotel_count}\n' \
                'show_photo={show_photo}\nphoto_count={photo_count}\nlang={language}'.format(
                    destination_id=self.destination_id,
                    hotels=self.hotels,
                    hotel_count=self.hotel_count,
                    show_photo=self.show_photo,
                    photo_count=self.photo_count,
                    language=self.language
                )


query_container = QueryContainer()
