from datetime import datetime, timedelta
from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from lexicon.lexicon import LEXICON
from database.birthday_db import birthdays, is_reminders_enabled, calculate_age, disable_reminders, enable_reminders

scheduler = None
router = Router()


def is_birthday_soon(birth_date: str, days: int) -> bool:
    """Проверяет, наступит ли день рождения в течение указанных дней"""
    try:
        day, month, year = map(int, birth_date.split('.'))
        today = datetime.now()
        next_date = datetime(today.year, month, day)

        # Если день рождения уже прошел в этом году, смотрим на следующий год
        if next_date < today:
            next_date = datetime(today.year + 1, month, day)

        return (next_date - today).days <= days
    except (ValueError, IndexError):
        return False


async def send_reminders(bot: Bot):
    """Отправка напоминаний пользователям"""
    for user_id, friends in birthdays.items():
        if is_reminders_enabled(user_id):
            for name, date in friends.items():
                if is_birthday_soon(date, days=3):
                    age = calculate_age(date)
                    await bot.send_message(
                        user_id,
                        f"🔔 Напоминание: через 3 дня день рождения у {name}!\n"
                        f"📅 Дата: {date}\n"
                        f"🎂 Исполняется: {age} лет"
                    )


def setup_scheduler(bot: Bot):
    global scheduler
    if scheduler is None:  # Чтобы не создавать дубликаты
        scheduler = AsyncIOScheduler()
        scheduler.add_job(
            send_reminders,
            'cron',
            hour=9,
            minute=0,
            args=(bot,)
        )
        scheduler.start()


@router.message(Command("start_reminders"))
async def start_reminders(message: Message, bot: Bot):
    """Команда для запуска напоминаний"""
    setup_scheduler(bot)
    await message.answer("🔔 Напоминания активированы! Вы будете получать уведомления за 3 дня до ДР.")

@router.message(Command("stop_reminders"))
async def stop_reminders(message: Message):
    disable_reminders(message.from_user.id)
    await message.answer(
        "🔕 Напоминания отключены\n"
        "Чтобы снова включить, используйте /start_reminders"
    )
