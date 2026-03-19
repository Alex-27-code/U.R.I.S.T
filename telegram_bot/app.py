import asyncio
import logging
from aiogram import Bot, Dispatcher

# Замените на ваш токен
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Здесь будут подключаться routers
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
