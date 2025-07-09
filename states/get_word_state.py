"""State for getting the best suitable word"""

# pylint: disable=too-few-public-methods

from aiogram.fsm.state import StatesGroup, State


class GetWord(StatesGroup):
    """New page State: get best suitable word"""
    get_word = State()
