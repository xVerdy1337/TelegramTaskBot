from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from app import db
from app.states import NewTaskState

create_task_router = Router()

@create_task_router.message(F.text.lower() == '🔸создать задачу')
async def get_create_task(message: Message, state: FSMContext):
    await message.answer("Введите текст задачи")
    await state.set_state(NewTaskState.GET_TEXT)

@create_task_router.message(StateFilter(NewTaskState.GET_TEXT))
async def set_text_new_task(message: Message, state: FSMContext):
    await db.add_task(message.from_user.id, message.text)
    await message.answer("Задача создана!")
    await state.clear()
