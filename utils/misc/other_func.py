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


def distance_from_str(distance_str: str) -> float:
    distance_str = distance_str.split()[0]
    if distance_str.count(','):
        distance_str = distance_str.replace(',', '.')
    return float(distance_str)


def miles_to_kilometers(value: float) -> float:
    return round(value * 1.609344, 2)


def kilometers_to_miles(value: float) -> float:
    return round(value / 1.609344, 2)
