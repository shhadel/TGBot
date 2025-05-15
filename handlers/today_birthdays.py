from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from lexicon.lexicon import LEXICON
from database.birthday_db import birthdays
from services.birthday_service import get_today_birthdays
from database.birthday_db import calculate_age
from datetime import datetime

router = Router()

@router.message(Command("today_birthdays"))
@router.message(F.text == LEXICON['btn_today'])
async def process_today_command(message: Message):
    user_data = birthdays.get(message.from_user.id, {})
    if not user_data:
        await message.answer(LEXICON['no_birthdays'])
    else:
        today = datetime.now().strftime("%d.%m")
        today_birthdays = []
        for name, date in user_data.items():
            if date.endswith(today):  # Сравниваем только день и месяц
                birth_year = int(date.split('.')[2])
                age = datetime.now().year - birth_year
                today_birthdays.append(
                    f"{name} - {date} ({age} лет)"
                )

        if not today_birthdays:
            await message.answer(LEXICON['no_today'])
        else:
            await message.answer(
                f"{LEXICON['today_list']}\n" + "\n".join(today_birthdays)
            )