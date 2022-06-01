from aiogram import executor
from loader import dp
import middlewares, filters, handlers

from utils.db_api.database import create_db1

from utils.notify_admins import on_startup_notify
from utils.set_commands import set_default_commands


async def on_startup(dispatcher):
    filters.setup(dispatcher)
    await on_startup_notify(dispatcher)
    await set_default_commands(dispatcher)
    await create_db1()

    print('Бот запущен!')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
