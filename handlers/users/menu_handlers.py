import logging

from aiogram.utils.exceptions import BotBlocked
from loguru import logger
from asyncio import sleep
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import admins
from keyboards.inline.govno_kb import categories_keyboard, subcategory_keyboard, items_keyboard, item_keyboard, \
    buy_item, menu_cd
from keyboards.keyvoard import mainMenu, kb_start_size, sizeMain
from loader import dp, bot
from states.Mailing import MailingService

from utils.db_api.database import Item

from utils.db_api.db_commands import get_item, show_size_user, check_z, get_photo, get_name_item, get_price_item, \
    get_decr_item, check_user, new_user, user_all_check


@dp.callback_query_handler(text='mailing', state=None)
async def Mailing(call: types.CallbackQuery):  # один из пунктов админки, выдает клаву с выбором операции
    text = call.message.text
    for admin in admins:
        try:
            await call.bot.send_message(chat_id=admin, text='Введите текст рассылки')
            await MailingService.text.set()

        except Exception as err:
            logging.exception(err)


@dp.callback_query_handler(text='add_photo', state=MailingService.state)
async def add_photo(call: types.CallbackQuery):
    await call.message.answer('Пришлите фото')
    await MailingService.photo.set()


@dp.callback_query_handler(text='next', state=MailingService.photo)
async def startMailing(call: types.CallbackQuery, state: FSMContext):
    users = await user_all_check()
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    await state.finish()
    for user in users:
        try:
            await call.bot.send_photo(chat_id=user.user_id, photo=photo, caption=text)
            await sleep(0.33)
        except Exception:
            pass
    await call.message.answer('Рассылка выполнена')


@dp.callback_query_handler(text='next', state=MailingService.state)
async def startMailing(call: types.CallbackQuery, state: FSMContext):
    users = await user_all_check()
    data = await state.get_data()
    text = data.get('text')
    await state.finish()
    for user in users:
        try:
            await call.bot.send_message(chat_id=user.user_id, text=text)
            await sleep(0.33)
        except Exception:
            pass
    await call.message.answer('Рассылка выполнена')


@dp.callback_query_handler(text="quit", state=[MailingService.text, MailingService.photo, MailingService.state])
async def quit_m(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer('Рассылка отменена')


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict):
    currrent_level = callback_data.get('level')
    category = callback_data.get('category')
    subcategory = callback_data.get('subcategory')
    item_id = int(callback_data.get('item_id'))

    levels = {
        "0": list_categories,
        "1": list_subcategories,
        "2": list_items,
        "3": show_item
    }
    currrent_level_function = levels[currrent_level]

    await currrent_level_function(call,
                                  category=category,
                                  subcategory=subcategory,
                                  item_id=item_id
                                  )


@dp.callback_query_handler(buy_item.filter())
async def send_admin(call: Union[types.Message, types.CallbackQuery], callback_data: dict):
    id_user_order = call.from_user.id
    check = await check_z(id_user_order)
    if check:
        name_user_order = call.from_user.username
        id_item_order = int(callback_data['item_id'])
        name_item = await Item.select('name').where(Item.id == id_item_order).gino.scalar()
        siz = await show_size_user(id_user_order)

        for admin in admins:
            try:
                await call.bot.send_message(admin,
                                            f'Новый заказ! \n'
                                            f'Товар №{id_item_order} - {name_item} \n'
                                            f'Пользователь Id {id_user_order} \n'
                                            f'Пользователь @{name_user_order}\n'
                                            f'{siz}')
            except Exception as err:
                logging.exception(err)

        await call.answer('Отправили заявку', show_alert=True)
    else:
        await call.answer('Для оформления заказа, введите личную информацию', show_alert=True)


async def anti_flood(*args, **kwargs):
    m = args[0]
    await m.answer("Не флуди :)")


@dp.message_handler(commands=['start'], state=None)
@dp.throttled(anti_flood, rate=5)
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, "Мы в главном меню", reply_markup=mainMenu)
    id_user = message.from_user.id
    firstname_user = message.from_user.first_name
    lastname_user = message.from_user.last_name

    check = await check_user(id_user)
    if check:
        pass
    else:
        for admin in admins:
            try:

                await bot.send_message(admin, 'Новый пользователь! \n'
                                              f'ID {id_user}\n'
                                              f'{firstname_user}')
                await new_user(user_id=id_user, user_first_name=firstname_user, user_last_name=lastname_user)
            except Exception as err:
                logging.exception(err)


async def list_categories(message: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await categories_keyboard()
    if isinstance(message, types.Message):
        await message.answer("Выберите категорию", reply_markup=markup)

    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)
        await bot.answer_callback_query(message.id)


async def list_subcategories(callback: types.CallbackQuery, category, **kwargs):
    markup = await subcategory_keyboard(category)
    await bot.answer_callback_query(callback.id)
    await callback.message.edit_reply_markup(markup)


async def list_items(callback: types.CallbackQuery, category, subcategory, **kwargs):
    markup = await items_keyboard(category=category, subcategory=subcategory)
    await bot.answer_callback_query(callback.id)
    await callback.message.answer("Смотри что у нас есть", reply_markup=markup)


async def show_item(callback: types.CallbackQuery, category, subcategory, item_id):
    markup = await item_keyboard(category, subcategory, item_id)
    item = await get_item(item_id)
    text = f'{item}'
    photo_id = await get_photo(item_id)
    name = await get_name_item(item_id)
    price = await get_price_item(item_id)
    decr = await get_decr_item(item_id)
    await bot.answer_callback_query(callback.id)

    await callback.message.answer_photo(
        photo=f'{photo_id}',
        caption=f"Наименование: {name}\n"
                f"________________________________________\n"
                f"Описание:"
                f" {decr}\n"
                f"________________________________________\n"
                f"Цена: {price} Руб",
        reply_markup=markup)

    # await callback.message.edit_text(text, reply_markup=markup)


# проверка ID фото
async def load_photo(message: types.Message):
    id_ph = message.photo[0].file_id
    await bot.send_message(message.from_user.id, id_ph)


@dp.message_handler(content_types=['text'])
@dp.throttled(anti_flood, rate=1)
async def bot_message(message: types.Message):
    if message.text == 'Личная информация':
        user_id = message.from_user.id
        siz = await show_size_user(user_id)
        check = await check_z(user_id)
        if check:
            await bot.send_message(message.from_user.id, f'Мои данные {siz}', reply_markup=sizeMain)
        else:
            await bot.send_message(message.from_user.id, 'Для оформления заказа необходимо указать информацию',
                                   reply_markup=kb_start_size)

    elif message.text == 'Доставка':
        await bot.send_message(message.from_user.id, 'Мы доставляем заказы по-всему Миру🙌🏻\n'
                                                     'По России:\n'
                                                     'Почта России 300₽\n '
                                                     'Сдэк 300₽\n'
                                                     '\n '
                                                     'В Беларусь:Почта России 500₽\n'
                                                     '(14 дней доставка)\n '
                                                     'Сдэк 500₽\n '
                                                     '(4 дня доставка)\n'
                                                     '\n'
                                                     'В другие страны стоимость доставки рассчитывается индивидуально\n '
                                                     '\n'
                                                     'От 4000₽ БЕСПЛАТНАЯ доставка', reply_markup=mainMenu)
    elif message.text == 'Как сделать заказ':
        await bot.send_message(message.from_user.id, 'Оформить заказ вы можете в боте или в любой соцсети\n'
                                                     '\n'
                                                     'Как оформить заказ в боте:\n'
                                                     '1. Внести личные данные в виде мерок;\n '
                                                     '2. Нажать кнопку «оформить» под изделием, которое хотите заказать;\n '
                                                     '3. В течение 5ти минут с вам свяжется администратор для оформления заказа и оплаты;\n'
                                                     '\n'
                                                     'Или заказ можно оформить, написав:\n'
                                                     'В «сообщения сообщества» в vk\n '
                                                     'https://vk.com/liioviio\n '
                                                     '\n '
                                                     'В Direct в Instagram \n '
                                                     'https://instagram.com/liioviio?utm_medium=copy_link',
                               reply_markup=mainMenu)
    elif message.text == 'Давай познакомимся':
        await bot.send_message(message.from_user.id, 'Привет, команда LIIOVIIO на связи! \n'
                                                     '\n'
                                                     'Давай познакомимся. Мы - российский бренд, которые на протяжение 2х лет дарит девушкам комфорт и красоту🙌🏻\n '
                                                     '\n'
                                                     'Мы создаём красивое нижнее белье в котором удобно весь день! Используем только мягкие материалы высокого качества. Отшиваем заказы для каждой из вас индивидуально по Вашим меркам🤍',
                               reply_markup=mainMenu)
    elif message.text == 'Главное меню':
        await bot.send_message(message.from_user.id, "Мы в главном меню", reply_markup=mainMenu)
    elif message.text == 'Каталог':
        await list_categories(message)

@dp.errors_handler(exception=BotBlocked)
async def errors_msg(update: types.Update, exception: BotBlocked):
    logger.exception(f'Bot blocked by user {update.message.from_user.id}')
    return True


