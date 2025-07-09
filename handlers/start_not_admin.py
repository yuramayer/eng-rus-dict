"""Bot reacts to the command /start for the others"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from filters.admin_checker import NotAdmin
from config.conf import admins_ids
from back.bot_back import create_not_admin_message

start_not_admin_router = Router()
start_not_admin_router.message.filter(
    NotAdmin(admins_ids)
)


@start_not_admin_router.message(F.text)
@start_not_admin_router.message(Command('start'))
async def cmd_start_not_admin(message: Message):
    """Not admins want to use the bot"""
    msg = create_not_admin_message()
    await message.answer(msg)
