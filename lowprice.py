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


url = "https://hotels4.p.rapidapi.com/locations/v2/search"

querystring = {"query": "new york", "locale": "en_US", "currency": "USD"}

headers = {
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    "X-RapidAPI-Key": "bae1651a05msh66bdf614f9bc0e9p1a06dfjsn581c7e145db3"
}

# response = requests.request("GET", url, headers=headers, params=querystring)
# data = json.loads(response.text)
# with open('result.json', 'w') as file:
#     json.dump(data, file, indent=4)

# with open('result.json', 'r') as file:
#     data = json.load(file)
#
#
# print(get_cities_list(data))