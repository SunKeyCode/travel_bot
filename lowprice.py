import telebot
import requests
import json
import re
from typing import Dict, List


def get_cities_list(request_data: Dict) -> List:
    for elem in request_data['suggestions'][0]['entities']:
        elem['caption'] = re.findall(r'<span.+</span>, (.+)', elem['caption'])[0]
    return request_data['suggestions'][0]['entities']


def get_cities():
    with open('result.json', 'r') as file:
        data = json.load(file)
    return get_cities_list(data)


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
#     # with open(f'hotels_{destination_id}.json', 'w') as file:
#     #     json.dump(data, file, indent=4)
#
#     return data['data']['body']['searchResults']['results']


# Временная функция для тестов
def get_hotels_by_destination_id(destination_id, request_headers):

    with open(f'hotels_{destination_id}.json', 'r') as file:
        data = json.load(file)

    return data['data']['body']['searchResults']['results']


"""
Написать рекурсию для поиска ключей в глубине словаря (result). 
Замерить скорость работы против простого обращения.
"""

headers = {
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    "X-RapidAPI-Key": "bae1651a05msh66bdf614f9bc0e9p1a06dfjsn581c7e145db3"
    }

# res = get_hotels_by_destination_id(destination_id="1506246", request_headers=headers)
# for i_res in res:
#     print(i_res['name'], i_res['ratePlan'])


# url = "https://hotels4.p.rapidapi.com/locations/v2/search"
#
# querystring = {"query": "new york", "locale": "en_US", "currency": "USD"}
#


# response = requests.request("GET", url, headers=headers, params=querystring)
# data = json.loads(response.text)
# with open('result.json', 'w') as file:
#     json.dump(data, file, indent=4)


#
#
# print(get_cities_list(data))