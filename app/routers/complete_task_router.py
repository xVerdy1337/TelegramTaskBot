from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from app import db
from app.states import StatusTaskState

complete_task_router = Router()

@complete_task_router.message(F.text.lower() == '🔸выполнить задачу')
async def status_task_get_id(message: Message, state: FSMContext):
    await message.answer("Введите номер задачи")
    await state.set_state(StatusTaskState.GET_INDEX)

@complete_task_router.message(StateFilter(StatusTaskState.GET_INDEX))
async def set_task_status(message: Message, state: FSMContext):
    if await db.task_index_exists(message.from_user.id, int(message.text) - 1):
        await message.answer(f"Задача №{message.text} выполнена!")
        await db.complete_task(message.from_user.id, int(message.text) - 1)
    else:
        await message.answer("Такой задачи не существует!")

    await state.clear()