import json

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from filters import IsPrivate
from handlers.admin.adminPanel import adminOrder, admin_cb, state_order
from keyboards.inline.govno_kb import bonus_kb
from loader import dp, bot
from states.Mailing import MailingService

# =================================Рассылка=================================


# функция рассылки сообщений
from states.admin import admin_trak, admin_bonus
from utils.db_api.db_commands import search_order, update_tracking, search_order_id, update_state, update_fin_state, \
    update_my_balans, check_user, my_balans, \
    search_com_qua_order


@dp.message_handler(IsPrivate(), state=MailingService.text)
async def mailing_text(message: types.Message, state: FSMContext):
    # await bot.send_message(message.from_user.id, 'Рассылка начата!')
    answer = message.text
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='📷 Добавить фотографию',
                                                               callback_data='add_photo'),
                                          InlineKeyboardButton(text='📩 Отправить', callback_data='next'),
                                          InlineKeyboardButton(text='❌ Отменить', callback_data='quit')
                                      ]
                                  ])
    await state.update_data(text=answer)
    await message.answer(text=answer, reply_markup=markup)
    await MailingService.state.set()


@dp.message_handler(IsPrivate(), state=MailingService.photo, content_types=types.ContentTypes.PHOTO)
async def mailing_photo(message: types.Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id  # возвращает файл id
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='📩 Отправить', callback_data='next'),
                                          InlineKeyboardButton(text='❌ Отменить', callback_data='quit')

                                      ]
                                  ])
    await message.answer_photo(photo=photo, caption=text, reply_markup=markup)


@dp.message_handler(IsPrivate(), state=MailingService.photo)
async def no_photo(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='❌ Отменить', callback_data='quit')
                                      ]
                                  ])
    await message.answer('Пришли мне фотографию', reply_markup=markup)


# =================================Заказы=================================


@dp.callback_query_handler(text="orders")
async def show_orders(callback: types.CallbackQuery):
    await callback.message.delete()
    id_orders = await search_order_id()
    for id_order in id_orders:
        id_or = id_order[0]
        markup = await adminOrder(id_or)
        item,name,number,state,tracking,com,qua=await search_com_qua_order(id_or)
        await bot.send_message(callback.from_user.id,text=f'Заказ № {id_or}\n\n'
                                                          f'<u>Наименование</u> -  <b>{item} - {qua} шт</b> \n\n'
                                                          f'<u>Комментарий</u> {com}\n\n'
                                                          f'<u>Статус заказа</u> - {state}\n'
                                                          f'<u>Трек номер</u> - <code>{tracking}</code> \n\n'
                                                          f'Имя {name}\n'
                                                          f'Номер телефона {number}\n',parse_mode='html',reply_markup=markup)



@dp.callback_query_handler(admin_cb.filter(admin_change="admin_change"))
async def add_tracking(callback: CallbackQuery, callback_data: dict):
    id_order = int(callback_data['id_order'])
    markup = await state_order(id_order)
    item,name,number,state,tracking,com,qua=await search_com_qua_order(id_order)
    await callback.message.answer(text=f'Выберите статус заказа № {id_order}\n\n'
                                       f'Текущий статус {state}', reply_markup=markup)


@dp.callback_query_handler(admin_cb.filter(state='state1'))
async def state1(callback: CallbackQuery, callback_data: dict):
    id_order = callback_data['id_order']
    id = int(id_order)
    state_order = 'Ваш заказ на пошиве, срок пошива 14 дней. Заказ может быть готов раньше, следите за готовностью в личном кабинете'
    await update_state(id, state_order)
    await callback.answer('Обновлено')
    await callback.message.delete()


@dp.callback_query_handler(admin_cb.filter(state='state2'))
async def state1(callback: CallbackQuery, callback_data: dict):
    id_order = callback_data['id_order']
    id = int(id_order)
    state_order = 'Ваш заказ готов, ожидает отправки'
    await update_state(id, state_order)
    await callback.answer('Обновлено')
    await callback.message.delete()

@dp.callback_query_handler(admin_cb.filter(state='state3'))
async def state3(callback: CallbackQuery, callback_data: dict):
    id_order = int(callback_data['id_order'])
    item,name,number,state,tracking,com,qua=await search_com_qua_order(id_order)
    state_order = f'Ваш заказ отправлен! Трек номер {tracking}'
    await update_state(id_order, state_order)
    await callback.answer('Обновлено')
    await callback.message.delete()


@dp.callback_query_handler(admin_cb.filter(state='state4'))
async def state1(callback: CallbackQuery, callback_data: dict):
    id_order = callback_data['id_order']
    id = int(id_order)
    finish_state = True
    await update_fin_state(id, finish_state)
    await callback.answer('Заказ закрыт')
    await callback.message.delete()


@dp.callback_query_handler(admin_cb.filter(tracking='tracking'))
async def add_tracking(callback: CallbackQuery, callback_data: dict, state: FSMContext):
    id_order = callback_data['id_order']
    id = int(id_order)
    await callback.message.delete()
    #markup=await state_order(id)
    await callback.bot.send_message(chat_id=callback.from_user.id, text=f'Введите трек номер для заказа № {id}')
    #await callback.bot.send_message(chat_id=callback.from_user.id,text='Выберите статус закза ',reply_markup=markup)
    async with state.proxy() as data:
        data['order_id'] = id
    await admin_trak.one.set()


@dp.message_handler(state=admin_trak.one)
async def add_track(message: types.Message, state: FSMContext):
    id_user = message.from_user.id
    tracking = message.text
    async with state.proxy() as data:
        id_order = data['order_id']
    await update_tracking(id_order, tracking)
    order = await search_order(id_order)
    await bot.send_message(chat_id=id_user, text=f"Для заказа № {order} обновлен трек номер {tracking}")
    await state.finish()


@dp.callback_query_handler(text='bonus')
async def add_bonus(callback: CallbackQuery):
    await admin_bonus.one.set()
    await callback.bot.send_message(callback.from_user.id, 'Введите ID пользователя ')


@dp.message_handler(state=admin_bonus.one)
async def add_bonus(message: types.Message, state: FSMContext):
    await admin_bonus.two.set()
    await message.bot.send_message(message.from_user.id, 'Введите бонусные рубли ')
    id_user = message.text
    async with state.proxy() as data:
        data['id_user'] = id_user


@dp.message_handler(state=admin_bonus.two)
async def add_bonus(message: types.Message, state: FSMContext):
    markup = await bonus_kb()
    await admin_bonus.three.set()
    balans = message.text
    async with state.proxy() as data:
        data['balans'] = balans

    async with state.proxy() as data:
        id_user = data['id_user']

    await message.bot.send_message(message.from_user.id, f'Начисляем ( {balans} ) бонусов \nПользователю с ID {id_user} ?',
                                   reply_markup=markup)


@dp.callback_query_handler(text='bonus_no', state=admin_bonus.three)
async def add_bonus(callback: CallbackQuery, state: FSMContext):
    id_user = callback.from_user.id
    await callback.bot.send_message(id_user, 'Отменили')
    await state.finish()


@dp.callback_query_handler(text='bonus_yes', state=admin_bonus.three)
async def add_bonus(callback: CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            balans = int(data['balans'])
            id_user = int(data['id_user'])

        check=await check_user(id_user)
        if check:
            balans_old=int(await my_balans(id_user))
            balans=balans_old+balans
            if balans<0:
                balans=0
            await update_my_balans(id_user, balans)
            await callback.bot.send_message(callback.from_user.id, f'Обновили!')
            #await callback.bot.send_message(id_user,'Вам начислены бонусные рубли!')
        else:
            await callback.bot.send_message(callback.from_user.id, f'Пользователь не найден. Проверьте правильность введенного ID.\n'
                                                                   f'Возможно, пользователь не пользовался ботом')
    except ValueError:
        await callback.bot.send_message(callback.from_user.id,'Что то пошло не так, попробуйте снова')
    await state.finish()
