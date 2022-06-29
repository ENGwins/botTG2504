from aiogram.dispatcher.filters.state import StatesGroup, State




class admin_bonus(StatesGroup):
    one= State()
    two= State()
    three= State()


class admin_trak(StatesGroup):
    one= State()
    two= State()

class change_catalog(StatesGroup):
    id_item=State()
    active=State()
    sale1=State()
    sale2=State()
