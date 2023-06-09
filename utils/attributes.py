from typing import Dict, List, Optional, Callable
import re
import logs.logs as log
from functools import wraps
from datetime import datetime
from utils.misc.other_func import distance_from_str


def track_key_error(func: Callable) -> Callable:
    """Декоратор для отслеживания KeyError исключений"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as exc:
            print(f'{datetime.now()} Ошибка поиска ключа в функции {__name__}.{func.__name__}:', exc)
            log.error_log(exc, 'Ошибка ключа', f'{__name__}.{func.__name__}')
            raise KeyError(f'Ошибка ключа в функции {__name__}.{func.__name__}')

    return wrapper


@track_key_error
def hotels(data: Dict, limit: Optional[int] = 100, max_distance=None) -> List[dict]:
    """
    Получает список с данными об отелях из словаря содержащего ответ сервера.
    :param data: словарь, содержащий ответ от сервера.
    :param limit: количество отелей, которое необходимо вернуть в списке.
    :param max_distance: фильтр по максимальному расстоянию от центра (используется в команде bestdeal)
    :rtype: List[Dict]
    """
    if max_distance is not None:
        items = data['data']['body']['searchResults']['results']
        try:
            result_data = filter(lambda item: distance_from_str(item['landmarks'][0]['distance']) <= max_distance, items)
            result_data = sorted(result_data, key=lambda elem: elem['ratePlan']['price']['exactCurrent'])
        except IndexError:
            return data['data']['body']['searchResults']['results'][:limit]
        return list(result_data)[:limit]
    else:
        return data['data']['body']['searchResults']['results'][:limit]


@track_key_error
def photo(data, limit: Optional[int] = None) -> List[dict]:
    """Получает список с данными о фотографиях из словаря содержащего ответ сервера"""
    if limit is None:
        return data['hotelImages']
    else:
        return data['hotelImages'][:limit]


@track_key_error
def destinations(request_data: Dict) -> List[Dict]:
    """Получаем список городов из словаря содержащего ответ сервера"""
    for elem in request_data['suggestions'][0]['entities']:
        elem['caption'] = re.sub(r'<[/]?span.*?>', '', elem['caption'])

    return request_data['suggestions'][0]['entities']


@track_key_error
def destinations_dict(request_data: Dict) -> Dict[str, str]:
    """Получает список найденных городов в виде словаря, где ключ - это id города, а значение - название"""
    result = dict()

    for elem in request_data['suggestions'][0]['entities']:
        result[elem['destinationId']] = re.sub(r'<[/]?span.*?>', '', elem['caption'])

    return result


@track_key_error
def get_hotel_id(hotel: Dict) -> str:
    return hotel['id']

# TODO добавить документацию
