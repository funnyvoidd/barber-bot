import asyncio
from aiogram import Bot, Dispatcher
from config.settings import BOT_TOKEN
from db import init_db
from bot.client import router as client_router
from bot.admin.router import admin_router

async def main():
    await init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(client_router)
    dp.include_router(admin_router)

    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())