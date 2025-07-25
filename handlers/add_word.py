"""User adds new word to the dictionary"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from states import AddWord
from keyboards.approve_keyboard import approve_kb
from keyboards.menu_keyboard import menu_kb, add_button
from back.db_back import add_word_for_user, user_exists, add_user
from back.bot_back import check_word_message
from back.msg_log import save_log_event


add_word_router = Router()


@add_word_router.message(F.text == add_button)
@add_word_router.message(Command('add_word'))
async def ask_word(message: Message, state: FSMContext):
    """Bot asks what word user wants to add"""

    save_log_event(
        message=message,
        direction='inbound',
        text=message.text,
        router='add_word_router',
        method='ask_word',
        event_type='command'
    )

    await state.clear()
    chat_id = str(message.from_user.id)
    if not user_exists(chat_id):
        add_user(chat_id)

        msg_answer = 'Словарь готов к работе 💫'
        await message.answer()

        save_log_event(
            message=message,
            direction='outbound',
            text=msg_answer,
            router='add_word_router',
            method='ask_word',
            event_type='message'
        )

    msg_answer = 'Какое 🇷🇺 слово добавить?'
    await message.answer(msg_answer,
                         reply_markup=ReplyKeyboardRemove())

    save_log_event(
        message=message,
        direction='outbound',
        text=msg_answer,
        router='add_word_router',
        method='ask_word',
        event_type='message'
    )

    await state.set_state(AddWord.add_word)


@add_word_router.message(AddWord.add_word)
async def ask_translation(message: Message, state: FSMContext):
    """Bot asks translation for the new word"""

    save_log_event(
        message=message,
        direction='inbound',
        text=message.text,
        router='add_word_router',
        method='ask_transation',
        event_type='message'
    )

    await state.update_data(add_word=message.text)
    msg_answer = f'Отправь 🇬🇧 перевод для слова: "{message.text}"'
    await message.answer(msg_answer, reply_markup=ReplyKeyboardRemove())

    save_log_event(
        message=message,
        direction='outbound',
        text=msg_answer,
        router='add_word_router',
        method='ask_translation',
        event_type='message'
    )

    await state.set_state(AddWord.add_translation)


@add_word_router.message(AddWord.add_translation)
async def ask_approve(message: Message,
                      state: FSMContext):
    """User should approve new pair: word & translation"""

    save_log_event(
        message=message,
        direction='inbound',
        text=message.text,
        router='add_word_router',
        method='ask_approve',
        event_type='message'
    )

    await state.update_data(
        add_translation=message.text)
    word = await state.get_value('add_word')
    translation = await state.get_value('add_translation')
    msg_answer = check_word_message(word, translation)
    await message.answer(msg_answer, reply_markup=approve_kb())

    save_log_event(
        message=message,
        direction='outbound',
        text=msg_answer,
        router='add_word_router',
        method='ask_approve',
        event_type='message'
    )

    await state.set_state(AddWord.approved)


@add_word_router.message(AddWord.approved, F.text == 'Да')
async def save_word(message: Message, state: FSMContext):
    """Bot saves new word to the database"""

    save_log_event(
        message=message,
        direction='inbound',
        text=message.text,
        router='add_word_router',
        method='save_word',
        event_type='message'
    )

    chat_id = str(message.from_user.id)
    word = await state.get_value('add_word')
    translation = await state.get_value('add_translation')
    add_word_for_user(chat_id, word, translation)
    await state.clear()

    msg_answer = 'Новое слово теперь в словаре 😌'
    await message.answer(msg_answer,
                         reply_markup=menu_kb())
    save_log_event(
        message=message,
        direction='outbound',
        text=msg_answer,
        router='add_word_router',
        method='save_word',
        event_type='message'
    )


@add_word_router.message(AddWord.approved, F.text == 'Нет')
async def decline_word(message: Message, state: FSMContext):
    """User decline the new word"""

    save_log_event(
        message=message,
        direction='inbound',
        text=message.text,
        router='add_word_router',
        method='decline_word',
        event_type='message'
    )

    msg_answer = 'Жаль 😿\n\nДавай попробуем ещё раз?'
    await state.clear()
    await message.answer(msg_answer, reply_markup=menu_kb())

    save_log_event(
        message=message,
        direction='outbound',
        text=msg_answer,
        router='add_word_router',
        method='decline_word',
        event_type='message'
    )


@add_word_router.message(AddWord.approved)
async def wrong_answer(message: Message):
    """Bot asks user to use the keyboard"""

    save_log_event(
        message=message,
        direction='inbound',
        text=message.text,
        router='add_word_router',
        method='wrong_answer',
        event_type='message'
    )

    msg_answer = 'Пожалуйста, ответь с помощью специальной клавиатуры'
    await message.answer(msg_answer, reply_markup=approve_kb())

    save_log_event(
        message=message,
        direction='outbound',
        text=msg_answer,
        router='add_word_router',
        method='wrong_answer',
        event_type='message'
    )
