from typing import List

from sqlalchemy import and_

from utils.db_api.database import Item, db, Size_users


async def add_item(**kwargs):
    newitem = await Item(**kwargs).create()
    return newitem


async def add_size(**kwargs):
    newsize = await Size_users(**kwargs).create()
    return newsize


async def show_size_user(user_id) -> Size_users:
    all_size=await Size_users.query.where(Size_users.id_user == user_id).gino.all()
    return all_size


# Получение категорий
async def get_categories() -> List[Item]:
    return await Item.query.distinct(Item.category_code).gino.all()


# Получение подкатегорий
async def get_subcategories(category) -> List[Item]:
    return await Item.query.distinct(Item.subcategory_code).where(Item.category_code == category).gino.all()


# Подсчет количества товаров в категории
async def count_items(category_code, subcategory_code=None):
    conditions = [Item.category_code == category_code]

    if subcategory_code:
        conditions.append(Item.subcategory_code == subcategory_code)
    total = await db.select([db.func.count()]).where(
        and_(*conditions)
    ).gino.scalar()
    return total


async def get_items(category_code, subcategory_code) -> List[Item]:
    items = await Item.query.where(
        and_(Item.category_code == category_code,
             Item.subcategory_code == subcategory_code)
    ).gino.all()
    #    print(items)
    return items


async def get_item(item_id) -> Item:
    item = await Item.query.where(Item.id == item_id).gino.first()
    return item
