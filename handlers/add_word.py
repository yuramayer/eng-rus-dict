"""User adds new word to the dictionary"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from filters.admin_checker import IsAdmin
from config.conf import admins_ids
from states import AddWord
from keyboards.approve_keyboard import approve_kb
from keyboards.menu_keyboard import menu_kb, add_button
from back.db_back import add_word_for_user, user_exists, add_user
from back.bot_back import check_word_message

add_word_router = Router()
add_word_router.message.filter(
    IsAdmin(admins_ids)
)


@add_word_router.message(F.text == add_button)
@add_word_router.message(Command('add_word'))
async def ask_word(message: Message, state: FSMContext):
    """Bot asks what word user wants to add"""
    await state.clear()
    chat_id = str(message.from_user.id)
    if not user_exists(chat_id):
        add_user(chat_id)
        await message.answer('Словарь готов к работе 💫')
    await message.answer('Какое слово добавить?',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddWord.add_word)


@add_word_router.message(AddWord.add_word)
async def ask_translation(message: Message, state: FSMContext):
    """Bot asks translation for the new word"""
    await state.update_data(add_word=message.text)
    msg = f'Отправь перевод для слова: "{message.text}"'
    await message.answer(msg, reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddWord.add_translation)


@add_word_router.message(AddWord.add_translation)
async def ask_approve(message: Message,
                      state: FSMContext):
    """User should approve new pair: word & translation"""
    await state.update_data(
        add_translation=message.text)
    word = await state.get_value('add_word')
    translation = await state.get_value('add_translation')
    msg = check_word_message(word, translation)
    await message.answer(msg, reply_markup=approve_kb())
    await state.set_state(AddWord.approved)


@add_word_router.message(AddWord.approved, F.text == 'Да')
async def save_word(message: Message, state: FSMContext):
    """Bot saves new word to the database"""
    chat_id = str(message.from_user.id)
    word = await state.get_value('add_word')
    translation = await state.get_value('add_translation')
    add_word_for_user(chat_id, word, translation)
    await state.clear()
    await message.answer('Новое слово теперь в словаре 😌',
                         reply_markup=menu_kb())


@add_word_router.message(AddWord.approved, F.text == 'Нет')
async def decline_word(message: Message, state: FSMContext):
    """User decline the new word"""
    msg = 'Жаль 😿\n\nДавай попробуем ещё раз?'
    await state.clear()
    await message.answer(msg, reply_markup=menu_kb())


@add_word_router.message(AddWord.approved)
async def wrong_answer(message: Message):
    """Bot asks user to use the keyboard"""
    msg = 'Пожалуйста, ответь с помощью специальной клавиатуры'
    await message.answer(msg, reply_markup=approve_kb())
