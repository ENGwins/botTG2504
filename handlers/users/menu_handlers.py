from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from keyboards.inline.govno_kb import categories_keyboard, subcategory_keyboard, items_keyboard, item_keyboard, \
    buy_item, menu_cd
from keyboards.keyvoard import mainMenu, kb_start_size, sizeMain
from loader import dp, bot
from states.sizeUser import set_Vg, set_Vpg, set_Vb, set_sizeL, set_Vt, FSMClient, start_testing, yes_not, set_V, \
    set_email, cancel_handler1
from utils.db_api.database import Item

from utils.db_api.db_commands import get_item, show_size_user, get_photo, check_z


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


"""@dp.callback_query_handler(buy_item.filter())
async def send_admin(call: Union[types.Message, types.CallbackQuery], callback_data: dict):
    await call.answer('Отправили заявку', show_alert=True)
    id_user_order = call.from_user.id
    name_user_order = call.from_user.username

    await call.answer()
    id_item_order = int(callback_data['item_id'])
    name_item = await Item.select('name').where(Item.id == id_item_order).gino.scalar()
    await call.bot.send_message(644812536,
                                f'Новый заказ! \nТовар №{id_item_order} - {name_item} \nПользователь Id {id_user_order} \nПользователь @{name_user_order}')"""


@dp.callback_query_handler(buy_item.filter())
async def send_admin(call: Union[types.Message, types.CallbackQuery], callback_data: dict):
    id_user_order = call.from_user.id
    check = await check_z(id_user_order)
    if check:
        name_user_order = call.from_user.username
        id_item_order = int(callback_data['item_id'])
        name_item = await Item.select('name').where(Item.id == id_item_order).gino.scalar()
        siz = await show_size_user(id_user_order)

        await call.bot.send_message(644812536,
                                    f'Новый заказ! \n'
                                    f'Товар №{id_item_order} - {name_item} \n'
                                    f'Пользователь Id {id_user_order} \n'
                                    f'Пользователь @{name_user_order}\n'
                                    f'{siz}')

        await call.answer('Отправили заявку', show_alert=True)
    else:
        await call.answer('Для оформления заказа, введите личную информацию', show_alert=True)


async def show_menu1(message: types.Message):
    await list_categories(message)


async def list_categories(message: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await categories_keyboard()

    if isinstance(message, types.Message):
        await message.answer("Выберите категорию", reply_markup=markup)

    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


async def list_subcategories(callback: types.CallbackQuery, category, **kwargs):
    markup = await subcategory_keyboard(category)
    await callback.message.edit_reply_markup(markup)


async def list_items(callback: types.CallbackQuery, category, subcategory, **kwargs):
    markup = await items_keyboard(category=category, subcategory=subcategory)
    await callback.message.edit_text("Смотри что у нас есть", reply_markup=markup)


async def show_item(callback: types.CallbackQuery, category, subcategory, item_id):
    photo = await get_photo(item_id)
    id_photo = f"{photo}"
    await bot.send_photo(callback.from_user.id, id_photo)

    markup = item_keyboard(category, subcategory, item_id)
    item = await get_item(item_id)
    text = f'Купи {item}'

    await callback.message.edit_text(text, reply_markup=markup)


async def start(message: types.Message):
    await bot.send_message(message.from_user.id, "Мы в главном меню", reply_markup=mainMenu)


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
        await bot.send_message(message.from_user.id, 'Информация по доставке', reply_markup=mainMenu)
    elif message.text == 'Как сделать заказ':
        await bot.send_message(message.from_user.id, 'Информация как сделать заказ', reply_markup=mainMenu)
    elif message.text == 'Давай познакомимся':
        await bot.send_message(message.from_user.id, 'Какая нибудь шляпа', reply_markup=mainMenu)


def register_handlers_menu(dp: Dispatcher):
    dp.register_message_handler(start, text='Главное меню')
    dp.register_message_handler(start, commands=['start'], state=None)
    dp.register_message_handler(show_menu1, text="Каталог")
    dp.register_message_handler(start_testing,text='Ввести заново',state='*')
    dp.register_message_handler(start_testing, text='Изменение размеров', state='*')
    dp.register_message_handler(cancel_handler1, state="*", commands="Главное меню")
    dp.register_message_handler(cancel_handler1, Text(equals='Главное меню', ignore_case=True), state="*")
    dp.register_message_handler(set_V, state=FSMClient.V)
    dp.register_message_handler(set_Vg, state=FSMClient.Vg)
    dp.register_message_handler(set_Vpg, state=FSMClient.Vpg)
    dp.register_message_handler(set_Vb, state=FSMClient.Vb)
    dp.register_message_handler(set_Vt, state=FSMClient.Vt)
    dp.register_message_handler(set_sizeL, state=FSMClient.sizeL)
    dp.register_message_handler(set_email, state=FSMClient.email)
    dp.register_message_handler(yes_not, state=FSMClient.check_size)
    dp.register_message_handler(bot_message, state='*')
