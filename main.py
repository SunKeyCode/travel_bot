import time
from datetime import date
import lowprice
import highprice
from telebot.types import Message
from bot import bot
from logs import error_log
from markup import calendar_days_markup
import callback


MAX_HOTELS = 10
MAX_PHOTO = 10


@bot.message_handler(commands=['start'])
def start_command(message: Message) -> None:
    bot.send_message(message.chat.id, 'Привет! Я бот, начинаем!')
    bot.send_message(message.chat.id, 'Вы можете использовать следующие команды:\n\n'
                                      '/lowprice - топ самых дешёвых отелей в городе.\n'
                                      '/highprice - топ самых дорогих отелей в городе.\n'
                                      '/bestdeal - топ отелей, '
                                      'наиболее подходящих по цене и расположению от центра.\n'
                                      '/history - показать историю поиска отелей.\n'
                                      '/help - показать список команд.'
                     )


@bot.message_handler(commands=['help'])
def help_command(message: Message) -> None:
    bot.send_message(message.chat.id, 'Вы можете использовать следующие команды:\n\n'
                                      '/lowprice - топ самых дешёвых отелей в городе.\n'
                                      '/highprice - топ самых дорогих отелей в городе.\n'
                                      '/bestdeal - топ отелей, '
                                      'наиболее подходящих по цене и расположению от центра.\n'
                                      '/history - показать историю поиска отелей.\n'
                                      '/help - показать список команд.'
                     )


@bot.message_handler(commands=['lowprice'])
def low_price_command(message: Message) -> None:
    lowprice.first_step(message)


@bot.message_handler(commands=['highprice'])
def high_price_command(message: Message) -> None:
    highprice.first_step(message)


@bot.message_handler(commands=['cal'])
def high_price_command(message: Message) -> None:
    now = date.today()
    bot.send_message(message.chat.id, 'Тест календаря', reply_markup=calendar_days_markup(now.year, now.month))


@bot.message_handler(content_types='text')
def other_text(message: Message) -> None:
    bot.send_message(message.chat.id, 'Такая команда мне не понятна...')


while True:
    try:
        bot.polling(none_stop=True, interval=0)
        break
    except Exception as exc:
        print('Возникло непредвиденное исключение в модуле main:', exc)
        error_log(exc, 'Непредвиденное исключение в модуле main')
        bot.stop_polling()
        time.sleep(2)
