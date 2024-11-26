from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.states import NewTaskState

create_task_router = Router()

@create_task_router.message(F.text.lower() == '🔸создать задачу')
async def get_create_task(message: Message, state: FSMContext):
    await message.answer("Введите текст задачи")
    await state.set_state(NewTaskState.GET_TEXT)