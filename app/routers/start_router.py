from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from app.keyboards import get_main_keyboard
from app import db

start_router = Router()

@start_router.message(Command('start'))
async def start(message: Message):
    if await db.user_exists(message.from_user.id):
        await message.answer('Добро пожаловать в бота, для управления задач!', reply_markup=get_main_keyboard())
        await db.add_user(message.from_user.id)
