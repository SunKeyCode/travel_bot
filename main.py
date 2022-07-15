import logs.logs as log

from telebot.types import Message
from time import sleep
from loader import bot
from database import DB
from utils.set_bot_commands import set_default_commands

from handlers.callback_handlers import callback
from handlers.default_handlers import handlers


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
    DB.check_user_settings(message)


DB.check_sql_tables()
set_default_commands(bot)

while True:
    try:
        bot.polling(none_stop=True, interval=0)
        break
    except Exception as exc:
        print('Возникло непредвиденное исключение в модуле main:', exc)
        log.error_log(exc, 'Непредвиденное исключение в модуле main')
        bot.stop_polling()
        sleep(2)
