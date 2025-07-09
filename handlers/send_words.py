"""Bot sends best suitable words for the user"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from back.db_back import get_user_dict, user_exists, add_user
from back.gpt_back import find_relevant_words
from back.bot_back import create_words_message
from states import GetWord
from keyboards.menu_keyboard import menu_kb, find_button


send_words_router = Router()


@send_words_router.message(F.text == find_button)
@send_words_router.message(Command('get_word'))
async def get_words(message: Message, state: FSMContext):
    """Bot asks user for the word"""
    await state.clear()
    chat_id = str(message.from_user.id)
    if not user_exists(chat_id):
        add_user(chat_id)
        await message.answer('Словарь готов к работе 💫')
    await message.answer('Какое слово найти?',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(GetWord.get_word)


@send_words_router.message(GetWord.get_word)
async def find_suitable_words(
        message: Message, state: FSMContext):
    """Bot finds words for the user & send it"""
    await state.clear()
    user_word = message.text
    chat_id = message.from_user.id
    user_words = get_user_dict(chat_id)
    if user_words == {}:
        await message.answer('У тебя пока нет слов в базе 🤔',
                             reply_markup=menu_kb())
        await state.clear()
        return
    relevant_words = find_relevant_words(
        user_words, user_word)
    relevant_dict = {key: value for key, value in user_words.items()
                     if key in relevant_words}
    if relevant_dict == {}:
        await message.answer('У тебя в словаре нет подходящих слов 🤷🏼‍♀️',
                             reply_markup=menu_kb())
        await state.clear()
        return

    msg = create_words_message(relevant_dict)

    await message.answer(msg, reply_markup=menu_kb())
