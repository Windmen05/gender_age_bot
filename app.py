#import cv2
#raise IOError(cv2.__version__)
async def on_startup(dp):
    import filters
    import middlewares
    import asyncio
    from data.config import admin_id
    from loader import bot, create_db
    filters.setup(dp)
    middlewares.setup(dp)
    await asyncio.sleep(10)
    await create_db()
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)


async def on_shutdown():
    from loader import bot
    bot.close()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)
