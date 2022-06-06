import requests
import json
import re
from typing import Dict, List


headers = {
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    "X-RapidAPI-Key": "bae1651a05msh66bdf614f9bc0e9p1a06dfjsn581c7e145db3"
    }


def get_photo(hotel_id: str) -> Dict:
    querystring = {"id": hotel_id}
    request = requests.get(
            'https://hotels4.p.rapidapi.com/properties/get-hotel-photos',
            headers=headers,
            params=querystring
        )
    data = json.loads(request.text)

    return data


# для тэстов
# def get_photo_data(hotel_id: str = '634418464') -> Dict:
#     with open('photo_634418464.json', 'r') as file:
#         data = json.load(file)
#
#     return data


# Временная функция для тестов
# def get_destinations():
#     with open('result.json', 'r') as file:
#         data = json.load(file)
#     return data


def get_destinations(destination):
    querystring = {"query": destination, "locale": "en_US", "currency": "USD"}
    destinations_request = requests.get(
            'https://hotels4.p.rapidapi.com/locations/v2/search',
            headers=headers,
            params=querystring
        )
    data = json.loads(destinations_request.text)

    return data


# Временная функция для тестов
def hotels_by_destination(destination_id):
    with open(f'hotels_{destination_id}.json', 'r') as file:
        data = json.load(file)

    return data


# def hotels_by_destination(destination_id, request_headers):
#     querystring = {
#         "destinationId": destination_id, "pageNumber": "1", "pageSize": "25", "checkIn": "2020-01-08",
#         "checkOut": "2020-01-15", "adults1": "1", "sortOrder": "PRICE", "locale": "en_US", "currency": "USD"
#     }
#     hotels_request = requests.get(
#         'https://hotels4.p.rapidapi.com/properties/list',
#         headers=request_headers,
#         params=querystring
#     )
#     data = json.loads(hotels_request.text)
#
#     return data['data']['body']['searchResults']['results']


if __name__ == '__main__':
    pass
    # print(get_photo())
