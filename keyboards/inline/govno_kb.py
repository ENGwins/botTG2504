from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from keyboards.inline.user import user_cb
from utils.db_api.db_commands import count_items, get_categories, get_subcategories, get_items, check_sale

menu_cd = CallbackData("show_menu1", "level", "category", "subcategory", "item_id", 'quantity', 'buy', 'id', 'page')
basket_cd = CallbackData('basket', 'user_id')


# buy_item = CallbackData("buy", "id_item", 'buy', 'new_basket_id', 'quantity')


def make_callback_data(level, category="0", subcategory="0", item_id="0", quantity='None', buy='0', id='0',
                       page='page'):
    return menu_cd.new(level=level, category=category, subcategory=subcategory, item_id=item_id, quantity=quantity,
                       buy=buy, id=id, page=page)


async def my_basket_kb(category, subcategory, total_amount, item_id, page, count_page, current_page: int = 0, **kwargs):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup(row_width=3)
    if page == 0:
        markup.row(
            InlineKeyboardButton(text="Назад",
                                 callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                                  category=category,
                                                                  subcategory=subcategory)
                                 ),

            InlineKeyboardButton(text='▶', callback_data=menu_cd.new(item_id='None',
                                                                     level='None',
                                                                     category=category,
                                                                     subcategory=subcategory,
                                                                     buy='None',
                                                                     quantity='None',
                                                                     id='page_incr',
                                                                     page=current_page))
        ),
        markup.add(InlineKeyboardButton('Изменить кол-во', callback_data=menu_cd.new(item_id=item_id,
                                                                                     level=CURRENT_LEVEL,
                                                                                     category=category,
                                                                                     subcategory=subcategory,
                                                                                     buy='None',
                                                                                     quantity='None',
                                                                                     id='None',
                                                                                     page=current_page)),
                   )
        markup.add(
            InlineKeyboardButton(text=f'✅ Оформить заказ на сумму: {total_amount} Руб',
                                 callback_data=menu_cd.new(item_id='None',
                                                           level=CURRENT_LEVEL,
                                                           category=category,
                                                           subcategory=subcategory,
                                                           buy='newbuy',
                                                           quantity='None',
                                                           id='None',
                                                           page=current_page))
        )
    elif page == count_page - 1:
        markup.row(
            InlineKeyboardButton(text="Назад",
                                 callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                                  category=category,
                                                                  subcategory=subcategory)
                                 ),
            InlineKeyboardButton(text='◀', callback_data=menu_cd.new(item_id='None',
                                                                     level='None',
                                                                     category=category,
                                                                     subcategory=subcategory,
                                                                     buy='None',
                                                                     quantity='None',
                                                                     id='page_decr',
                                                                     page=current_page))
        ),
        markup.add(InlineKeyboardButton('Изменить кол-во', callback_data=menu_cd.new(item_id=item_id,
                                                                                     level=CURRENT_LEVEL,
                                                                                     category=category,
                                                                                     subcategory=subcategory,
                                                                                     buy='None',
                                                                                     quantity='None',
                                                                                     id='None',
                                                                                     page=current_page)),
                   )
        markup.add(
            InlineKeyboardButton(text=f'✅ Оформить заказ на сумму: {total_amount} Руб',
                                 callback_data=menu_cd.new(item_id='None',
                                                           level=CURRENT_LEVEL,
                                                           category=category,
                                                           subcategory=subcategory,
                                                           buy='newbuy',
                                                           quantity='None',
                                                           id='None',
                                                           page=current_page))
        )
    else:
        markup.row(
            InlineKeyboardButton(text='◀', callback_data=menu_cd.new(item_id='None',
                                                                     level='None',
                                                                     category=category,
                                                                     subcategory=subcategory,
                                                                     buy='None',
                                                                     quantity='None',
                                                                     id='page_decr',
                                                                     page=current_page)),

            InlineKeyboardButton('Изменить кол-во', callback_data=menu_cd.new(item_id=item_id,
                                                                              level=CURRENT_LEVEL,
                                                                              category=category,
                                                                              subcategory=subcategory,
                                                                              buy='None',
                                                                              quantity='None',
                                                                              id='None',
                                                                              page=current_page)),

            InlineKeyboardButton(text='▶', callback_data=menu_cd.new(item_id='None',
                                                                     level='None',
                                                                     category=category,
                                                                     subcategory=subcategory,
                                                                     buy='None',
                                                                     quantity='None',
                                                                     id='page_incr',
                                                                     page=current_page))
        ),
        markup.add(
            InlineKeyboardButton(text=f'✅ Оформить заказ на сумму: {total_amount} Руб',
                                 callback_data=menu_cd.new(item_id='None',
                                                           level=CURRENT_LEVEL,
                                                           category=category,
                                                           subcategory=subcategory,
                                                           buy='newbuy',
                                                           quantity='None',
                                                           id='None',
                                                           page=current_page))
        )
        markup.insert(
            InlineKeyboardButton(text="Назад",
                                 callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                                  category=category,
                                                                  subcategory=subcategory))
        ),
    return markup


async def basket_kb(total_amount, item_id, category, subcategory, count_item, current_page: int = 0):
    CURRENT_LEVEL = 3

    markup = InlineKeyboardMarkup(row_width=3)
    markup.row(InlineKeyboardButton('➖', callback_data=menu_cd.new(item_id=item_id,
                                                                   level=CURRENT_LEVEL,
                                                                   category=category,
                                                                   subcategory=subcategory,
                                                                   buy='None',
                                                                   quantity='quantity_decr',
                                                                   id='None',
                                                                   page=current_page)),

               InlineKeyboardButton(text=f'{count_item} шт.', callback_data='pass'),

               InlineKeyboardButton('➕', callback_data=menu_cd.new(item_id=item_id,
                                                                   level=CURRENT_LEVEL,
                                                                   category=category,
                                                                   subcategory=subcategory,
                                                                   buy='None',
                                                                   quantity='quantity_incr',
                                                                   id='None',
                                                                   page=current_page)),
               ),

    markup.insert(
        InlineKeyboardButton(text='Назад', callback_data=menu_cd.new(item_id=item_id,
                                                                     level=CURRENT_LEVEL,
                                                                     category=category,
                                                                     subcategory=subcategory,
                                                                     buy='book',
                                                                     quantity='None',
                                                                     id='None',
                                                                     page=current_page)),
    ),
    markup.insert(
        InlineKeyboardButton(text='✅ Оформить', callback_data=menu_cd.new(item_id=item_id,
                                                                          level=CURRENT_LEVEL,
                                                                          category=category,
                                                                          subcategory=subcategory,
                                                                          buy='newbuy',
                                                                          quantity='None',
                                                                          id='None',
                                                                          page=current_page))
    ),
    markup.row(
        InlineKeyboardButton(text=f'🛍 Моя корзина: {total_amount} руб', callback_data=menu_cd.new(item_id='None',
                                                                                                   level=CURRENT_LEVEL,
                                                                                                   category=category,
                                                                                                   subcategory=subcategory,
                                                                                                   buy='None',
                                                                                                   quantity='None',
                                                                                                   id='page_incr',
                                                                                                   page=current_page)))
    # markup.add(*buttons)

    return markup


async def item_keyboard(category, subcategory, id_item, total_amount, max_pages: int, key='book', page: int = 0):
    CURRENT_LEVEL = 3
    # ---------------------------------
    previous_page = page - 1
    previous_page_text = "<< "
    current_page_text = f"Фото {page + 1} из {max_pages}"
    next_page = page + 1
    next_page_text = " >>"

    markup = InlineKeyboardMarkup(row_width=3)
    if max_pages == 1:
       pass
    elif page == max_pages-1:
        markup.add(
            InlineKeyboardButton(
                text=previous_page_text,
                callback_data=menu_cd.new(item_id=id_item,
                                          level=CURRENT_LEVEL,
                                          category=category,
                                          subcategory=subcategory,
                                          buy=key,
                                          quantity='None',
                                          id='None',
                                          page=previous_page)),
            InlineKeyboardButton(
                text=current_page_text,
                callback_data=menu_cd.new(item_id=id_item,
                                          level=CURRENT_LEVEL,
                                          category=category,
                                          subcategory=subcategory,
                                          buy=key,
                                          quantity='None',
                                          id='None',
                                          page='current_page'))

        )


    elif page < 1:
        markup.add(
            InlineKeyboardButton(
                text=current_page_text,
                callback_data=menu_cd.new(item_id=id_item,
                                          level=CURRENT_LEVEL,
                                          category=category,
                                          subcategory=subcategory,
                                          buy=key,
                                          quantity='None',
                                          id='None',
                                          page='current_page')),

            InlineKeyboardButton(
                text=next_page_text,
                callback_data=menu_cd.new(item_id=id_item,
                                          level=CURRENT_LEVEL,
                                          category=category,
                                          subcategory=subcategory,
                                          buy=key,
                                          quantity='None',
                                          id='None',
                                          page=next_page))
        )
    else:
        markup.add(
            InlineKeyboardButton(
                text=previous_page_text,
                callback_data=menu_cd.new(item_id=id_item,
                                          level=CURRENT_LEVEL,
                                          category=category,
                                          subcategory=subcategory,
                                          buy=key,
                                          quantity='None',
                                          id='None',
                                          page=previous_page)),

            InlineKeyboardButton(
                text=current_page_text,
                callback_data=menu_cd.new(item_id=id_item,
                                          level=CURRENT_LEVEL,
                                          category=category,
                                          subcategory=subcategory,
                                          buy=key,
                                          quantity='None',
                                          id='None',
                                          page='current_page')),
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=menu_cd.new(item_id=id_item,
                                          level=CURRENT_LEVEL,
                                          category=category,
                                          subcategory=subcategory,
                                          buy=key,
                                          quantity='None',
                                          id='None',
                                          page=next_page))
        )
    markup.row(
        InlineKeyboardButton(text="Назад",
                             callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                              category=category,
                                                              subcategory=subcategory)
                             ),
        InlineKeyboardButton(text=f'🛍 {total_amount} руб',
                             callback_data=menu_cd.new(item_id='None',
                                                       level=CURRENT_LEVEL,
                                                       category=category,
                                                       subcategory=subcategory,
                                                       buy='None',
                                                       quantity='None',
                                                       id='page_',
                                                       page=page)),

        InlineKeyboardButton(text="💥 В корзину", callback_data=menu_cd.new(item_id=id_item,
                                                                            level=CURRENT_LEVEL,
                                                                            category=category,
                                                                            subcategory=subcategory,
                                                                            buy='buy',
                                                                            quantity='None',
                                                                            id='None',
                                                                            page=page))
    )

    return markup


async def categories_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=1)
    categories = await get_categories()
    for category in categories:
        number_of_items = await count_items(category.category_code)  # функция подсчета товаров в категории
        button_text = f"{category.category_name} ({number_of_items} шт)"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category.category_code)
        markup.add(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    return markup


async def subcategory_keyboard(category):
    global button_text
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)

    subcategories = await get_subcategories(category)  # получаем подкатегории для нашей категории

    for subcategory in subcategories:
        temp=False
        number_of_items = await count_items(category_code=category, subcategory_code=subcategory.subcategory_code)
        #print(subcategory.id)
        items = await get_items(category_code=category, subcategory_code=subcategory.subcategory_code)
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category,
                                           subcategory=subcategory.subcategory_code)
        for item in items:
            if await check_sale(item.id):

                temp=True

        if temp:
            button_text = f"🔥 {subcategory.subcategory_name} ({number_of_items}шт)"
        else:
            button_text = f"{subcategory.subcategory_name} ({number_of_items}шт)"

        markup.insert(
                InlineKeyboardButton(text=button_text, callback_data=callback_data)
            )

    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1)
        )
    )
    return markup


async def items_keyboard(category, subcategory):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=1)

    items = await get_items(category, subcategory)

    for item in items:
        if await check_sale(item.id):
            button_text = f"🔥 {item.name}- ₽ {item.price-item.sale} "
        else:
            button_text = f"{item.name}- ₽ {item.price}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category, subcategory=subcategory,
                                           item_id=item.id)
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             category=category)
        )
    )
    return markup


async def pay_kb():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(text="▶ Продолжить", callback_data=user_cb.new(id_user="None",
                                                                            my_size='None',
                                                                            my_orders='None',
                                                                            menu='None',
                                                                            comment='None',
                                                                            id_order="None",
                                                                            buy='buynew',
                                                                            id_item='None'
                                                                            )),
    )
    markup.row(
        InlineKeyboardButton(text="🔄 Изменить размеры", callback_data=user_cb.new(id_user="None",
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


async def order_comment():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton('💵 Оплата', pay=True))
    markup.add(InlineKeyboardButton(text='📝 Добавить комментарий к заказу',
                                    callback_data=user_cb.new(id_user="None",
                                                              my_size='None',
                                                              my_orders='None',
                                                              menu='None',
                                                              comment='newcomment',
                                                              id_order='None',
                                                              buy='None',
                                                              id_item='None'
                                                              )
                                    )
               )

    return markup


async def bonus_kb():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton('Да', callback_data='bonus_yes'))
    markup.add(InlineKeyboardButton(text='Нет',
                                    callback_data="bonus_no"
                                    )
               )

    return markup
