from aiogram.fsm.state import State, StatesGroup


class Chat(StatesGroup):
    active = State()
    inactive = State()
    waiting = State()