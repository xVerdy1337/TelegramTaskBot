import motor.motor_asyncio
from typing import Optional
from app.config import MONGO_URI


class Database:
    def __init__(self,
                 uri: str = MONGO_URI,
                 collection_name: str = 'tasks',
                 db_name: str = 'users'
    ):
        """
        Initialize the database connection.

        :param uri: MongoDB connection URI
        :param collection_name: Name of the collection to use
        :param db_name: Name of the database
        """
        self.uri: str = uri
        self.client: motor.AsyncIOMotorClient = motor.motor_asyncio.AsyncIOMotorClient(self.uri)
        self.collection_name: str = collection_name
        self.db_name: str = db_name
        self.collection: motor.AsyncIOMotorCollection = self.client[self.db_name][self.collection_name]

    async def create_connection(self) -> motor.motor_asyncio.AsyncIOMotorCollection:
        """
        Create and return a database collection connection.

        :return: AsyncIO Motor Collection
        """
        db = self.client[self.db_name]
        return db[self.collection_name]

    async def add_user(self, telegram_id: int) -> None:
        """
        Add a new user to the database if not exists.

        :param telegram_id: Unique Telegram user identifier
        """
        await self.collection.update_one(
            {'telegram_id': telegram_id},
            {'$setOnInsert': {self.collection_name: []}},
            upsert=True
        )

    async def add_task(self, telegram_id: int, task_text: str) -> None:
        """
        Add a new task for a specific user.

        :param telegram_id: Unique Telegram user identifier
        :param task_text: Text description of the task
        """
        await self.collection.update_one(
            {'telegram_id': telegram_id},
            {'$push': {self.collection_name: {'task_text': task_text, 'task_status': False}}}
        )

    async def get_tasks(self, telegram_id: int) -> list[dict]:
        """
        Retrieve all tasks for a specific user.

        :param telegram_id: Unique Telegram user identifier
        :return: List of tasks or empty list
        """
        user = await self.collection.find_one({'telegram_id': telegram_id})
        if user:
            return user.get(self.collection_name, [])
        return []

    async def get_task_status(self, telegram_id: int, task_index: int) -> Optional[bool]:
        """
        Get the status of a specific task.

        :param telegram_id: Unique Telegram user identifier
        :param task_index: Index of the task in the user's task list
        :return: Task status or None if task not found
        """
        user = await self.collection.find_one({'telegram_id': telegram_id})
        if user and 0 <= task_index < len(user[self.collection_name]):
            return user[self.collection_name][task_index]['task_status']
        return None

    async def get_task_text(self, telegram_id: int, task_index: int) -> Optional[str]:
        """
        Get the text of a specific task.

        :param telegram_id: Unique Telegram user identifier
        :param task_index: Index of the task in the user's task list
        :return: Task text or None if task not found
        """
        user = await self.collection.find_one({'telegram_id': telegram_id})
        if user and 0 <= task_index < len(user[self.collection_name]):
            return user[self.collection_name][task_index]['task_text']
        return None

    async def edit_task_text(self, telegram_id: int, task_index: int, new_task_text: str) -> None:
        """
        Edit the text of a specific task.

        :param telegram_id: Unique Telegram user identifier
        :param task_index: Index of the task in the user's task list
        :param new_task_text: New text for the task
        """
        await self.collection.update_one(
            {'telegram_id': telegram_id},
            {'$set': {f'{self.collection_name}.{task_index}.task_text': new_task_text}}
        )

    async def complete_task(self, telegram_id: int, task_index: int) -> None:
        """
        Mark a specific task as completed.

        :param telegram_id: Unique Telegram user identifier
        :param task_index: Index of the task in the user's task list
        """
        await self.collection.update_one(
            {'telegram_id': telegram_id},
            {'$set': {f'{self.collection_name}.{task_index}.task_status': True}}
        )

    async def delete_task(self, telegram_id: int, task_index: int) -> None:
        """
        Delete a specific task from the user's task list.

        :param telegram_id: Unique Telegram user identifier
        :param task_index: Index of the task in the user's task list
        """
        await self.collection.update_one(
            {'telegram_id': telegram_id},
            {'$unset': {f'{self.collection_name}.{task_index}': 1}}
        )
        await self.collection.update_one(
            {'telegram_id': telegram_id},
            {'$pull': {self.collection_name: None}}
        )

    async def task_index_exists(self, telegram_id: int, task_index: int) -> bool:
        """
        Check if a specific task index exists for a user.

        :param telegram_id: Unique Telegram user identifier
        :param task_index: Index of the task in the user's task list
        :return: Boolean indicating task index existence
        """
        user = await self.collection.find_one(
            {'telegram_id': telegram_id, f'{self.collection_name}.{task_index}': {'$exists': True}},
            {'projection': {'_id': 1}}
        )
        return user is not None

    async def user_exists(self, telegram_id: int) -> bool:
        """
        Check if a user exists in the database.

        :param telegram_id: Unique Telegram user identifier
        :return: Boolean indicating user existence
        """
        user = await self.collection.find_one({'telegram_id': telegram_id})
        return bool(user)
