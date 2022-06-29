from telebot.types import Message, CallbackQuery
import step_functions
from bot import bot, queries, QueryContainer, Commands,MAX_HOTELS, MAX_PHOTO
from typing import Dict


def first_step(message: Message):
    bot.send_message(message.chat.id, 'Введите название города для поиска:')
    queries[message.chat.id]: Dict[QueryContainer] = QueryContainer(user_id=int(message.chat.id), command=Commands.lowprice)
    bot.register_next_step_handler(message, step_functions.print_destinations)
