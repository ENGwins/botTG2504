import logging

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.config import admins
from loader import dp

dp.message_handler(commands=['admin'])
async def adminPanel(message:types.Message):
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Рассылка', callback_data='mailing'),
                                          InlineKeyboardButton(text='Изменение каталога', callback_data='change'),
                                          InlineKeyboardButton(text='Кнопка1 админа', callback_data='pass'),
                                          InlineKeyboardButton(text='Кнопка2 админа', callback_data='pass1')
                                      ]
                                  ])
    for admin in admins:
        try:
            await message.answer('Хаю-хай, в адмн панель залетай!',reply_markup=markup)

        except Exception as err:
            logging.exception(err)




