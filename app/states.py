from aiogram.fsm.state import State, StatesGroup


class MessageState(StatesGroup):
    waiting_for_message = State()
