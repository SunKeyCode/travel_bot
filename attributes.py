from typing import Dict, List, Optional


def hotels_list(data: Dict, limit: Optional[int] = None) -> List[dict]:
    if limit is None:
        return data['data']['body']['searchResults']['results']
    else:
        return data['data']['body']['searchResults']['results'][:limit]


def photo_list(data, limit: Optional[int] = None) -> List[dict]:
    if limit is None:
        return data['hotelImages']
    else:
        return data['hotelImages'][:limit]


def get_hotel_id(hotel: Dict) -> str:
    return hotel['id']
