import telebot
import lowprice
from telebot import formatting
from typing import Optional
from bot import bot


MAX_HOTELS = 10
MAX_PHOTO = 10


class QueryContainer:

    def __init__(self):
        self.destination_id: Optional[str] = None
        self.hotels = list()
        self.hotel_count: int = MAX_HOTELS
        self.show_photo: bool = False
        self.photo_count: int = MAX_PHOTO


query_container = QueryContainer()


@bot.message_handler(commands=['lowprice'])
def low_price(message):
    # bot.send_message(message.chat.id, 'Введите город для поиска')
    lowprice.first_step(message)


# @bot.message_handler(content_types='text')
# def answer(message: telebot.types.Message) -> None:
#     bot.send_message(message.chat.id, 'Такая команда мне не понятна...')
#
#
# def get_destination(message):
#     destinations = hotels_api_requests.get_destinations()
#     markup = destination_markup(destinations)
#     bot.send_message(
#         message.chat.id, f'Что из этого Вы имели ввиду?:',
#         reply_markup=markup,
#     )
#
#
# def print_hotels(message) -> None:
#     hotels_list = lowprice.hotel_attrs(query_container.hotel_count)
#
#     if not message.text.isdigit():
#         bot.send_message(message.chat.id, 'О-оу! Тут нужно вводить цифру.')
#         bot.register_next_step_handler(message, print_hotels)
#         return
#     elif (int(message.text) < 1) or (int(message.text) > MAX_HOTELS):
#         bot.send_message(message.chat.id, f'Количество должно быть от 1 до {MAX_PHOTO}')
#         bot.register_next_step_handler(message, print_hotels)
#         return
#
#     query_container.photo_count = int(message.text)
#     with open('photo_634418464.json', 'r') as file:
#         data = json.load(file)
#     media = list()
#
#     for photo in lowprice.formatted_photo_data(data, limit=query_container.photo_count):
#         media.append(InputMediaPhoto(photo, 'Hotel'))
#     for i_hotel in hotels_list:
#         bot.send_message(message.chat.id, i_hotel, parse_mode='HTML')
#         bot.send_media_group(message.chat.id, media)
#
#
# @bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'photo')
# def callback(call: telebot.types.CallbackQuery):
#     bot.answer_callback_query(callback_query_id=call.id, text='Выполнено')
#     if call.data.split(':')[1] == 'yes':
#         bot.edit_message_text(
#             chat_id=call.message.chat.id,
#             message_id=call.message.id,
#             text=f'Сколько фотографий показать? Не больше {MAX_PHOTO}'
#         )
#
#         query_container.show_photo = True
#         query_container.photo_count = call.data.split(':')[1]
#         bot.register_next_step_handler(call.message, print_hotels)
#     elif call.data.split(':')[1] == 'no':
#         bot.edit_message_text(
#             chat_id=call.message.chat.id,
#             message_id=call.message.id,
#             text=f'Вот отели, которые я нашел:'
#         )
#         hotels_list = lowprice.hotel_attrs(query_container.hotel_count)
#         for i_hotel in hotels_list:
#             bot.send_message(call.message.chat.id, i_hotel, parse_mode='HTML')


bot.infinity_polling()
