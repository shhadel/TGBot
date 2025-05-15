from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_friends_keyboard(names: list[str], action: str):
    """
    Создает inline-клавиатуру со списком друзей
    :param names: список имен друзей
    :param action: префикс для callback_data ("edit" или "delete")
    :return: объект InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()

    for name in names:
        builder.button(text=name, callback_data=f"{action}:{name}")

    builder.adjust(1)  # Каждая кнопка в отдельной строке
    return builder.as_markup()