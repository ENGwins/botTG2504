
from typing import List

from sqlalchemy import and_, or_
from utils.db_api.database import Item, db, Size_users, Admin, Purchase, Basket


async def add_item(**kwargs):
    newitem = await Item(**kwargs).create()
    return newitem


async def add_size(**kwargs):
    newsize = await Size_users(**kwargs).create()
    return newsize


async def show_size_user(user_id):
    all_size = await Size_users.query.where(Size_users.id_user == user_id).gino.all()
    return all_size[0]


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
async def new_user(referral, **kwargs):
    if referral != 0:
        await Admin(referral=referral, **kwargs).create()
    else:
        await Admin(**kwargs).create()
    return


async def check_user(user_id):  # смотрим есть ли зайпись данных по Айди клиента
    check = await db.scalar(db.exists(Admin.query.where(Admin.user_id == user_id)).select())
    return check


async def user_all_check():
    users = await Admin.select("user_id").gino.all()
    return users


async def check_referral(referral_id):
    # count_ref = await db.func.count(Admin.referral == referral_id).gino.scalar()
    count_ref = await db.select([db.func.count()]).where(
        Admin.referral == referral_id
    ).gino.scalar()
    return count_ref


async def check_referral_order(user_id):
    ref = await Admin.select("referral").where(Admin.user_id == user_id).gino.scalar()
    return ref


# Purchase________________________________________________________________

async def new_order(**kwargs):
    await Purchase(**kwargs).create()
    return


async def search_order(id_order):
    orders = await Purchase.query.where(Purchase.id == id_order).gino.first()
    return orders


async def search_order_id():
    id_order = await Purchase.select('id').where(
        and_(Purchase.finish_state == False, Purchase.successful == True)).gino.all()
    return id_order


async def update_state(id_order, state_order):
    order = await Purchase.query.where(Purchase.id == id_order).gino.first()
    await order.update(state=state_order).apply()
    return


async def update_tracking(id_order, tracking):
    order = await Purchase.query.where(Purchase.id == id_order).gino.first()
    await order.update(tracking=tracking).apply()
    return


async def update_fin_state(id_order, finish_state):
    order = await Purchase.query.where(Purchase.id == id_order).gino.first()
    await order.update(finish_state=finish_state).apply()
    return


async def count_work_order():
    temp = await Purchase.query.where(and_(Purchase.finish_state == False, Purchase.successful == True)).gino.all()
    count = len(temp)
    return count


async def show_my_orders(id_user):
    orders = await Purchase.query.where(Purchase.buyer == id_user).where(Purchase.successful == True).gino.all()
    return orders


async def my_balans(id_user):
    balans = await Admin.select('balans').where(Admin.user_id == id_user).gino.scalar()
    return balans


async def update_my_balans(id_user, new_balans):
    balans = await Admin.query.where(Admin.user_id == id_user).gino.first()
    await balans.update(balans=new_balans).apply()
    return


async def add_my_comment(id_order, comment):
    order = await Purchase.query.where(Purchase.id == id_order).gino.first()
    await order.update(comment=comment).apply()
    return


async def update_order_pay(id_order, number, amount, shipping_adress, successful, purchase_time, state):
    order = await Purchase.query.where(Purchase.id == id_order).gino.first()
    await order.update(number=number, amount=amount, shipping_adress=shipping_adress,
                       successful=successful, purchase_time=purchase_time, state=state).apply()
    return


async def search_info_order(order_id):
    info_order = {}
    info_order["item_id"] = await Purchase.select('item_id').where(Purchase.id == order_id).gino.first()
    return info_order["item_id"]


async def total_amounts(id_user):  # сумма покупок пользователя
    total_amounts = await Purchase.select('amount').where(Purchase.buyer == id_user).gino.all()
    total = 0
    for i in total_amounts:
        total += i[0]
    return total


"""async def search_json(id_order):
    json_str = await Purchase.select('shipping_adress').where(Purchase.id == id_order)

    #json_encoder=json.dumps(json_str.__dict__)
    return json_str
"""
async def search_com_qua_order(id_order):
    item = await Purchase.select('name_item').where(Purchase.id == id_order).gino.scalar()
    com = await Purchase.select('comment').where(Purchase.id == id_order).gino.scalar()
    name = await Purchase.select('name').where(Purchase.id == id_order).gino.scalar()
    number = await Purchase.select('number').where(Purchase.id == id_order).gino.scalar()
    state = await Purchase.select('state').where(Purchase.id == id_order).gino.scalar()
    tracking = await Purchase.select('tracking').where(Purchase.id == id_order).gino.scalar()
    qua = await Purchase.select('quantity').where(Purchase.id == id_order).gino.scalar()
    return item,name,number,state,tracking,com,qua



"""
       =============== basket =========================
"""


async def total_amount_basket(user_id):  # cумма в корзине
    totalo = []
    total = 0
    id_all = await Basket.select('id').where(
        Basket.user_id == user_id).gino.all()
    for id in id_all:
        quantity = await Basket.select('quantity').where(
            and_(Basket.id == int(id[0]), Basket.user_id == user_id)).gino.scalar()
        amount = await Basket.select('amount').where(
            and_(Basket.id == int(id[0]), Basket.user_id == user_id)).gino.scalar()
        sum = int(quantity) * int(amount)
        totalo.append(sum)
    for i in totalo:
        total += i
    return total


async def add_item_basket(user_id, item_id, amount, **kwargs):
    newitem = await Basket(user_id=user_id, item_id=item_id, amount=amount, **kwargs).create()
    return newitem


async def chek_basket(user_id, item_id):
    check = await db.scalar(
        db.exists(Basket.query.where(and_(Basket.user_id == user_id, Basket.item_id == item_id))).select())
    return check


async def update_quantity(user_id, item_id, quantity):
    old_quantity = await Basket.select('quantity').where(
        and_(Basket.user_id == user_id, Basket.item_id == item_id)).gino.scalar()
    old_q = int(old_quantity) + int(quantity)

    if old_q < 1:
        dell = await Basket.query.where(and_(Basket.user_id == user_id, Basket.item_id == item_id)).gino.first()
        await dell.delete()
    else:
        new_quantity = await Basket.query.where(and_(Basket.user_id == user_id, Basket.item_id == item_id)).gino.first()
        await new_quantity.update(quantity=old_q).apply()
    return


async def count_item_basket(user_id, item_id):
    temp = await Basket.select('quantity').where(
        and_(Basket.user_id == user_id, Basket.item_id == item_id)).gino.scalar()
    count = temp
    return count


async def show_basket(user_id):
    id_item_id = []
    id_all = await Basket.select('id').where(
        Basket.user_id == user_id).gino.all()
    item_id = await Basket.select('item_id').where(
        Basket.user_id == user_id).gino.all()
    id_item_id.append(id_all)
    id_item_id.append(item_id)
    return id_item_id


async def count_basket(user_id):
    all = await Basket.select('id').where(
        Basket.user_id == user_id).gino.all()
    return all


async def delete_basket(user_id):
    dell = await Basket.query.where(Basket.user_id == user_id).gino.all()
    for i in dell:
        await i.delete()


"""    for id in id_all:
        quantity = await Basket.select('quantity').where(
            and_(Basket.id == int(id[0]), Basket.user_id == user_id)).gino.scalar()
        amount = await Basket.select('amount').where(
            and_(Basket.id == int(id[0]), Basket.user_id == user_id)).gino.scalar()
    return f'Количество: {quantity}\n Цена: {amount}'"""


async def chek_photos(item_id):
    photo = await Item.select("photo").where(Item.id == item_id).gino.scalar()
    photo2 = await Item.select("photo2").where(Item.id == item_id).gino.scalar()
    photo3 = await Item.select("photo3").where(Item.id == item_id).gino.scalar()
    photo4 = await Item.select("photo4").where(Item.id == item_id).gino.scalar()
    photo = [photo, photo2, photo3, photo4]
    photo_id_all = []
    for id in photo:
        if id != '0':
            photo_id_all.append(id)
    return photo_id_all
