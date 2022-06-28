import logging

from aiogram import Dispatcher
from data.config import SUPER_ADMIN


async def on_startup_notify(dp: Dispatcher):

    try:
        text = "Бот запущен"
        await dp.bot.send_message(chat_id=SUPER_ADMIN, text=text)
    except Exception as err:
        logging.exception(err)
