import logs.logs as log

from time import sleep
from loader import bot
from database import DB
from utils.set_bot_commands import set_default_commands

from handlers.callback_handlers import callback
from handlers.default_handlers import handlers


DB.check_sql_tables()
set_default_commands(bot)

while True:
    try:
        bot.polling(none_stop=True, interval=0)
        break
    # TODO базовые исключения не ловим
    # TODO объявите свое от Exception и ловите его
    except Exception as exc:
        print('Возникло непредвиденное исключение в модуле main:', exc)
        log.error_log(exc, 'Непредвиденное исключение в модуле main')
        bot.stop_polling()
        sleep(2)
