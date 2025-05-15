from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from lexicon.lexicon import LEXICON
from database.birthday_db import birthdays
from database.birthday_db import calculate_age

router = Router()

@router.message(Command("show_birthdays"))
@router.message(F.text == LEXICON['btn_show'])
async def process_show_command(message: Message):
    user_data = birthdays.get(message.from_user.id, {})
    if not user_data:
        await message.answer(LEXICON['no_birthdays'])
    else:
        lines = [LEXICON['show_list']]
        for name, date in user_data.items():
            age = calculate_age(date)
            lines.append(LEXICON['birthday_entry'].format(
                name=name,
                date=date,
                age=age
            ))
        await message.answer("\n".join(lines))