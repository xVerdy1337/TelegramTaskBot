from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔸Создать задачу'),
            KeyboardButton(text='🔸Список задач'),
        ],
        [
            KeyboardButton(text='🔸Выполнить задачу'),
            KeyboardButton(text='🔸Удалить задачу'),
        ]
    ],
    resize_keyboard=True
)

