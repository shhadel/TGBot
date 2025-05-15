from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from lexicon.lexicon import LEXICON
from database.birthday_db import birthdays
from keyboards.friends_kb import create_friends_keyboard

router = Router()

@router.message(Command("delete_birthday"))
async def process_delete_command(message: Message):
    user_data = birthdays.get(message.from_user.id, {})
    if not user_data:
        await message.answer(LEXICON['no_birthdays'])
        return
    await message.answer(
        LEXICON['prompt_delete'],
        reply_markup=create_friends_keyboard(list(user_data.keys()), 'delete')
    )

@router.callback_query(lambda c: c.data.startswith('delete:'))
async def process_delete_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    friend_name = callback.data.split(':')[1]
    if friend_name in birthdays.get(user_id, {}):
        del birthdays[user_id][friend_name]
        await callback.message.answer(LEXICON['birthday_deleted'].format(name=friend_name))
    await callback.answer()