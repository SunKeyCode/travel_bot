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

    return '\n'.join(hotel_content)
