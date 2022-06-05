import hotels_api_requests
from markup import destination_markup


def next_step(bot, message, step=None):
    bot = bot
    bot.register_next_step_handler(message, get_destination)


def get_destination(message):
    destinations = hotels_api_requests.get_destinations()
    markup = destination_markup(destinations)
    bot.send_message(
        message.chat.id, f'Что из этого Вы имели ввиду?:',
        reply_markup=markup,
        )
