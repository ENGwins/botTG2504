from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from keyboards.inline.user import user_cb, set_size, userPanel, yes_no, add_comment_kb
from keyboards.keyvoard import kb_size, mainMenu
from loader import dp, bot
from states.sizeUser import FSMClient, FSMpersonal
from utils.db_api.db_commands import check_z, show_size_user, delete_size, add_size, show_my_orders, add_my_comment, \
    search_order


@dp.callback_query_handler(user_cb.filter(my_size='my_size_new'), state='*')
async def start_testing(message: types.Message):
    user_id = message.from_user.id
    check = await check_z(user_id)
    if check:
        await delete_size(user_id)
    await bot.send_message(message.from_user.id, 'Следуйте подсказам')
    await set_V(message)
    # await FSMClient.Vg.set()


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
# @dp.message_handler(state=FSMClient.V)
async def set_V(message: types.Message):
    #    await FSMClient.Vg.set()
    # await FSMClient.next()
    await FSMClient.Vg.set()
    photoVg = 'AgACAgIAAxkBAAIVW2Jb3zfT-MVjX5lD9eQNN-TaLFGLAAIVvDEbOJjZSkGR-BcJnxPWAQADAgADcwADJAQ'
    await bot.send_photo(message.from_user.id, photoVg, caption='Напишите Ваш обхват груди')


# Ловим ответ и пшем в словарь
@dp.message_handler(state=FSMClient.Vg)
async def set_Vg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size_Vg'] = message.text
    await FSMClient.next()
    photoVog = 'AgACAgIAAxkBAAIVZ2Jb31ES3K0P4dlai8HDv28d33RdAAIWvDEbOJjZSlLZ4D4tXOWpAQADAgADcwADJAQ'
    await bot.send_photo(message.from_user.id, photoVog, caption='Теперь напишите Ваш обхват под грудью')


# Ловим второй ответ
@dp.message_handler(state=FSMClient.Vpg)
async def set_Vpg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size_Vpg'] = message.text
    await FSMClient.next()
    photoVb = 'AgACAgIAAxkBAAIVQ2Jb3uitgeUVDxVaQx1Gwtgt-IaOAAIPvDEbOJjZSmcykz8BbPEbAQADAgADcwADJAQ'
    await bot.send_photo(message.from_user.id, photoVb, caption='Напишите Ваш обхват в талии')


@dp.message_handler(state=FSMClient.Vt)
async def set_Vt(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size_Vt'] = message.text
    photoVt = 'AgACAgIAAxkBAAIVT2Jb3wmNdbWxVPZpEUb5SkMhO36pAAITvDEbOJjZSj-DvGbsUJp8AQADAgADcwADJAQ'
    await bot.send_photo(message.from_user.id, photoVt, caption='Напишите Ваш обхват в бедрах')
    await FSMClient.next()


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
    markup = await yes_no()
    await bot.send_message(message.from_user.id, f'Вы ввели:'
                                                 f'\n {siz}', reply_markup=markup)

    await state.finish()


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


# =============================================    Главное меню =========================================

@dp.callback_query_handler(user_cb.filter(my_size='my_size'))
async def my_size(callback: CallbackQuery, callback_data: dict):
    await callback.message.delete()
    user_id = int(callback_data['id_user'])
    await callback.answer()
    check = await check_z(user_id)
    if check:
        siz = await show_size_user(user_id)
        markup = await set_size()
        await callback.bot.send_message(callback.from_user.id, f'Мои данные {siz}', reply_markup=markup)
    else:
        markup = await set_size()
        await callback.bot.send_message(chat_id=callback.from_user.id,
                                        text='Для оформления заказа необходимо указать информацию', reply_markup=markup)


@dp.callback_query_handler(user_cb.filter(menu=['back', 'ok']))
async def back(callback: CallbackQuery):
    await callback.message.delete()
    await userPanel(callback)


@dp.callback_query_handler(user_cb.filter(my_orders='my_orders'))
async def my_orders(callback: CallbackQuery, callback_data: dict,state:FSMContext):
    user_id = int(callback_data['id_user'])
    orders = await show_my_orders(user_id)
    await callback.answer('Загружаем данные')
    for order in orders:
        id_order=order.id
        markup = await add_comment_kb(id_order)
        await callback.bot.send_message(chat_id=user_id, text=f'Ваш заказ: \n {order}', reply_markup=markup)


@dp.callback_query_handler(user_cb.filter(comment='comment'))
async def add_comment(callback: CallbackQuery, callback_data: dict, state: FSMContext):
    id_order = callback_data['id_order']
    id = int(id_order)
    id_user = callback.from_user.id
    await callback.bot.send_message(chat_id=id_user, text=f'Введите комментарий для заказа № {id}')
    async with state.proxy() as data:
        data['order_id'] = id
    await FSMpersonal.one.set()


@dp.message_handler(state=FSMpersonal.one)
async def add_comment(message: types.Message, state: FSMContext):
    id_user = message.from_user.id
    comment = message.text
    async with state.proxy() as data:
        id_order = data['order_id']
    await add_my_comment(id_order=id_order, comment=comment)
    await bot.send_message(chat_id=id_user, text=f"Комментарий успешно добавлен")
    await state.finish()
