from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from loader import bot
from utils.db_api.db_commands import add_size, show_size_user


class FSMClient(StatesGroup):
    Vg = State()
    Vpg = State()
    Vb = State()
    Vt = State()
    sizeL = State()
    check_size = State()


# Начало диалога загрузки нового пункта меню
async def start_testing(message: types.Message):
    await FSMClient.Vg.set()
    photoVg = 'AgACAgIAAxkBAAIVW2Jb3zfT-MVjX5lD9eQNN-TaLFGLAAIVvDEbOJjZSkGR-BcJnxPWAQADAgADcwADJAQ'
    await bot.send_photo(message.from_user.id, photoVg)
    await bot.send_message(message.from_user.id, 'Введите размер обхват груди')


# Выход из состояний
async def cancel_handler1(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Отмена")


# Ловим ответ и пшем в словарь
async def set_Vg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size_Vg'] = message.text
    await FSMClient.next()
    photoVog = 'AgACAgIAAxkBAAIVZ2Jb31ES3K0P4dlai8HDv28d33RdAAIWvDEbOJjZSlLZ4D4tXOWpAQADAgADcwADJAQ'
    await bot.send_photo(message.from_user.id, photoVog)
    await bot.send_message(message.from_user.id, 'Теперь введи резмер обхват под грудью')


# Ловим второй ответ
async def set_Vpg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size_Vpg'] = message.text
    await FSMClient.next()
    photoVb = 'AgACAgIAAxkBAAIVT2Jb3wmNdbWxVPZpEUb5SkMhO36pAAITvDEbOJjZSj-DvGbsUJp8AQADAgADcwADJAQ'
    await bot.send_photo(message.from_user.id, photoVb)
    await bot.send_message(message.from_user.id, 'Введи обхват беред')


# Ловим третий ответ
async def set_Vb(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size_Vb'] = message.text
    await FSMClient.next()
    photoVt = 'AgACAgIAAxkBAAIVQ2Jb3uitgeUVDxVaQx1Gwtgt-IaOAAIPvDEbOJjZSmcykz8BbPEbAQADAgADcwADJAQ'
    await bot.send_photo(message.from_user.id, photoVt)
    await bot.send_message(message.from_user.id, 'Введи обхват талии')


async def set_Vt(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size_Vt'] = message.text
    await FSMClient.next()
    await bot.send_message(message.from_user.id, 'Введите ваш размер груди')


# Четвертый ответ

async def set_sizeL(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sizeL'] = message.text
    async with state.proxy() as data:
        data['id_user'] = message.from_user.id
    await add_size(id_user=data['id_user'],
                   size_Vg=data['size_Vg'],
                   size_Vpg=data['size_Vpg'],
                   size_Vt=data['size_Vt'],
                   size_Vb=data['size_Vb'],
                   sizeL=data['sizeL']
                   )
    user_id=message.from_user.id
    siz=await show_size_user(user_id)
    await bot.send_message(message.from_user.id, f'Твой размер {siz}')
    await FSMClient.next()
    await bot.send_message(message.from_user.id, 'Все верно? пока написать Да')



async def yes_not(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        await bot.send_message(message.from_user.id, 'Размеры добавлены!')
        await state.finish()

