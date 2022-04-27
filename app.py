from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    import filters
    filters.setup(dp)

    import middlewares
    middlewares.setup(dp)

    await set_default_commands(dp)

    from loader import db
    from utils.db_api.db_gino import on_startup
    print('Подключение к PSG')
    await on_startup(dp)

    print('Удаление БД')
    await db.gino.drop_all()

    print('Cоздание БД')
    await db.gino.create_all()
    print('Готово')



    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)

    print('Бот запущен!')


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
