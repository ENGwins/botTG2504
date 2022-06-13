
from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMClient(StatesGroup):
    Vg = State()
    Vpg = State()
    Vt = State()
    Vb = State()
    sizeL = State()
 #   email = State()
    check_size = State()


class FSMpersonal(StatesGroup):
    one=State()

