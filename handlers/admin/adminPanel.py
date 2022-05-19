import logging

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ContentTypes

from data.config import admins
from loader import dp, bot


@dp.message_handler(commands=['admin'])
async def adminPanel(message: types.Message):
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
            await message.answer('Хаю-хай, в адмн панель залетай!', reply_markup=markup)

        except Exception as err:
            logging.exception(err)


@dp.message_handler(commands=['pay'])
async def pay(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Товар №1 - 100р', callback_data='pay1'),

                                      ]
                                  ])
    await bot.send_message(message.from_user.id, 'Тестовая оплата', reply_markup=markup)


YOOToken = '381764678:TEST:37370'


@dp.callback_query_handler(text='pay1')
async def test_pay(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_invoice(chat_id=call.from_user.id, title='Товар №1', description='описание\n'
                                                                                    'в\n '
                                                                                    'несколько\n '
                                                                                    'строк\no'
                                                                                    '345',
                           payload='item 1',
                           provider_token=YOOToken,
                           currency='RUB',
                           start_parameter='test_bot',
                           prices=[
                               {
                                   'label': 'Руб',
                                   'amount': 10000
                               }
                           ]
                           )


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == 'item 1':
        await bot.send_message(message.from_user.id, 'Товар оплачен')
