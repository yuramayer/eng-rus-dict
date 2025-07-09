"""Creates yes/no keyboard"""

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

kb_buttons = ['Нет', 'Да']


def approve_kb() -> ReplyKeyboardMarkup:
    """Return the keyboard with buttons: yes / no"""
    kb = ReplyKeyboardBuilder()
    for btn in kb_buttons:
        kb.button(text=btn)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
