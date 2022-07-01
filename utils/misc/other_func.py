from re import fullmatch
from loader import Commands


def format_date(date: str) -> str:
    new_date = date.split('-')
    new_date = new_date[::-1]
    return '.'.join(new_date)


def define_lang(text: str) -> str:
    if fullmatch(r'[а-яА-Я\W\d]+', text) is not None:
        return 'ru_RU'
    else:
        return 'en_US'


def get_sort_order(command: Commands) -> str:
    if command == Commands.lowprice:
        return 'PRICE'
    elif command == Commands.highprice:
        return 'PRICE_HIGHEST_FIRST'
    elif command == Commands.bestdeal:
        return 'DISTANCE_FROM_LANDMARK'
