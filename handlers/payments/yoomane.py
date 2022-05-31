import typing
from aiogram import types
from aiogram.types import LabeledPrice

from data.config import YOOToken
from data.message import RUSSIAN_POST_SHIPPING_OPTION, PICKUP_SHIPPING_OPTION, RUSSIAN_POST_SHIPPING_OPTION_BY, \
    PICKUP_SHIPPING_OPTION_BY
from keyboards.inline.govno_kb import buy_item
from loader import bot, dp
from utils.db_api.db_commands import get_name_item, get_price_item, get_decr_item


@dp.callback_query_handler(buy_item.filter(buy='buynew'))
async def test_pay(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    callback_data_item_id = int(callback_data['item_id'])
    name = await get_name_item(callback_data_item_id)
    price_get = await get_price_item(callback_data_item_id)
    price = int(price_get * 100)
    decr = await get_decr_item(callback_data_item_id)

    await bot.delete_message(call.from_user.id, call.message.message_id)
    PRICES = [LabeledPrice(label=f'{name}', amount=price)]

    await bot.send_invoice(chat_id=call.from_user.id,
                           title=f'{name}',
                           description=f'{decr}',
                           payload=f'{callback_data_item_id}',
                           provider_token=YOOToken,
                           currency='RUB',
                           need_email=True,
                           need_name=True,
                           send_phone_number_to_provider=True,
                           is_flexible=True,
                           need_phone_number=True,
                           start_parameter='test_bot',
                           prices=PRICES,

                           )


@dp.shipping_query_handler()
async def process_shipping_query(shipping_query: types.ShippingQuery):
    shipping_options = []

    if shipping_query.shipping_address.country_code == 'RU':
        shipping_options.append(RUSSIAN_POST_SHIPPING_OPTION)
        shipping_options.append(PICKUP_SHIPPING_OPTION)

    elif shipping_query.shipping_address.country_code == 'BY':
        shipping_options.append(RUSSIAN_POST_SHIPPING_OPTION_BY)
        shipping_options.append(PICKUP_SHIPPING_OPTION_BY)


    else:
        await bot.answer_shipping_query(shipping_query.id,
                                        ok=False,
                                        error_message='Извините, доставка по указанному вами адресу невозможна. Свяжитесь с админом')
    await bot.answer_shipping_query(
        shipping_query.id,
        ok=True,
        shipping_options=shipping_options
    )


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):  # подтверждение наличия товара
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
