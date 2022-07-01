from telebot.types import Message
from time import sleep
from loader import bot, Commands
from logs import error_log
from step_functions import first_step
import DB
from utils.format import parse_history_data
from step_functions import print_start_message
from utils.set_bot_commands import set_default_commands

import handlers.callback_handlers.callback


@bot.message_handler(commands=['start'])
def start_command(message: Message) -> None:
    bot.send_message(message.chat.id, 'Привет! Я бот, начинаем!')
    bot.send_message(message.chat.id, 'Вы можете использовать следующие команды:\n\n'
                                      '/lowprice - топ самых дешёвых отелей в городе.\n'
                                      '/highprice - топ самых дорогих отелей в городе.\n'
                                      '/bestdeal - топ отелей, '
                                      'наиболее подходящих по цене и расположению от центра.\n'
                                      '/history - показать историю поиска отелей.\n'
                                      '/settings - настройки бота.\n'
                                      '/help - показать список команд.'
                     )
    DB.check_settings_table(message)


@bot.message_handler(commands=['help'])
def help_command(message: Message) -> None:
    bot.send_message(message.chat.id, 'ℹ Вы можете использовать следующие команды:\n\n'
                                      '/lowprice - топ самых дешёвых отелей в городе.\n'
                                      '/highprice - топ самых дорогих отелей в городе.\n'
                                      '/bestdeal - топ отелей, '
                                      'наиболее подходящих по цене и расположению от центра.\n'
                                      '/history - показать историю поиска отелей.\n'
                                      '/help - показать список команд.'
                     )


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
def best_deal_command(message: Message) -> None:
    history_data = DB.get_history(message, 0)
    history_data = parse_history_data(history_data)
    for elem in history_data:
        bot.send_message(message.chat.id, elem, parse_mode='HTML')

    print_start_message(message)


@bot.message_handler(content_types='text')
def other_text(message: Message) -> None:
    bot.send_message(message.chat.id, 'Такая команда мне не понятна...')


DB.check_sql_tables()
set_default_commands(bot)

while True:
    try:
        bot.polling(none_stop=True, interval=0)
        break
    except Exception as exc:
        print('Возникло непредвиденное исключение в модуле main:', exc)
        error_log(exc, 'Непредвиденное исключение в модуле main')
        bot.stop_polling()
        sleep(2)
