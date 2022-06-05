from typing import Dict, List


def hotels(req_data: Dict) -> List[dict]:
    return req_data['data']['body']['searchResults']['results']
