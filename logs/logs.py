import datetime
import json
import os
from typing import Optional


def get_path() -> str:
    directory = 'logs'
    file = 'error_log.json'
    db_path = os.path.join(directory, file)

    return db_path


def error_log(exc: Exception, error_message: str, func: Optional[str] = None) -> None:

    path = get_path()

    if os.path.exists(os.path.abspath(path)):
        with open(path, 'r', encoding='utf-8') as file:
            current_data = json.load(file)
    else:
        current_data = dict()

    new_error = dict()
    new_error['time'] = datetime.datetime.today().time().__str__()
    new_error['exception_type'] = exc.__class__.__name__
    new_error['exception_text'] = exc.__str__()
    new_error['function'] = func
    new_error['description'] = error_message
    if current_data.get(datetime.datetime.today().date().__str__()) is None:
        current_data[datetime.datetime.today().date().__str__()] = [new_error]
    else:
        current_data[datetime.datetime.today().date().__str__()].append(new_error)

    with open(path, 'w', encoding='utf-8') as file:
        json.dump(current_data, file, ensure_ascii=False, indent=4)

# TODO добавить документацию
