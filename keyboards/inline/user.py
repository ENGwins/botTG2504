from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import bot

user_cb = CallbackData('user', 'id_user', 'my_size', 'my_orders')


async def userPanel(message: types.Message):
    id_user = message.from_user.id

    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton(text='Мерки', callback_data=user_cb.new(id_user=id_user,
                                                                     my_size='my_size',
                                                                     my_orders='None'
                                                                     )),
        InlineKeyboardButton(text='Мои заказы', callback_data=user_cb.new(id_user=id_user,
                                                                          my_size='None',
                                                                          my_orders='my_orders'
                                                                          )),
    )

    await bot.send_message(message.from_user.id, 'Вы зашли в личный кабинет', reply_markup=markup)
