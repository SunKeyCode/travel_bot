from telebot.types import Message
from step_functions import print_start_message, first_step
from loader import bot, Commands
from database import DB
from keyboards.inline import inline_markup
from utils.format import parse_history_data
from config_data import config


@bot.message_handler(commands=['start'])
def start_command(message: Message) -> None:
    bot.send_message(message.chat.id, 'Привет! Я бот, начинаем!')  # дописать приветствие
    print_start_message(message)
    DB.check_user_settings(message)


@bot.message_handler(commands=['help'])
def help_command(message: Message) -> None:
    print_start_message(message)


@bot.message_handler(commands=['lowprice'])
def low_price_command(message: Message) -> None:
    first_step(message, Commands.lowprice)


@bot.message_handler(commands=['highprice'])
def high_price_command(message: Message) -> None:
    first_step(message, Commands.highprice)


@bot.message_handler(commands=['bestdeal'])
def best_deal_command(message: Message) -> None:
    first_step(message, Commands.bestdeal)


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    history_data = DB.read_history(message, config.HISTORY_DEPTH)
    history_data = parse_history_data(history_data)
    for elem in history_data:
        bot.send_message(message.chat.id, elem, parse_mode='HTML')

    print_start_message(message)


@bot.message_handler(commands=['settings'])
def settings(message: Message) -> None:
    bot.send_message(message.chat.id, '🔧 Настройки: ', reply_markup=inline_markup.settings_markup())


@bot.message_handler(content_types='text')
def other_text(message: Message) -> None:
    bot.send_message(message.chat.id, 'Такая команда мне не понятна...')


# TODO добавить документацию
