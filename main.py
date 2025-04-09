from aiogram import Dispatcher
import asyncio

import logging

from core.init_bot import bot
from components.handlers.user_handlers import router as user_router
from database.init_database import init_db


logging.basicConfig(level=logging.INFO)


async def main():
    dp = Dispatcher()
    dp.include_router(user_router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(init_db())
        asyncio.run(main())
    except:
        pass
