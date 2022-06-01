from aiogram import Dispatcher

from .anti_flood import ThrottlingMiddleware
from .private_chat import IsPrivate
from loader import dp
# from .is_admin import AdminFilter


def setup(dp:Dispatcher):
    dp.filters_factory.bind(IsPrivate)
    dp.middleware.setup(ThrottlingMiddleware())

