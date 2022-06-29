import telebot
import enum
from datetime import date
from typing import Optional, Dict


TOKEN = '5178171548:AAGudbH7zz4sJpE6UNW1e2DX5ALUhy6ZS9w'
bot = telebot.TeleBot(TOKEN)

MAX_HOTELS = 10
MAX_PHOTO = 10


class Steps(enum.Enum):

    destination = 'destination'
    checkin_date = 'checkin_date'
    checkout_date = 'checkout_date'


class Commands(enum.Enum):

    lowprice = 'lowprice'
    highprice = 'highprice'
    bestdeal = 'bestdeal'
    history = 'history'


class QueryContainer:

    def __init__(self, user_id: int, command: Commands) -> None:
        self.user = user_id
        self.command = command
        self.destination_id: Optional[str] = None
        self.destinations: Dict[str, str] = dict()
        self.hotels = list()
        self.hotel_count: int = 0
        self.show_photo: bool = False
        self.photo_count: int = 0
        self.language: str = 'en_US'
        self.currency: str = 'USD'
        self.checkin_date: Optional[date] = None
        self.checkout_date: Optional[date] = None
        self.min_price: Optional[int] = None
        self.max_price: Optional[int] = None
        self.max_distance: Optional[float] = None

    def __str__(self):
        return 'user={user}\ndestination_id={destination_id}\nhotels={hotels}\nhotel_count={hotel_count}\n' \
                'show_photo={show_photo}\nphoto_count={photo_count}\nlang={language}\ncommand={command}\n' \
               'check_in={check_in}\ncheck_out={check_out}\nmin_price={min_price}\nmax_price={max_price}\n' \
               'max_distance={max_distance}\n'.format(
                    user=self.user,
                    destination_id=self.destination_id,
                    hotels=self.hotels,
                    hotel_count=self.hotel_count,
                    show_photo=self.show_photo,
                    photo_count=self.photo_count,
                    language=self.language,
                    command=self.command,
                    check_in=self.checkin_date,
                    check_out=self.checkout_date,
                    min_price=self.min_price,
                    max_price=self.max_price,
                    max_distance=self.max_distance
                    )


queries: Dict[int, QueryContainer] = dict()
