import os

from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('API_KEY')
API_HOST = "hotels4.p.rapidapi.com"

MAX_HOTELS = 10
MAX_PHOTO = 10
HISTORY_DEPTH = 2

DEFAULT_COMMANDS = (
    ('start', 'Запустить бота'),
    ('lowprice', 'Самые дешевые отели'),
    ('highprice', 'Самые дорогие отели'),
    ('bestdeal', 'Самые дешёвые отели ближайшие к центру города'),
    ('history', 'История запросов'),
    ('setting', 'Настройки бота'),
    ('help', 'Показать помощь')

)
