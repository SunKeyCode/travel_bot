import telebot
import hotels_api_requests
import json
import re
from telebot import formatting
from attributes import hotels
from typing import Dict, List


def hotel_attrs_to_string(hotels: List):
    strings = list()
    for i_hotel in hotels:
        hotel_content = list()
        hotel_content.append('<ins><b>Название</b></ins>: {}'.format(i_hotel['name']))
        hotel_content.append('<ins><b>Адрес</b></ins>: {}, {}, {}, {}, {}'.format(
            i_hotel['address']['postalCode'],
            i_hotel['address']['countryName'],
            i_hotel['address']['region'],
            i_hotel['address']['locality'],
            i_hotel['address']['streetAddress']
            )
        )
        hotel_content.append('<ins><b>Расстояние от центра</b></ins>: {}'.format(i_hotel['landmarks'][0]['distance']))
        strings.append('\n'.join(hotel_content))

    return strings


def hotel_attrs(limit):
    data = hotels_api_requests.hotels_by_destination('1506246')
    return hotel_attrs_to_string(hotels(data)[:limit])


def formatted_photo_data(data: Dict, limit: int = 10) -> List[str]:
    result = list()
    for index, elem in enumerate(data['hotelImages']):
        result.append(elem['baseUrl'].format(size='z'))
        if index >= limit - 1:
            break
    return result


if __name__ == '__main__':
    with open('photo_634418464.json', 'r') as file:
        data = json.load(file)

    photo = formatted_photo_data(data)
    print(photo)
