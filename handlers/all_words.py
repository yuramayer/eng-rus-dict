"""Bot sends all user's words"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from back.db_back import get_user_dict, user_exists, add_user
from back.bot_back import create_all_words_message
from back.msg_log import save_log_event
from keyboards.menu_keyboard import menu_kb


all_words_router = Router()


@all_words_router.message(Command('all_words'))
async def send_all_words(message: Message, state: FSMContext):
    """Bot sends all user's words to the user"""

    save_log_event(
        message=message,
        direction='inbound',
        text=message.text,
        router='all_words_router',
        method='send_all_words',
        event_type='command'
    )

    await state.clear()
    chat_id = str(message.from_user.id)
    if not user_exists(chat_id):
        add_user(chat_id)
        msg_answer = 'Словарь готов к работе 💫'
        await message.answer(msg_answer)

        save_log_event(
            message=message,
            direction='outbound',
            text=msg_answer,
            router='all_words_router',
            method='send_all_words',
            event_type='message'
        )

    chat_id = message.from_user.id
    user_words = get_user_dict(chat_id)

    if user_words == {}:

        msg_answer = 'У тебя пока нет слов в базе 🤔'

        await message.answer(msg_answer,
                             reply_markup=menu_kb())

        save_log_event(
            message=message,
            direction='outbound',
            text=msg_answer,
            router='all_words_router',
            method='send_all_words',
            event_type='message'
        )

        return

    msg_answer = create_all_words_message(user_words)

    await message.answer(msg_answer, reply_markup=menu_kb())

    save_log_event(
            message=message,
            direction='outbound',
            text=msg_answer,
            router='all_words_router',
            method='send_all_words',
            event_type='message'
        )
