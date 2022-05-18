from aiogram import Dispatcher

from .anti_flood import ThrottlingMiddleware
from loader import dp
# from .is_admin import AdminFilter


def setup(dp:Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())

