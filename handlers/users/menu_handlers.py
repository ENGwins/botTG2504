from typing import Union

from aiogram import types, Dispatcher

from keyboards.inline.govno_kb import categories_keyboard, subcategory_keyboard, items_keyboard, item_keyboard, \
    buy_item, menu_cd
from loader import dp
from utils.db_api.db_commands import get_item

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
    await call.answer('Отправили заявку',show_alert=True)
    id_user_order= call.from_user.id
    id_item_order=callback_data['item_id']
    await call.answer()
    await call.bot.send_message(644812536,f'Новый заказ! \nТовар №{id_item_order} \nПользователь {id_user_order}')



async def show_menu1(message: types.Message):
    await list_categories(message)


async def list_categories(message: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await categories_keyboard()

    if isinstance(message, types.Message):
        await message.answer("Смотри, что у нас есть", reply_markup=markup)

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
    markup = item_keyboard(category, subcategory, item_id)

    item = await get_item(item_id)
    text = f'Купи {item}'
    await callback.message.edit_text(text, reply_markup=markup)


def register_handlers_menu(dp: Dispatcher):
    dp.register_message_handler(show_menu1, commands=['menu'])
