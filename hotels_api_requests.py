import requests
import json
import re
from typing import Dict, List

headers = {
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    "X-RapidAPI-Key": "bae1651a05msh66bdf614f9bc0e9p1a06dfjsn581c7e145db3"
    }


def destinations_remove_tags(request_data: Dict) -> List:
    for elem in request_data['suggestions'][0]['entities']:
        elem['caption'] = re.findall(r'<span.+</span>, (.+)', elem['caption'])[0]
    return request_data['suggestions'][0]['entities']


# Временная функция для тестов
def get_destinations():
    with open('result.json', 'r') as file:
        data = json.load(file)
    return destinations_remove_tags(data)


# def get_destinations(request_headers: str):
#     querystring = {"query": "new york", "locale": "en_US", "currency": "USD"}
#     destinations_request = requests.get(
#             'https://hotels4.p.rapidapi.com/locations/v2/search',
#             headers=request_headers,
#             params=querystring
#         )
#     data = json.loads(destinations_request.text)
#
#     return destinations_remove_tags(data)


# Временная функция для тестов
def get_hotels_by_destination_id(destination_id, request_headers):
    with open(f'hotels_{destination_id}.json', 'r') as file:
        data = json.load(file)

    return data['data']['body']['searchResults']['results']


# def get_hotels_by_destination_id(destination_id, request_headers):
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
