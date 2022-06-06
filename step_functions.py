import hotels_api
from markup import destination_markup, yes_no_markup, link_markup
from telebot.types import InputMediaPhoto
from bot import bot, query_container
import formatting
import attributes


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
    if no_photo:
        hotels = attributes.hotels_list(hotels_api.hotels_by_destination('1506246'), limit=query_container.hotel_count)
        for i_hotel in hotels:
            url = f'https://www.hotels.com/ho{attributes.get_hotel_id(i_hotel)}'
            markup = link_markup('Перейти на страницу отеля ->', url)
            bot.send_message(message.chat.id, formatting.hotel_to_str(i_hotel), parse_mode='HTML', reply_markup=markup)
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
    # hotels_api.get_photo()
    # with open('photo_634418464.json', 'r') as file:
    #     response_data = json.load(file)

    # for photo in attributes.photo_list(data, limit=query_container.photo_count):
    #     media.append(InputMediaPhoto(formatting.format_photo(photo, 'z'), 'Hotel'))
    for i_hotel in hotels:
        hotel_id = attributes.get_hotel_id(i_hotel)
        response_data = hotels_api.get_photo(hotel_id)
        media = list()
        for photo in attributes.photo_list(response_data, limit=query_container.photo_count):
            media.append(InputMediaPhoto(formatting.format_photo(photo, 'z'), i_hotel['name']))
        url = f'https://www.hotels.com/ho{attributes.get_hotel_id(i_hotel)}'
        markup = link_markup('Перейти на страницу отеля ->', url)
        bot.send_media_group(message.chat.id, media)
        bot.send_message(message.chat.id, formatting.hotel_to_str(i_hotel), parse_mode='HTML', reply_markup=markup)
    print(query_container)
