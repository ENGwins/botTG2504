import asyncio

from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import sql, TIMESTAMP, JSON

from data.config import POSTGRES_URI

db = Gino()


class Item(db.Model):
    __tablename__ = 'catalog2'
    query: sql.Select

    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    category_code = db.Column(db.String(20))
    #  img = db.Column(db.String(250))

    category_name = db.Column(db.String(50))

    subcategory_code = db.Column(db.String(20))

    subcategory_name = db.Column(db.String(50))

    name = db.Column(db.String(50))
    photo = db.Column(db.String(250))
    price = db.Column(db.Integer)
    decription = db.Column(db.String)
    photo2= db.Column(db.String(250))
    photo3 = db.Column(db.String(250))
    photo4 = db.Column(db.String(250))
    state = db.Column(db.String(250))


class Size_users(db.Model):
    __tablename__ = 'Size_users'
    query: sql.Select

    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    id_user = db.Column(db.Integer)

    size_Vg = db.Column(db.String(50))

    size_Vpg = db.Column(db.String(50))

    size_Vt = db.Column(db.String(50))
    size_Vb = db.Column(db.String(50))
    sizeL = db.Column(db.String(50))
    referral = db.Column(db.Integer)

    def __repr__(self):
        return f"""
Обхват груди: {self.size_Vg}
Обхват под грудью: {self.size_Vpg}
Обхват талии: {self.size_Vt}
Обхват бедер: {self.size_Vb}
Размер лифа: {self.sizeL}
"""


class Purchase(db.Model):
    __tablename__ = 'purchases'
    query: sql.Select
    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    name = db.Column(db.String(20))  # имя
    number = db.Column(db.String(20))
    name_item = db.Column(db.String(100))  # наименование товара
    buyer = db.Column(db.BigInteger)  # id покупателя
    item_id = db.Column(db.Integer)
    amount = db.Column(db.Integer)  # сумма покупки
    quantity = db.Column(db.Integer)  # количество товаров покупки
    # purchase_time = db.Column(TIMESTAMP)  # время покупки
    purchase_time = db.Column(db.String(50))
    shipping_adress = db.Column(JSON)  # адрес
    successful = db.Column(db.Boolean, default=False)  # cтатус покупки
    state = db.Column(db.String(200))  # Статус заказа
    tracking = db.Column(db.String(20), default='-')  # Трек номер
    comment = db.Column(db.String(200), default='')  # Комментарий
    finish_state = db.Column(db.Boolean, default=False)  # готов
    gift = db.Column(db.String(100), default='')  # подарок из фортуны

    # def __repr__(self):
    def __repr__(self):
        id_new = self.id
        return str(id_new)


"""
Номер заказа: {self.id}
Номер телефона: {self.number}
Имя заказчика: {self.name}

Товар: {self.name_item}

Время заказа: {self.purchase_time}

Статус заказа: {self.state}

Комментарий: {self.comment}
Трек: {self.tracking}

"""


class Admin(db.Model):
    __tablename__ = 'forAdmin'
    query: sql.Select
    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    user_id = db.Column(db.BigInteger)  # id покупателя
    user_first_name = db.Column(db.String(50))
    user_last_name = db.Column(db.String(50))
    referral = db.Column(db.String(50), default=0)
    balans = db.Column(db.Integer, default=0)
   # basket = db.Column(JSON)

    def __repr__(self):
        return f"""
ID: {self.user_id}
Имя: {self.user_first_name}
Фамилия: {self.user_last_name}
Баланс: {self.balans}
"""


class Basket(db.Model):
    __tablename__ = 'Basket'
    query: sql.Select
    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    user_id=db.Column(db.BigInteger)
    item_id=db.Column(db.BigInteger)
    quantity=db.Column(db.BigInteger)
    amount=db.Column(db.BigInteger)



async def create_db1():
    await db.set_bind(POSTGRES_URI)
    db.gino: GinoSchemaVisitor
    await db.gino.create_all()


asyncio.get_event_loop().run_until_complete(create_db1())
