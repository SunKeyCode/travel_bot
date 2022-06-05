import telebot
from typing import Dict, List
import step_functions
from bot import bot


def first_step(message):
    bot.send_message(message.chat.id, 'Введите город для поиска')
    bot.register_next_step_handler(message, step_functions.get_destination)


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'destination')
def callback(call: telebot.types.CallbackQuery):

    bot.answer_callback_query(callback_query_id=call.id, text='Выполнено')
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=f'Сколько отелей показать? Не больше 10'
    )

    # query_container.destination_id = call.data.split(':')[1]
    bot.register_next_step_handler(call.message, step_functions.show_photo)


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'photo')
def callback(call: telebot.types.CallbackQuery):
    bot.answer_callback_query(callback_query_id=call.id, text='Выполнено')
    if call.data.split(':')[1] == 'yes':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=f'Сколько фотографий показать? Не больше 10'
        )

        # query_container.show_photo = True
        # query_container.photo_count = call.data.split(':')[1]
        # bot.register_next_step_handler(call.message, print_hotels)
        step_functions.print_hotels(message=call.message, no_photo=False)
    elif call.data.split(':')[1] == 'no':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=f'Вот отели, которые я нашел:'
        )
        step_functions.print_hotels(message=call.message, no_photo=True)


def hotel_attrs_to_string(hotels: List):
    strings = list()
    for i_hotel in hotels:
        hotel_content = list()
        hotel_content.append('<b>Название</b>: {}'.format(i_hotel['name']))
        hotel_content.append('<b>Адрес</b>: {}, {}, {}, {}, {}'.format(
            i_hotel['address']['postalCode'],
            i_hotel['address']['countryName'],
            i_hotel['address']['region'],
            i_hotel['address']['locality'],
            i_hotel['address']['streetAddress']
            )
        )
        hotel_content.append('<b>Расстояние от центра</b>: {}'.format(i_hotel['landmarks'][0]['distance']))
        strings.append('\n'.join(hotel_content))

    return strings


if __name__ == '__main__':
    pass
