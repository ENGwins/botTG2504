from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ContentTypes

from data.config import YOOToken
from loader import bot, dp

"""
@dp.message_handler(commands=['pay'])
async def pay(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Товар №1 - 100р', callback_data='pay1')

                                      ]
                                  ])
    await bot.send_message(message.from_user.id, 'Тестовая оплата', reply_markup=markup)

"""


@dp.callback_query_handler(text='pay')
async def test_pay(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_invoice(chat_id=call.from_user.id, title='Товар №1', description='описание товара',
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
