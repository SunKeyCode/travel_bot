from typing import Dict, List, Optional
import re
import logs


def distance_from_str(distance_str: str) -> float:
    return float(distance_str.split()[0])


def hotels(data: Dict, limit: Optional[int] = 100, max_distance=None) -> List[dict]:
    try:
        if max_distance is not None:
            items = data['data']['body']['searchResults']['results']
            result_data = filter(lambda item: distance_from_str(item['landmarks'][0]['distance']) <= max_distance, items)
            return list(result_data)[:limit]
        else:
            return data['data']['body']['searchResults']['results'][:limit]
    except KeyError as exc:
        print('Ошибка поиска ключа:', exc)
        logs.error_log(exc, 'Ошибка ключа', hotels.__name__)
        raise KeyError(f'Ошибка ключа в функции {hotels.__name__}')


def photo(data, limit: Optional[int] = None) -> List[dict]:
    try:
        if limit is None:
            return data['hotelImages']
        else:
            return data['hotelImages'][:limit]
    except KeyError as exc:
        print('Ошибка поиска ключа:', exc)
        logs.error_log(exc, 'Ошибка ключа', photo.__name__)
        raise KeyError(f'Ошибка ключа в функции {photo.__name__}')


def destinations(request_data: Dict) -> List[Dict]:
    for elem in request_data['suggestions'][0]['entities']:
        try:  # убрать???
            elem['caption'] = re.sub(r'<[/]?span.*?>', '', elem['caption'])
        except IndexError as exc:
            print(f'При форматировании строки {elem} возникла ошибка', exc)
            logs.error_log(exc, f"Ошибка в строке {elem['caption']}", destinations.__name__)
    try:
        return request_data['suggestions'][0]['entities']
    except KeyError as exc:
        print('Ошибка поиска ключа:', exc)
        logs.error_log(exc, 'Ошибка ключа', destinations.__name__)
        raise KeyError(f'Ошибка ключа в функции {destinations.__name__}')


def destinations_dict(request_data: Dict) -> Dict[str, str]:
    result = dict()
    try:
        for elem in request_data['suggestions'][0]['entities']:
            result[elem['destinationId']] = re.sub(r'<[/]?span.*?>', '', elem['caption'])
    except KeyError as exc:
        print('Ошибка поиска ключа в функции destinations_dict:', exc)
        logs.error_log(exc, 'Ошибка ключа', destinations.__name__)
        raise KeyError(f'Ошибка ключа в функции {destinations.__name__}')

    return result


def get_hotel_id(hotel: Dict) -> str:
    try:
        return hotel['id']
    except KeyError as exc:
        print('Ошибка поиска ключа:', exc)
        logs.error_log(exc, 'Ошибка ключа', get_hotel_id.__name__)
        raise KeyError(f'Ошибка ключа в функции {get_hotel_id.__name__}')
