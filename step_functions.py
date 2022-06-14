import api
from markup import destination_markup, yes_no_markup, link_markup
from telebot.types import Message, InputMediaPhoto
from bot import bot, query_container
import format
import attributes
from logs import error_log
from CustomExceptions import ApiRequestError
from typing import Callable
import functools
from re import fullmatch


MAX_HOTELS = 10
MAX_PHOTO = 10


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


def define_lang(text: str) -> str:
    if fullmatch(r'[а-яА-Я\W\d]+', text) is not None:
        return 'ru_RU'
    else:
        return 'en_US'


@track_exception
def print_destinations(message: Message) -> None:

    lang = define_lang(message.text)

    query_container.language = lang

    response = api.get_destinations(message.text, language=lang)
    destinations = attributes.destinations(response)

    if destinations:
        markup = destination_markup(destinations)
        bot.send_message(
            message.chat.id, f'Выберите нужный вариант',
            reply_markup=markup,
            )
    else:
        bot.send_message(message.chat.id, 'К сожалению, я ничего не нашел по Вашему запросу...')


def show_photo(message):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'О-оу! Тут нужно вводить цифру.')
        bot.register_next_step_handler(message, show_photo)
        return
    elif (int(message.text) < 1) or (int(message.text) > MAX_HOTELS):
        bot.send_message(message.chat.id, f'Количество должно быть от 1 до {MAX_HOTELS}')
        bot.register_next_step_handler(message, show_photo)
        return

    query_container.hotel_count = int(message.text)
    markup = yes_no_markup()
    bot.send_message(message.chat.id, 'Показать фото отелей?', reply_markup=markup)


@track_exception
def print_hotels(message, no_photo=True):
    if no_photo:

        hotels = attributes.hotels(
            api.hotels_by_destination(query_container.destination_id, language=query_container.language),
            limit=query_container.hotel_count
        )

        for i_hotel in hotels:
            url = f'https://www.hotels.com/ho{attributes.get_hotel_id(i_hotel)}'
            markup = link_markup('Перейти на страницу отеля ->', url)
            bot.send_message(message.chat.id, format.format_hotel(i_hotel), parse_mode='HTML', reply_markup=markup)
    else:
        bot.register_next_step_handler(message, _print_hotels)


@track_exception
def _print_hotels(message: Message) -> None:
    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'О-оу! Тут нужно вводить цифру.')
        bot.register_next_step_handler(message, _print_hotels)
        return
    elif (int(message.text) < 1) or (int(message.text) > MAX_HOTELS):
        bot.send_message(message.chat.id, f'Количество должно быть от 1 до {MAX_PHOTO}')
        bot.register_next_step_handler(message, _print_hotels)
        return

    hotels = attributes.hotels(
        api.hotels_by_destination(query_container.destination_id, language=query_container.language),
        limit=query_container.hotel_count
    )

    query_container.photo_count = int(message.text)

    for i_hotel in hotels:
        hotel_id = attributes.get_hotel_id(i_hotel)
        response_data = api.get_photo(hotel_id)

        media = list()
        for photo in attributes.photo(response_data, limit=query_container.photo_count):
            media.append(InputMediaPhoto(format.format_photo(photo, 'z'), i_hotel['name']))

        url = f'https://www.hotels.com/ho{attributes.get_hotel_id(i_hotel)}'
        markup = link_markup('Перейти на страницу отеля ->', url)
        bot.send_media_group(message.chat.id, media)
        bot.send_message(message.chat.id, format.format_hotel(i_hotel), parse_mode='HTML', reply_markup=markup)
