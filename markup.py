from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.callback_data import CallbackData, CallbackDataFilter


city_callback = CallbackData('destination_id', prefix='destination')
photo_callback = CallbackData('answer', prefix='photo')


def yes_no_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Да', callback_data=photo_callback.new(answer='yes')))
    markup.add(InlineKeyboardButton('Нет', callback_data=photo_callback.new(answer='no')))

    return markup


def destination_markup(destinations):
    markup = InlineKeyboardMarkup()
    for item in destinations:
        markup.add(InlineKeyboardButton(
            f'{item["name"]}, {item["caption"]}',
            callback_data=city_callback.new(destination_id=item['destinationId']))
        )

    return markup


def link_markup(caption: str, url: str):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(caption, url=url))

    return markup
