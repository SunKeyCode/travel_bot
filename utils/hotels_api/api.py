import requests
import json

import logs.logs as log

from typing import Dict, Tuple, Callable, Optional
from utils.CustomExceptions import ApiRequestError
from functools import wraps
from datetime import datetime
from config_data.config import API_KEY, API_HOST


headers = {
    "X-RapidAPI-Host": API_HOST,
    "X-RapidAPI-Key": API_KEY
    }


def track_api_exception(func: Callable) -> Callable:
    """Декоратор для отслеживания ошибок, связанных с модулем requests"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (requests.ConnectionError, requests.HTTPError, requests.Timeout) as exc:
            log.error_log(exc, 'Ошибка при работе с requests', f'{__name__}.{func.__name__}')
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


@track_api_exception
def get_destinations(destination: str, language: str = 'en_US') -> Dict:
    querystring = {"query": destination, "locale": language, "currency": "USD"}

    request = requests.get(
            'https://hotels4.p.rapidapi.com/locations/v2/search',
            headers=headers,
            params=querystring,
            timeout=20
    )
    request.raise_for_status()

    data = json.loads(request.text)

    return data


@track_api_exception
def hotels_by_destination(
        destination_id: str, check_in: str, check_out: str, locale: str = 'en_US',
        sort_order: str = 'PRICE', price_range: Optional[Tuple[int]] = None, currency: str = 'USD') -> Dict:

    querystring = {
        "destinationId": destination_id, "pageNumber": "1", "pageSize": "25", "checkIn": check_in,
        "checkOut": check_out, "adults1": "1", "sortOrder": sort_order, "locale": locale, "currency": currency
    }
    if price_range is not None:
        querystring['priceMin'] = str(price_range[0])
        querystring['priceMax'] = str(price_range[1])
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
