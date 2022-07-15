import re
import datetime  # нужно для функции eval()

import logs.logs as log

from typing import Dict, List, Union
from utils.misc.other_func import format_date


def format_price(price: Union[int, str]) -> str:
    if not isinstance(price, str):
        price = '{price:,d}'.format(price=price)
    if price.count(','):
        price = price.replace(',', ' ')

    return price


def format_hotel(hotel: Dict, date_delta: int, currency: str) -> str:
    if currency == 'USD':
        currency = '$'
    elif currency == 'RUB':
        currency = 'руб.'

    name = hotel['name']
    address = list()
    address.append(hotel['address'].get('postalCode', ''))
    address.append(hotel['address']['countryName'])
    address.append(hotel['address']['region'])
    address.append(hotel['address']['locality'])
    address.append(hotel['address'].get('streetAddress', ''))
    address = list(filter(lambda elem: elem, address))
    address = ', '.join(address)
    try:
        distance = hotel['landmarks'][0]['distance']
    except IndexError:
        distance = '-'

    try:
        price = int(round(float(hotel['ratePlan']['price']['exactCurrent'])))
    except ValueError as exc:
        price = 0
        print(exc)
        log.error_log(exc, f'Ошибка преобразования типа в {hotel}', f'{__name__}.{format_hotel.__name__}')

    try:
        total_price = re.findall(
            r'[0-9,]+(?=\s)',
            hotel['ratePlan']['price'].get('fullyBundledPricePerStay', '')
        )[0]
    except IndexError:
        total_price = date_delta * price

    hotel_content = list()

    hotel_content.append(f'▫<b>Название отеля:</b> {name}')
    hotel_content.append(f'▫<b>Адрес отеля:</b> {address}')
    hotel_content.append(f'▫<b>Расстояние от центра:</b> {distance}')
    hotel_content.append(f'▫<b>Цена за сутки:</b> {format_price(price)} {currency}')
    hotel_content.append(f'▫<b>Общая стоимость:</b> {format_price(total_price)} {currency}')

    return '\n'.join(hotel_content)


def format_history(hotel: Dict, currency: str) -> str:
    if currency == 'USD':
        currency = '$'
    elif currency == 'RUB':
        currency = 'руб.'

    name = hotel['name']

    try:
        distance = hotel['landmarks'][0]['distance']
    except IndexError:
        distance = '-'
    try:
        price = int(round(float(hotel['ratePlan']['price']['exactCurrent'])))
    except ValueError as exc:
        price = 0
        print(exc)
        log.error_log(exc, f'Ошибка преобразования типа в {hotel}', f'{__name__}.{format_hotel.__name__}')

    hotel_content = list()

    hotel_content.append(f'  ▫<b>Название:</b> {name}')
    hotel_content.append(f'  ▫<b>Расстояние от центра:</b> {distance}')
    hotel_content.append(f'  ▫<b>Цена за сутки:</b> {format_price(price)} {currency}')

    return '\n'.join(hotel_content)


def format_photo(photo: Dict, size) -> str:
    try:
        return photo['baseUrl'].format(size=size)
    except KeyError as exc:
        print('Ошибка поиска ключа:', exc)
        log.error_log(exc, 'Ошибка ключа', f'{__name__}.{format_photo.__name__}')
        raise KeyError(f'Ошибка ключа в функции {__name__}.{format_photo.__name__}')


def parse_history_data(data: List) -> List[str]:
    result = list()
    for elem in data:
        params_data = eval(elem["params"])
        params = list()
        params.append(f'    Город: {params_data["destination"]}')
        params.append(f'    Дата заезда: {params_data["checkin"].strftime("%d.%m.%Y")}')
        params.append(f'    Дата выезда: {params_data["checkout"].strftime("%d.%m.%Y")}')
        if params_data["min_price"] is not None:
            params.append(f'    Мин. цена: {params_data["min_price"]}')
        if params_data["max_price"] is not None:
            params.append(f'    Макс. цена: {params_data["max_price"]}')
        if params_data["max_distance"] is not None:
            params.append(f'    Макс. расстояние от центра: {params_data["max_distance"]}')
        params = '\n'.join(params)

        res_string = list()
        res_string.append(f'<u>Дата и время:</u> {format_date(elem["date"])} {elem["time"]}')
        res_string.append(f'<u>Команда:</u> /{elem["command"]}')
        res_string.append(f'<u>Параметры запроса:</u>\n{params}')
        res_string.append(f'\n<u>Результат:</u>\n{elem["result"]}')

        result.append('\n'.join(res_string))

    return result
