from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config_data.config import load_config
from filters.is_admin import IsAdmin
from database.birthday_db import birthdays

router = Router()
admin_id = load_config().tg_bot.admin_id

@router.message(Command("admin"), IsAdmin(admin_id=admin_id))
async def process_admin_command(message: Message):
    total_users = len(birthdays)
    total_records = sum(len(b) for b in birthdays.values())
    await message.answer(
        f"📊 Статистика бота:\n"
        f"👤 Пользователей: {total_users}\n"
        f"🎂 Записей: {total_records}"
    )