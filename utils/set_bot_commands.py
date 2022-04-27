from aiogram import types

async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand(command='/start',description='Запуск бота'),
        types.BotCommand(command='/help', description='Помощь'),
        types.BotCommand(command='/register',description='Регистрация'),
        types.BotCommand(command='/profile', description='Получить данные БД')
    ])