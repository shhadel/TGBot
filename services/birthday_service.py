from datetime import datetime
from typing import Dict, List, Tuple

def register_user(data: Dict[int, Dict[str, str]], user_id: int) -> None:
    """Регистрирует пользователя в системе"""
    if user_id not in data:
        data[user_id] = {}

def get_today_birthdays(user_data: Dict[str, str]) -> List[str]:
    """Возвращает список имен с днем рождения сегодня"""
    today = datetime.now().strftime("%d.%m")
    return [name for name, date in user_data.items() if date == today]

def get_stats(data: Dict[int, Dict[str, str]]) -> Tuple[int, int]:
    """Возвращает статистику по пользователям и записям"""
    total_users = len(data)
    total_birthdays = sum(len(bdays) for bdays in data.values())
    return total_users, total_birthdays