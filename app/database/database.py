import motor.motor_asyncio
from app.config import MONGO_URI


class Database:
    def __init__(self, uri: str = MONGO_URI, collection_name: str = 'tasks', db_name: str = 'users'):
        self.uri = uri
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.uri)
        self.collection_name = collection_name
        self.db_name = db_name
        self.collection = self.client[self.db_name][self.collection_name]

    async def create_connection(self):
        db = self.client[self.db_name]
        return db[self.collection_name]

    async def add_user(self, telegram_id):
        await self.collection.update_one(
            {'telegram_id': telegram_id},
            {'$setOnInsert': {self.collection_name: []}},
            upsert=True
        )

    async def add_task(self, telegram_id, task_text):
        await self.collection.update_one(
            {'telegram_id': telegram_id},
            {'$push': {self.collection_name: {'task_text': task_text, 'task_status': False}}}
        )

    async def get_tasks(self, telegram_id):
        user = await self.collection.find_one({'telegram_id': telegram_id})
        if user:
            return user.get(self.collection_name, [])
        return []

    async def get_task_status(self, telegram_id, task_index):
        user = await self.collection.find_one({'telegram_id': telegram_id})
        if user and 0 <= task_index < len(user[self.collection_name]):
            return user[self.collection_name][task_index]['task_status']
        return None

    async def get_task_text(self, telegram_id, task_index):
        user = await self.collection.find_one({'telegram_id': telegram_id})
        if user and 0 <= task_index < len(user[self.collection_name]):
            return user[self.collection_name][task_index]['task_text']
        return None

    async def edit_task(self, telegram_id, task_index, new_task_text):
        await self.collection.update_one(
            {'telegram_id': telegram_id},
            {'$set': {f'{self.collection_name}.{task_index}.task_text': new_task_text}}
        )

    async def complete_task(self, telegram_id, task_index):
        await self.collection.update_one(
            {'telegram_id': telegram_id},
            {'$set': {f'{self.collection_name}.{task_index}.task_status': True}}
        )

    async def delete_task(self, telegram_id, task_index):
        await self.collection.update_one(
            {'telegram_id': telegram_id},
            {'$unset': {f'{self.collection_name}.{task_index}': 1}}
        )
        await self.collection.update_one(
            {'telegram_id': telegram_id},
            {'$pull': {self.collection_name: None}}
        )

    async def task_index_exists(self, telegram_id, task_index):
        user = await self.collection.find_one(
            {'telegram_id': telegram_id, f'{self.collection_name}.{task_index}': {'$exists': True}},
            {'projection': {'_id': 1}}
        )
        return user is not None

    async def user_exists(self, telegram_id):
        user = await self.collection.find_one({'telegram_id': telegram_id})
        return bool(user)
