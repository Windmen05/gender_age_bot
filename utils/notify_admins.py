import logging

from aiogram import Dispatcher

from data.config import admin_id


async def on_startup_notify(dp: Dispatcher):
    for admin in admin_id:
        try:
            await dp.bot.send_message(admin, "Bot started")

        except Exception as err:
            logging.exception(err)
