from typing import Dict, Union
import logs
import re


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
    distance = hotel['landmarks'][0]['distance']
    try:
        price = int(round(float(hotel['ratePlan']['price']['exactCurrent'])))
    except ValueError as exc:
        price = 0
        print(exc)
        logs.error_log(exc, f'Ошибка преобразования типа в {hotel}', f'{__name__}.{format_hotel.__name__}')

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


def format_photo(photo: Dict, size) -> str:
    try:
        return photo['baseUrl'].format(size=size)
    except KeyError as exc:
        print('Ошибка поиска ключа:', exc)
        logs.error_log(exc, 'Ошибка ключа', f'{__name__}.{format_photo.__name__}')
        raise KeyError(f'Ошибка ключа в функции {__name__}.{format_photo.__name__}')
