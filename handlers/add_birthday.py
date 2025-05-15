from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
from database.birthday_db import calculate_age

from lexicon.lexicon import LEXICON
from database.birthday_db import birthdays

router = Router()


class AddBirthdayState(StatesGroup):
    name = State()
    date = State()


@router.message(Command("add_birthday"))
@router.message(F.text == LEXICON['btn_add'])
async def process_add_command(message: Message, state: FSMContext):
    await state.set_state(AddBirthdayState.name)
    await message.answer(LEXICON['add_name'])


@router.message(AddBirthdayState.name)
async def process_name_step(message: Message, state: FSMContext):
    name = message.text.strip()
    if not name:
        await message.answer(LEXICON['add_name'])
        return
    if name in birthdays.get(message.from_user.id, {}):
        await message.answer(LEXICON['name_exists'])
        return
    await state.update_data(name=name)
    await state.set_state(AddBirthdayState.date)
    await message.answer(LEXICON['add_date'])


@router.message(AddBirthdayState.date)
async def process_date_step(message: Message, state: FSMContext):
    date_text = message.text.strip()
    try:
        # Проверяем полный формат даты
        datetime.strptime(date_text, "%d.%m.%Y")
    except ValueError:
        await message.answer(LEXICON['invalid_date'])
        return

    data = await state.get_data()
    friend_name = data["name"]
    birthdays[message.from_user.id][friend_name] = date_text
    await state.clear()

    # Вычисляем возраст для подтверждающего сообщения
    age = calculate_age(date_text)
    await message.answer(
        f"{LEXICON['birthday_added'].format(name=friend_name, date=date_text)}\n"
        f"На сегодняшний день: {age} лет"
    )