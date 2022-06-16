import api
import format
import attributes

from logs import error_log
from CustomExceptions import ApiRequestError
from markup import destination_markup, yes_no_markup, link_markup, calendar_days_markup

from datetime import date
from telebot.types import Message, InputMediaPhoto
from bot import bot, queries, Steps, Commands
from typing import Callable
import functools
from re import fullmatch


MAX_HOTELS = 10
MAX_PHOTO = 10


def define_lang(text: str) -> str:
    if fullmatch(r'[а-яА-Я\W\d]+', text) is not None:
        return 'ru_RU'
    else:
        return 'en_US'


def get_sort_order(command: Commands) -> str:
    if command == Commands.lowprice:
        return 'PRICE'
    elif command == Commands.highprice:
        return 'PRICE_HIGHEST_FIRST'


def track_exception(func: Callable) -> Callable:
    """Декоратор для отслеживания исключений KeyError, ApiRequestError и Exception"""
    @functools.wraps(func)
    def wrapper(message: Message, *args, **kwargs):
        try:
            return func(message, *args, **kwargs)
        except KeyError:
            bot.send_message(message.chat.id, 'Упс... Что-то пошло не так при расшифровке ответа от сервера. '
                                              'Попробуйте повторить всё с начала.')
        except ApiRequestError:
            bot.send_message(message.chat.id, 'Упс... Что-то пошло не так при запросе к серверу. '
                                              'Попробуйте повторить всё с начала.')
        except Exception as exc:
            error_log(exc, 'Непредвиденное исключение', func.__name__)
            bot.send_message(message.chat.id, 'Упс... Что-то пошло не так. '
                                              'Попробуйте повторить всё с начала.')
            print(f'Исключение в функции {func.__name__}', exc)

    return wrapper


def print_start_message(message: Message) -> None:
    bot.send_message(message.chat.id, 'Вы можете использовать следующие команды:\n\n'
                                      '/lowprice - топ самых дешёвых отелей в городе.\n'
                                      '/highprice - топ самых дорогих отелей в городе.\n'
                                      '/bestdeal - топ отелей, '
                                      'наиболее подходящих по цене и расположению от центра.\n'
                                      '/history - показать историю поиска отелей.')


def next_step(message: Message, curr_step: Steps) -> None:
    """Определяем следующий шаг в зависимости от текущей команды"""
    if curr_step == Steps.destination:
        get_date(message, 'Выберите дату заезда:')
    if curr_step == Steps.checkin_date:
        get_date(message, 'Выберите дату выезда:')
    if curr_step == Steps.checkout_date:
        if queries[message.chat.id].command in (Commands.lowprice, Commands.highprice):
            bot.send_message(message.chat.id, text=f'Сколько отелей показать? Не больше {MAX_HOTELS}')
            bot.register_next_step_handler(message, show_photo)


@track_exception
def print_destinations(message: Message) -> None:

    lang = define_lang(message.text)

    queries[message.chat.id].language = lang

    response = api.get_destinations(message.text, language=lang)
    destinations = attributes.destinations(response)

    if destinations:
        markup = destination_markup(destinations)
        bot.send_message(message.chat.id, f'Выберите нужный вариант', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'К сожалению, я ничего не нашел по Вашему запросу...')
        print_start_message(message)


def get_date(message: Message, text: str):
    now = date.today()
    bot.send_message(message.chat.id, text, reply_markup=calendar_days_markup(now.year, now.month))


def show_photo(message):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'О-оу! Тут нужно вводить цифру.')
        bot.register_next_step_handler(message, show_photo)
        return
    elif (int(message.text) < 1) or (int(message.text) > MAX_HOTELS):
        bot.send_message(message.chat.id, f'Количество должно быть от 1 до {MAX_HOTELS}')
        bot.register_next_step_handler(message, show_photo)
        return

    queries[message.chat.id].hotel_count = int(message.text)

    markup = yes_no_markup()
    bot.send_message(message.chat.id, 'Показать фото отелей?', reply_markup=markup)


@track_exception
def print_hotels(message: Message, no_photo=True):
    if no_photo:
        hotels = attributes.hotels(
            api.hotels_by_destination(
                destination_id=queries[message.chat.id].destination_id,
                check_in=queries[message.chat.id].checkin_date.strftime('%Y-%m-%d'),
                check_out=queries[message.chat.id].checkout_date.strftime('%Y-%m-%d'),
                language=queries[message.chat.id].language,
                sort_order=get_sort_order(queries[message.chat.id].command)
            ),
            limit=queries[message.chat.id].hotel_count
        )
        for i_hotel in hotels:
            url = f'https://www.hotels.com/ho{attributes.get_hotel_id(i_hotel)}'
            markup = link_markup('Перейти на страницу отеля ->', url)
            bot.send_message(message.chat.id, format.format_hotel(i_hotel), parse_mode='HTML', reply_markup=markup)
        print_start_message(message)
    else:
        bot.register_next_step_handler(message, _print_hotels)


@track_exception
def _print_hotels(message: Message) -> None:
    """Печатает отели с фотографиями"""
    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'О-оу! Тут нужно вводить цифру.')
        bot.register_next_step_handler(message, _print_hotels)
        return
    elif (int(message.text) < 1) or (int(message.text) > MAX_HOTELS):
        bot.send_message(message.chat.id, f'Количество должно быть от 1 до {MAX_PHOTO}')
        bot.register_next_step_handler(message, _print_hotels)
        return

    hotels = attributes.hotels(
        api.hotels_by_destination(
            destination_id=queries[message.chat.id].destination_id,
            check_in=queries[message.chat.id].checkin_date.strftime('%Y-%m-%d'),
            check_out=queries[message.chat.id].checkout_date.strftime('%Y-%m-%d'),
            language=queries[message.chat.id].language,
            sort_order=get_sort_order(queries[message.chat.id].command)
        ),
        limit=queries[message.chat.id].hotel_count
    )

    queries[message.chat.id].photo_count = int(message.text)

    for i_hotel in hotels:
        hotel_id = attributes.get_hotel_id(i_hotel)
        response_data = api.get_photo(hotel_id)

        media = list()
        for photo in attributes.photo(data=response_data, limit=queries[message.chat.id].photo_count):
            media.append(InputMediaPhoto(format.format_photo(photo, 'z'), i_hotel['name']))

        url = f'https://www.hotels.com/ho{attributes.get_hotel_id(i_hotel)}'
        markup = link_markup('Перейти на страницу отеля ->', url)
        bot.send_media_group(message.chat.id, media)
        bot.send_message(message.chat.id, format.format_hotel(i_hotel), parse_mode='HTML', reply_markup=markup)

    print_start_message(message)
