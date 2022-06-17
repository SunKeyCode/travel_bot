from typing import Dict
import logs
import re


def format_hotel(hotel: Dict) -> str:
    hotel_content = list()
    try:
        # сделать везде get
        hotel_content.append('<b>Название</b>: {}'.format(hotel['name']))
        hotel_content.append('<b>Адрес</b>: {}, {}, {}, {}, {}'.format(
            hotel['address'].get('postalCode', ''),
            hotel['address']['countryName'],
            hotel['address']['region'],
            hotel['address']['locality'],
            hotel['address'].get('streetAddress', '')
            )
        )
        hotel_content.append('<b>Расстояние от центра</b>: {}'.format(hotel['landmarks'][0]['distance']))
        hotel_content.append('<b>Цена за сутки</b>: {}'.format(hotel['ratePlan']['price']['current']))
        try:
            total_price = re.findall(
                r'\$\d+[,]?\d+',
                hotel['ratePlan']['price'].get('fullyBundledPricePerStay', '')
            )[0]
            hotel_content.append('<b>Общая стоимость проживания: {}</b>'.format(total_price))
        except (IndexError, TypeError) as exc:
            print('Ошибка получения реквизита fullyBundledPricePerStay')
            logs.error_log(exc, 'Отсутствует реквизит fullyBundledPricePerStay', f'{__name__}.{format_hotel.__name__}')
    except KeyError as exc:
        print('Ошибка поиска ключа:', exc)
        logs.error_log(exc, f'Ошибка ключа в {hotel}', f'{__name__}.{format_hotel.__name__}')
        raise KeyError(f'Ошибка ключа, функция: {__name__}.{format_hotel.__name__}')

    return '\n'.join(hotel_content)


def format_photo(photo: Dict, size) -> str:
    try:
        return photo['baseUrl'].format(size=size)
    except KeyError as exc:
        print('Ошибка поиска ключа:', exc)
        logs.error_log(exc, 'Ошибка ключа', f'{__name__}.{format_photo.__name__}')
        raise KeyError(f'Ошибка ключа в функции {__name__}.{format_photo.__name__}')
