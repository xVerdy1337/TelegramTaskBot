from aiogram import Bot, Dispatcher
from .config import BOT_TOKEN
from .database import Database

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
db = Database()