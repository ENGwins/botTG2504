from typing import Union

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from aiogram.utils.callback_data import CallbackData

from loader import bot
from utils.db_api.db_commands import my_balans

user_cb = CallbackData('user', 'id_user', 'my_size', 'my_orders', 'menu', 'comment', 'id_order', 'buy', 'id_item')


async def userPanel(message: Union[types.Message, types.CallbackQuery]):
    id_user = message.from_user.id

    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton(text='👙 Мерки', callback_data=user_cb.new(id_user=id_user,
                                                                        my_size='my_size',
                                                                        my_orders='None',
                                                                        menu='None',
                                                                        comment='None',
                                                                        id_order='None',
                                                                        buy='None',
                                                                        id_item='None'
                                                                        )),
        InlineKeyboardButton(text='🧾 Мои заказы', callback_data=user_cb.new(id_user=id_user,
                                                                             my_size='None',
                                                                             my_orders='my_orders',
                                                                             menu='None',
                                                                             comment='None',
                                                                             id_order='None',
                                                                             buy='None',
                                                                             id_item='None'
                                                                             ))
    ),
    markup.insert(
        InlineKeyboardButton(text='₽ Получить бонусы!', callback_data=user_cb.new(id_user=id_user,
                                                                                      my_size='None',
                                                                                      my_orders='None',
                                                                                      menu='referral',
                                                                                      comment='None',
                                                                                      id_order='None',
                                                                                      buy='None',
                                                                                      id_item='None'
                                                                                      ))
    )

    # await bot.send_message(message.from_user.id, '🙍‍♀️Личный кабинет', reply_markup=markup)
    user_id = message.from_user.id
    balans = await my_balans(user_id)
    await bot.send_message(message.from_user.id, text=(f'🙍‍♀️Личный кабинет\n\n'
                                                       f' Мои бонусы: {balans}\n '
                                                       f'1 бонус = 1 руб \n(списание автоматически при оформлении заказа)\n\n'
                                                       f'ID для начисления бонусов за отзыв: `{user_id}`'), reply_markup=markup,
                           parse_mode=ParseMode.MARKDOWN)


async def set_size():
    markup = InlineKeyboardMarkup(row_width=1)

    markup.row(
        InlineKeyboardButton(text='🖍 Указать|обновить мерки', callback_data=user_cb.new(id_user="None",
                                                                                         my_size='my_size_new',
                                                                                         my_orders='None',
                                                                                         menu='None',
                                                                                         comment='None',
                                                                                         id_order='None',
                                                                                         buy='None',
                                                                                         id_item='None'
                                                                                         ))
    ),
    markup.add(
        InlineKeyboardButton(text='⬅️ Назад', callback_data=user_cb.new(id_user="None",
                                                                        my_size='None',
                                                                        my_orders='None',
                                                                        menu="back",
                                                                        comment='None',
                                                                        id_order='None',
                                                                        buy='None',
                                                                        id_item='None'
                                                                        )),
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
                                                                             id_order='None',
                                                                             buy='None',
                                                                             id_item='None'
                                                                             )),

        InlineKeyboardButton(text='🔁 Ввести заново', callback_data=user_cb.new(id_user="None",
                                                                                my_size='my_size_new',
                                                                                my_orders='None',
                                                                                menu='None',
                                                                                comment='None',
                                                                                id_order='None',
                                                                                buy='None',
                                                                                id_item='None'
                                                                                ))
    )
    return markup


async def add_comment_kb(id_order):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(text='📝 Добавить|обновить комментарий', callback_data=user_cb.new(id_user="None",
                                                                                       my_size='None',
                                                                                       my_orders='None',
                                                                                       menu="None",
                                                                                       comment='comment',
                                                                                       id_order=id_order,
                                                                                       buy='None',
                                                                                       id_item='None'
                                                                                       ))
    )
    return markup


async def size_next(lvl):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton(
            text='Далее', callback_data=user_cb.new(id_user='None',
                                                    my_size='None',
                                                    my_orders='None',
                                                    menu=lvl + 1,
                                                    comment='None',
                                                    id_order='None',
                                                    buy='None',
                                                    id_item='None')
        ),
        InlineKeyboardButton(
            text='Назад', callback_data=user_cb.new(id_user='None',
                                                    my_size='None',
                                                    my_orders='None',
                                                    menu=lvl - 1,
                                                    comment='None',
                                                    id_order='None',
                                                    buy='None',
                                                    id_item='None')
        )

    )
    return markup
