import requests
import json
from typing import Dict, List
from logs import error_log
from CustomExceptions import ApiRequestError


headers = {
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    "X-RapidAPI-Key": "bae1651a05msh66bdf614f9bc0e9p1a06dfjsn581c7e145db3"
    }

# написать декоратор для отслеживания ошибок


def get_photo(hotel_id: str) -> Dict:
    querystring = {"id": hotel_id}
    try:
        request = requests.get(
                'https://hotels4.p.rapidapi.com/properties/get-hotel-photos',
                headers=headers,
                params=querystring,
                timeout=20
        )
        request.raise_for_status()

        data = json.loads(request.text)
    except (requests.ConnectionError, requests.HTTPError, requests.Timeout) as exc:
        error_log(exc, 'Ошибка при работе с requests', f'{__name__}.{get_photo.__name__}')
        print('Ошибка при работе с requests:', exc)
        raise ApiRequestError

    return data


def get_destinations(destination: str, language: str = 'en_US') -> Dict:
    querystring = {"query": destination, "locale": language, "currency": "USD"}
    try:
        request = requests.get(
                'https://hotels4.p.rapidapi.com/locations/v2/search',
                headers=headers,
                params=querystring,
                timeout=20
        )
        request.raise_for_status()

        data = json.loads(request.text)
    except (requests.ConnectionError, requests.HTTPError, requests.Timeout) as exc:
        error_log(exc, 'Ошибка при работе с requests', f'{__name__}.{get_destinations.__name__}')
        print('Ошибка при работе с requests:', exc)
        raise ApiRequestError('Ошибка в функции get_destinations')

    return data


def hotels_by_destination(destination_id, language='en_US', sort_order='PRICE'):
    # querystring = {
    #     "destinationId": destination_id, "pageNumber": "1", "pageSize": "25", "checkIn": "2022-06-20",
    #     "checkOut": "2022-07-10", "adults1": "1", "sortOrder": sort_order, "locale": language, "currency": "USD"
    # }
    querystring = {
        "destinationId": destination_id, "pageNumber": "1", "pageSize": "25", "checkIn": "2022-06-20",
        "checkOut": "2022-07-10", "adults1": "1", "sortOrder": sort_order, "locale": "en_US", "currency": "USD"
    }
    print(querystring)
    try:
        request = requests.get(
            'https://hotels4.p.rapidapi.com/properties/list',
            headers=headers,
            params=querystring,
            timeout=20
        )
        request.raise_for_status()

        data = json.loads(request.text)
    except (requests.ConnectionError, requests.HTTPError, requests.Timeout) as exc:
        error_log(exc, 'Ошибка при работе с requests', f'{__name__}.{hotels_by_destination.__name__}')
        print('Ошибка при работе с requests:', exc)
        raise ApiRequestError

    return data


# для тэстов
# def get_photo_data(hotel_id: str = '634418464') -> Dict:
#     with open('photo_634418464.json', 'r') as file:
#         data = json.load(file)
#
#     return data


# для тестов
# def get_destinations():
#     with open('result.json', 'r') as file:
#         data = json.load(file)
#     return data


# для тестов
# def hotels_by_destination(destination_id):
#     with open(f'hotels_{destination_id}.json', 'r') as file:
#         data = json.load(file)
#
#     return data


if __name__ == '__main__':
    pass
    # print(get_photo())
