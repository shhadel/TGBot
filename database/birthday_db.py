from services.storage_json import load_birthdays
from datetime import datetime
# database/birthday_db.py
# Глобальный словарь для хранения дней рождения.
# Формат: { user_id: { friend_name: "DD.MM", ... }, ... }
birthdays: dict[int, dict[str, str]] = load_birthdays()

def calculate_age(birth_date: str) -> int:
    """Вычисляет возраст по дате рождения в формате DD.MM.YYYY"""
    day, month, year = map(int, birth_date.split('.'))
    today = datetime.now()
    age = today.year - year
    if (today.month, today.day) < (month, day):
        age -= 1
    return age

def get_user_birthdays(user_id: int) -> dict[str, str]:
    """Возвращает словарь дней рождения для пользователя"""
    return birthdays.get(user_id, {})

def add_birthday(user_id: int, name: str, date: str) -> None:
    """Добавляет день рождения для пользователя"""
    if user_id not in birthdays:
        birthdays[user_id] = {}
    birthdays[user_id][name] = date

def delete_birthday(user_id: int, name: str) -> None:
    """Удаляет день рождения для пользователя"""
    if user_id in birthdays and name in birthdays[user_id]:
        del birthdays[user_id][name]

reminders_enabled = {}

def enable_reminders(user_id: int):
    reminders_enabled[user_id] = True

def disable_reminders(user_id: int):
    reminders_enabled[user_id] = False

def is_reminders_enabled(user_id: int) -> bool:
    return reminders_enabled.get(user_id, True)  # По умолчанию включено