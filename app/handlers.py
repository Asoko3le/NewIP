from aiogram import F, Router, types, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, Filter, CommandObject
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import sqlite3
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton,   InlineKeyboardMarkup, InputMediaPhoto, Message)
from app.defs import * 


class SupportState(StatesGroup):
    waiting_for_message = State()
    wait_answer = State()


import app.keyboards as kb

# роутер, для замены dp
router = Router()
bot = Bot(token='7590317034:AAFmD3C2fLxlyq9WeMUgKd6Vuy7F3YHSoJw')

conn = sqlite3.connect('struct.db')
cursor = conn.cursor()
ADMINss_ID='7454057015'



@router.message(Command("start"))
async def cmd_start(message: types.Message, command: CommandObject, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    await state.clear() 
    if firstconnect(user_id) == False: 
        vidacha_dannih_firststart(user_id) 
        await bot.send_message(ADMINss_ID, f'Новый пользователь:\nID: {user_id}\n@{username}')
        await message.answer(f"ProfitY — ваш помощник в выборе образовательного направления и соответствующего вуза\n\nРады приветствовать тебя! Приветствуем тебя! Выбери направление, или пройди небольшой тест для определения возможных вариантов!",
            reply_markup=kb.start_bot)
    else:
        Napravlenie, opisanie, code_for = start_help(user_id)
        await message.answer(f'Ваше направление:\n{Napravlenie}\n\nНайди подходящие курсы на портале и реши куда поступать!',reply_markup=kb.main_menu)


@router.callback_query(lambda c: c.data.startswith('main:'))
async def tsh(callback: types.CallbackQuery):
    unique = callback.data.split(":")[1]
    user_id = callback.from_user.id
    username =callback.from_user.username
    if unique !='':
        NewNapr(user_id, unique)
    if firstconnect(user_id) == False: 
        vidacha_dannih_firststart(user_id) 
        await bot.send_message(ADMINss_ID, f'Новый пользователь:\nID: {user_id}\n@{username}')
        await callback.message.edit_text(f"ProfitY — ваш помощник в выборе образовательного направления и соответствующего вуза\n\nРады приветствовать тебя! Приветствуем тебя! Выбери направление, или пройди небольшой тест для определения возможных вариантов!",
                                         reply_markup=kb.start_bot)
    else:
        Napravlenie, opisanie, code_for = start_help(user_id)
        await callback.message.edit_text(f'Ваше направление:\n{Napravlenie}\n\nНайди подходящие курсы на портале и реши куда поступать!',reply_markup=kb.main_menu)


@router.callback_query(F.data=='Podrobnee')
async def tsh(callback: CallbackQuery):
    user_id = callback.from_user.id
    clr_fltr(user_id)
    Napravlenie, opisanie, code_for = start_help(user_id)
    podrob = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Уч. заведения по направлению🏫', callback_data=f'UchebZaved:{code_for}:1')],
    [InlineKeyboardButton(text='Бесплатные курсы📚', url = 'https://dopobr.petersburgedu.ru')],
    [InlineKeyboardButton(text='Назад📌', callback_data='main:')]
])
    await callback.message.edit_text(f'{opisanie}',reply_markup=podrob)


@router.callback_query(F.data=='znayu')
async def tsh(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите уклон направления",reply_markup=kb.vibor_first_napr)



@router.callback_query(lambda c: c.data.startswith("vibor:"))
async def tsh(callback: types.CallbackQuery, state: FSMContext):
    unique = callback.data.split(":")[1]
    user_id = callback.from_user.id
    username =callback.from_user.username
    keyboard, ykl = KB(unique,"FVIBOR","znayu")
    await callback.message.edit_text(f'Направления с {ykl}',reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith("FVIBOR:"))
async def tsh(callback: types.CallbackQuery, state: FSMContext):
    unique = callback.data.split(":")[1]
    user_id = callback.from_user.id
    username =callback.from_user.username
    Napravlenie, opisanie, code = about_napr(unique)
    kbr = viborat_nazad_test(code)
    await callback.message.edit_text(f'{opisanie}',reply_markup=kbr)




@router.callback_query(F.data=='obzor_vyzov')
async def tsh(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username
    clr_fltr(user_id)
    await callback.message.edit_text("Выберите уклон направления",reply_markup=kb.first_napr_vyz)


@router.callback_query(lambda c: c.data.startswith("VyzS:"))
async def tsh(callback: types.CallbackQuery, state: FSMContext):
    unique = callback.data.split(":")[1]
    user_id = callback.from_user.id
    username =callback.from_user.username
    keyboard, ykl = KB(unique,"VyzW","obzor_vyzov")
    await callback.message.edit_text(f"Подборка вузов с {ykl}",reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith("VyzW:"))
async def tsh(callback: types.CallbackQuery, state: FSMContext):
    unique = callback.data.split(":")[1]
    stranic = int(callback.data.split(":")[2])
    user_id = callback.from_user.id
    username =callback.from_user.username
    kbr , name = vyzkb(user_id, unique,stranic,'Vyz')
    await callback.message.edit_text(f"Подборка вузов по профессии - {name}",reply_markup=kbr)



@router.callback_query(lambda c: c.data.startswith("filtr:"))
async def tsh(callback: types.CallbackQuery, state: FSMContext):
    unique = callback.data.split(":")[1]
    zaved = callback.data.split(":")[2]
    user_id = callback.from_user.id
    username =callback.from_user.username
    addgorodfilter(user_id,unique)

    kbr = filtrkb(user_id,zaved)
    try:
        await callback.message.edit_text(f"Выберите город для поиска",reply_markup=kbr)
    except:
        await callback.answer('Максимум фальтров')
        await callback.message.edit_text(f"Выберите город для поиска\n(2 города макс.)",reply_markup=kbr)


@router.callback_query(lambda c: c.data.startswith("Vyz:"))
async def tsh(callback: types.CallbackQuery, state: FSMContext):
    unique = callback.data.split(":")[1]
    user_id = callback.from_user.id
    username =callback.from_user.username
    gorod, polnoe, prbb, prbp, site = infovyz(unique,'vyz')
    kbr = KeyBVyz(site,unique,"Vyz")
    await callback.message.edit_text(f"{polnoe}\nГород - {gorod}\nПроходной бал бюджет - {prbb}\nПроходной бал платное - {prbp}",reply_markup=kbr)


@router.callback_query(lambda c: c.data.startswith("prohodnoy:"))
async def tsh(callback: types.CallbackQuery, state: FSMContext):
    unique = callback.data.split(":")[1]
    zaved = callback.data.split(":")[2]
    user_id = callback.from_user.id
    KeyBoard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад📌', callback_data=f'Vyz:{unique}')]
])
    await callback.message.edit_text('Средний балл ЕГЭ в вузе\n\n\nСредний балл ЕГЭ в вузе определяется для всего вуза и является официальной статистикой.\n\nСредний балл ЕГЭ вуза — это минимальный средний балл одного ЕГЭ крайнего абитуриента, поступившего в вуз. Рассчитывается он так: сумма баллов ЕГЭ по экзаменам, которые необходимы для участия в конкурсе на программы вуза, деленная на количество экзаменов, которые должен сдать абитуриент',reply_markup=KeyBoard)



@router.callback_query(F.data=='StartTest')
async def tsh(callback: CallbackQuery):
    user_id = callback.from_user.id
    newTEST(user_id)
    await callback.message.edit_text(f"Ответь на 15 вопросов, которые помогут определить подходящее тебе направления!",reply_markup=kb.test_nach)
    

@router.callback_query(lambda c: c.data.startswith("TEST:"))
async def tsh(callback: types.CallbackQuery, state: FSMContext):
    unique = callback.data.split(":")[1]
    user_id = callback.from_user.id
    username =callback.from_user.username
    nomer_voprosa, otveti = unique.split("#")
    if nomer_voprosa !=1:
        test_otvet(user_id,otveti)
    cursor.execute('SELECT text, otvet1, otvet2, otvet3 FROM bazatest WHERE Voprosnomer = ?',(nomer_voprosa,))
    
    
    if int(nomer_voprosa) !=16:
        text, otvet1, otvet2, otvet3  = cursor.fetchone()
        kbr = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='A', callback_data=f'TEST:{int(nomer_voprosa)+1}#{otvet1}')],
        [InlineKeyboardButton(text='B', callback_data=f'TEST:{int(nomer_voprosa)+1} #{otvet2}')],
        [InlineKeyboardButton(text='C', callback_data=f'TEST:{int(nomer_voprosa)+1}#{otvet3}')],
    ])
        text= text.replace('\\n', '\n')
        await callback.message.edit_text(f"{text}",reply_markup=kbr)
    else:
        result1, result2 = help_test_2(user_id)
        code1, code2 = help_sort_test(user_id)
        konec = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f'Выбрать {result1}', callback_data=f'main:{code1}')],
            [InlineKeyboardButton(text=f'Выбрать {result2}', callback_data=f'main:{code2}')],
            [InlineKeyboardButton(text='Вернутся обратно', callback_data='main:')]
    ])
        await callback.message.edit_text(f"Вы завершили тест, ваш результат \n\nПредпологаем:\n{result1} или {result2}",reply_markup=konec)
    
        
@router.callback_query(F.data=='obzor_napravleniy')
async def tsh(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    clr_fltr(user_id)
    await callback.message.edit_text("Выберите уклон направления",reply_markup=kb.vibor_obzor)

        
@router.callback_query(lambda c: c.data.startswith("Oobzor:"))
async def tsh(callback: types.CallbackQuery, state: FSMContext):
    unique = callback.data.split(":")[1]
    user_id = callback.from_user.id
    username =callback.from_user.username
    keyboard, ykl = KB(unique,"Obzor_nap","obzor_napravleniy")
    await callback.message.edit_text(f'Направления с {ykl}',reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith("Obzor_nap:"))
async def tsh(callback: types.CallbackQuery, state: FSMContext):
    unique = callback.data.split(":")[1]
    user_id = callback.from_user.id
    username =callback.from_user.username
    Napravlenie, opisanie, code = about_napr(unique)
    kbr = obzorKB(code,'UchebZaved')
    await callback.message.edit_text(f'{opisanie}',reply_markup=kbr)


@router.callback_query(F.data=='Dop')
async def tsh(callback: CallbackQuery):
    await callback.message.edit_text('▼Дополнительно▼',reply_markup=kb.Dop)



@router.callback_query(F.data=='Support')
async def tsh(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    username = callback.from_user.username
    await callback.message.delete()
    await state.clear()
    await callback.message.answer('Приветсвуем в поддержке\n\n\nМы готовы предоставить максимально эффективную помощь в подборе направления и необходимых решений. Пожалуйста, расскажите, чем мы можем вам помочь.', reply_markup=kb.mainTP)
    await callback.answer() 




@router.callback_query(F.data=='help')
async def tsh(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    username = callback.from_user.username
    await callback.message.answer("Отправьте сообщение в поддержку. Вы можете прикреплять текст, фото и файлы.")
    await state.set_state(SupportState.waiting_for_message)

@router.message(SupportState.waiting_for_message)
async def receive_support_message(message: types.Message, state: FSMContext):

    tp = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ответить', callback_data=f'otvet:{message.from_user.id}')], 
    [InlineKeyboardButton(text='Закрыть', callback_data=f'main:')]
    ])


    forward_text = f"📩 Сообщение в поддержку от @{message.from_user.username} (ID: {message.from_user.id}):"

    # Если это текстовое сообщение
    if message.text:
        await message.bot.send_message(ADMINss_ID, f"{forward_text}\n\n{message.text}",reply_markup=tp)

    # Если это фото
    elif message.photo:
        photo = message.photo[-1].file_id  # Берем лучшее качество
        caption = message.caption if message.caption else "Без подписи"
        await message.bot.send_photo(ADMINss_ID, photo, caption=f"{forward_text}\n\n{caption}",reply_markup=tp)

    # Если это документ
    elif message.document:
        document = message.document.file_id
        caption = message.caption if message.caption else "Без подписи"
        await message.bot.send_document(ADMINss_ID, document, caption=f"{forward_text}\n\n{caption}",reply_markup=tp)

    # Если это видео
    elif message.video:
        video = message.video.file_id
        caption = message.caption if message.caption else "Без подписи"
        await message.bot.send_video(ADMINss_ID, video, caption=f"{forward_text}\n\n{caption}",reply_markup=tp)

    await message.answer("Ваше сообщение отправлено в поддержку! Ожидайте ответа.",reply_markup=kb.closeTP)
    await state.clear()


@router.callback_query(lambda c: c.data.startswith("otvet:"))
async def tsh(callback: types.CallbackQuery, state: FSMContext):
    unique = callback.data.split(":")[1]
    await callback.message.answer('Введите ответ:')
    await state.set_state(SupportState.wait_answer)
    await state.update_data(user_id=unique)

@router.message(SupportState.wait_answer)
async def receive_support_message(message: types.Message, state: FSMContext):
    text = message.text 
    data = await state.get_data()
    user_id = data['user_id']
    tp = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ответить', callback_data=f'help')], 
    [InlineKeyboardButton(text='Закрыть', callback_data=f'main')]
    ])
    await message.bot.send_message(user_id, f"Ответ от поддержки:\n\n{text}",reply_markup=tp)
    await message.answer("Ваше сообщение отправлено! Ожидайте ответа.",reply_markup=kb.closeTP)
    await state.clear() 

@router.callback_query(lambda c: c.data.startswith("UchebZavedbez:"))
async def tsh(callback: types.CallbackQuery, state: FSMContext):
    unique = callback.data.split(":")[1]
    user_id = callback.from_user.id
    tp = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вузы', callback_data=f'obzor_vyzov')],
    [InlineKeyboardButton(text='Ссузы', callback_data=f'obzor_syzov')], 
    [InlineKeyboardButton(text='Закрыть', callback_data=f'main:')]
    ])
    clr_fltr(user_id)
    await callback.message.edit_text("Выберите учебное заведение:",reply_markup=tp)




@router.callback_query(lambda c: c.data.startswith("UchebZaved:"))
async def tsh(callback: types.CallbackQuery, state: FSMContext):
    unique = callback.data.split(":")[1]
    user_id = callback.from_user.id
    tp = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вузы', callback_data=f'VyzW:{unique}:1')],
    [InlineKeyboardButton(text='Ссузы', callback_data=f'SyzW:{unique}:1')], 
    [InlineKeyboardButton(text='Закрыть', callback_data=f'main:')]
    ])
    clr_fltr(user_id)
    await callback.message.edit_text("Выберите учебное заведение:",reply_markup=tp)




@router.callback_query(F.data=='obzor_syzov')
async def tsh(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username
    clr_fltr(user_id)
    await callback.message.edit_text("Выберите уклон направления",reply_markup=kb.first_napr_kol)


@router.callback_query(lambda c: c.data.startswith("SyzS:"))
async def tsh(callback: types.CallbackQuery, state: FSMContext):
    unique = callback.data.split(":")[1]
    user_id = callback.from_user.id
    username =callback.from_user.username
    keyboard, ykl = KB(unique,"SyzW","obzor_syzov")
    await callback.message.edit_text(f"Подборка колледжуй с {ykl}",reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith("SyzW:"))
async def tsh(callback: types.CallbackQuery, state: FSMContext):
    unique = callback.data.split(":")[1]
    stranic = int(callback.data.split(":")[2])
    user_id = callback.from_user.id
    username =callback.from_user.username
    kbr , name = vyzkb(user_id, unique,stranic,'Syz')
    await callback.message.edit_text(f"Подборка колледжей по профессии - {name}",reply_markup=kbr)



@router.callback_query(lambda c: c.data.startswith("Syz:"))
async def tsh(callback: types.CallbackQuery, state: FSMContext):
    unique = callback.data.split(":")[1]
    user_id = callback.from_user.id
    username =callback.from_user.username
    gorod, polnoe, prbb, prbp, site = infovyz(unique,'syz')
    kbr = KeyBVyz(site,unique,'Syz')
    await callback.message.edit_text(f"{polnoe}\nГород - {gorod}",reply_markup=kbr)


