import typing
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import LabeledPrice

from data.config import YOOToken
from data.message import RUSSIAN_POST_SHIPPING_OPTION, PICKUP_SHIPPING_OPTION, RUSSIAN_POST_SHIPPING_OPTION_BY, \
    PICKUP_SHIPPING_OPTION_BY
from filters import IsPrivate
from keyboards.inline.govno_kb import buy_item, order_comment
from keyboards.inline.user import user_cb
from loader import bot, dp
from states.pay import FSMpay
from utils.db_api.db_commands import get_name_item, get_price_item, get_decr_item, my_balans


@dp.callback_query_handler(user_cb.filter(buy='buynew'))  # при нижатии на продолжить
async def test_pay(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    id_user=call.from_user.id
    callback_data_item_id = int(callback_data['id_item'])
    name = await get_name_item(callback_data_item_id)

    balans = await my_balans(id_user)
    price_get = await get_price_item(callback_data_item_id)
    price_balans=(int(price_get)-int(balans))
    price = int(price_balans * 100)
    decr = await get_decr_item(callback_data_item_id)

    payload=f'{callback_data_item_id}, {balans}'

    await bot.delete_message(call.from_user.id, call.message.message_id)
    PRICES = [LabeledPrice(label=f'{name}', amount=price)]
    markup = await order_comment()
    await bot.send_invoice(chat_id=call.from_user.id,
                           title=f'{name}',
                           description=f'{decr}',
                           payload=payload,
                           provider_token=YOOToken,
                           currency='RUB',
                           need_email=True,
                           need_name=True,
                           send_phone_number_to_provider=True,
                           is_flexible=True,
                           need_phone_number=True,
                           start_parameter='test_bot',
                           prices=PRICES,
                           reply_markup=markup,
                           )


@dp.callback_query_handler(user_cb.filter(comment='newcomment'))  # при нажатии на кнопку доб коммент
async def add_comment(callback: types.CallbackQuery):
    await callback.message.answer('Введите комментарий к заказу')
    await FSMpay.state1.set()


@dp.message_handler(IsPrivate(), state=FSMpay.state1)
async def add_commentt(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['comment'] = message.text

    await bot.send_message(chat_id=message.from_user.id, text='Отлично! Можете переходить к оплате')
    await FSMpay.state2.set()


@dp.shipping_query_handler(state=FSMpay.state2)
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
                                        error_message='Извините, доставка по указанному вами адресу невозможна. Свяжитесь с админом для оформления заказа')
    await bot.answer_shipping_query(
        shipping_query.id,
        ok=True,
        shipping_options=shipping_options
    )
    # await FSMpay.state3.set()


@dp.pre_checkout_query_handler(state=FSMpay.state2)
@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery,
                                     state: FSMContext):  # подтверждение наличия товара
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

    # await FSMpay.state4.set()
