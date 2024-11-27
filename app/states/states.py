from aiogram.fsm.state import StatesGroup, State

class NewTaskState(StatesGroup):
    GET_TEXT = State()

class StatusTaskState(StatesGroup):
    GET_INDEX = State()

class DeleteTaskState(StatesGroup):
    GET_INDEX = State()
