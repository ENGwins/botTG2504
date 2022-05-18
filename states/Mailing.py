from aiogram.dispatcher.filters.state import StatesGroup, State


class MailingService(StatesGroup):
    text= State()
    state= State()
    photo=State()
