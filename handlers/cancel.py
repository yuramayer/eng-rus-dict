"""Bot reacts to the command /start for the admins"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.menu_keyboard import menu_kb


cancel_router = Router()


@cancel_router.message(Command('cancel'))
async def cmd_cancel(message: Message, state: FSMContext):
    """User cancels the current state"""
    await state.clear()
    await message.answer('Операция отменена 👌🏻',
                         reply_markup=menu_kb())
