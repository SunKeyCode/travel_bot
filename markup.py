from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.callback_data import CallbackData, CallbackDataFilter


city_callback = CallbackData('destination_id', prefix='destination')
photo_callback = CallbackData('answer', prefix='photo')
command_callback = CallbackData('command_name', prefix='command')


def command_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('lowprice', callback_data=command_callback.new(command_name='lowprice')))
    markup.add(InlineKeyboardButton('highprice', callback_data=command_callback.new(command_name='highprice')))
    markup.add(InlineKeyboardButton('bestdeal', callback_data=command_callback.new(command_name='bestdeal')))
    markup.add(InlineKeyboardButton('history', callback_data=command_callback.new(command_name='history')))

    return markup


def yes_no_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Да', callback_data=photo_callback.new(answer='yes')))
    markup.add(InlineKeyboardButton('Нет', callback_data=photo_callback.new(answer='no')))

    return markup


def destination_markup(destinations):
    markup = InlineKeyboardMarkup()
    for item in destinations:
        markup.add(InlineKeyboardButton(
            f'{item["caption"]}',
            callback_data=city_callback.new(destination_id=item['destinationId']))
        )

    return markup


def link_markup(caption: str, url: str):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(caption, url=url))

    return markup
