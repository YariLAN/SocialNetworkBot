from aiogram.fsm.state import StatesGroup, State


class AuthUserDto(StatesGroup):
    name = State()
