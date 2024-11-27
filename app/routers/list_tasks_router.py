from aiogram import Router, F
from aiogram.types import Message
from app import db

list_tasks_router = Router()

@list_tasks_router.message(F.text.lower() == '🔸список задач')
async def list_tasks(message: Message):
    tasks = await db.get_tasks(message.from_user.id)
    result = ''

    for index, task in enumerate(tasks):
        result += f"{index + 1}) {task["task_text"]} - "
        result += f"✅ Выполнено! \n" if task["task_status"] else f"❎ Не выполнено \n"

    await message.answer(result)
