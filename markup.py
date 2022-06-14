import calendar
import locale
from datetime import date, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.callback_data import CallbackData, CallbackDataFilter


city_callback = CallbackData('destination_id', prefix='destination')
photo_callback = CallbackData('answer', prefix='photo')
command_callback = CallbackData('command_name', prefix='command')
date_choice_callback = CallbackData('year', 'month', 'day', prefix='date_choice')

EMTPY_FIELD = '1'
# написать для всех систем!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""for windows"""
locale.setlocale(locale.LC_TIME, ('Russian_Russia', '1251'))

WEEK_DAYS = [calendar.day_abbr[i] for i in range(7)]
MONTHS = [(i, calendar.month_name[i]) for i in range(1, 13)]


def yes_no_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Да', callback_data=photo_callback.new(answer='yes')))
    markup.add(InlineKeyboardButton('Нет', callback_data=photo_callback.new(answer='no')))

    return markup


def destination_markup(destinations):
    markup = InlineKeyboardMarkup()
    for item in destinations:
        markup.add(InlineKeyboardButton(
            f'{item["caption"]}',
            callback_data=city_callback.new(destination_id=item['destinationId']))
        )

    return markup


def link_markup(caption: str, url: str):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(caption, url=url))

    return markup


def calendar_days_markup(year: int, month: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=7)
    today = date.today()

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
            if day == today.day and today.year == year and today.month == month:
                day_name = '🔘'
                button = InlineKeyboardButton(
                    text=day_name,
                    callback_data=date_choice_callback.new(year=year, month=month, day=today.day)
                )
            elif day != 0:
                day_name = str(day)
                button = InlineKeyboardButton(
                    text=day_name,
                    callback_data=date_choice_callback.new(year=year, month=month, day=day_name)
                )
            else:
                button = InlineKeyboardButton(text=day_name, callback_data=EMTPY_FIELD)
            week_buttons.append(button)
        keyboard.add(*week_buttons)

    previous_date = date(year=year, month=month, day=1) - timedelta(days=1)
    next_date = date(year=year, month=month, day=1) + timedelta(days=31)

    # keyboard.add(
    #     InlineKeyboardButton(
    #         text='Previous month',
    #         callback_data=calendar_factory.new(year=previous_date.year, month=previous_date.month)
    #     ),
    #     InlineKeyboardButton(
    #         text='Zoom out',
    #         callback_data=calendar_zoom.new(year=year)
    #     ),
    #     InlineKeyboardButton(
    #         text='Next month',
    #         callback_data=calendar_factory.new(year=next_date.year, month=next_date.month)
    #     ),
    # )

    return keyboard
