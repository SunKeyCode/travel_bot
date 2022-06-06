import api
from markup import destination_markup, yes_no_markup, link_markup
from telebot.types import Message, InputMediaPhoto
from bot import bot, query_container
import format
import attributes
from logs import error_log


MAX_HOTELS = 10
MAX_PHOTO = 10


def print_destinations(message: Message) -> None:
    response = api.get_destinations(message.text)
    destinations = attributes.destinations(response)
    if destinations:
        markup = destination_markup(destinations)
        bot.send_message(
            message.chat.id, f'Выберите нужный вариант',
            reply_markup=markup,
            )
    else:
        bot.send_message(message.chat.id, 'К сожалению я ничего не нашел по Вашему запросу...')


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


def print_hotels(message, no_photo=True):
    if no_photo:
        hotels = attributes.hotels(
            api.hotels_by_destination(query_container.destination_id),
            limit=query_container.hotel_count
        )
        for i_hotel in hotels:
            url = f'https://www.hotels.com/ho{attributes.get_hotel_id(i_hotel)}'
            markup = link_markup('Перейти на страницу отеля ->', url)
            bot.send_message(message.chat.id, format.format_hotel(i_hotel), parse_mode='HTML', reply_markup=markup)
    else:
        bot.register_next_step_handler(message, _print_hotels)


def _print_hotels(message: Message) -> None:
    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'О-оу! Тут нужно вводить цифру.')
        bot.register_next_step_handler(message, _print_hotels)
        return
    elif (int(message.text) < 1) or (int(message.text) > MAX_HOTELS):
        bot.send_message(message.chat.id, f'Количество должно быть от 1 до {MAX_PHOTO}')
        bot.register_next_step_handler(message, _print_hotels)
        return
    try:
        hotels = attributes.hotels(
            api.hotels_by_destination(query_container.destination_id),
            limit=query_container.hotel_count
        )
    except Exception as exc:
        bot.send_message(message.chat.id, 'Что-то пошло не так при запросе списка отелей...')
        error_log(exc, 'Ошибка при попытке получения отеля по destination_id.')
        raise exc

    query_container.photo_count = int(message.text)
    # api.get_photo()
    # with open('photo_634418464.json', 'r') as file:
    #     response_data = json.load(file)

    # for photo in attributes.photo(data, limit=query_container.photo_count):
    #     media.append(InputMediaPhoto(formatting.format_photo(photo, 'z'), 'Hotel'))
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
    print(query_container)
