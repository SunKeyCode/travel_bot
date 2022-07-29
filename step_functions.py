from utils.hotels_api import api
from utils import attributes, format
from utils.misc.other_func import define_lang, get_sort_order
import keyboards.inline.inline_markup as inline_markup
import logs.logs as log

from utils.CustomExceptions import ApiRequestError, UnexpectedException
from datetime import date
from telebot.types import Message, InputMediaPhoto
from loader import bot, queries, QueryContainer, Steps, Commands
from typing import Callable, Dict
import functools
from database.DB import write_history, get_currency, get_locale
from config_data import config


def track_exception(func: Callable) -> Callable:
    """Декоратор для отслеживания исключений KeyError, ApiRequestError и UnexpectedException"""
    @functools.wraps(func)
    def wrapper(message: Message, *args, **kwargs):
        try:
            return func(message, *args, **kwargs)
        except KeyError:
            bot.send_message(message.chat.id, '❗ Упс... Что-то пошло не так при расшифровке ответа от сервера. '
                                              'Попробуйте повторить всё сначала.')
            print_start_message(message)
        except ApiRequestError:
            bot.send_message(message.chat.id, '❗ Упс... Что-то пошло не так при запросе к серверу. '
                                              'Попробуйте повторить всё сначала.')
            print_start_message(message)
        except UnexpectedException as exc:
            log.error_log(exc, 'Непредвиденное исключение', func.__name__)
            bot.send_message(message.chat.id, '❗ Упс... Что-то пошло не так. '
                                              'Попробуйте повторить всё сначала.')
            print(f'Исключение в функции {func.__name__}', exc)
            print_start_message(message)

    return wrapper


def print_start_message(message: Message) -> None:
    """Выводит информационное сообщение со списком всех команд"""
    bot.send_message(message.chat.id, 'ℹ Вы можете использовать следующие команды:\n\n'
                                      '/lowprice - топ самых дешёвых отелей в городе.\n'
                                      '/highprice - топ самых дорогих отелей в городе.\n'
                                      '/bestdeal - топ отелей, '
                                      'наиболее подходящих по цене и расположению от центра.\n'
                                      '/history - показать историю поиска отелей.\n'
                                      '/settings - настройки бота.\n'
                                      '/help - показать список команд.'
                     )


def load_settings(message: Message) -> None:
    """Загружает настройки из БД для ткущего пользователя"""
    queries[message.chat.id].currency = get_currency(message)
    queries[message.chat.id].locale = get_locale(message)
    if queries[message.chat.id].locale == 'en_US':
        queries[message.chat.id].distance_units = 'miles'
    elif queries[message.chat.id].locale == 'ru_RU':
        queries[message.chat.id].distance_units = 'km'
    else:
        queries[message.chat.id].distance_units = 'miles'


def first_step(message: Message, command: Commands) -> None:
    """Первый шаг для всех команд, кроме команды history"""
    bot.send_message(message.chat.id, 'Введите название города для поиска:')
    queries[message.chat.id]: Dict[QueryContainer] = QueryContainer(user_id=int(message.chat.id), command=command)
    load_settings(message)
    bot.register_next_step_handler(message, print_destinations)


def next_step(message: Message, curr_step: Steps) -> None:
    """
    Определяем следующий шаг в зависимости от текущей команды.
    :param curr_step: шаг, на котором находимся в данный момент.
    """
    curr_setting = queries[message.chat.id].currency
    if curr_setting == 'USD':
        currency = 'долларах'
        price_range = '50 100'
    elif curr_setting == 'RUB':
        currency = 'рублях'
        price_range = '1000 5000'
    else:
        currency = 'долларах'
        price_range = '50 100'

    if curr_step == Steps.destination:
        print_calendar(message, 'Выберите дату заезда 📅:', date.today())
    elif curr_step == Steps.checkin_date:
        print_calendar(message, 'Выберите дату выезда 📅:', queries[message.chat.id].checkin_date)
    elif curr_step == Steps.checkout_date:
        if queries[message.chat.id].command in (Commands.lowprice, Commands.highprice):
            bot.send_message(message.chat.id, text=f'Сколько отелей показать? Не больше {config.MAX_HOTELS}')
            bot.register_next_step_handler(message, get_hotels_count)
        elif queries[message.chat.id].command == Commands.bestdeal:
            bot.send_message(
                message.chat.id,
                f'Введите диапазон цен (в {currency}) через пробел, \n<b>пример</b>: {price_range}',
                parse_mode='HTML'
            )
            bot.register_next_step_handler(message, get_price_range)


@track_exception
def print_destinations(message: Message) -> None:
    """Печатает список для выбора места назначения"""
    lang = define_lang(message.text)

    queries[message.chat.id].language = lang

    response = api.get_destinations(message.text, language=lang)
    destinations = attributes.destinations(response)
    queries[message.chat.id].destinations = attributes.destinations_dict(response)

    if destinations:
        markup = inline_markup.destination_markup(destinations)
        bot.send_message(message.chat.id, f'Выберите нужный вариант 👇', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'К сожалению, я ничего не нашел по Вашему запросу...')
        print_start_message(message)


def print_calendar(message: Message, text: str, limit_date: date):
    """Печатает разметку календаря в чате"""
    now = date.today()
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=inline_markup.calendar_days_markup(now.year, limit_date.month, limit_date)
    )


def get_price_range(message: Message) -> None:
    """Получает диапазон цен для команды bestdeal от пользователя"""
    if queries[message.chat.id].distance_units == 'miles':
        distance_unt = 'в миллях'
    elif queries[message.chat.id].distance_units == 'km':
        distance_unt = 'в километрах'
    else:
        distance_unt = 'в миллях'

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
        bot.send_message(message.chat.id, f'Введите максимальное расстояние от центра ({distance_unt}):')
        bot.register_next_step_handler(message, get_max_distance)
    except (TypeError, ValueError):
        bot.send_message(message.chat.id, '❌ Вы неправильно ввели диапазон... Попробуйте еще раз!')
        next_step(message, Steps.checkout_date)


def get_max_distance(message: Message) -> None:
    """Получает максимальное расстояние от центра для команды bestdeal от пользователя"""
    try:
        if float(message.text) > 0:
            queries[message.chat.id].max_distance = float(message.text)
            bot.send_message(message.chat.id, text=f'Сколько отелей показать? Не больше {config.MAX_HOTELS}')
            bot.register_next_step_handler(message, get_hotels_count)
        else:
            raise ValueError
    except (TypeError, ValueError):
        bot.send_message(message.chat.id, '❌ О-оу... вы что-то не так ввели. Расстояние до цента должно вводится '
                                          'числом и быть больше 0 (например 3.5 или 5), попробуйте ще раз:')
        bot.register_next_step_handler(message, get_max_distance)


def get_hotels_count(message):
    """Получает количество отелей для вывода от пользователя"""
    if not message.text.isdigit():
        bot.send_message(message.chat.id, '❌ О-оу! Тут нужно вводить цифру.')
        bot.register_next_step_handler(message, get_hotels_count)
        return
    elif (int(message.text) < 1) or (int(message.text) > config.MAX_HOTELS):
        bot.send_message(message.chat.id, f'Количество должно быть от 1 до {config.MAX_HOTELS}')
        bot.register_next_step_handler(message, get_hotels_count)
        return

    queries[message.chat.id].hotel_count = int(message.text)

    markup = inline_markup.yes_no_markup()
    bot.send_message(message.chat.id, 'Показать фото отелей?', reply_markup=markup)


@track_exception
def print_hotels(message: Message) -> None:
    """Печатает отели с фотографиями или без"""
    if queries[message.chat.id].show_photo:
        if not message.text.isdigit():
            bot.send_message(message.chat.id, 'О-оу! Тут нужно вводить цифру.')
            bot.register_next_step_handler(message, print_hotels)
            return
        elif (int(message.text) < 1) or (int(message.text) > config.MAX_PHOTO):
            bot.send_message(message.chat.id, f'Количество должно быть от 1 до {config.MAX_PHOTO}')
            bot.register_next_step_handler(message, print_hotels)
            return
        bot.send_message(message.chat.id, 'Ищем отели... ⌛')
        queries[message.chat.id].photo_count = int(message.text)

    if queries[message.chat.id].min_price is None or queries[message.chat.id].max_price is None:
        price_range = None
    else:
        price_range = (queries[message.chat.id].min_price, queries[message.chat.id].max_price)

    currency = queries[message.chat.id].currency

    hotels = attributes.hotels(
        api.hotels_by_destination(
            destination_id=queries[message.chat.id].destination_id,
            check_in=queries[message.chat.id].checkin_date.strftime('%Y-%m-%d'),
            check_out=queries[message.chat.id].checkout_date.strftime('%Y-%m-%d'),
            locale=queries[message.chat.id].locale,
            sort_order=get_sort_order(queries[message.chat.id].command),
            price_range=price_range,
            currency=currency
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

    if queries[message.chat.id].show_photo:
        for i_hotel in hotels:
            hotel_id = attributes.get_hotel_id(i_hotel)
            photo_data = api.get_photo(hotel_id)

            media = list()
            for photo in attributes.photo(data=photo_data, limit=queries[message.chat.id].photo_count):
                media.append(InputMediaPhoto(format.format_photo(photo, 'z'), i_hotel['name']))
            url = f'https://www.hotels.com/ho{hotel_id}'
            markup = inline_markup.link_markup('Перейти на страницу отеля 🔗', url)
            bot.send_media_group(message.chat.id, media)
            bot.send_message(
                message.chat.id, format.format_hotel(i_hotel, date_delta.days, currency),
                parse_mode='HTML', reply_markup=markup
            )
    else:
        for i_hotel in hotels:
            url = f'https://www.hotels.com/ho{attributes.get_hotel_id(i_hotel)}'
            markup = inline_markup.link_markup('Перейти на страницу отеля 🔗', url)
            bot.send_message(
                message.chat.id, format.format_hotel(i_hotel, date_delta.days, currency),
                parse_mode='HTML', reply_markup=markup
            )
    print_start_message(message)

# TODO вынести файл в определенный модуль из корня проекта
# TODO дописать документацию всем функциям

