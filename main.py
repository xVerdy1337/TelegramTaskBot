import asyncio
from app import bot, dp
from app.routers import (start_router, list_tasks_router, create_task_router,
                         delete_task_router, complete_task_router)

dp.include_router(start_router)
dp.include_router(list_tasks_router)
dp.include_router(create_task_router)
dp.include_router(delete_task_router)
dp.include_router(complete_task_router)

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
