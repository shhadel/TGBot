from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение\n'
        'Доступные команды:\n'
        '/caps <текст> - переводит текст в верхний регистр\n'
        '/reverse <текст> - переворачивает текст'
    )

# Команда /caps
@dp.message(Command(commands=['caps']))
async def process_caps_command(message: Message):
    text = message.text[5:].strip()
    if text:
        await message.reply(text.upper())
    else:
        await message.reply("Пожалуйста, укажите текст после команды /caps")

# Команда /reverse
@dp.message(Command(commands=['reverse']))
async def process_reverse_command(message: Message):
    text = message.text[8:].strip()
    if text:
        await message.reply(text[::-1])
    else:
        await message.reply("Пожалуйста, укажите текст после команды /reverse")

# Фильтр приветствий
@dp.message(F.text.lower().in_(["привет", "здравствуйте", "здравствуй", "добрый день", "доброе утро", "добрый вечер"]))
async def send_hello(message: Message):
    await message.reply("Приветствую тебя, дружище!")

# Фильтр приветствий
@dp.message(F.text.lower().in_(["пока", "до свидания", "до связи"]))
async def send_hello(message: Message):
    await message.reply("Всего хорошего, дружище!")


# Фильтр вопросов
@dp.message(F.text.contains('?'))
async def send_question(message: Message):
    await message.reply("Хороший вопрос! Но я просто эхо-бот...")

@dp.message(F.photo)
async def send_photo(message: Message):
    if message.caption is not None:
        await message.reply(text=f' Что это за {message.caption}')
    else:
        await message.reply("Данный формат пока не поддерживается")

@dp.message(F.document)
async def send_document(message: Message):
    if message.caption is not None:
        await message.reply(text=f' Что это за {message.caption}')
    else:
        await message.reply("Данный формат пока не поддерживается")

@dp.message(F.sticker)
async def send_sticker(message: Message):
    await message.reply_sticker(message.sticker.file_id)

@dp.message(F.text)
async def send_echo(message: Message):
    if message.text is not None:
        await message.reply(text=message.text)
    else:
        await message.reply("Текст не обнаружен")

if __name__ == '__main__':
    dp.run_polling(bot)
