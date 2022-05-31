from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


from utils.db_api.db_commands import count_items, get_categories, get_subcategories, get_items

menu_cd = CallbackData("show_menu1", "level", "category", "subcategory", "item_id")
buy_item = CallbackData("states", "item_id", 'buy')


def make_callback_data(level, category="0", subcategory="0", item_id="0"):
    return menu_cd.new(level=level, category=category, subcategory=subcategory, item_id=item_id)


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
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)

    subcategories = await get_subcategories(category)  # получаем подкатегории для нашей категории
    for subcategory in subcategories:
        number_of_items = await count_items(category_code=category, subcategory_code=subcategory.subcategory_code)

        button_text = f"{subcategory.subcategory_name}({number_of_items}шт)"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category,
                                           subcategory=subcategory.subcategory_code)

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
        button_text = f"{item.name}- ₽{item.price}"
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


async def pay_kb(item_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(text="▶ Продолжить", callback_data=buy_item.new(item_id=item_id, buy='buynew'))
    )
    markup.row(
        InlineKeyboardButton(text="🔄 Изменить размеры", callback_data='pass')
    )
    markup.row(
        InlineKeyboardButton(text="◀ Назад", callback_data='pass')
    )
    return markup


async def item_keyboard(category, subcategory, item_id):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup(row_width=1)

    markup.row(
        InlineKeyboardButton(text="Оформить", callback_data=buy_item.new(item_id=item_id, buy='None'))
    )

    markup.row(
        InlineKeyboardButton(text="Назад",
                             callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                              category=category,
                                                              subcategory=subcategory)
                             )

    )

    return markup
