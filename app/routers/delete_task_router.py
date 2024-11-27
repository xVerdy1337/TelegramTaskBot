from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from app import db
from app.states import DeleteTaskState

delete_task_router = Router()

@delete_task_router.message(F.text.lower() == '🔸удалить задачу')
async def get_index_delete_task(message: Message, state: FSMContext):
    await message.answer("Введите номер задачи")
    await state.set_state(DeleteTaskState.GET_INDEX)


@delete_task_router.message(StateFilter(DeleteTaskState.GET_INDEX))
async def task_delete(message: Message, state: FSMContext):
    if await db.task_index_exists(message.from_user.id, int(message.text) - 1):
        await message.answer(f'Задача №{message.text} удалена!')
        await db.delete_task(message.from_user.id, int(message.text) - 1)
    else:
        await message.answer("Такой задачи не существует!")

    await state.clear()
