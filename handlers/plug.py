"""Bot couldn't read the message from user"""

from aiogram import Router
from aiogram.types import Message
from keyboards.menu_keyboard import menu_kb
from back.bot_back import create_plug_message


plug_router = Router()


@plug_router.message()
async def plug_msg(message: Message):
    """Bot couldn't understand user, asks with menu"""
    msg = create_plug_message()
    await message.answer(msg,
                         reply_markup=menu_kb())
