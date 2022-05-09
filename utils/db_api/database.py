import asyncio


from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import sql

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

    def __repr__(self):
        return f"""
Наименование {self.name}

Описание: {self.decription}
Цена: {self.price}
"""


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
    email = db.Column(db.String(50))

    def __repr__(self):
        return f"""
Обхват груди: {self.size_Vg}
Обхват под грудью: {self.size_Vpg}
Обхват бедер: {self.size_Vb}
Обхват талии: {self.size_Vt}
Размер груди: {self.sizeL}
Email: {self.email}
"""


async def create_db1():
    await db.set_bind(POSTGRES_URI)
    db.gino: GinoSchemaVisitor
    await db.gino.create_all()


asyncio.get_event_loop().run_until_complete(create_db1())