from typing import List

from sqlalchemy import and_

from utils.db_api.database import Item, db, Size_users, Admin


async def add_item(**kwargs):
    newitem = await Item(**kwargs).create()
    return newitem


async def add_size(**kwargs):
    newsize = await Size_users(**kwargs).create()
    return newsize


async def show_size_user(user_id) -> Size_users:
    all_size = await Size_users.query.where(Size_users.id_user == user_id).gino.all()
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
    item = await Item.select("name").where(Item.id == item_id).gino.scalar()
    return item


async def get_photo(item_id) -> Item:
    item_photo = await Item.select("photo").where(Item.id == item_id).gino.scalar()
    return item_photo


async def get_name_item(item_id) -> Item:
    name_photo = await Item.select("name").where(Item.id == item_id).gino.scalar()
    return name_photo


async def get_price_item(item_id) -> Item:
    price_photo = await Item.select("price").where(Item.id == item_id).gino.scalar()
    return price_photo


async def get_decr_item(item_id) -> Item:
    decr_photo = await Item.select("decription").where(Item.id == item_id).gino.scalar()
    return decr_photo


async def delete_size(user_id):
    size = await Size_users.query.where(Size_users.id_user == user_id).gino.first()
    await size.delete()


async def check_z(user_id):  # смотрим есть ли зайпись данных по Айди клиента
    check = await db.scalar(db.exists(Size_users.query.where(Size_users.id_user == user_id)).select())
    return check


# ADMIN________________________________________________________________
async def new_user(**kwargs):
    newuser = await Admin(**kwargs).create()
    return newuser

async def check_user(user_id):  # смотрим есть ли зайпись данных по Айди клиента
    check = await db.scalar(db.exists(Admin.query.where(Admin.user_id == user_id)).select())
    return check