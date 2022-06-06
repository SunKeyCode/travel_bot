from typing import List, Dict


def hotel_to_str(hotel: Dict) -> str:
    hotel_content = list()
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

    return '\n'.join(hotel_content)


def _format_photo(data: Dict, limit: int = 10) -> List[str]:
    result = list()
    for index, elem in enumerate(data['hotelImages']):
        result.append(elem['baseUrl'].format(size='z'))
        if index >= limit - 1:
            break
    return result


def format_photo(photo: Dict, size) -> str:
    return photo['baseUrl'].format(size=size)
