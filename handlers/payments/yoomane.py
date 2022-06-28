import typing
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import LabeledPrice
from sqlalchemy import and_

from data.config import YOOToken
from data.message import RUSSIAN_POST_SHIPPING_OPTION, PICKUP_SHIPPING_OPTION, RUSSIAN_POST_SHIPPING_OPTION_BY, \
    PICKUP_SHIPPING_OPTION_BY
from filters import IsPrivate
from keyboards.inline.govno_kb import order_comment
from keyboards.inline.user import user_cb
from loader import bot, dp
from states.pay import FSMpay
from utils.db_api.database import Basket
from utils.db_api.db_commands import get_name_item, get_price_item, get_decr_item, my_balans, show_basket


@dp.callback_query_handler(user_cb.filter(buy='buynew'))  # при нижатии на продолжить
async def test_pay(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    global item, quantity, item_id, name
    PRICES = []
    pl = {}
    callback_data_item = []
    sum_amount = 0
    total_balans = 0
    await call.answer(text='При доставке СДЭК указывайте адрес пункта выдачи', show_alert=True)
    id_user = call.from_user.id
    item_id_orders = await show_basket(id_user)

    for item_in_order in item_id_orders[1]:
        item_id = item_in_order[0]
        price_get = int(await get_price_item(item_id)) * 100
        quantity = int(await Basket.select('quantity').where(
            and_(Basket.user_id == id_user, Basket.item_id == item_id)).gino.scalar())
        sum_amount += price_get * quantity

    if sum_amount > 299900:
        balans = int(await my_balans(id_user) * 100)
        old_balans = balans

        for item_in_order in item_id_orders[1]:
            item_id = item_in_order[0]
            name = await get_name_item(item_id)
            price_get = int(await get_price_item(item_id)) * 100
            quantity = int(await Basket.select('quantity').where(
                and_(Basket.user_id == id_user, Basket.item_id == item_id)).gino.scalar())

            quantity_t = quantity
            while not quantity_t == 0:
                if old_balans > 100:
                    sale_one_item_2 = price_get / 2
                    if balans > sale_one_item_2:
                        sale_one_item = int(price_get / 2)
                    else:
                        sale_one_item = balans
                    price_sale = int(price_get - sale_one_item)
                    old_balans = int(old_balans - sale_one_item)
                    item = [item_id, name, price_sale, quantity]
                    callback_data_item.append(item)
                    pl[item_id] = [quantity]
                    quantity_t -= 1
                    total_balans += sale_one_item
                else:
                    item = [item_id, name, price_get, quantity]
                    callback_data_item.append(item)
                    pl[item_id] = [quantity]
                    quantity_t -= 1

    else:
        for item_in_order in item_id_orders[1]:
            item_id = item_in_order[0]
            quantity = int(await Basket.select('quantity').where(
                and_(Basket.user_id == id_user, Basket.item_id == item_id)).gino.scalar())
            name = await get_name_item(item_id)
            price_get = int(await get_price_item(item_id)) * 100
            item = [item_id, name, price_get, quantity]
            quantity_t = quantity
            while not quantity_t == 0:
                quantity_t -= 1
                item = [item_id, name, price_get, quantity]
                callback_data_item.append(item)
                pl[item_id] = [quantity]

        total_balans = 0
    new_balans = int(int(await my_balans(id_user)) - (int(total_balans)))


    pl[id_user] = [new_balans]
    for i in callback_data_item:
        PRICES.append(types.LabeledPrice(label=i[1], amount=i[2]))
        name = i[1]

    if len(PRICES) > 1:
        name = 'Комплекты'
        decr = '-'
    else:
        decr = await get_decr_item(item_id)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    markup = await order_comment()
    await bot.send_invoice(chat_id=call.from_user.id,
                           title=f'{name}',
                           description=f'{decr}',
                           payload=pl,
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
                           max_tip_amount=1000000,
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


"""
    if int(price_get) > 2999:
        price_2 = int(price_get / 2)
        balans= await my_balans(id_user)

        if balans>price_2:
            balans=price_2
            price_balans = (int(price_get) - int(balans))
            price = int(price_balans * 100)
        else:
            price_balans = (int(price_get) - int(balans))
            price = int(price_balans * 100)
            balans=price_2

    else:
        price = int(price_get * 100)
        balans=0"""
