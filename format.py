from typing import List, Dict
import logs


def format_hotel(hotel: Dict) -> str:
    hotel_content = list()
    try:
        hotel_content.append('<b>Название</b>: {}'.format(hotel['name']))
        hotel_content.append('<b>Адрес</b>: {}, {}, {}, {}, {}'.format(
            hotel['address']['postalCode'],
            hotel['address']['countryName'],
            hotel['address']['region'],
            hotel['address']['locality'],
            hotel['address']['streetAddress']
            )
        )
        hotel_content.append('<b>Расстояние от центра</b>: {}'.format(hotel['landmarks'][0]['distance']))
        hotel_content.append('<b>Цена</b>: {}'.format(hotel['ratePlan']['price']['current']))
    except KeyError as exc:
        print('Ошибка поиска ключа:', exc)
        logs.error_log(exc, 'Ошибка ключа', f'{__name__}.{format_hotel.__name__}')
        raise KeyError(f'Ошибка ключа, функция: {__name__}.{format_hotel.__name__}')

    return '\n'.join(hotel_content)


def format_photo(photo: Dict, size) -> str:
    try:
        return photo['baseUrl'].format(size=size)
    except KeyError as exc:
        print('Ошибка поиска ключа:', exc)
        logs.error_log(exc, 'Ошибка ключа', f'{__name__}.{format_photo.__name__}')
        raise KeyError(f'Ошибка ключа в функции {__name__}.{format_photo.__name__}')
