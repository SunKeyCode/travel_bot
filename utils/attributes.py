from typing import Dict, List, Optional, Callable
import re
import logs
from functools import wraps
from datetime import datetime


def track_key_error(func: Callable) -> Callable:
    """Декоратор для отслеживания KeyError исключений"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as exc:
            print(f'{datetime.now()} Ошибка поиска ключа в функции {__name__}.{func.__name__}:', exc)
            logs.error_log(exc, 'Ошибка ключа', f'{__name__}.{func.__name__}')
            raise KeyError(f'Ошибка ключа в функции {__name__}.{func.__name__}')

    return wrapper


def distance_from_str(distance_str: str) -> float:
    distance_str = distance_str.split()[0]
    if distance_str.count(','):
        distance_str = distance_str.replace(',', '.')
    return float(distance_str)


@track_key_error
def hotels(data: Dict, limit: Optional[int] = 100, max_distance=None) -> List[dict]:

    if max_distance is not None:
        items = data['data']['body']['searchResults']['results']
        result_data = filter(lambda item: distance_from_str(item['landmarks'][0]['distance']) <= max_distance, items)
        result_data = sorted(result_data, key=lambda elem: elem['ratePlan']['price']['exactCurrent'])
        return list(result_data)[:limit]
    else:
        return data['data']['body']['searchResults']['results'][:limit]


@track_key_error
def photo(data, limit: Optional[int] = None) -> List[dict]:

    if limit is None:
        return data['hotelImages']
    else:
        return data['hotelImages'][:limit]


@track_key_error
def destinations(request_data: Dict) -> List[Dict]:
    for elem in request_data['suggestions'][0]['entities']:
        try:  # убрать???
            elem['caption'] = re.sub(r'<[/]?span.*?>', '', elem['caption'])
        except IndexError as exc:
            print(f'При форматировании строки {elem} возникла ошибка', exc)
            logs.error_log(exc, f"Ошибка в строке {elem['caption']}", destinations.__name__)

    return request_data['suggestions'][0]['entities']


@track_key_error
def destinations_dict(request_data: Dict) -> Dict[str, str]:
    result = dict()

    for elem in request_data['suggestions'][0]['entities']:
        result[elem['destinationId']] = re.sub(r'<[/]?span.*?>', '', elem['caption'])

    return result


@track_key_error
def get_hotel_id(hotel: Dict) -> str:
    return hotel['id']
