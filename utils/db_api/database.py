import asyncio

from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import sql, TIMESTAMP, JSON

from data.config import POSTGRES_URI

db = Gino()


class Item(db.Model):
    __tablename__ = 'catalog2_local'
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


class Size_users(db.Model):
    __tablename__ = 'Size_users_local'
    query: sql.Select

    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    id_user = db.Column(db.Integer)

    size_Vg = db.Column(db.String(50))

    size_Vpg = db.Column(db.String(50))

    size_Vt = db.Column(db.String(50))
    size_Vb = db.Column(db.String(50))
    sizeL = db.Column(db.String(50))
    email = db.Column(db.String(50))
    referral = db.Column(db.Integer)

    def __repr__(self):
        return f"""
Обхват груди: {self.size_Vg}
Обхват под грудью: {self.size_Vpg}
Обхват талии: {self.size_Vt}
Обхват бедер: {self.size_Vb}
Размер лифа: {self.sizeL}
Email: {self.email}
"""


class Purchase(db.Model):
    __tablename__ = 'purchases_local'
    query: sql.Select
    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    buyer = db.Column(db.BigInteger)  # id покупателя
    item_id = db.Column(db.Integer)
    amount = db.Column(db.Integer)  # сумма покупки
    quantity = db.Column(db.Integer)  # количество товаров покупки
    purchase_time = db.Column(TIMESTAMP)  # время покупки
    shipping_adress = db.Column(JSON)  # адрес
    phone_number = db.Column(db.String(50))
    successful = db.Column(db.Boolean, default=False)  # cтатус покупки


class Admin(db.Model):
    __tablename__ = 'forAdmin_local'
    query: sql.Select
    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    user_id = db.Column(db.BigInteger)  # id покупателя
    user_first_name = db.Column(db.String(50))
    user_last_name = db.Column(db.String(50))

    def __repr__(self):
        return f"""
ID: {self.user_id}
Имя: {self.user_first_name}
Фамилия: {self.user_last_name}

"""


async def create_db1():
    await db.set_bind(POSTGRES_URI)
    db.gino: GinoSchemaVisitor
    await db.gino.create_all()


asyncio.get_event_loop().run_until_complete(create_db1())
