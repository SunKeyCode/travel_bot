from typing import Dict, List, Optional
import re
import logs


def hotels(data: Dict, limit: Optional[int] = None) -> List[dict]:
    try:
        if limit is None:
            return data['data']['body']['searchResults']['results']
        else:
            return data['data']['body']['searchResults']['results'][:limit]
    except KeyError as exc:
        print(exc)
        logs.error_log(exc, 'Ошибка ключа', hotels.__name__)
        raise KeyError(f'Ошибка ключа в функции {hotels.__name__}')


def photo(data, limit: Optional[int] = None) -> List[dict]:
    if limit is None:
        return data['hotelImages']
    else:
        return data['hotelImages'][:limit]


def destinations(request_data: Dict) -> List[Dict]:
    for elem in request_data['suggestions'][0]['entities']:
        try:
            elem['caption'] = re.sub(r'<[/]?span.{0,}?>', '', elem['caption'])
        except IndexError as exc:
            print(f'При форматировании строки {elem} возникла ошибка', exc)
            logs.error_log(exc, f"Ошибка в строке {elem['caption']}", destinations.__name__)
    return request_data['suggestions'][0]['entities']


def get_hotel_id(hotel: Dict) -> str:
    return hotel['id']
