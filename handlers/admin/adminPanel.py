from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from data.config import admins
from filters import IsPrivate
from loader import dp, bot
from utils.db_api.db_commands import count_work_order, user_all_check

admin_cb = CallbackData('order', 'id_order', 'admin_change', 'tracking', 'state')


@dp.message_handler(IsPrivate(),user_id=admins,commands=['admin'])
async def adminPanel(message: types.Message):
    count = await count_work_order()
    count_users=len(await user_all_check())
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton(text='Рассылка', callback_data='mailing'),
        InlineKeyboardButton(text='Начислить бонусы', callback_data='bonus')
    )
    markup.insert(
        InlineKeyboardButton(text=f'Активные заказы - ({count})', callback_data='orders')
    )
    markup.insert(
        InlineKeyboardMarkup(text='Изменение каталога',callback_data=admin_cb.new(id_order='0',
                                                                                  admin_change='chage_catalog',
                                                                                  tracking='0',
                                                                                  state='0'))
    )
    markup.insert(
        InlineKeyboardMarkup(text='Установить скидку',callback_data=admin_cb.new(id_order='0',
                                                                                  admin_change='sale',
                                                                                  tracking='0',
                                                                                  state='0'))
    )

    await bot.send_message(message.from_user.id, 'Хаю-хай, в админ панель залетай!\n'
                                                 f'Кол-во пользователей - {count_users}', reply_markup=markup)


async def adminOrder(id_order):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton(text='Изменить статус',
                             callback_data=admin_cb.new(id_order=id_order,
                                                        admin_change="admin_change",
                                                        tracking="None",
                                                        state='None')),
        InlineKeyboardButton(text='Добавить трек',
                             callback_data=admin_cb.new(id_order=id_order,
                                                        admin_change="None",
                                                        tracking="tracking",
                                                        state='None'))
    )
    markup.insert(
        InlineKeyboardButton(text='Закрыть заказ',
                             callback_data=admin_cb.new(id_order=id_order,
                                                        admin_change="None",
                                                        tracking="None",
                                                        state='state4'))
    )
    return markup


async def state_order(id_order):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton(text='На пошиве',
                             callback_data=admin_cb.new(id_order=id_order,
                                                        admin_change="None",
                                                        tracking="None",
                                                        state='state1')),
        InlineKeyboardButton(text='Ожидает отправления',
                             callback_data=admin_cb.new(id_order=id_order,
                                                        admin_change="None",
                                                        tracking="None",
                                                        state='state2'))
    )
    markup.insert(
        InlineKeyboardButton(text='Отправлен',
                             callback_data=admin_cb.new(id_order=id_order,
                                                        admin_change="None",
                                                        tracking="None",
                                                        state='state3'))
    )
    return markup


async def change_catalog_kb(item_id):
    markup=InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton(text='Есть в наличии',callback_data=admin_cb.new(id_order=item_id,
                                                        admin_change="active",
                                                        tracking="None",
                                                        state='None')),

        InlineKeyboardButton(text='Закончились',callback_data=admin_cb.new(id_order=item_id,
                                                        admin_change="deactivate",
                                                        tracking="None",
                                                        state='None')))
    return markup
