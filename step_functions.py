import api
import format
import attributes

from logs import error_log
from CustomExceptions import ApiRequestError
from markup import destination_markup, yes_no_markup, link_markup, calendar_days_markup

from datetime import date
from telebot.types import Message, InputMediaPhoto
from bot import bot, queries, QueryContainer, Steps, Commands
from typing import Callable, Dict
import functools
from re import fullmatch
from DB import write_history


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
    elif command == Commands.bestdeal:
        return 'DISTANCE_FROM_LANDMARK'


def track_exception(func: Callable) -> Callable:
    """Декоратор для отслеживания исключений KeyError, ApiRequestError и Exception"""
    @functools.wraps(func)
    def wrapper(message: Message, *args, **kwargs):
        try:
            return func(message, *args, **kwargs)
        except KeyError:
            bot.send_message(message.chat.id, '❗ Упс... Что-то пошло не так при расшифровке ответа от сервера. '
                                              'Попробуйте повторить всё с начала.')
        except ApiRequestError:
            bot.send_message(message.chat.id, '❗ Упс... Что-то пошло не так при запросе к серверу. '
                                              'Попробуйте повторить всё с начала.')
        except Exception as exc:
            error_log(exc, 'Непредвиденное исключение', func.__name__)
            bot.send_message(message.chat.id, '❗ Упс... Что-то пошло не так. '
                                              'Попробуйте повторить всё с начала.')
            print(f'Исключение в функции {func.__name__}', exc)

    return wrapper


def print_start_message(message: Message) -> None:
    bot.send_message(message.chat.id, 'ℹ Вы можете использовать следующие команды:\n\n'
                                      '/lowprice - топ самых дешёвых отелей в городе.\n'
                                      '/highprice - топ самых дорогих отелей в городе.\n'
                                      '/bestdeal - топ отелей, '
                                      'наиболее подходящих по цене и расположению от центра.\n'
                                      '/history - показать историю поиска отелей.')


def first_step(message: Message, command: Commands) -> None:
    """Первый шаг для всех команд, кроме команды history"""
    bot.send_message(message.chat.id, 'Введите название города для поиска:')
    queries[message.chat.id]: Dict[QueryContainer] = QueryContainer(user_id=int(message.chat.id), command=command)
    bot.register_next_step_handler(message, print_destinations)


def next_step(message: Message, curr_step: Steps) -> None:
    """Определяем следующий шаг в зависимости от текущей команды"""
    if queries[message.chat.id].currency == 'USD':
        currency = 'долларах'
        price_range = '50 100'
    elif queries[message.chat.id].currency == 'RUB':
        currency = 'рублях'
        price_range = '1000 5000'
    else:
        currency = 'долларах'
        price_range = '50 100'

    if curr_step == Steps.destination:
        get_date(message, 'Выберите дату заезда 📅:')
    elif curr_step == Steps.checkin_date:
        get_date(message, 'Выберите дату выезда 📅:')
    elif curr_step == Steps.checkout_date:
        if queries[message.chat.id].command in (Commands.lowprice, Commands.highprice):
            bot.send_message(message.chat.id, text=f'Сколько отелей показать? Не больше {MAX_HOTELS}')
            bot.register_next_step_handler(message, show_photo)
        elif queries[message.chat.id].command == Commands.bestdeal:
            bot.send_message(
                message.chat.id,
                f'Введите диапазон цен (в {currency}) через пробел, \n<b>пример</b>: {price_range}',
                parse_mode='HTML'
            )
            bot.register_next_step_handler(message, get_price_range)


@track_exception
def print_destinations(message: Message) -> None:

    lang = define_lang(message.text)

    queries[message.chat.id].language = lang

    response = api.get_destinations(message.text, language=lang)
    destinations = attributes.destinations(response)
    queries[message.chat.id].destinations = attributes.destinations_dict(response)

    if destinations:
        markup = destination_markup(destinations)
        bot.send_message(message.chat.id, f'Выберите нужный вариант 👇👇👇', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'К сожалению, я ничего не нашел по Вашему запросу...')
        print_start_message(message)


def get_date(message: Message, text: str):
    now = date.today()
    bot.send_message(message.chat.id, text, reply_markup=calendar_days_markup(now.year, now.month))


def get_price_range(message: Message) -> None:

    try:
        prices = list(map(int, message.text.split()))

        if len(prices) != 2:
            raise ValueError
        for value in prices:
            if int(value) < 0:
                raise ValueError
        if min(prices) == 0:
            queries[message.chat.id].min_price = 1
        else:
            queries[message.chat.id].min_price = min(prices)
        queries[message.chat.id].max_price = max(prices)
        bot.send_message(message.chat.id, 'Введите максимальное расстояние от центра:')
        bot.register_next_step_handler(message, get_max_distance)
    except (TypeError, ValueError):
        bot.send_message(message.chat.id, '❌ Вы неправильно ввели диапазон... Попробуйте еще раз!')
        next_step(message, Steps.checkout_date)


def get_max_distance(message: Message) -> None:
    try:
        if float(message.text) > 0:
            queries[message.chat.id].max_distance = float(message.text)
            bot.send_message(message.chat.id, text=f'Сколько отелей показать? Не больше {MAX_HOTELS}')
            bot.register_next_step_handler(message, show_photo)
        else:
            raise ValueError
    except (TypeError, ValueError):
        bot.send_message(message.chat.id, '❌ О-оу... вы что-то не так ввели. Расстояние до цента должно вводится '
                                          'числом и быть больше 0, попробуйте ще раз:')
        bot.register_next_step_handler(message, get_max_distance)


def show_photo(message):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, '❌ О-оу! Тут нужно вводить цифру.')
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
def print_hotels(message: Message) -> None:
    """Печатает отели с фотографиями или без"""
    if queries[message.chat.id].show_photo:
        if not message.text.isdigit():
            bot.send_message(message.chat.id, 'О-оу! Тут нужно вводить цифру.')
            bot.register_next_step_handler(message, print_hotels)
            return
        elif (int(message.text) < 1) or (int(message.text) > MAX_HOTELS):
            bot.send_message(message.chat.id, f'Количество должно быть от 1 до {MAX_PHOTO}')
            bot.register_next_step_handler(message, print_hotels)
            return
        bot.send_message(message.chat.id, 'Ищем отели... ⌛')
        queries[message.chat.id].photo_count = int(message.text)

    if queries[message.chat.id].min_price is None or queries[message.chat.id].max_price is None:
        price_range = None
    else:
        price_range = (queries[message.chat.id].min_price, queries[message.chat.id].max_price)

    hotels = attributes.hotels(
        api.hotels_by_destination(
            destination_id=queries[message.chat.id].destination_id,
            check_in=queries[message.chat.id].checkin_date.strftime('%Y-%m-%d'),
            check_out=queries[message.chat.id].checkout_date.strftime('%Y-%m-%d'),
            language=queries[message.chat.id].language,
            # language='en_US',
            sort_order=get_sort_order(queries[message.chat.id].command),
            price_range=price_range
        ),
        limit=queries[message.chat.id].hotel_count,
        max_distance=queries[message.chat.id].max_distance
    )
    queries[message.chat.id].hotels = hotels

    write_history(queries[message.chat.id])

    if not hotels:
        bot.send_message(message.chat.id, '😞 По Вашему запросу не найдено ни одного отеля... Попробуйте '
                                          'изменить параметры поиска (например расширить диапазон цен).')
        print_start_message(message)
        return

    date_delta = queries[message.chat.id].checkout_date - queries[message.chat.id].checkin_date
    currency = queries[message.chat.id].currency

    if queries[message.chat.id].show_photo:
        for i_hotel in hotels:
            hotel_id = attributes.get_hotel_id(i_hotel)
            photo_data = api.get_photo(hotel_id)

            media = list()
            for photo in attributes.photo(data=photo_data, limit=queries[message.chat.id].photo_count):
                media.append(InputMediaPhoto(format.format_photo(photo, 'z'), i_hotel['name']))
            url = f'https://www.hotels.com/ho{hotel_id}'
            markup = link_markup('Перейти на страницу отеля 🔗', url)
            bot.send_media_group(message.chat.id, media)
            bot.send_message(
                message.chat.id, format.format_hotel(i_hotel, date_delta.days, currency),
                parse_mode='HTML', reply_markup=markup
            )
    else:
        for i_hotel in hotels:
            url = f'https://www.hotels.com/ho{attributes.get_hotel_id(i_hotel)}'
            markup = link_markup('Перейти на страницу отеля 🔗', url)
            bot.send_message(
                message.chat.id, format.format_hotel(i_hotel, date_delta.days, currency),
                parse_mode='HTML', reply_markup=markup
            )
    print_start_message(message)
