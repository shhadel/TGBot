from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from datetime import datetime

from lexicon.lexicon import LEXICON
from database.birthday_db import birthdays
from keyboards.friends_kb import create_friends_keyboard

router = Router()
pending_edit = {}


@router.message(Command("edit_birthday"))
async def process_edit_command(message: Message):
    user_data = birthdays.get(message.from_user.id, {})
    if not user_data:
        await message.answer(LEXICON['no_birthdays'])
        return
    await message.answer(
        LEXICON['prompt_edit'],
        reply_markup=create_friends_keyboard(list(user_data.keys()), 'edit')
    )


@router.callback_query(lambda c: c.data.startswith('edit:'))
async def process_edit_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    friend_name = callback.data.split(':')[1]
    if friend_name in birthdays.get(user_id, {}):
        pending_edit[user_id] = friend_name
        await callback.message.answer(LEXICON['edit_date'].format(name=friend_name))
    await callback.answer()


@router.message(lambda message: message.from_user.id in pending_edit)
async def process_new_date(message: Message):
    user_id = message.from_user.id
    try:
        datetime.strptime(message.text, "%d.%m")
    except ValueError:
        await message.answer(LEXICON['invalid_date'])
        return

    friend_name = pending_edit.pop(user_id)
    birthdays[user_id][friend_name] = message.text
    await message.answer(
        LEXICON['birthday_updated'].format(name=friend_name, date=message.text)
    )