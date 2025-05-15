import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config_data.config import load_config
from services.storage_json import save_birthdays
from database.birthday_db import birthdays
from handlers.reminders import router as reminders_router
from handlers.reminders import setup_scheduler
from handlers import (
    start_help,
    add_birthday,
    show_birthdays,
    today_birthdays,
    edit_birthday,
    delete_birthday,
    admin
)

async def main():
    # Загрузка конфигурации
    config = load_config()

    # Инициализация бота и диспетчера
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация роутеров
    dp.include_router(start_help.router)
    dp.include_router(add_birthday.router)
    dp.include_router(show_birthdays.router)
    dp.include_router(today_birthdays.router)
    dp.include_router(edit_birthday.router)
    dp.include_router(delete_birthday.router)
    dp.include_router(admin.router)
    dp.include_router(reminders_router)

    setup_scheduler(bot)

    try:
        await dp.start_polling(bot)
    finally:
        save_birthdays(birthdays)

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())