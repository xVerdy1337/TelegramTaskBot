import os
import asyncio

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from modules import *


load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()


async def main():
    global collection
    collection = await create_connection()
    await dp.start_polling(bot)


@dp.message(Command('start'))
async def start(message: types.Message):
    if await user_exists(collection, message.from_user.id):
        await message.answer('Добро пожаловать в бота, для управления задач!', reply_markup=main_keyboard)
        await add_user(collection, message.from_user.id)


@dp.message(F.text.lower() == '🔸создать задачу')
async def get_create_task(message: types.Message, state: FSMContext):
    await message.answer("Введите текст задачи")
    await state.set_state(NewTaskState.GET_TEXT)


@dp.message(StateFilter(NewTaskState.GET_TEXT))
async def set_text_new_task(message: types.Message, state: FSMContext):
    await add_task(collection, message.from_user.id, message.text)
    await message.answer("Задача создана!")
    await state.clear()


@dp.message(F.text.lower() == '🔸список задач')
async def list_tasks(message: types.Message):
    tasks = await get_tasks(collection, message.from_user.id)
    result = ''

    for index, task in enumerate(tasks):
        result += f"{index + 1}) {task["task_text"]} - "
        result += f"✅ Выполнено! \n" if task["task_status"] else f"❎ Не выполнено \n"

    await message.answer(result)


@dp.message(F.text.lower() == '🔸выполнить задачу')
async def status_task_get_id(message: types.Message, state: FSMContext):
    await message.answer("Введите номер задачи")
    await state.set_state(StatusTaskState.GET_INDEX)


@dp.message(StateFilter(StatusTaskState.GET_INDEX))
async def set_task_status(message: types.Message, state: FSMContext):
    if await task_index_exists(collection, message.from_user.id, int(message.text) - 1):
        await message.answer(f"Задача №{message.text} выполнена!")
        await complete_task(collection, message.from_user.id, int(message.text) - 1)
    else:
        await message.answer("Такой задачи не существует!")

    await state.clear()


@dp.message(F.text.lower() == '🔸удалить задачу')
async def get_index_delete_task(message: types.Message, state: FSMContext):
    await message.answer("Введите номер задачи")
    await state.set_state(DeleteTaskState.GET_INDEX)


@dp.message(StateFilter(DeleteTaskState.GET_INDEX))
async def task_delete(message: types.Message, state: FSMContext):
    if await task_index_exists(collection, message.from_user.id, int(message.text) - 1):
        await message.answer(f'Задача №{message.text} удалена!')
        await delete_task(collection, message.from_user.id, int(message.text) - 1)
    else:
        await message.answer("Такой задачи не существует!")

    await state.clear()

if __name__ == '__main__':
    asyncio.run(main())
