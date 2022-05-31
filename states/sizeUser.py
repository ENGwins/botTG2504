from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text

from keyboards.keyvoard import kb_yes_no, kb_size, mainMenu
from loader import bot, dp
from utils.db_api.db_commands import add_size, show_size_user, delete_size, check_z


class FSMClient(StatesGroup):
    V = State()
    Vg = State()
    Vpg = State()
    Vt = State()
    Vb = State()
    sizeL = State()
    email = State()
    check_size = State()


@dp.message_handler(text='Ввести заново', state='*')
@dp.message_handler(text='Изменение размеров', state='*')
async def start_testing(message: types.Message):
    user_id = message.from_user.id
    check = await check_z(user_id)
    if check:
        await delete_size(user_id)
    await bot.send_message(message.from_user.id, 'Следуйте подсказам', reply_markup=kb_size)
    await FSMClient.V.set()


# Выход из состояний
@dp.message_handler(commands="Главное меню", state="*")
@dp.message_handler(Text(equals='Главное меню', ignore_case=True), state="*")
async def cancel_handler1(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, "Мы в главном меню", reply_markup=mainMenu)


# Начало диалога загрузки нового пункта меню
@dp.message_handler(state=FSMClient.V)
async def set_V(message: types.Message, state: FSMContext):
    #    await FSMClient.Vg.set()
    await FSMClient.next()
    photoVg = 'AgACAgIAAxkBAAIVW2Jb3zfT-MVjX5lD9eQNN-TaLFGLAAIVvDEbOJjZSkGR-BcJnxPWAQADAgADcwADJAQ'
    await bot.send_photo(message.from_user.id, photoVg)
    await bot.send_message(message.from_user.id, 'Напишите Ваш обхват груди')


# Ловим ответ и пшем в словарь
@dp.message_handler(state=FSMClient.Vg)
async def set_Vg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size_Vg'] = message.text
    await FSMClient.next()
    photoVog = 'AgACAgIAAxkBAAIVZ2Jb31ES3K0P4dlai8HDv28d33RdAAIWvDEbOJjZSlLZ4D4tXOWpAQADAgADcwADJAQ'
    await bot.send_photo(message.from_user.id, photoVog)
    await bot.send_message(message.from_user.id, 'Теперь напишите Ваш обхват под грудью')


# Ловим второй ответ
@dp.message_handler(state=FSMClient.Vpg)
async def set_Vpg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size_Vpg'] = message.text
    await FSMClient.next()
    photoVb = 'AgACAgIAAxkBAAIVQ2Jb3uitgeUVDxVaQx1Gwtgt-IaOAAIPvDEbOJjZSmcykz8BbPEbAQADAgADcwADJAQ'
    await bot.send_photo(message.from_user.id, photoVb)
    await bot.send_message(message.from_user.id, 'Напишите Ваш обхват в талии')


@dp.message_handler(state=FSMClient.Vt)
async def set_Vt(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size_Vt'] = message.text
    photoVt = 'AgACAgIAAxkBAAIVT2Jb3wmNdbWxVPZpEUb5SkMhO36pAAITvDEbOJjZSj-DvGbsUJp8AQADAgADcwADJAQ'
    await bot.send_photo(message.from_user.id, photoVt)
    await FSMClient.next()
    await bot.send_message(message.from_user.id, 'Напишите Ваш обхват в бедрах')


# Ловим третий ответ
@dp.message_handler(state=FSMClient.Vb)
async def set_Vb(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size_Vb'] = message.text
    await FSMClient.next()
    await bot.send_message(message.from_user.id, 'Напишите Ваш размер лифа')


@dp.message_handler(state=FSMClient.sizeL)
async def set_sizeL(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sizeL'] = message.text
    async with state.proxy() as data:
        data['id_user'] = message.from_user.id

    await bot.send_message(message.from_user.id, 'Контактый email')
    await FSMClient.next()


@dp.message_handler(state=FSMClient.email)
async def set_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text

    await add_size(id_user=data['id_user'],
                   size_Vg=data['size_Vg'],
                   size_Vpg=data['size_Vpg'],
                   size_Vt=data['size_Vt'],
                   size_Vb=data['size_Vb'],
                   sizeL=data['sizeL'],
                   email=data['email']
                   )
    user_id = message.from_user.id
    siz = await show_size_user(user_id)
    await bot.send_message(message.from_user.id, f'Мои данные {siz}')
    await bot.send_message(message.from_user.id, 'Все верно?', reply_markup=kb_yes_no)

    await FSMClient.next()


# Четвертый ответ

@dp.message_handler(state=FSMClient.check_size)
async def yes_not(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        await bot.send_message(message.from_user.id, 'Информация добавлена!', reply_markup=mainMenu)
        await state.finish()
    elif message.text == 'Ввести заново':
        await bot.send_message(message.from_user.id, 'Удаляем запись', reply_markup=kb_size)
        user_id = message.from_user.id
        await delete_size(user_id)
        await FSMClient.first()
