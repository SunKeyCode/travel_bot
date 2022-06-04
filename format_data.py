from typing import List, Dict


def hotel_to_str(hotel: Dict) -> str:
    hotel_content = list()
    hotel_content.append('<ins><b>Название</b></ins>: {}'.format(hotel['name']))
    hotel_content.append('<ins><b>Адрес</b></ins>: {}, {}, {}, {}, {}'.format(
        hotel['address']['postalCode'],
        hotel['address']['countryName'],
        hotel['address']['region'],
        hotel['address']['locality'],
        hotel['address']['streetAddress']
        )
    )
    hotel_content.append('<ins><b>Расстояние от центра</b></ins>: {}'.format(hotel['landmarks'][0]['distance']))

    return '\n'.join(hotel_content)
