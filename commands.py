import telebot
import hotels_api
from markup import destination_markup


class Commands:

    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot


class LowPrice(Commands):

    def __init__(self, bot):
        super().__init__(bot)
