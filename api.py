import requests
import json
from typing import Dict, Tuple, Callable, Optional
from logs import error_log
from CustomExceptions import ApiRequestError
from functools import wraps
from datetime import datetime


headers = {
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    "X-RapidAPI-Key": "bae1651a05msh66bdf614f9bc0e9p1a06dfjsn581c7e145db3"
    }


def track_api_exception(func: Callable) -> Callable:
    """Декоратор для отслеживания ошибок, связанных с модулем requests"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (requests.ConnectionError, requests.HTTPError, requests.Timeout) as exc:
            error_log(exc, 'Ошибка при работе с requests', f'{__name__}.{func.__name__}')
            print(f'{datetime.now()} Ошибка при работе с requests:', exc)
            raise ApiRequestError
    return wrapper


@track_api_exception
def get_photo(hotel_id: str) -> Dict:
    querystring = {"id": hotel_id}

    request = requests.get(
            'https://hotels4.p.rapidapi.com/properties/get-hotel-photos',
            headers=headers,
            params=querystring,
            timeout=20
    )
    request.raise_for_status()

    data = json.loads(request.text)

    return data


# @track_api_exception
# def get_destinations(destination: str, language: str = 'en_US') -> Dict:
#     querystring = {"query": destination, "locale": language, "currency": "USD"}
#
#     request = requests.get(
#             'https://hotels4.p.rapidapi.com/locations/v2/search',
#             headers=headers,
#             params=querystring,
#             timeout=20
#     )
#     request.raise_for_status()
#
#     data = json.loads(request.text)
#
#     return data


@track_api_exception
def hotels_by_destination(
        destination_id: str, check_in: str, check_out: str, language: str = 'en_US',
        sort_order: str = 'PRICE', price_range: Optional[Tuple[int]] = None) -> Dict:
    # querystring = {
    #     "destinationId": destination_id, "pageNumber": "1", "pageSize": "25", "checkIn": "2022-06-20",
    #     "checkOut": "2022-07-10", "adults1": "1", "sortOrder": sort_order, "locale": language, "currency": "USD"
    # }
    querystring = {
        "destinationId": destination_id, "pageNumber": "1", "pageSize": "25", "checkIn": check_in,
        "checkOut": check_out, "adults1": "1", "sortOrder": sort_order, "locale": "en_US", "currency": "USD"
    }
    if price_range is not None:
        querystring['priceMin'] = price_range[0]
        querystring['priceMax'] = price_range[1]
    print(querystring)

    request = requests.get(
        'https://hotels4.p.rapidapi.com/properties/list',
        headers=headers,
        params=querystring,
        timeout=20
    )
    request.raise_for_status()

    data = json.loads(request.text)

    return data


# для тэстов
# def get_photo_data(hotel_id: str = '634418464') -> Dict:
#     with open('photo_634418464.json', 'r') as file:
#         data = json.load(file)
#
#     return data


# для тестов
def get_destinations(destination: str, language: str = 'en_US'):
    with open('result.json', 'r') as file:
        data = json.load(file)
    return data


# для тестов
# def hotels_by_destination(destination_id):
#     with open(f'hotels_{destination_id}.json', 'r') as file:
#         data = json.load(file)
#
#     return data
