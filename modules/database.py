import os
import motor.motor_asyncio

from dotenv import load_dotenv


async def create_connection():
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URI"))
    db = client['users']
    return db['tasks']


async def add_user(collection, telegram_id):
    await collection.update_one(
        {'telegram_id': telegram_id},
        {'$setOnInsert': {'tasks': []}},
        upsert=True
    )


async def add_task(collection, telegram_id, task_text):
    await collection.update_one(
        {'telegram_id': telegram_id},
        {'$push': {'tasks': {'task_text': task_text, 'task_status': False}}}
    )


async def get_tasks(collection, telegram_id):
    user = await collection.find_one({'telegram_id': telegram_id})
    if user:
        return user.get('tasks', [])
    return []


async def get_task_status(collection, telegram_id, task_index):
    user = await collection.find_one({'telegram_id': telegram_id})
    if user and 0 <= task_index < len(user['tasks']):
        return user['tasks'][task_index]['task_status']
    return None


async def get_task_text(collection, telegram_id, task_index):
    user = await collection.find_one({'telegram_id': telegram_id})
    if user and 0 <= task_index < len(user['tasks']):
        return user['tasks'][task_index]['task_text']
    return None


async def edit_task(collection, telegram_id, task_index, new_task_text):
    await collection.update_one(
        {'telegram_id': telegram_id},
        {'$set': {f'tasks.{task_index}.task_text': new_task_text}}
    )


async def complete_task(collection, telegram_id, task_index):
    await collection.update_one(
        {'telegram_id': telegram_id},
        {'$set': {f'tasks.{task_index}.task_status': True}}
    )


async def delete_task(collection, telegram_id, task_index):
    await collection.update_one(
        {'telegram_id': telegram_id},
        {'$unset': {f'tasks.{task_index}': 1}}
    )
    await collection.update_one(
        {'telegram_id': telegram_id},
        {'$pull': {'tasks': None}}
    )


async def task_index_exists(collection, telegram_id, task_index):
    user = await collection.find_one(
        {'telegram_id': telegram_id, f'tasks.{task_index}': {'$exists': True}},
        {'projection': {'_id': 1}}
    )
    return user is not None


async def user_exists(collection, telegram_id):
    user = await collection.find_one({'telegram_id': telegram_id})
    return bool(user)

