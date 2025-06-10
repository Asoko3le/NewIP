from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton,   InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder


main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подробнее про направление📍', callback_data='Podrobnee')],
    [InlineKeyboardButton(text='Выбрать уч. заведение🏫', callback_data='UchebZavedbez:')],
    [InlineKeyboardButton(text='Обзор всех направлений🔍', callback_data='obzor_napravleniy')],
    [InlineKeyboardButton(text='Дополнительно🖇', callback_data='Dop')]
])


vibor_first_napr = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Физико-математические🧮', callback_data='vibor:F')],
    [InlineKeyboardButton(text='Гуманитарные✍', callback_data='vibor:G')],
    [InlineKeyboardButton(text='Химико-биолгиеческие🧪', callback_data='vibor:H')],
    [InlineKeyboardButton(text='Назад📌', callback_data='main:')]
])
first_napr_vyz = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Физико-математические🧮', callback_data='VyzS:F')],
    [InlineKeyboardButton(text='Гуманитарные✍', callback_data='VyzS:G')],
    [InlineKeyboardButton(text='Химико-биолгиеческие🧪', callback_data='VyzS:H')],
    [InlineKeyboardButton(text='Назад📌', callback_data='main:')]
])
first_napr_kol = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Физико-математические🧮', callback_data='KolS:F')],
    [InlineKeyboardButton(text='Гуманитарные✍', callback_data='KolS:G')],
    [InlineKeyboardButton(text='Химико-биолгиеческие🧪', callback_data='KolS:H')],
    [InlineKeyboardButton(text='Назад📌', callback_data='main:')]
])

vibor_obzor = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Физико-математические🧮', callback_data='Oobzor:F')],
    [InlineKeyboardButton(text='Гуманитарные✍', callback_data='Oobzor:G')],
    [InlineKeyboardButton(text='Химико-биолгиеческие🧪', callback_data='Oobzor:H')],
    [InlineKeyboardButton(text='Назад📌', callback_data='main:')]
])




start_bot = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Я знаю направление☑️', callback_data='znayu')],
    [InlineKeyboardButton(text='Пройти мини-тест📝', callback_data='StartTest')]
])

test_nach = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Приступить>>>', callback_data='TEST:1#')],
    [InlineKeyboardButton(text='Назад📌', callback_data='main:')]
])


Dop = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Выбрать другое направление🔍', callback_data='obzor_napravleniy')],
    [InlineKeyboardButton(text='Пройти тест на направление📝', callback_data='StartTest')],
    [InlineKeyboardButton(text='Бесплатные курсы📚', url = 'https://dopobr.petersburgedu.ru')],
    [InlineKeyboardButton(text='Поддержка кураторов💻', callback_data='Support')],
    [InlineKeyboardButton(text='Назад📌', callback_data='main:')]
])


mainTP = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Написать вопрос?!', callback_data='help')],
    [InlineKeyboardButton(text='<Вернуться', callback_data='main:')] 
])
closeTP = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='<Вернуться', callback_data='main:')]   
])

