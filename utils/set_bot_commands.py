from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot):
    """Заполняет меню команд бота"""
    # TODO однобуквенности быть недолжно
    bot.set_my_commands(
        [BotCommand(*command) for command in DEFAULT_COMMANDS]
    )

# TODO добавить документацию
