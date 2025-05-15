from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lexicon.lexicon import LEXICON

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=LEXICON['btn_add'])],
        [KeyboardButton(text=LEXICON['btn_show']),
         KeyboardButton(text=LEXICON['btn_today'])]
    ],
    resize_keyboard=True
)