from aiogram import F, Router, types, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import re
import sqlite3
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton,   InlineKeyboardMarkup)
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton,   InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bs4 import *
import requests


bot = Bot(token='7590317034:AAFmD3C2fLxlyq9WeMUgKd6Vuy7F3YHSoJw')






def firstconnect(user_id):
    conn = sqlite3.connect('struct.db')
    cursor = conn.cursor()

    cursor.execute('SELECT napravlenie FROM users WHERE user_id = ?',(user_id,))
    napr = cursor.fetchone()
    if napr == None or napr[0] == None:
        return False
    else:
        return True
    
    
def vidacha_dannih_firststart(user_id):
    conn = sqlite3.connect('struct.db')
    cursor = conn.cursor()

    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)',(user_id,))
    conn.commit()
    cursor.execute('INSERT OR IGNORE INTO vyzfilter (user_id, gorod1, gorod2) VALUES (?,?,?)',(user_id,"No",'No',))
    conn.commit()


def newTEST(user_id):
    conn = sqlite3.connect('struct.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT OR REPLACE INTO test_result 
    (user_id, Inz, It, Mark, Him, Econ, Bot, Alle, Psihoter, Ecol, Psiholog, Prep, Zhur, Adv, Fin, Buh)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (user_id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    conn.commit()

def process_input(text):
    
    parts = text.split('/')
    
    if len(parts) == 1:
        a = parts[0]
        b = None
    elif len(parts) == 2:
        a = parts[0]
        b = parts[1]
    elif len(parts) == 3:
        a = parts[0]
        b = parts[1]

    return a,b

def test_otvet(user_id,otveti):
    conn = sqlite3.connect('struct.db')
    cursor = conn.cursor()
    otvet1, otvet2 = process_input(otveti)
    if otveti is None or otveti == '':
        return
    if otvet2 != None:
        cursor.execute(f'UPDATE test_result SET {otvet1} = {otvet1} + 1 ,{otvet2} = {otvet2} + 1 WHERE user_id = ?', (user_id,))
        conn.commit()
    else:
        cursor.execute(f'UPDATE test_result SET {otvet1} = {otvet1} + 1 WHERE user_id = ?', (user_id,))
        conn.commit()
    
def help_sort_test(user_id):
    conn = sqlite3.connect('struct.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, Inz, It, Mark, Him, Econ, Bot, Alle, Psihoter, Ecol, Psiholog, Prep, Zhur, Adv, Fin, Buh  FROM test_result WHERE user_id = ?' ,(user_id,))
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0]
        professions = {
            'F1': row[1],
            'F2': row[2],
            'G1': row[3],
            'H1': row[4],
            'F3': row[5],
            'H5': row[6],
            'H4': row[7],
            'H3': row[8],
            'H2': row[9],
            'G5': row[10],
            'G4': row[11],
            'G3': row[12],
            'G2': row[13],
            'F5': row[14],
            'F4': row[15]
    }
    sorted_professions = sorted(professions.items(), key=lambda x: x[1], reverse=True)
    
    max_nap = sorted_professions[0][0]
    max_nap2 = sorted_professions[1][0]
    return max_nap, max_nap2


def help_test_2(user_id):
    conn = sqlite3.connect('struct.db')
    cursor = conn.cursor()
    max_nap, max_nap2 = help_sort_test(user_id)
    cursor.execute('SELECT name FROM directions WHERE code = ?', (max_nap,))
    re11 = cursor.fetchone()
    result1 = re11[0]
    cursor.execute('SELECT name FROM directions WHERE code = ?', (max_nap2,))
    re22 = cursor.fetchone()
    result2 = re22[0]

    return result1,result2

def start_help(user_id):
    conn = sqlite3.connect('struct.db')
    cursor = conn.cursor()

    cursor.execute('SELECT napravlenie FROM users WHERE user_id = ?',(user_id,))
    napravlenie_code = cursor.fetchone()
    cursor.execute('SELECT name, Descript FROM directions WHERE code = ?',(napravlenie_code[0],))
    Napravlenie, opisanie= cursor.fetchone()
    return Napravlenie, opisanie, napravlenie_code[0]



def KB(code,data,lastdata):
    conn = sqlite3.connect('struct.db')
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT code, name FROM directions WHERE code LIKE '{code}%'")
    result = cursor.fetchall()
    builder = InlineKeyboardBuilder()
    for NameCode in result:

        builder.button(text=f"{NameCode[1]}", callback_data=f"{data}:{NameCode[0]}:1")
    builder.button(text=f"Назад<<<", callback_data=f"{lastdata}")
    builder.adjust(1)
    kb = builder.as_markup()
    
    if code == "F":
        ykl = 'физико-математическим уклоном'
        return kb, ykl
    elif code == "G":
        ykl = 'гуманитарным уклоном'
        return kb, ykl
    elif code == "H":
        ykl = 'химико-биологическим уклоном'
        return kb, ykl


def NewNapr(user_id,Code):
    conn = sqlite3.connect('struct.db')
    cursor = conn.cursor()
    
    cursor.execute(f'UPDATE users SET napravlenie = "{Code}" WHERE user_id = ?',(user_id,))
    conn.commit()


def about_napr(code):
    conn = sqlite3.connect('struct.db')
    cursor = conn.cursor()

    cursor.execute('SELECT name, Descript FROM directions WHERE code = ?',(code,))
    Napravlenie, opisanie= cursor.fetchone()
    return Napravlenie, opisanie, code


def viborat_nazad_test(code):
    conn = sqlite3.connect('struct.db')
    cursor = conn.cursor()
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Выбрать', callback_data=f'main:{code}')],
    [InlineKeyboardButton(text='Поменять', callback_data='znayu')],
    [InlineKeyboardButton(text='Пройти мини-тест', callback_data='StartTest')],
    [InlineKeyboardButton(text='Назад<<<', callback_data='main:')]
])
    return kb

def obzorKB(code,zaved):
    conn = sqlite3.connect('struct.db')
    cursor = conn.cursor()
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Уч. заведения по направлению🏫', callback_data=f'UchebZaved:{code}')],
    [InlineKeyboardButton(text='Бесплатные курсы📚', url='https://dopobr.petersburgedu.ru/')],
    [InlineKeyboardButton(text='Сменить направление', callback_data=f'main:{code}')],
    [InlineKeyboardButton(text='Назад<<<', callback_data='main:')]
])
    return kb



def vyzkb(user_id, code, stranic, zaved):
    conn = sqlite3.connect('struct.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT sokrash, {zaved.lower()}_sokr, gorodind FROM {zaved.lower()} WHERE napravlenie = ?',(code,))
    resulty = cursor.fetchall()
    result = resulty[10*(stranic-1):10*(stranic)]
    cursor.execute(f'SELECT gorod1,gorod2 FROM vyzfilter WHERE user_id = ?',(user_id,))
    resultgorod = cursor.fetchone()
    if 'No' not in resultgorod[0] or 'No' not in resultgorod[1]:
        vrem = []
        for i in resulty:
            if i[2] in resultgorod:
                vrem.append(i)
        resulty = vrem
    result = resulty[10*(stranic-1):10*(stranic)]

    builder = InlineKeyboardBuilder()
    for SokrTeg in result:
        if "No" in resultgorod[1] and "No" in resultgorod[0] :
            builder.button(text=f"{SokrTeg[0]}", callback_data=f"{zaved}:{SokrTeg[1]}")
        elif SokrTeg[2] in resultgorod: 
            builder.button(text=f"{SokrTeg[0]}", callback_data=f"{zaved}:{SokrTeg[1]}")
    if stranic*10 < len(resulty):
        builder.button(text=f"Дальше>>>", callback_data=f"{zaved}W:{code}:{stranic+1}")
    if stranic > 1:
        builder.button(text=f"Вернуться<<<", callback_data=f"{zaved}W:{code}:{stranic-1}")
    builder.button(text=f"Настройки поиска⚙️", callback_data=f"filtr::{zaved}")
    builder.button(text=f"Назад<<<", callback_data=f"main:")
    builder.adjust(1)
    kb = builder.as_markup()
    
    cursor.execute(f'UPDATE vyzfilter SET category = "{code}" WHERE user_id = ?',(user_id,))
    conn.commit()
    cursor.execute('SELECT name FROM directions WHERE code = ?',(code,))
    name = cursor.fetchone()
    return kb, name[0]

def clr_fltr(user_id):
    conn = sqlite3.connect('struct.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE vyzfilter SET gorod1 = "No", gorod2 = "No" WHERE user_id = ?',(user_id,))
    conn.commit()

def filtrkb(user_id,zaved):
    conn = sqlite3.connect('struct.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT category FROM vyzfilter WHERE user_id =?',(user_id,))
    codik = cursor.fetchone()
    try:
        cursor.execute(f'SELECT gorod,gorodind FROM {zaved.lower()} WHERE napravlenie = ?',(codik[0],))
        resultsity = cursor.fetchall()
    except: 
        pass

    cursor.execute('SELECT gorod1, gorod2 FROM vyzfilter WHERE user_id = ?',(user_id,))
    goroda = cursor.fetchone()

    builder = InlineKeyboardBuilder()

    for kbinf in set(resultsity):
        
        if kbinf[1] in goroda:
            builder.button(text=f"{kbinf[0]}✅", callback_data=f"filtr:{kbinf[1]}:{zaved}")
        else:
            builder.button(text=f"{kbinf[0]}", callback_data=f"filtr:{kbinf[1]}:{zaved}")
    
    builder.button(text=f"Назад<<<", callback_data=f"{zaved}W:{codik[0]}:1")
    builder.adjust(1)
    kb = builder.as_markup()
    return kb


def addgorodfilter(user_id,city):
    conn = sqlite3.connect('struct.db')
    cursor = conn.cursor()

    if city is None or city == "":
        return

    cursor.execute('SELECT gorod1,gorod2 FROM vyzfilter WHERE user_id = ?',(user_id,))
    gorod1,gorod2 = cursor.fetchone()
    if gorod1 == 'No' and gorod2 =="No":
        cursor.execute(f'UPDATE vyzfilter SET gorod1 = "{city}" WHERE user_id =?',(user_id,))
        conn.commit()
    elif gorod2 == city:
        cursor.execute('UPDATE vyzfilter SET gorod2 = "No" WHERE user_id =?',(user_id,))
        conn.commit()
    elif gorod1 == city:
        cursor.execute('UPDATE vyzfilter SET gorod1 = "No" WHERE user_id =?',(user_id,))
        conn.commit()
    elif gorod1 != 'No' and gorod2 == 'No':
        cursor.execute(f'UPDATE vyzfilter SET gorod2 = "{city}" WHERE user_id =?',(user_id,))
        conn.commit()
    elif gorod2 != 'No' and gorod1 == 'No':
        cursor.execute(f'UPDATE vyzfilter SET gorod1 = "{city}" WHERE user_id =?',(user_id,))
        conn.commit()


def infovyz(codevyz,zaved):
    conn = sqlite3.connect('struct.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT gorod, polnoe, prbb, prbp, site FROM {zaved} WHERE {zaved}_sokr =?',(codevyz,))
    gorod, polnoe, prbb, prbp, site = cursor.fetchone()
    return gorod, polnoe, prbb, prbp, site


def KeyBVyz(site,code,zaved):
    conn = sqlite3.connect('struct.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT napravlenie FROM {zaved.lower()} WHERE {zaved.lower()}_sokr = ? ",(code,))
    codenap = cursor.fetchone()
    KeyBoard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сайт учебного заведения🌐', url=f'{site}')],
    [InlineKeyboardButton(text='Что такое "Проходной бал"?', callback_data=f'prohodnoy:{code}:{zaved}')],
    [InlineKeyboardButton(text='Назад📌', callback_data=f'{zaved}W:{codenap[0]}:1')]
])
    return KeyBoard
def KeyBKol(site,code,zaved):
    conn = sqlite3.connect('struct.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT napravlenie FROM {zaved.lower()} WHERE {zaved.lower()}_sokr = ? ",(code,))
    codenap = cursor.fetchone()
    KeyBoard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сайт учебного заведения🌐', url=f'{site}')],
    [InlineKeyboardButton(text='Назад📌', callback_data=f'{zaved}W:{codenap[0]}')]
])
    return KeyBoard




