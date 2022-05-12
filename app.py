from aiogram import executor

from handlers.users import menu_handlers

from utils.db_api.database import create_db1
from loader import dp
from utils.notify_admins import on_startup_notify

menu_handlers.register_handlers_menu(dp)


async def on_startup(dispatcher):
    await on_startup_notify(dispatcher)
    await set_default_commands(dispatcher)
    await create_db1()

    print('Бот запущен!')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup,skip_updates=True)
#  bot.polling(none_stop=True, interval=0)
