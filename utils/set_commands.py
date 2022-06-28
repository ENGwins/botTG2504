from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', '🔃Перезапуск бота'), # пока добавляем только одну команду
            types.BotCommand('help','ℹ Помощь')
        ]
    )