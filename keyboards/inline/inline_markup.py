import calendar
import locale

from typing import Optional, List
from loader import Locale, Currency
from datetime import date, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.callback_data import CallbackData
from sys import platform


destination_callback = CallbackData('destination_id', prefix='destination')
photo_callback = CallbackData('answer', prefix='photo')
date_choice_callback = CallbackData('year', 'month', 'day', prefix='date_choice')
change_month_callback = CallbackData('year', 'month', prefix='change_month')

EMTPY_FIELD = '1'

if platform == 'win32':
    locale.setlocale(locale.LC_TIME, ('Russian_Russia', '1251'))
elif platform == 'darwin':
    locale.setlocale(locale.LC_TIME, ('ru_RU', 'UTF-8'))

WEEK_DAYS = [calendar.day_abbr[i] for i in range(7)]
MONTHS = [(i, calendar.month_name[i]) for i in range(1, 13)]


def settings_markup(mode: str = 'main', current: Optional[str] = None) -> InlineKeyboardMarkup:
    """
    Создает кнопки меню settings.
    :param mode: страница меню для которого создаются кнопки (может принимать значения main, locale, currency)
    :param current: текущее значение в БД (помечается при создании кнопки)
    :return: markup
    :rtype: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup()
    if mode == 'main':
        markup.add(InlineKeyboardButton('язык запросов (locale)', callback_data='settings:main:locale'))
        markup.add(InlineKeyboardButton('валюта (currency)', callback_data='settings:main:currency'))
        markup.add(InlineKeyboardButton('❌ Выход', callback_data='settings:main:exit'))
    elif mode == 'locale':
        for elem in Locale:
            if current == elem.name:
                markup.add(InlineKeyboardButton(f'{elem.value} ☑', callback_data=f'settings:locale:{elem.name}'))
            else:
                markup.add(InlineKeyboardButton(f'{elem.value}', callback_data=f'settings:locale:{elem.name}'))
        markup.add(InlineKeyboardButton('🔙 Назад', callback_data='settings:locale:exit'))
    elif mode == 'currency':
        for elem in Currency:
            if current == elem.name:
                markup.add(InlineKeyboardButton(f'{elem.value}  ☑', callback_data=f'settings:currency:{elem.name}'))
            else:
                markup.add(InlineKeyboardButton(f'{elem.value}', callback_data=f'settings:currency:{elem.name}'))
        markup.add(InlineKeyboardButton('🔙 Назад', callback_data='settings:currency:exit'))

    return markup


def yes_no_markup() -> InlineKeyboardMarkup:
    """Кнопки да/нет для фотографий отеля"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('✅ Да', callback_data=photo_callback.new(answer='yes')))
    markup.add(InlineKeyboardButton('❌ Нет', callback_data=photo_callback.new(answer='no')))

    return markup


def destination_markup(destinations: List) -> InlineKeyboardMarkup:
    """
    Формирует кнопки для выбора города.
    :param destinations: список, содержащий все найденные варианты по запросу пользователя.
    :return: markup
    :rtype: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup()
    for item in destinations:
        markup.add(InlineKeyboardButton(
            f'{item["caption"]}',
            callback_data=destination_callback.new(destination_id=item['destinationId']))
        )

    return markup


def link_markup(caption: str, url: str):
    """
    Кнопка ссылки на страницу отеля.
    :param caption: заголовок кнопки
    :param url: url страницы
    :return: markup
    :rtype: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(caption, url=url))

    return markup


def calendar_days_markup(year: int, month: int, limit_date: Optional[date] = None) -> InlineKeyboardMarkup:
    """
    Формирует календарь для выбора дат заезда/выезда.
    :param year: текущий год
    :param month: месяц
    :param limit_date: дата, от которой показываем дни в календаре (дни меньше этой даты отображаются пустыми клетками)
    :return: markup
    :rtype: InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardMarkup(row_width=7)

    keyboard.add(
        InlineKeyboardButton(
            text=date(year=year, month=month, day=1).strftime('%b %Y'),
            callback_data=EMTPY_FIELD
        )
    )
    keyboard.add(*[InlineKeyboardButton(text=day, callback_data=EMTPY_FIELD) for day in WEEK_DAYS])
    for week in calendar.Calendar().monthdayscalendar(year=year, month=month):
        week_buttons = []
        for day in week:
            day_name = ' '
            if day == limit_date.day and limit_date.year == year and limit_date.month == month:
                day_name = '🔘'
                button = InlineKeyboardButton(
                    text=day_name,
                    callback_data=date_choice_callback.new(year=year, month=month, day=limit_date.day)
                )
            elif day != 0:
                curr_date = date(year=year, month=month, day=day)
                if curr_date > limit_date:
                    day_name = str(day)
                    button = InlineKeyboardButton(
                        text=day_name,
                        callback_data=date_choice_callback.new(year=year, month=month, day=day_name)
                    )
                else:
                    button = InlineKeyboardButton(text=day_name, callback_data=EMTPY_FIELD)
            else:
                button = InlineKeyboardButton(text=day_name, callback_data=EMTPY_FIELD)
            week_buttons.append(button)
        keyboard.add(*week_buttons)

    previous_date = date(year=year, month=month, day=1) - timedelta(days=1)
    next_date = date(year=year, month=month, day=1) + timedelta(days=31)
    if previous_date >= limit_date:
        callback_date = change_month_callback.new(year=previous_date.year, month=previous_date.month)
        text = '⬅ пред. месяц'
    else:
        callback_date = EMTPY_FIELD
        text = ' '
    keyboard.add(
        InlineKeyboardButton(
            text=text,
            callback_data=callback_date
        ),
        InlineKeyboardButton(
            text='след. месяц ➡',
            callback_data=change_month_callback.new(year=next_date.year, month=next_date.month)
        )
    )

    return keyboard

# TODO добавить документацию

