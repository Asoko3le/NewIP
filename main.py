import asyncio

from aiogram import Bot, Dispatcher, types, F

from app.handlers import router



async def main():
    bot = Bot(token='7590317034:AAFmD3C2fLxlyq9WeMUgKd6Vuy7F3YHSoJw')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')

