"""Bot reacts to the command /start for the admins"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from filters.admin_checker import IsAdmin
from config.conf import admins_ids
from back.db_back import user_exists, add_user
from back.bot_back import create_start_message
from keyboards.menu_keyboard import menu_kb


start_admin_router = Router()
start_admin_router.message.filter(
    IsAdmin(admins_ids)
)


@start_admin_router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    """Bot says hi to the admins"""
    await state.clear()
    chat_id = str(message.from_user.id)
    if not user_exists(chat_id):
        add_user(chat_id)
        await message.answer('Словарь готов к работе 💫')
    msg = create_start_message()
    await message.answer(msg, reply_markup=menu_kb())
