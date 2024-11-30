import asyncio
from aiogram import Bot, Dispatcher

from app.db_setup import db_start
from app.handlers import router
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()



async def on_startup():
    await db_start()
    print("Started up successfully")


async def main():
    try:
        print("Bot is running...")
        dp.include_router(router)
        await on_startup()
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
