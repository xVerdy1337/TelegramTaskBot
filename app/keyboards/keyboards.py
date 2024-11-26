from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_main_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(
        text='🔸Создать задачу'
    )

    builder.button(
        text='🔸Список задач'
    )

    builder.button(
        text='🔸Выполнить задачу'
    )

    builder.button(
        text='🔸Удалить задачу'
    )

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
