import logging
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from data.config import admins
from keyboards.inline.govno_kb import categories_keyboard, subcategory_keyboard, items_keyboard, item_keyboard, \
    buy_item, menu_cd
from keyboards.keyvoard import mainMenu, kb_start_size, sizeMain
from loader import dp, bot
from states.sizeUser import start_testing, cancel_handler1, set_V, FSMClient, set_Vg, set_Vpg, set_Vb, set_Vt, \
    set_sizeL, set_email, yes_not

from utils.db_api.database import Item

from utils.db_api.db_commands import get_item, show_size_user, check_z, get_photo, get_name_item, get_price_item, \
    get_decr_item, check_user, new_user


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict):
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


@dp.callback_query_handler(buy_item.filter())
async def send_admin(call: Union[types.Message, types.CallbackQuery], callback_data: dict):
    id_user_order = call.from_user.id
    check = await check_z(id_user_order)
    if check:
        name_user_order = call.from_user.username
        id_item_order = int(callback_data['item_id'])
        name_item = await Item.select('name').where(Item.id == id_item_order).gino.scalar()
        siz = await show_size_user(id_user_order)

        for admin in admins:
            try:
                await call.bot.send_message(admin,
                                            f'Новый заказ! \n'
                                            f'Товар №{id_item_order} - {name_item} \n'
                                            f'Пользователь Id {id_user_order} \n'
                                            f'Пользователь @{name_user_order}\n'
                                            f'{siz}')
            except Exception as err:
                logging.exception(err)



        await call.answer('Отправили заявку', show_alert=True)
    else:
        await call.answer('Для оформления заказа, введите личную информацию', show_alert=True)


async def start(message: types.Message):
    await bot.send_message(message.from_user.id, "Мы в главном меню", reply_markup=mainMenu)
    id_user=message.from_user.id
    firstname_user=message.from_user.first_name
    lastname_user = message.from_user.last_name

    check=await check_user(id_user)
    if check:
        pass
    else:
        for admin in admins:
            try:

                await bot.send_message(admin, 'Новый пользователь! \n'
                                                  f'ID {id_user}\n'
                                                  f'{firstname_user}')
                await new_user(user_id=id_user,user_first_name=firstname_user,user_last_name=lastname_user)
            except Exception as err:
                logging.exception(err)


async def show_menu1(message: types.Message):
    await list_categories(message)


async def list_categories(message: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await categories_keyboard()
    if isinstance(message, types.Message):
        await message.answer("Выберите категорию", reply_markup=markup)

    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)
        await bot.answer_callback_query(message.id)


async def list_subcategories(callback: types.CallbackQuery, category, **kwargs):
    markup = await subcategory_keyboard(category)
    await bot.answer_callback_query(callback.id)
    await callback.message.edit_reply_markup(markup)


async def list_items(callback: types.CallbackQuery, category, subcategory, **kwargs):
    markup = await items_keyboard(category=category, subcategory=subcategory)
    await bot.answer_callback_query(callback.id)
    await callback.message.answer("Смотри что у нас есть", reply_markup=markup)


async def show_item(callback: types.CallbackQuery, category, subcategory, item_id):
    markup = await item_keyboard(category, subcategory, item_id)
    item = await get_item(item_id)
    text = f'{item}'
    photo_id = await get_photo(item_id)
    name = await get_name_item(item_id)
    price = await get_price_item(item_id)
    decr = await get_decr_item(item_id)
    await bot.answer_callback_query(callback.id)

    await callback.message.answer_photo(
        photo=f'{photo_id}',
        caption=f"Наименование: {name}\n"
                f"________________________________________\n"
                f"Описание:"
                f" {decr}\n"
                f"________________________________________\n"
                f"Цена: {price} Руб",
        reply_markup=markup)

    #await callback.message.edit_text(text, reply_markup=markup)


# Ловим ответ и пшем в словарь
async def load_photo(message: types.Message):
    id_ph = message.photo[0].file_id
    await bot.send_message(message.from_user.id, id_ph)


async def bot_message(message: types.Message):
    if message.text == 'Личная информация':
        user_id = message.from_user.id
        siz = await show_size_user(user_id)
        check = await check_z(user_id)
        if check:
            await bot.send_message(message.from_user.id, f'Мои данные {siz}', reply_markup=sizeMain)
        else:
            await bot.send_message(message.from_user.id, 'Для оформления заказа необходимо указать информацию',
                                   reply_markup=kb_start_size)

    elif message.text == 'Доставка':
        await bot.send_message(message.from_user.id, 'Мы доставляем заказы по-всему Миру🙌🏻\n'
                                                     'По России:\n'
                                                     'Почта России 300₽\n '
                                                     'Сдэк 300₽\n'
                                                     '\n '
                                                     'В Беларусь:Почта России 500₽\n'
                                                     '(14 дней доставка)\n '
                                                     'Сдэк 500₽\n '
                                                     '(4 дня доставка)\n'
                                                     '\n'
                                                     'В другие страны стоимость доставки рассчитывается индивидуально\n '
                                                     '\n'
                                                     'От 4000₽ БЕСПЛАТНАЯ доставка', reply_markup=mainMenu)
    elif message.text == 'Как сделать заказ':
        await bot.send_message(message.from_user.id, 'Оформить заказ вы можете в боте или в любой соцсети\n'
                                                     '\n'
                                                     'Как оформить заказ в боте:\n'
                                                     '1. Внести личные данные в виде мерок;\n '
                                                     '2. Нажать кнопку «оформить» под изделием, которое хотите заказать;\n '
                                                     '3. В течение 5ти минут с вам свяжется администратор для оформления заказа и оплаты;\n'
                                                     '\n'
                                                     'Или заказ можно оформить, написав:\n'
                                                     'В «сообщения сообщества» в vk\n '
                                                     'https://vk.com/liioviio\n '
                                                     '\n '
                                                     'В Direct в Instagram \n '
                                                     'https://instagram.com/liioviio?utm_medium=copy_link', reply_markup=mainMenu)
    elif message.text == 'Давай познакомимся':
        await bot.send_message(message.from_user.id, 'Привет, команда LIIOVIIO на связи! \n'
                                                     '\n'
                                                     'Давай познакомимся. Мы - российский бренд, которые на протяжение 2х лет дарит девушкам комфорт и красоту🙌🏻\n '
                                                     '\n'
                                                     'Мы создаём красивое нижнее белье в котором удобно весь день! Используем только мягкие материалы высокого качества. Отшиваем заказы для каждой из вас индивидуально по Вашим меркам🤍', reply_markup=mainMenu)


def register_handlers_menu(dp: Dispatcher):

    dp.register_message_handler(show_menu1, text="Каталог")
    dp.register_message_handler(start, text='Главное меню')
    dp.register_message_handler(start, commands=['start'], state=None)
    dp.register_message_handler(start_testing, text='Ввести заново', state='*')
    dp.register_message_handler(start_testing, text='Изменение размеров', state='*')
    dp.register_message_handler(cancel_handler1, state="*", commands="Главное меню")
    dp.register_message_handler(cancel_handler1, Text(equals='Главное меню', ignore_case=True), state="*")
    dp.register_message_handler(set_V, state=FSMClient.V)
    dp.register_message_handler(set_Vg, state=FSMClient.Vg)
    dp.register_message_handler(set_Vpg, state=FSMClient.Vpg)
    dp.register_message_handler(set_Vt, state=FSMClient.Vt)
    dp.register_message_handler(set_Vb, state=FSMClient.Vb)
    dp.register_message_handler(set_sizeL, state=FSMClient.sizeL)
    dp.register_message_handler(set_email, state=FSMClient.email)
    dp.register_message_handler(yes_not, state=FSMClient.check_size)
    dp.register_message_handler(bot_message, state='*')
 #   dp.register_message_handler(load_photo, content_types=["photo"])
