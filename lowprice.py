import telebot
import hotels_api_requests
import json
import re
from telebot import formatting
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


def hotel_attrs():
    data = hotels_api_requests.hotels_by_destination_id('1506246')
    return hotel_attrs_to_string(data[:5])
