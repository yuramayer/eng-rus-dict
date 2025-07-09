"""Creates menu keyboard"""

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


find_button = 'Найти слово в словаре'
add_button = 'Добавить новое слово'

kb_buttons = [find_button, add_button]


def menu_kb() -> ReplyKeyboardMarkup:
    """Return the keyboard with menu buttons"""
    kb = ReplyKeyboardBuilder()
    for btn in kb_buttons:
        kb.button(text=btn)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
