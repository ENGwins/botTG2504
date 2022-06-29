import logging
import json
import types


from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes
from aiogram.utils.exceptions import BotBlocked
from loguru import logger
from asyncio import sleep
from typing import Union

import emoji
from datetime import datetime
from aiogram import types
from data.config import admins, SUPER_ADMIN, ID_PHOTO_MENU
from data.message import dict_for_message_shipping
from filters import IsPrivate
from handlers.admin.referral import check_referral_id
from keyboards.inline.govno_kb import categories_keyboard, items_keyboard, item_keyboard, \
    menu_cd, pay_kb, subcategory_keyboard, basket_kb,my_basket_kb
from keyboards.inline.user import userPanel
from keyboards.keyvoard import mainMenu
from loader import dp, bot
from states.Mailing import MailingService
from states.pay import FSMpay

from utils.db_api.database import Item

from utils.db_api.db_commands import get_item, show_size_user, check_z, get_photo, get_name_item, get_price_item, \
    get_decr_item, check_user, user_all_check, new_order, update_my_balans, my_balans, new_user, check_referral_order, \
    total_amounts, total_amount_basket, chek_basket, add_item_basket, update_quantity, count_item_basket, show_basket, \
    count_basket, delete_basket, chek_photos, check_sale

user_num_photo = {}


@dp.callback_query_handler(text='mailing', state=None)
async def Mailing(call: types.CallbackQuery):  # один из пунктов админки, выдает клаву с выбором операции=
    await call.message.answer(text='Введите текст рассылки')
    await MailingService.text.set()


@dp.callback_query_handler(text='add_photo', state=MailingService.state)
async def add_photo(call: types.CallbackQuery):
    await call.message.answer('Пришлите фото')
    await MailingService.photo.set()


@dp.callback_query_handler(text='next', state=MailingService.photo)
async def startMailing(call: types.CallbackQuery, state: FSMContext):
    users = await user_all_check()
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    await state.finish()
    for user in users:
        try:
            await call.bot.send_photo(chat_id=user.user_id, photo=photo, caption=text)
            await sleep(0.33)
        except Exception:
            pass
    await call.message.answer('Рассылка выполнена')


@dp.callback_query_handler(text='next', state=MailingService.state)
async def startMailing(call: types.CallbackQuery, state: FSMContext):
    users = await user_all_check()
    data = await state.get_data()
    text = data.get('text')
    await state.finish()
    for user in users:
        try:
            await call.bot.send_message(chat_id=user.user_id, text=text)
            await sleep(0.33)
        except Exception:
            pass
    await call.message.answer('Рассылка выполнена')


@dp.callback_query_handler(text="quit", state=[MailingService.text, MailingService.photo, MailingService.state])
async def quit_m(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer('Рассылка отменена')


user_data = {}

@dp.callback_query_handler(menu_cd.filter(id=['page_incr', 'page_decr', 'page_']))
async def page(callback: types.CallbackQuery, callback_data: dict):
    category = callback_data.get('category')
    subcategory = callback_data.get('subcategory')
    global id_bas, item_id_bas, page, count
    callback_data_page = callback_data['id']
    page_tek = user_data.get(callback.from_user.id, -1)
    user_id = callback.from_user.id
    total_amount = await total_amount_basket(user_id)

    if int(total_amount) == 0:
        await callback.answer('В корзине ничего нет', show_alert=True)
    else:

        if callback_data_page == 'page_incr':
            counts = await count_basket(user_id)
            count = len(counts)
            user_data[callback.from_user.id] = int(page_tek) + 1
            if user_data[callback.from_user.id] > count - 1:
                user_data[callback.from_user.id] = count - 1
                await show_basket(user_id)
                await callback.answer()
            else:
                page = page_tek + 1
                id = await show_basket(user_id)
                id_bas = id[0][page][0]
                item_id_bas = id[1][page][0]
                await callback.answer()

        elif callback_data_page == 'page_decr':
            user_data[callback.from_user.id] = int(page_tek) - 1
            if user_data[callback.from_user.id] < 0:
                user_data[callback.from_user.id] = 0
                await callback.answer()
            else:
                page = page_tek - 1
                id = await show_basket(user_id)
                id_bas = id[0][page][0]
                item_id_bas = id[1][page][0]

                await callback.answer()

        else:
            page_tek = 0
            page = 0
            counts = await count_basket(user_id)
            count = len(counts)
            user_data[callback.from_user.id] = int(page_tek)
            id = await show_basket(user_id)
            id_bas = id[0][page][0]
            item_id_bas = id[1][page][0]
            await callback.answer()

        photo_id = await get_photo(item_id_bas)
        name = await get_name_item(item_id_bas)
        decr = await get_decr_item(item_id_bas)
        price = await get_price_item(item_id_bas)
        sale=await check_sale(item_id_bas)
        count_item_bask = await count_item_basket(user_id, item_id_bas)
        # text = await show_basket(user_id, page)

        item_id = item_id_bas
        markup = await my_basket_kb(total_amount=total_amount, item_id=item_id, category=category,
                                    subcategory=subcategory, page=page, count_page=count)
        await bot.edit_message_media(media=types.InputMediaPhoto(photo_id), chat_id=callback.message.chat.id,
                                     message_id=callback.message.message_id)
        await bot.edit_message_caption(
            chat_id=callback.message.chat.id, message_id=callback.message.message_id,
            caption=f"<u>Наименование:</u> \n<b>{name}</b>\n"
                    f"\n"
                    f"<u>Описание:</u>\n"
                    f" {decr}\n"
                    f"\n"
                    f"<u>Цена:</u>\n <b>{price-sale} Руб</b>\n\n"
                    f"Количество в корзине {count_item_bask}\n\n"
                    f"Страница {page + 1} из {count}", parse_mode="html", reply_markup=markup
        )


# await bot.send_message(user_id, text)


@dp.callback_query_handler(menu_cd.filter(buy='buy'))  # при нажатии на кнопку в корзину
async def basket(call: Union[types.Message, types.CallbackQuery], callback_data: dict):
    category = callback_data.get('category')
    subcategory = callback_data.get('subcategory')
    id_user = call.from_user.id
    item_id = int(callback_data['item_id'])
    amount = await get_price_item(item_id)
    chek=await chek_basket(id_user,item_id)
    if chek==True:
        await update_quantity(id_user, item_id, quantity=1)
    else:
        await add_item_basket(user_id=id_user, item_id=item_id, quantity=1, amount=amount)
    await call.answer('Добавлено в корзину')
    total_amount = await total_amount_basket(id_user)  # запрос в БД общую сумму в корзине
    count_item = await count_item_basket(id_user, item_id)
    markup = await basket_kb(total_amount=total_amount, item_id=item_id,
                             category=category, subcategory=subcategory, count_item=count_item)

    await call.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(menu_cd.filter(quantity=["quantity_incr", 'quantity_decr']))
async def callbacks_num(callback: types.CallbackQuery, callback_data: dict):

    item_id = int(callback_data['item_id'])
    id_user = callback.from_user.id
    category = callback_data.get('category')
    subcategory = callback_data.get('subcategory')
    max_pages = len(await chek_photos(item_id))
    callback_data_quantity = callback_data['quantity']

    if callback_data_quantity == 'quantity_incr':
        await update_quantity(id_user, item_id, 1)
        await callback.answer('Добавили')
        total_amount = await total_amount_basket(id_user)  # запрос в БД общую сумму в корзине
        count_item = await count_item_basket(id_user, item_id)
        cnt = int(count_item)
        markup = await basket_kb(total_amount=total_amount, item_id=item_id,
                                 category=category, subcategory=subcategory, count_item=cnt)
        await callback.message.delete_reply_markup()
        await callback.message.edit_reply_markup(reply_markup=markup)


    elif callback_data_quantity == 'quantity_decr':
        try:
            await update_quantity(id_user, item_id, -1)
            check = await chek_basket(id_user, item_id)
            total_amount = await total_amount_basket(id_user)

            if not check:
                markup = await item_keyboard(id_item=item_id, category=category, subcategory=subcategory,
                                             total_amount=total_amount, max_pages=max_pages, key='book', page=0)

                await callback.message.edit_reply_markup(reply_markup=markup)
                # pass   # что то делаем когда  удалили все элементы из корзины
            else:
                total_amount = await total_amount_basket(id_user)  # запрос в БД общую сумму в корзине
                count_item = await count_item_basket(id_user, item_id)
                cnt = int(count_item)
                markup = await basket_kb(total_amount=total_amount, item_id=item_id,
                                         category=category, subcategory=subcategory, count_item=cnt)
                await callback.message.delete_reply_markup()
                await callback.message.edit_reply_markup(reply_markup=markup)
        except:
            pass
        await callback.answer('Убрали')


# @dp.callback_query_handler(menu_cd.filter(buy='newbuy'))  # при нажатии на кнопку Оформить
async def send_admin(call: Union[types.Message, types.CallbackQuery], callback_data: dict):
    id_user = call.from_user.id
    check = await check_z(id_user)
    if check:
        item_id = int(callback_data['item_id'])
        name_item = await Item.select('name').where(Item.id == item_id).gino.scalar()
        siz = await show_size_user(id_user)  # запрос размеров по id_user
        try:
            markup = await pay_kb()
            await call.bot.send_message(id_user,
                                        f'Вы хотите оформить заказ: \n{name_item} \n'
                                        f' \n'
                                        f'Ваши размеры для пошива: {siz} \n', reply_markup=markup)
            await call.answer()
        except Exception as err:
            logging.exception(err)
    else:
        await call.answer('Для оформления заказа, перейдите в личный кабинет и заполните мерки', show_alert=True)


@dp.callback_query_handler(menu_cd.filter(buy='newbuy'))
async def order(callback: Union[types.Message, types.CallbackQuery]):
    id_user = callback.from_user.id
    check = await check_z(id_user)

    if check:
        siz = await show_size_user(id_user)
        markup = await pay_kb()
        total_amount = await total_amount_basket(id_user)
        await callback.bot.send_message(id_user,
                                        f'Вы хотите оформить заказ на сумму: {total_amount} Руб\n \n'
                                        f' \n'
                                        f'Проверьте Ваши размеры для пошива: {siz} \n', reply_markup=markup)
    else:
        await callback.answer('Для оформления заказа, перейдите в личный кабинет и заполните мерки', show_alert=True)


@dp.callback_query_handler(menu_cd.filter(buy='close'))
async def list_categories(message: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await categories_keyboard()
    if isinstance(message, types.Message):
        await bot.send_photo(chat_id=message.from_user.id, photo=ID_PHOTO_MENU, caption='Выберите категорию',
                             reply_markup=markup)


    elif isinstance(message, types.CallbackQuery):
        await message.message.delete()
        call = message
        await bot.answer_callback_query(message.id)
        await bot.send_photo(chat_id=call.from_user.id, photo=ID_PHOTO_MENU, caption='Выберите категорию',
                             reply_markup=markup)


async def anti_flood(*args, **kwargs):
    m = args[0]
    await m.answer("Слишком часто отправляете сообщение!")


@dp.message_handler(IsPrivate(), commands=['start'], state="*")
@dp.throttled(anti_flood, rate=5)
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, 'Вы в главном меню! ', reply_markup=mainMenu)
    id_user = message.from_user.id
    firstname_user = message.from_user.first_name
    lastname_user = message.from_user.last_name

    check = await check_user(id_user)
    if check:
        pass
    else:
        try:
            await bot.send_message(SUPER_ADMIN, 'Новый пользователь! \n'
                                                f'ID {id_user}\n'
                                                f'{firstname_user}')
            new_ref = '0'
            await new_user(user_id=id_user, user_first_name=firstname_user, user_last_name=lastname_user,
                           referral=new_ref)
            start_command = message.text
            referral_id = str(start_command[7:])
            if referral_id!='':
                new_ref =str(await check_referral_id(referral_id, id_user))
                old_balans = int(await my_balans(int(new_ref)))
                new_balans = 50 + old_balans
                await update_my_balans(id_user=int(new_ref), new_balans=new_balans)

                await bot.send_message(referral_id,
                                       f"По вышей ссылке приглашен пользователь {message.from_user.first_name}\n"
                                       f"Вам начислено 50 бонусов!")





        except Exception as err:
            logging.exception(err)


@dp.callback_query_handler(text='pass')
async def pas(callback: types.CallbackQuery):
    await callback.answer()


async def list_subcategories(callback: types.CallbackQuery, category, **kwargs):
    markup = await subcategory_keyboard(category)
    await bot.answer_callback_query(callback.id)
    await callback.message.edit_reply_markup(markup)


async def list_items(callback: types.CallbackQuery, category, subcategory, **kwargs):
    markup = await items_keyboard(category=category, subcategory=subcategory)

    await bot.answer_callback_query(callback.id)
    await bot.edit_message_media(media=types.InputMediaPhoto(ID_PHOTO_MENU), chat_id=callback.message.chat.id,
                                 message_id=callback.message.message_id, reply_markup=markup)


@dp.callback_query_handler(menu_cd.filter(buy='book'))
async def show_item_2(callback: types.CallbackQuery, callback_data: dict):
    category = callback_data.get('category')
    subcategory = callback_data.get('subcategory')

    item_id = int(callback_data['item_id'])
    user_id = callback.from_user.id
    total_amount = await total_amount_basket(user_id)
    count_item = await count_item_basket(user_id, item_id)
    current_page = int(callback_data.get('page'))
    id_all_photo = await chek_photos(item_id)
    max_pages = len(await chek_photos(item_id))
    photo_id = id_all_photo[int(current_page)]
    name = await get_name_item(item_id)
    price = await get_price_item(item_id)
    decr = await get_decr_item(item_id)
    await callback.answer()
    sale=await check_sale(item_id)
    new_price = price - sale
    if sale:
        caption = f"<u>Наименование:</u> \n<b>{name}</b>\n\n" \
                   f"<u>Описание:</u>\n" \
                   f"{decr}\n\n" \
                   f"Акция! 😍\n\n" \
                   f"<u>Цена:</u>\n <del><b>{price} Руб</b></del>\n" \
                   f"<b> {new_price} Руб</b>"
    else:

        caption = f"<u>Наименование:</u> \n<b>{name}</b>\n\n" \
                   f"<u>Описание:</u>\n" \
                   f"{decr}\n\n" \
                   f"<u>Цена:</u>\n <b>{price} Руб</b>\n"


    markup = await item_keyboard(category, subcategory, item_id, total_amount, max_pages=max_pages, key='book',
                                 page=current_page)

    await bot.edit_message_media(media=types.InputMediaPhoto(photo_id), chat_id=callback.message.chat.id,
                                 message_id=callback.message.message_id, reply_markup=markup)

    await bot.edit_message_caption(
        chat_id=callback.message.chat.id, message_id=callback.message.message_id,
        caption=caption,reply_markup=markup
    )


async def show_item(callback: types.CallbackQuery, category, subcategory, item_id):
    # markup=get_page_keyboard(max_pages=max_pages,page=current_page)
    # вызыв клавиатуры
    max_pages = len(await chek_photos(item_id))
    current_page = 0

    user_id = callback.from_user.id
    check = await chek_basket(user_id, item_id)
    total_amount = await total_amount_basket(user_id)
    # id_ph_all = await chek_photos(item_id)
    # count_photo_item = len(id_ph_all)
    # media=[]

    if not check:
        markup = await item_keyboard(category, subcategory, item_id, total_amount, max_pages=max_pages, key='book',
                                     page=current_page)

    else:
        # запрос в БД общую сумму в корзине
        count_item = await count_item_basket(user_id, item_id)
        markup = await basket_kb(total_amount=total_amount, item_id=item_id, category=category, subcategory=subcategory,
                                 count_item=count_item)
        await callback.message.edit_reply_markup(reply_markup=markup)

    photo_id = await get_photo(item_id)
    name = await get_name_item(item_id)
    price = await get_price_item(item_id)
    decr = await get_decr_item(item_id)
    await bot.answer_callback_query(callback.id)
    sale=await check_sale(item_id)
    new_price = price - sale
    if sale:
        caption = f"<u>Наименование:</u> \n<b>{name}</b>\n\n" \
                   f"<u>Описание:</u>\n" \
                   f"{decr}\n\n" \
                   f"Акция! 😍\n\n" \
                   f"<u>Цена:</u>\n <del><b>{price} Руб</b></del>\n" \
                   f"<b> {new_price} Руб</b>"
    else:

        caption = f"<u>Наименование:</u> \n<b>{name}</b>\n\n" \
                   f"<u>Описание:</u>\n" \
                   f"{decr}\n\n" \
                   f"<u>Цена:</u>\n <b>{price} Руб</b>\n"
    # for id in id_ph_all:
    #    media.append(InputMediaPhoto(id,f'{name}'))

    await bot.edit_message_media(media=types.InputMediaPhoto(photo_id), chat_id=callback.message.chat.id,
                                 message_id=callback.message.message_id, reply_markup=markup)
    await bot.edit_message_caption(
        chat_id=callback.message.chat.id, message_id=callback.message.message_id,
        caption=caption, parse_mode="html", reply_markup=markup
    )




# проверка ID фото
@dp.message_handler(IsPrivate(), content_types=['photo'])
async def load_photo(message: types.Message):
    id_ph = message.photo[0].file_id
    await bot.send_message(message.from_user.id, id_ph)


# Оплата прошла
@dp.message_handler(IsPrivate(), content_types=ContentTypes.SUCCESSFUL_PAYMENT, state=FSMpay.state2)
@dp.message_handler(IsPrivate(), content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message, state: FSMContext):
    global id, q
    async with state.proxy() as data:
        if not data:
            com = ''
        else:
            com = data['comment']

    await bot.send_message(message.from_user.id, 'Товар оплачен, вы можете отследить статус заказа в личном кабинете')
    json_str = str(message.successful_payment.order_info)
    info_order = json.loads(json_str)
    name = info_order['name']
    number = info_order['phone_number']
    email = info_order['email']
    shipping_address = info_order['shipping_address']
    country = shipping_address['country_code']
    states = shipping_address['state']
    city = shipping_address['city']
    street_line1 = shipping_address['street_line1']
    street_line2 = shipping_address['street_line2']
    post_code = shipping_address['post_code']
    shipping = message.successful_payment.shipping_option_id
    shipping_name = dict_for_message_shipping.get(shipping)
    total_amount = int(message.successful_payment.total_amount) / 100
    id_user_order = message.from_user.id
    newdat = datetime.now()
    newdate = str(newdat).split('.')[0]
    payload = message.successful_payment.invoice_payload
    pll = payload[1:-1]
    plll = pll.split(', ')

    pl = []
    dict_pl = []
    for i in plll:
        pl.append(i)
    for n in pl:
        qua = n.split(':')
        qdd = qua[-1][1:-1]
        q = qdd[1:]
        id = qua[0]
        tp = (id, q)
        dict_pl.append(tp)

    new_balans = dict_pl[-1][-1]
    id_us = dict_pl[-1][-2]  # можно сделать проверу id
    await update_my_balans(id_user_order, int(new_balans))  # обновить баланс

    dict = dict_pl[:-1]
    siz = await show_size_user(id_user_order)
    for n in dict:
        item_id = int(n[0])
        quantity = int(n[1])
        name_item = await get_item(item_id)
        await new_order(name=name, number=number, name_item=name_item, buyer=id_user_order, amount=total_amount,
                        quantity=quantity, shipping_adress=json_str,
                        successful=True, purchase_time=newdate, item_id=item_id,
                        state='Заказ оплачен и оформлен, ожидается подтверждение менеджером', comment=com)
        for admin in admins:
            await bot.send_message(admin,
                                   f'Новый заказ! \n {name_item}\n'
                                   f'Количество: {quantity}\n'
                                   f'----------------------------------------\n'
                                   f' Имя: {name}\n Номер телефона: {number}\n email: {email}\n'
                                   f'----------------------------------------\n'
                                   f'-----Адрес доставки-----\n Доставка: {shipping_name}\n Страна: {country}\n Область: {states}\n Город: {city}\n Улица 1: {street_line1}\n Улица 2: {street_line2}\n Индекс: {post_code}\n '
                                   f'----------------------------------------\n'
                                   f'-----Размеры:-----\n'
                                   f'{siz}\n\nКомментарий: {com}')

    my_total = await total_amounts(id_user_order)
    await delete_basket(id_user_order)
    try:
        check_ref = await check_referral_order(id_user_order)
        check_ref = int(check_ref)
        ref_user_balans = await my_balans(check_ref)
        new_balans = ref_user_balans + 150
        if check_ref != 0 and my_total == 0:
            await update_my_balans(check_ref, new_balans)  # обновить баланс
            await bot.send_message(check_ref, 'Ваш друг совершил первый заказ.\nВам начислено 150 бонусов!')
    except:
        pass

    await state.finish()


@dp.message_handler(IsPrivate(), commands=['help'], state="*")
@dp.throttled(anti_flood, rate=5)
async def help(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Связь с администратором @liza_liioviio\n\n'
                                                              'Если возникли проблемы с ботом, контакт разработчика @rakeevS')


@dp.message_handler(IsPrivate(), content_types=['text'], state=None)
@dp.throttled(anti_flood, rate=1)
async def bot_message(message: types.Message, state: FSMContext):
    if message.text == (emoji.emojize(':scroll:') + 'Каталог'):
        await state.finish()
        await list_categories(message)

    elif message.text == 'Назад':
        await bot.send_message(message.from_user.id, "Мы в главном меню", reply_markup=mainMenu)

    elif message.text == (emoji.emojize(':woman_frowning:') + 'Личный кабинет'):

        await userPanel(message)

    elif message.text == (emoji.emojize(':rocket:') + 'Доставка'):
        await bot.send_message(message.from_user.id, 'Мы доставляем заказы по всему миру🙌🏻\n'
                                                     'По России:\n'
                                                     'Почта России 300₽\n '
                                                     'Сдэк 300₽\n'
                                                     '\n '
                                                     'В Беларусь:Почта России 500₽\n'
                                                     '(14 дней доставка)\n '
                                                     'СДЭК 500₽\n '
                                                     '(4 дня доставка)\n'
                                                     '\n'
                                                     'В другие страны стоимость доставки рассчитывается индивидуально\n '
                               , reply_markup=mainMenu)
    elif message.text == '❓ Как сделать заказ':
        await bot.send_message(message.from_user.id, 'Оформить заказ Вы можете в боте или в любой соц.сети\n'
                                                     '\n'
                                                     'Как оформить заказ в боте:\n'
                                                     ' 1. Ввести личные данные в виде мерок\n '
                                                     '2. При доставке СДЭК необходимо указать адрес пункта выдачи в '
                                                     'поле "Адрес 2" либо в комментарии платежа\n '
                                                     '3. Статус заказа отслеживается в личном кабинете\n'
                                                     '\n'
                                                     'Также заказ можно оформить, написав:\n'
                                                     'В «сообщения сообщества» в vk\n '
                                                     'https://vk.com/liioviio\n '
                                                     '\n '
                                                     'В Direct в Instagram \n '
                                                     'https://instagram.com/liioviio?utm_medium=copy_link',
                               reply_markup=mainMenu)

    elif message.text == 'О нас':
        await bot.send_message(message.from_user.id, 'Привет, команда LIIOVIIO на связи! \n'
                                                     '\n'
                                                     'Давай познакомимся. Мы - российский бренд, который на протяжении 2х лет дарит девушкам комфорт и красоту🙌🏻\n '
                                                     '\n'
                                                     'Мы создаём красивое нижнее белье в котором удобно весь день! Используем только мягкие материалы высокого качества. Отшиваем заказы для каждой из вас индивидуально по Вашим меркам🤍',
                               reply_markup=mainMenu)
    elif message.text == '₽ Бонусы':
        await bot.send_message(message.from_user.id, 'Для получения бонусов необходимо:\n'
                                                     ' 1. Приведите друга в бота - 50 бонусов\n\n '
                                                     '2. Ваш друг совершил заказ? Ещё 150 бонусов Ваши\n\n '
                                                     '3. Отметь нас в stories/посте в Instagram и мы начислим 100 бонусов')
    else:
        await message.delete()


@dp.errors_handler(exception=BotBlocked)
async def errors_msg(update: types.Update, exception: BotBlocked):
    logger.exception(f'Bot blocked by user {update.message.from_user.id}')
    return True



@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict):
    try:
        currrent_level = callback_data.get('level')
        category = callback_data.get('category')
        subcategory = callback_data.get('subcategory')
        item_id = int(callback_data.get('item_id'))
        levels = {
            "0": list_categories,
            "1": list_subcategories,
            "2": list_items,
            "3": show_item
        }
        currrent_level_function = levels[currrent_level]

        await currrent_level_function(call,
                                      category=category,
                                      subcategory=subcategory,
                                      item_id=item_id
                                      )
    except:
        pass
