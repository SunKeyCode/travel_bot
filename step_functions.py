import hotels_api
from markup import destination_markup, yes_no_markup
from telebot.types import InputMediaPhoto
from bot import bot, query_container
import formatting
import attributes
import json


MAX_HOTELS = 10
MAX_PHOTO = 10


def get_destination(message):
    destinations = hotels_api.get_destinations()
    markup = destination_markup(destinations)
    bot.send_message(
        message.chat.id, f'Что из этого Вы имели ввиду?',
        reply_markup=markup,
        )


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
    # hotels_list = lowprice.hotel_attrs(query_container.hotel_count)
    if no_photo:
        hotels = attributes.hotels_list(hotels_api.hotels_by_destination('1506246'), limit=query_container.hotel_count)
        for i_hotel in hotels:
            bot.send_message(message.chat.id, formatting.hotel_to_str(i_hotel), parse_mode='HTML')
    else:
        bot.register_next_step_handler(message, _print_hotels)


def _print_hotels(message) -> None:
    hotels = attributes.hotels_list(hotels_api.hotels_by_destination('1506246'), limit=query_container.hotel_count)

    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'О-оу! Тут нужно вводить цифру.')
        bot.register_next_step_handler(message, _print_hotels)
        return
    elif (int(message.text) < 1) or (int(message.text) > MAX_HOTELS):
        bot.send_message(message.chat.id, f'Количество должно быть от 1 до {MAX_PHOTO}')
        bot.register_next_step_handler(message, _print_hotels)
        return

    query_container.photo_count = int(message.text)
    with open('photo_634418464.json', 'r') as file:
        data = json.load(file)
    media = list()

    for photo in attributes.photo_list(data, limit=query_container.photo_count):
        media.append(InputMediaPhoto(formatting.format_photo(photo, 'z'), 'Hotel'))
    for i_hotel in hotels:
        bot.send_message(message.chat.id, formatting.hotel_to_str(i_hotel), parse_mode='HTML')
        bot.send_media_group(message.chat.id, media)
    print(query_container)
