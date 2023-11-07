from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from calendar import Calendar
from datetime import date

from filters import *


rt = Router()
calendar = Calendar()
current_month = None


@rt.message(Command('calendar'), Admin() or Manager())
async def show_calendar(message: Message):
    global current_month
    current_month = date(date.today().year, date.today().month, 1)
    kb = await create_calendar()
    await message.answer('Календар', reply_markup=kb)


@rt.callback_query(F.data == 'previous')
async def previous_month(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=await create_calendar(-1))



@rt.callback_query(F.data == 'next')
async def previous_month(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=await create_calendar(1))


async def create_calendar(shift: int = 0) -> InlineKeyboardMarkup:
    global current_month
    try:
        current_month = date(current_month.year, current_month.month+shift, 1)
    except ValueError:
        current_month = date(current_month.year+shift, current_month.month+shift-shift*12, 1)
    year = current_month.strftime('%B %Y')
    days_list = calendar.monthdayscalendar(current_month.year, current_month.month)
    weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд']
    calendar_keys = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=year, callback_data=year)],
        [InlineKeyboardButton(text=day, callback_data=day) for day in weekdays],
        *[[InlineKeyboardButton(text=str(day) if day else ' ',
                                callback_data=str(day)) for day in week] for week in days_list],
        [
            InlineKeyboardButton(text='<-', callback_data='previous'),
            InlineKeyboardButton(text=' ', callback_data=' '),
            InlineKeyboardButton(text='->', callback_data='next')
        ]
    ])
    return calendar_keys
