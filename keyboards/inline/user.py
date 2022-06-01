from typing import Union


from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import bot

user_cb = CallbackData('user', 'id_user', 'my_size', 'my_orders', 'menu', 'comment', 'id_order')


async def userPanel(message: Union[types.Message, types.CallbackQuery]):
    id_user = message.from_user.id

    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton(text='👙 Мерки', callback_data=user_cb.new(id_user=id_user,
                                                                        my_size='my_size',
                                                                        my_orders='None',
                                                                        menu='None',
                                                                        comment='None',
                                                                        id_order='None'
                                                                        )),
        InlineKeyboardButton(text='🧾 Мои заказы', callback_data=user_cb.new(id_user=id_user,
                                                                             my_size='None',
                                                                             my_orders='my_orders',
                                                                             menu='None',
                                                                             comment='None',
                                                                             id_order='None'
                                                                             )),
    )

    await bot.send_message(message.from_user.id, '🙍‍♀️Личный кабинет', reply_markup=markup)


async def set_size():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(text='⬅️ Назад', callback_data=user_cb.new(id_user="None",
                                                                        my_size='None',
                                                                        my_orders='None',
                                                                        menu="back",
                                                                        comment='None',
                                                                        id_order='None'
                                                                        )),
        InlineKeyboardButton(text='🔁 Ввести заново', callback_data=user_cb.new(id_user="None",
                                                                                my_size='my_size_new',
                                                                                my_orders='None',
                                                                                menu='None',
                                                                                comment='None',
                                                                                id_order='None'
                                                                                ))
    )
    return markup


async def yes_no():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(text='✅ Подтверждаю', callback_data=user_cb.new(id_user="None",
                                                                             my_size='None',
                                                                             my_orders='None',
                                                                             menu="ok",
                                                                             comment='None',
                                                                             id_order='None'
                                                                             )),

        InlineKeyboardButton(text='🔁 Ввести заново', callback_data=user_cb.new(id_user="None",
                                                                                my_size='my_size_new',
                                                                                my_orders='None',
                                                                                menu='None',
                                                                                comment='None',
                                                                                id_order='None'
                                                                                ))
    )
    return markup


async def add_comment_kb(id_order):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(text='📝 Добавить комментарий', callback_data=user_cb.new(id_user="None",
                                                                                       my_size='None',
                                                                                       my_orders='None',
                                                                                       menu="None",
                                                                                       comment='comment',
                                                                                       id_order=id_order
                                                                                       ))
    )
    return markup
